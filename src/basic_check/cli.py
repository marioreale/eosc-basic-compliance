"""Command line: fetch once, assess, report."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import typer
import yaml

from . import checks, report
from .fetch import MAX_CHILDREN, collect_all, load_evidence

app = typer.Typer(
    add_completion=False,
    help="Check EOSC Node Landing Pages against checklist v3.0.",
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NODES = ROOT / "nodes.yaml"
DEFAULT_CHECKLIST = ROOT / "checklist" / "v3.0.yaml"
DEFAULT_RESULTS = ROOT / "results"


def _load_nodes(path: Path, only: str = "") -> list[dict]:
    data = yaml.safe_load(path.read_text())
    nodes = data["nodes"]
    if only:
        wanted = {x.strip() for x in only.split(",") if x.strip()}
        unknown = wanted - {n["id"] for n in nodes}
        if unknown:
            raise typer.BadParameter(f"unknown node id(s): {', '.join(sorted(unknown))}")
        nodes = [n for n in nodes if n["id"] in wanted]
    return nodes


@app.command()
def collect(
    nodes_file: Path = typer.Option(DEFAULT_NODES, "--nodes", "-n"),
    results_dir: Path = typer.Option(DEFAULT_RESULTS, "--results"),
    only: str = typer.Option("", "--only", help="Comma-separated node ids"),
    delay: float = typer.Option(2.0, "--delay", help="Seconds between hosts"),
    depth: int = typer.Option(
        1,
        "--depth",
        min=0,
        max=1,
        help="0 = landing page only. 1 = also follow links that can settle a "
        "checklist point (policies, contact, about), capped per node.",
    ),
    max_children: int = typer.Option(
        MAX_CHILDREN, "--max-children", help="Cap on followed pages per node at depth 1"
    ),
):
    """Fetch each landing page and save the evidence. Depth 1 by default."""
    nodes = _load_nodes(nodes_file, only)
    evidence_dir = results_dir / "evidence"
    if depth >= 1:
        typer.echo(
            f"Fetching {len(nodes)} landing page(s), {delay}s apart, then following up to "
            f"{max_children} checklist-relevant link(s) per node (depth 1):"
        )
    else:
        typer.echo(f"Fetching {len(nodes)} landing page(s), one request each, {delay}s apart:")
    asyncio.run(
        collect_all(nodes, evidence_dir, delay_s=delay, depth=depth, max_children=max_children)
    )
    typer.echo(f"\nEvidence written to {evidence_dir}")


@app.command()
def assess(
    nodes_file: Path = typer.Option(DEFAULT_NODES, "--nodes", "-n"),
    checklist_file: Path = typer.Option(DEFAULT_CHECKLIST, "--checklist", "-c"),
    results_dir: Path = typer.Option(DEFAULT_RESULTS, "--results"),
    only: str = typer.Option("", "--only"),
    approved_names: Path | None = typer.Option(
        None,
        "--approved-names",
        help="Optional text file, one Tripartite-approved node name per line. "
        "Without it, point 3's name requirement cannot be checked.",
    ),
    run_id: str = typer.Option("", "--run"),
):
    """Apply the checklist to already-collected evidence and write the reports."""
    nodes = _load_nodes(nodes_file, only)
    checklist = yaml.safe_load(checklist_file.read_text())
    evidence_dir = results_dir / "evidence"

    names: list[str] = []
    if approved_names:
        names = [ln.strip() for ln in approved_names.read_text().splitlines() if ln.strip()]

    run = {
        "run_id": run_id or datetime.now(UTC).strftime("%Y-%m-%d-%H%M"),
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "checklist": checklist,
        "approved_names_supplied": bool(names),
        "nodes": [],
    }

    missing: list[str] = []
    for node in nodes:
        path = evidence_dir / f"{node['id']}.json"
        if not path.exists():
            missing.append(node["id"])
            continue
        ev = load_evidence(evidence_dir, node["id"])
        results = checks.run_all(ev, names or None, node.get('eosc_page', ''))
        run["nodes"].append(
            {
                "id": node["id"],
                "name": node["name"],
                "url": node["url"],
                "fetch": {
                    "http_status": ev.http_status,
                    "final_url": ev.final_url,
                    "fetched_at": ev.fetched_at,
                    "error": ev.error,
                    "robots_note": ev.robots_note,
                    "screenshot": ev.screenshot,
                    "crawl_depth": ev.crawl_depth,
                    "crawl_note": ev.crawl_note,
                    "children": [
                        {
                            "url": c.url,
                            "final_url": c.final_url,
                            "selected_for": c.selected_for,
                            "link_text": c.link_text,
                            "http_status": c.http_status,
                            "title": c.title,
                            "chars": len(c.main_text),
                            "error": c.error,
                        }
                        for c in ev.children
                    ],
                    "children_skipped": ev.children_skipped,
                },
                "results": [asdict(r) for r in results],
            }
        )

    if missing:
        # Assessing a subset while presenting it as the whole run is the failure
        # mode that matters most here: a short table looks complete.
        run["missing_evidence"] = missing
        typer.secho(
            f"\n  {len(missing)} node(s) have no evidence and were NOT assessed: "
            f"{', '.join(missing)}\n  Run `collect` for them before treating this as complete.",
            fg=typer.colors.RED,
        )

    paths = report.write_all(run, results_dir)
    tally: dict[str, int] = {}
    for node in run["nodes"]:
        for res in node["results"]:
            tally[res["verdict"]] = tally.get(res["verdict"], 0) + 1

    typer.echo(f"\nAssessed {len(run['nodes'])} node(s) against {len(checklist['points'])} points.")
    for verdict in ("PASS", "FAIL", "MANUAL_REVIEW", "ERROR"):
        if tally.get(verdict):
            typer.echo(f"  {verdict:14} {tally[verdict]}")
    for kind, path in paths.items():
        typer.echo(f"  {kind:5} {path}")

    if missing:
        raise typer.Exit(2)


@app.command()
def run(
    nodes_file: Path = typer.Option(DEFAULT_NODES, "--nodes", "-n"),
    results_dir: Path = typer.Option(DEFAULT_RESULTS, "--results"),
    only: str = typer.Option("", "--only"),
    delay: float = typer.Option(2.0, "--delay"),
    depth: int = typer.Option(1, "--depth", min=0, max=1),
):
    """collect, then assess."""
    collect(
        nodes_file=nodes_file,
        results_dir=results_dir,
        only=only,
        delay=delay,
        depth=depth,
        max_children=MAX_CHILDREN,
    )
    assess(nodes_file=nodes_file, results_dir=results_dir, only=only)


@app.command()
def points(checklist_file: Path = typer.Option(DEFAULT_CHECKLIST, "--checklist", "-c")):
    """Print the checklist points and whether each is machine-decidable."""
    checklist = yaml.safe_load(checklist_file.read_text())
    for p in checklist["points"]:
        labels = {True: "by inspection", "partial": "partly", False: "human judgement"}
        dec = labels[p.get("decidable")]
        typer.echo(f"{p['id']:4} [{dec:15}] {p['title']}")


@app.command()
def show(
    node_id: str = typer.Argument(...),
    results_dir: Path = typer.Option(DEFAULT_RESULTS, "--results"),
):
    """Print one node's results."""
    data = json.loads((results_dir / "results.json").read_text())
    for node in data["nodes"]:
        if node["id"] == node_id:
            typer.echo(f"{node['name']} — {node['url']}")
            for res in node["results"]:
                typer.echo(f"\n  [{res['verdict']}] {res['point_id']} {res['title']}")
                typer.echo(f"      {' '.join(res['message'].split())}")
                for item in res.get("evidence", []):
                    typer.echo(f"      - {item}")
            return
    raise typer.BadParameter(f"no results for {node_id}")


if __name__ == "__main__":
    app()
