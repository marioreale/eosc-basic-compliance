"""Command line: fetch once, assess, report."""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import typer
import yaml

from . import checks, report
from .fetch import (
    DEFAULT_FETCH_BUDGET,
    MAX_CHILDREN,
    collect_all,
    load_evidence,
    without_depth_2,
)
from .names import ApprovedNames

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NODES = ROOT / "nodes.yaml"
# The checklist revision applied by default. This line is the one place to change
# when a new revision is adopted: add checklist/vX.Y.yaml beside the old one (see
# checklist/README.md), then point this at it. Help texts, tests and reports all
# follow from here.
DEFAULT_CHECKLIST = ROOT / "checklist" / "v3.0.yaml"
DEFAULT_CHECKLIST_LABEL = f"checklist/{DEFAULT_CHECKLIST.name}"
# The official Tripartite-approved node names, committed alongside the checklist
# they serve. Used unless --approved-names names another file, so the name half
# of point 3 is assessed by default instead of silently skipped.
DEFAULT_APPROVED_NAMES = ROOT / "checklist" / "approved-names.txt"
DEFAULT_RESULTS = ROOT / "results"
# One-off --url checks write here by default rather than into results/, so an ad
# hoc check of one candidate page cannot overwrite the committed federation report
# with a one-row table. assess() rewrites results.md, index.html and results.json
# wholesale, so sharing a directory would silently destroy the published run.
DEFAULT_ONEOFF = ROOT / "results" / "one-off"


def _node_ids(path: Path = DEFAULT_NODES) -> str:
    """The configured node ids, for the help text. Never fails: help must print
    even when nodes.yaml is missing or broken."""
    try:
        return ", ".join(n["id"] for n in yaml.safe_load(path.read_text())["nodes"])
    except Exception:  # noqa: BLE001 - help text only
        return "see the id: fields in nodes.yaml"


# One help text per option, shared by every command that takes it, so that
# collect, assess and run cannot describe the same option differently. The
# README's "Command-line options" section mirrors these; keep them in step.
H_NODES = (
    "Node list to use instead of nodes.yaml. Use it to keep a separate list of "
    "candidate nodes, or to rebuild an old run with the list it was collected with."
)
H_RESULTS = (
    "Folder to write to (or read from) instead of results/, e.g. /tmp/trial for "
    "a scratch run. With an explicit --results, --only also narrows the report."
)
H_ONLY = (
    "Comma-separated node ids to fetch, e.g. egi,eudat. Ids only, not names. "
    "Writing to results/, the report still covers every node and marks which "
    "were re-fetched; with --results DIR it covers only these."
)
H_SKIP = (
    "Leave these nodes out of the run entirely: not fetched, not assessed, "
    "not in the report, which states that they were skipped. Node id or name "
    "(e.g. eosc-it, Italy or 'EOSC Node Italy'), case-insensitive; "
    "comma-separated or repeated. An unknown or ambiguous value is an error."
)
H_URL = (
    "Check this URL directly, without adding it to nodes.yaml. Repeatable. "
    "Writes to results/one-off/ so a published run is never overwritten. "
    "Cannot be combined with --only or --skip. With --node, the alternative "
    "landing page to check for that node."
)
H_EOSC_PAGE = (
    "With a single --url: the node's own eosc.eu page, so a point 4 failure "
    "can name the exact URL that is missing. With --node it replaces that "
    "node's configured eosc_page."
)
H_NODE = (
    "Check one configured node at an alternative landing page URL, given with "
    "--url: every point, with the node's id, name, eosc_page and approved name, "
    "but the page fetched from --url. nodes.yaml is not changed. Node id or name, "
    "as for --skip. Writes to results/one-off/ (or a --results DIR other than "
    "results/) and the report says the URL is not the configured one."
)
H_DELAY = "Seconds to wait between hosts, to go easy on the servers."
H_DEPTH = (
    "0 = landing page only. 1 = also follow links that can settle a checklist "
    "point (policies, contact, about), capped per node. 2 = one further hop "
    "from those pages, under --fetch-budget; the report then shows both depths "
    "side by side."
)
H_MAX_CHILDREN = "Most linked pages followed per node at depth 1 (run always uses 8)."
H_FETCH_BUDGET = (
    "Depth 2 only: hard ceiling on second-hop requests for the whole run, "
    "shared across nodes. Raise it deliberately; it exists to keep a check "
    "from becoming a crawl of other people's sites."
)
H_CHECKLIST = (
    f"Checklist rules file to use instead of {DEFAULT_CHECKLIST_LABEL}, e.g. a "
    "newer revision committed beside it as checklist/vX.Y.yaml."
)
H_APPROVED_NAMES = (
    "Text file of Tripartite-approved node names for point 3, one per line, "
    f"replacing the committed default ({DEFAULT_APPROVED_NAMES.name}). Write "
    "'node-id: Name' to tie a name to one node; a bare name applies to every "
    "node and cannot establish whose name it is. See docs/GUIDE.md section 3."
)
H_NO_APPROVED_NAMES = (
    "Use no approved-name list at all, not even the committed default. Point "
    "3's name requirement is then not assessed."
)
H_STRICT_SEPARATORS = (
    "Match the separator characters in an approved name literally. By default "
    "whitespace, pipe, hyphen, en dash, colon, slash and middle dot are "
    "interchangeable, because matching the official list literally matched "
    "none of the pages checked. Use this to see the strict result."
)
H_RUN = (
    "Label for this run, recorded in the report, e.g. trial-1. "
    "Default: the current UTC time as YYYY-MM-DD-HHMM."
)

EPILOG = (
    f"Node ids (from nodes.yaml): {_node_ids()}.\n\n"
    "Examples:\n\n"
    "basic-check run --only egi,eudat --results /tmp/trial\n\n"
    "basic-check run --skip Italy --results /tmp/trial\n\n"
    "basic-check run --skip eosc-it,bbmri-eric --depth 0 --results /tmp/trial\n\n"
    "basic-check assess --only eosc-cz --results /tmp/trial   (offline)\n\n"
    "basic-check run --url https://example.org/eosc-node/\n\n"
    "basic-check run --node bbmri-eric --url https://alt.example.org/eosc-node/\n\n"
    "basic-check show geant\n\n"
    "basic-check --print-config   (ids, landing page URLs, approved names)\n\n"
    "Only collect and run contact the nodes; assess, points and show never do. "
    "Full reference: README.md, section Command-line options."
)

app = typer.Typer(
    add_completion=False,
    help=f"Check EOSC Node Landing Pages against checklist {DEFAULT_CHECKLIST.stem}.\n\n"
    "collect fetches the pages and saves the evidence (the only step that "
    "contacts the nodes); assess judges the saved evidence offline and writes "
    "the reports; run does both. Every command has its own --help.",
    epilog=EPILOG,
)



# --- listing the configuration: basic-check --list-nodes and friends --------

# The name-to-node mapping. The default list (approved-names.txt) is the
# official file as circulated and is unscoped, so it cannot say which name is
# whose; the scoped copy carries the same names, each tied to a node id, and
# tests/test_checklist.py keeps the two identical.
SCOPED_APPROVED_NAMES = ROOT / "checklist" / "approved-names-scoped.txt"

H_LIST_NODES = (
    "List the node ids in nodes.yaml, one per line, and exit. --list-nodes-ids "
    "is the same option."
)
H_LIST_NLPS = "List each node id with its Node Landing Page URL from nodes.yaml, and exit."
H_LIST_APPROVED_NAMES = (
    "List each node id with its approved name, from "
    "checklist/approved-names-scoped.txt, and exit."
)
H_SHOW_NODE = (
    "Print one node's configuration and exit: its id, Node Landing Page URL and "
    "approved name, as one --print-config row. Node id or name, as for --skip."
)
H_PRINT_CONFIG = (
    "Print a table with one row per node: id, Node Landing Page URL and "
    "approved name, with the files they come from, and exit."
)


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _config_rows(
    nodes_file: Path = DEFAULT_NODES, scoped_file: Path = SCOPED_APPROVED_NAMES
) -> tuple[list[dict], list[str]]:
    """One row per configured node, in nodes.yaml order: id, name, url and the
    approved names tied to it; plus the names tied to no node (which count for
    every node). Read only, from local files: nothing is fetched."""
    try:
        nodes = yaml.safe_load(nodes_file.read_text(encoding="utf-8"))["nodes"]
    except (OSError, yaml.YAMLError, KeyError, TypeError) as exc:
        raise typer.BadParameter(f"cannot read the node list {_rel(nodes_file)}: {exc}") from exc
    try:
        names = ApprovedNames.load(scoped_file)
    except OSError as exc:
        raise typer.BadParameter(f"cannot read {_rel(scoped_file)}: {exc}") from exc
    rows = [
        {
            "id": n["id"],
            "name": n.get("name", ""),
            "url": n.get("url", ""),
            "approved": list(names.per_node.get(n["id"].lower(), ())),
        }
        for n in nodes
    ]
    return rows, list(names.unscoped)


def _columns(rows: list[list[str]], header: list[str] | None = None) -> str:
    """Plain, left-aligned columns: no box drawing and no wrapping, so a long
    URL stays on one line and the output can be piped to grep or cut."""
    table = ([header] if header else []) + rows
    widths = [max(len(r[i]) for r in table) for i in range(len(table[0]))]
    fmt = lambda r: "  ".join(c.ljust(w) for c, w in zip(r, widths, strict=True)).rstrip()  # noqa: E731
    out = [fmt(r) for r in table]
    if header:
        out.insert(1, "  ".join("-" * w for w in widths))
    return "\n".join(out)


def _approved_cell(row: dict) -> str:
    return "; ".join(row["approved"]) if row["approved"] else "(none)"


CONFIG_HEADER = ["Node id", "Node Landing Page URL", "Approved name"]


def _config_row(rows: list[dict], value: str) -> dict:
    """The row --show-node names: an id or a name, in any case, as for --skip.
    Unknown or ambiguous values are errors that list the valid ids."""
    known = ", ".join(r["id"] for r in rows)
    hits = [r for r in rows if value.strip().casefold() in _node_keys(r)]
    if not hits:
        raise typer.BadParameter(
            f"--show-node: no node matches {value!r}. Use a node id or name; ids are: {known}"
        )
    if len(hits) > 1:
        raise typer.BadParameter(
            f"--show-node {value!r} matches more than one node "
            f"({', '.join(r['id'] for r in hits)}); use the node id"
        )
    return hits[0]


def _print_listings(
    list_nodes: bool,
    list_nlps: bool,
    list_names: bool,
    print_config: bool,
    show_node: str = "",
) -> None:
    rows, unscoped = _config_rows()
    blocks: list[str] = []
    if list_nodes:
        blocks.append("\n".join(r["id"] for r in rows))
    if list_nlps:
        blocks.append(_columns([[r["id"], r["url"]] for r in rows]))
    if list_names:
        blocks.append(_columns([[r["id"], _approved_cell(r)] for r in rows]))
    if print_config:
        table = _columns(
            [[r["id"], r["url"], _approved_cell(r)] for r in rows],
            header=CONFIG_HEADER,
        )
        notes = [
            f"{len(rows)} node(s). Ids and URLs from {_rel(DEFAULT_NODES)}; approved "
            f"names from {_rel(SCOPED_APPROVED_NAMES)}.",
            f"assess and run use {_rel(DEFAULT_APPROVED_NAMES)} by default: the same "
            "names, unscoped, so each counts for every node.",
        ]
        if unscoped:
            notes.append(
                "Also tied to no node, so valid for every node: " + "; ".join(unscoped) + "."
            )
        blocks.append(table + "\n\n" + "\n".join(notes))
    if show_node.strip():
        row = _config_row(rows, show_node)
        blocks.append(
            _columns([[row["id"], row["url"], _approved_cell(row)]], header=CONFIG_HEADER)
        )
    typer.echo("\n\n".join(blocks))


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    list_nodes: bool = typer.Option(False, "--list-nodes", "--list-nodes-ids", help=H_LIST_NODES),
    list_nlps: bool = typer.Option(False, "--list-nlps", help=H_LIST_NLPS),
    list_approved_names: bool = typer.Option(
        False, "--list-approved-names", help=H_LIST_APPROVED_NAMES
    ),
    print_config: bool = typer.Option(False, "--print-config", help=H_PRINT_CONFIG),
    show_node: str = typer.Option("", "--show-node", metavar="NODE", help=H_SHOW_NODE),
) -> None:
    """Top-level listing flags. They read local files only and contact no node."""
    wanted = (list_nodes, list_nlps, list_approved_names, print_config, show_node)
    if not any(v.strip() if isinstance(v, str) else v for v in wanted):
        if ctx.invoked_subcommand is None:
            # What Typer prints for a bare `basic-check` when no callback exists.
            typer.echo(
                f"{ctx.get_usage()}\nTry 'basic-check --help' for help.\n\nError: Missing command.",
                err=True,
            )
            raise typer.Exit(2)
        return
    if ctx.invoked_subcommand is not None:
        raise typer.BadParameter(
            "--list-nodes, --list-nodes-ids, --list-nlps, --list-approved-names, "
            "--print-config and --show-node are used on their own, without a command."
        )
    _print_listings(*wanted)
    raise typer.Exit(0)


def _slug(url: str) -> str:
    """A stable, filesystem-safe node id derived from the URL.

    Includes the path, because several EOSC nodes live on a shared host: a bare
    hostname would make eosc.eu/a and eosc.eu/b collide and silently overwrite
    each other's evidence.
    """
    parsed = urlparse(url)
    raw = (parsed.netloc + parsed.path).lower()
    raw = re.sub(r"^www\.", "", raw)
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return slug or "one-off"


def _nodes_from_urls(urls: list[str], eosc_page: str = "") -> list[dict]:
    """Build throwaway node records from bare URLs given on the command line."""
    if eosc_page and len(urls) > 1:
        raise typer.BadParameter("--eosc-page applies to a single --url; pass a nodes file instead")
    nodes, seen = [], set()
    for url in urls:
        url = url.strip()
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise typer.BadParameter(f"--url must be an absolute http(s) URL, got {url!r}")
        node_id = _slug(url)
        if node_id in seen:
            raise typer.BadParameter(f"--url given twice for the same page: {url}")
        seen.add(node_id)
        nodes.append(
            {
                "id": node_id,
                "name": parsed.netloc.removeprefix("www."),
                "url": url,
                "eosc_page": eosc_page,
                "ad_hoc": True,
            }
        )
    return nodes


def _resolve(
    urls: list[str] | None,
    nodes_file: Path,
    only: str,
    results_dir: Path | None,
    eosc_page: str = "",
    skip: list[str] | None = None,
    node: str = "",
) -> tuple[list[dict], list[dict], Path]:
    """Decide what to fetch, what to report on, and where to write it.

    Two node lists, because they are not the same question. `--only` says which
    sites to send requests to; it does not say which nodes the report is about.
    Conflating them destroyed the published report: `assess --only egi` rewrote
    results.md, index.html and results.json wholesale with a single row, and a
    one-node table looks exactly like a complete one.

    So when writing to the published directory, the report always covers every
    node in the nodes file and `--only` narrows the fetch alone. Writing
    somewhere else with an explicit `--results` is the deliberate case — nothing
    published is at risk — and there `--only` narrows both, which is what makes
    a quick scratch run of one node usable.

    --url and --only remain mutually exclusive rather than silently ignored:
    --only filters a configured list by id, and an id the user never chose is
    not something to filter on.

    `--skip` is the opposite question and is answered differently: it takes the
    named nodes out of the run altogether, fetch *and* report, in every
    directory. Leaving a skipped node in the report would bring back the exit-2
    "no evidence" outcome the option exists to avoid. What keeps a shorter
    report from passing for a complete one is that the omission is recorded in
    results.json and stated in both reports (see _do_assess).
    """
    urls = [u for u in (urls or []) if u.strip()]
    skip_values = _split_values(skip)
    if node.strip():
        alt = _node_at_url(nodes_file, node.strip(), urls, only, skip_values, eosc_page)
        return [alt], [alt], _alternative_results_dir(results_dir)
    if urls:
        if only:
            raise typer.BadParameter(
                "--only filters the nodes file; it cannot be combined with --url"
            )
        if skip_values:
            raise typer.BadParameter(
                "--skip filters the nodes file; it cannot be combined with --url"
            )
        ad_hoc = _nodes_from_urls(urls, eosc_page)
        return ad_hoc, ad_hoc, (results_dir or DEFAULT_ONEOFF)
    if eosc_page:
        raise typer.BadParameter(
            "--eosc-page is only meaningful with --url; use nodes.yaml otherwise"
        )
    selected = _load_nodes(nodes_file, only)
    reported = selected if results_dir is not None else _load_nodes(nodes_file)
    if skip_values:
        skipped = _skip_ids(_load_nodes(nodes_file), skip_values)
        selected = [n for n in selected if n["id"] not in skipped]
        reported = [n for n in reported if n["id"] not in skipped]
        if not selected:
            raise typer.BadParameter("--skip leaves nothing left to check")
    return selected, reported, (results_dir if results_dir is not None else DEFAULT_RESULTS)


def _node_at_url(
    nodes_file: Path,
    node: str,
    urls: list[str],
    only: str,
    skip_values: list[str],
    eosc_page: str,
) -> dict:
    """The configured record of one node, with its landing page URL replaced.

    For checking a node at a page other than the registered one — a candidate
    new address, a staging copy, a mirror — without editing nodes.yaml. Unlike a
    bare --url, the node keeps its id, so its scoped approved name, its eosc_page
    and its evidence file name all still apply, and the result is comparable
    with the node's row in the federation run.

    The configured URL is kept on the record, so the report can say that this
    is not the registered page. Every ambiguity is an error rather than a
    guess, because a wrong guess would fetch a page the user did not ask for.
    """
    if only:
        raise typer.BadParameter("--node already selects the node; drop --only")
    if skip_values:
        raise typer.BadParameter("--node checks a single node; it cannot be combined with --skip")
    if len(urls) != 1:
        raise typer.BadParameter(
            "--node needs exactly one --url, the alternative landing page to check"
            + (f" (got {len(urls)})" if urls else "")
            + ". To check the node at its configured URL, use --only instead."
        )
    (url,) = urls
    url = url.strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise typer.BadParameter(f"--url must be an absolute http(s) URL, got {url!r}")
    nodes = _load_nodes(nodes_file)
    hits = [n for n in nodes if node.casefold() in _node_keys(n)]
    if not hits:
        known = ", ".join(n["id"] for n in nodes)
        raise typer.BadParameter(
            f"--node: no node matches {node!r}. Use a node id or name; ids are: {known}"
        )
    if len(hits) > 1:
        raise typer.BadParameter(
            f"--node {node!r} matches more than one node "
            f"({', '.join(n['id'] for n in hits)}); use the id"
        )
    record = dict(hits[0])
    record["configured_url"] = record["url"]
    record["url"] = url
    if eosc_page:
        record["configured_eosc_page"] = record.get("eosc_page", "")
        record["eosc_page"] = eosc_page
    return record


def _alternative_results_dir(results_dir: Path | None) -> Path:
    """Where a --node run writes. Never the published results/.

    The evidence file is named after the node id, so writing a --node run into
    results/ would overwrite the reviewed evidence for that node with a page
    that is not its registered one. Refused outright, not merely defaulted away.
    """
    if results_dir is None:
        return DEFAULT_ONEOFF
    if results_dir.resolve() == DEFAULT_RESULTS.resolve():
        raise typer.BadParameter(
            "--node would overwrite the published run in results/ with a page that is "
            "not the node's configured one. Drop --results (results/one-off/ is used) "
            "or name another folder."
        )
    return results_dir


def _split_values(values: list[str] | None) -> list[str]:
    """Flatten a repeatable option whose values may also be comma-separated,
    so `--skip a,b` and `--skip a --skip b` mean the same thing."""
    return [v.strip() for raw in (values or []) for v in raw.split(",") if v.strip()]


def _node_keys(node: dict) -> set[str]:
    """Every spelling that names this node for --skip, casefolded: its id, its
    name, and its name without an "EOSC Node " / "EOSC " prefix, so that
    `Italy` names "EOSC Node Italy" and `Finland` names "EOSC Finland"."""
    name = node.get("name", "")
    keys = {node["id"], name}
    for prefix in ("EOSC Node ", "EOSC "):
        if name.startswith(prefix):
            keys.add(name[len(prefix):])
    return {k.strip().casefold() for k in keys if k.strip()}


def _skip_ids(nodes: list[dict], values: list[str]) -> set[str]:
    """Resolve --skip values to node ids.

    Strict on purpose: an unmatched value is an error, not a no-op, because a
    typo that skipped nothing would fetch the very node the user meant to leave
    alone. A value naming more than one node is an error for the same reason.
    """
    ids: set[str] = set()
    unknown: list[str] = []
    for value in values:
        hits = [n["id"] for n in nodes if value.casefold() in _node_keys(n)]
        if not hits:
            unknown.append(value)
        elif len(hits) > 1:
            raise typer.BadParameter(
                f"--skip {value!r} matches more than one node ({', '.join(hits)}); use the id"
            )
        else:
            ids.add(hits[0])
    if unknown:
        known = ", ".join(n["id"] for n in nodes)
        raise typer.BadParameter(
            f"--skip: no node matches {', '.join(map(repr, unknown))}. "
            f"Use a node id or name; ids are: {known}"
        )
    return ids


def _skipped(nodes_file: Path, skip: list[str] | None, urls: list[str] | None) -> list[str]:
    """The ids --skip removed, for the record. Called after _resolve has
    validated the values, so it cannot raise for a reason _resolve did not."""
    values = _split_values(skip)
    if not values or [u for u in (urls or []) if u.strip()]:
        return []
    return sorted(_skip_ids(_load_nodes(nodes_file), values))


def _selection(only: str) -> list[str]:
    """The node ids named by --only, as a list."""
    return [x.strip() for x in only.split(",") if x.strip()]


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
    nodes_file: Path = typer.Option(
        DEFAULT_NODES, "--nodes", "-n", help=H_NODES, show_default="nodes.yaml"
    ),
    results_dir: Path = typer.Option(None, "--results", help=H_RESULTS, show_default="results/"),
    only: str = typer.Option("", "--only", help=H_ONLY),
    skip: list[str] = typer.Option(
        None,
        "--skip",
        help=H_SKIP,
    ),
    url: list[str] = typer.Option(
        None,
        "--url",
        help=H_URL,
    ),
    eosc_page: str = typer.Option("", "--eosc-page", help=H_EOSC_PAGE),
    node: str = typer.Option("", "--node", help=H_NODE),
    delay: float = typer.Option(2.0, "--delay", help=H_DELAY),
    depth: int = typer.Option(
        1,
        "--depth",
        min=0,
        max=2,
        help=H_DEPTH,
    ),
    max_children: int = typer.Option(
        MAX_CHILDREN, "--max-children", help=H_MAX_CHILDREN
    ),
    fetch_budget: int = typer.Option(
        DEFAULT_FETCH_BUDGET,
        "--fetch-budget",
        min=0,
        help=H_FETCH_BUDGET,
    ),
):
    """Fetch each landing page and save the evidence. Contacts the nodes.

    Depth 1 by default. Evidence goes to results/evidence/ (or --results DIR),
    with personal data masked. Nothing is judged here; run assess afterwards.
    """
    nodes, _reported, resolved = _resolve(
        url, nodes_file, only, results_dir, eosc_page, skip, node
    )
    _do_collect(nodes, resolved, delay, depth, max_children, fetch_budget)


def _do_collect(
    nodes: list[dict],
    results_dir: Path,
    delay: float,
    depth: int,
    max_children: int,
    fetch_budget: int = DEFAULT_FETCH_BUDGET,
) -> None:
    """The actual work, taking plain values.

    Kept separate from the Typer command because calling a Typer-decorated
    function directly from Python passes its OptionInfo defaults rather than the
    real ones. `run` did exactly that and crashed with
    "'OptionInfo' object has no attribute 'read_text'" for any argument the caller
    did not spell out. The tests now call these _do_* functions, so that class of
    breakage is caught.
    """
    evidence_dir = results_dir / "evidence"
    if depth >= 2:
        typer.echo(
            f"Fetching {len(nodes)} landing page(s), {delay}s apart, then following up to "
            f"{max_children} checklist-relevant link(s) per node, then one further hop "
            f"under a shared budget of {fetch_budget} request(s) (depth 2):"
        )
    elif depth >= 1:
        typer.echo(
            f"Fetching {len(nodes)} landing page(s), {delay}s apart, then following up to "
            f"{max_children} checklist-relevant link(s) per node (depth 1):"
        )
    else:
        typer.echo(f"Fetching {len(nodes)} landing page(s), one request each, {delay}s apart:")
    asyncio.run(
        collect_all(
            nodes,
            evidence_dir,
            delay_s=delay,
            depth=depth,
            max_children=max_children,
            fetch_budget=fetch_budget,
        )
    )
    typer.echo(f"\nEvidence written to {evidence_dir}")
    if depth == 1:
        # Discoverability: the deeper option is worth knowing about without
        # having to read --help. Say what it costs, so the hint is not a nudge
        # to hammer other people's servers.
        typer.echo(
            "\nTip: this was depth 1, the default. Add --depth=2 to follow one further "
            "hop from the pages already fetched (policy indexes that link on to the "
            f"actual policy), bounded by --fetch-budget, default {DEFAULT_FETCH_BUDGET} "
            "request(s) for the whole run. A depth-2 report shows both depths side by "
            "side so you can see what the extra requests bought."
        )


@app.command()
def assess(
    nodes_file: Path = typer.Option(
        DEFAULT_NODES, "--nodes", "-n", help=H_NODES, show_default="nodes.yaml"
    ),
    checklist_file: Path = typer.Option(
        DEFAULT_CHECKLIST, "--checklist", "-c", help=H_CHECKLIST,
        show_default=DEFAULT_CHECKLIST_LABEL,
    ),
    results_dir: Path = typer.Option(None, "--results", help=H_RESULTS, show_default="results/"),
    only: str = typer.Option("", "--only", help=H_ONLY),
    skip: list[str] = typer.Option(
        None,
        "--skip",
        help=H_SKIP,
    ),
    url: list[str] = typer.Option(
        None,
        "--url",
        help=H_URL,
    ),
    eosc_page: str = typer.Option("", "--eosc-page", help=H_EOSC_PAGE),
    node: str = typer.Option("", "--node", help=H_NODE),
    approved_names: Path | None = typer.Option(
        None,
        "--approved-names",
        help=H_APPROVED_NAMES,
    ),
    no_approved_names: bool = typer.Option(
        False,
        "--no-approved-names",
        help=H_NO_APPROVED_NAMES,
    ),
    strict_separators: bool = typer.Option(
        False,
        "--strict-separators",
        help=H_STRICT_SEPARATORS,
    ),
    run_id: str = typer.Option("", "--run", help=H_RUN),
):
    """Apply the checklist to already-collected evidence and write the reports.

    Offline: no node is contacted. Writes results.json, results.md, results.csv
    and index.html. Row headings come from the node list, so after changing a
    node's URL, rebuild an old run with --nodes pointing at the old list.
    """
    _fetched, reported, resolved = _resolve(
        url, nodes_file, only, results_dir, eosc_page, skip, node
    )
    _do_assess(
        reported, resolved, checklist_file, approved_names, run_id, no_approved_names,
        strict_separators=strict_separators,
        selection=_selection(only),
        skipped=_skipped(nodes_file, skip, url),
    )


def _digest(path: Path) -> str:
    """SHA-256 of the list actually read, or "" if it could not be read.

    The tool cannot know whether an approved-names file is current — that is a
    fact about the world, not about the bytes. What it can do is say precisely
    which bytes it used, so a reader comparing this run against the circulated
    file, or against an earlier run, has something to compare. Empty rather
    than the hash of nothing when no list was used: sha256("") is a
    real-looking hex string and would read as a list that was read and found
    empty.
    """
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _resolve_names(
    approved_names: Path | None,
    no_approved_names: bool,
    strict_separators: bool = False,
) -> tuple[ApprovedNames, str, bool, str]:
    """Decide which approved-name list a run uses, and record which it was.

    Three cases, in precedence order: an explicit opt-out, an operator file, or
    the list committed with the checklist. The report has to be able to say
    which one was in force — a reader must not have to assume that a run they
    are looking at vetted its own name list. Returns the list, a printable
    source, whether that source was the committed default, and the SHA-256 of
    the bytes read.
    """
    if no_approved_names:
        return ApprovedNames(), "", False, ""

    if approved_names is not None:
        try:
            loaded = ApprovedNames.load(approved_names, strict_separators=strict_separators)
            return loaded, str(approved_names), False, _digest(approved_names)
        except FileNotFoundError:
            # Neither a traceback nor a silent fall back to the default: the
            # operator named a specific list, and checking a different one is
            # not a smaller failure than checking none.
            raise typer.BadParameter(
                f"approved-names file not found: {approved_names}",
                param_hint="--approved-names",
            ) from None

    try:
        # Recorded repo-relative: the committed report is published, and the
        # absolute path of whoever ran it is neither useful nor theirs to leak.
        rel = DEFAULT_APPROVED_NAMES.relative_to(ROOT).as_posix()
        loaded = ApprovedNames.load(DEFAULT_APPROVED_NAMES, strict_separators=strict_separators)
        return loaded, rel, True, _digest(DEFAULT_APPROVED_NAMES)
    except FileNotFoundError:
        # Only reachable if the repository file was deleted. Say so instead of
        # quietly producing a run whose point 3 checked no name at all.
        typer.secho(
            f"warning: the default approved-names list is missing ({DEFAULT_APPROVED_NAMES}); "
            "point 3's name requirement will not be assessed",
            err=True,
            fg=typer.colors.YELLOW,
        )
        return ApprovedNames(), "", False, ""


def _do_assess(
    nodes: list[dict],
    results_dir: Path,
    checklist_file: Path,
    approved_names: Path | None = None,
    run_id: str = "",
    no_approved_names: bool = False,
    strict_separators: bool = False,
    selection: list[str] | None = None,
    skipped: list[str] | None = None,
) -> dict:
    """See _do_collect for why this is not the Typer command itself."""
    checklist = yaml.safe_load(checklist_file.read_text())
    evidence_dir = results_dir / "evidence"

    names, names_source, default_used, names_sha256 = _resolve_names(
        approved_names, no_approved_names, strict_separators
    )

    run = {
        "run_id": run_id or datetime.now(UTC).strftime("%Y-%m-%d-%H%M"),
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "checklist": checklist,
        "approved_names": {
            "supplied": names.supplied,
            "scoped": names.scoped,
            "count": len(names.unscoped) + sum(len(v) for v in names.per_node.values()),
            "source": names_source,
            "default_used": default_used,
            # Which bytes were used. Staleness is not something the tool can
            # judge, but it can be made checkable.
            "sha256": names_sha256,
            "strict_separators": names.strict_separators,
        },
        # Which nodes this run re-fetched, when that was narrower than the
        # report. Empty means the whole nodes file. Recorded because the report
        # now covers every node either way, so the reader would otherwise have
        # no way to tell how fresh any given row is.
        "selection": sorted(selection or []),
        # Which configured nodes --skip left out. They are absent from "nodes"
        # by request, not for want of evidence, so they are not missing_evidence
        # — but a report without them must say so.
        "skipped": sorted(skipped or []),
        # Kept for readers of older result files.
        "approved_names_supplied": names.supplied,
        "nodes": [],
    }

    missing: list[str] = []
    url_mismatch: list[dict] = []
    # --node runs: the node was checked at a page other than its configured one,
    # on purpose. Recorded so no report of it can pass for the node's assessment.
    alternative = [
        {"id": n["id"], "configured_url": n["configured_url"], "url": n["url"]}
        for n in nodes
        if n.get("configured_url")
    ]
    if alternative:
        run["alternative_url"] = alternative
    for node in nodes:
        path = evidence_dir / f"{node['id']}.json"
        if not path.exists():
            missing.append(node["id"])
            continue
        ev = load_evidence(evidence_dir, node["id"])
        # The row is labelled with the URL from the nodes file, but its verdicts
        # come from the evidence. After a URL change, and before the node is
        # collected again, the two describe different pages. Said out loud,
        # because otherwise the report shows the new address above verdicts it
        # never produced.
        if ev.requested_url and ev.requested_url != node["url"]:
            url_mismatch.append(
                {
                    "id": node["id"],
                    "configured_url": node["url"],
                    "evidence_url": ev.requested_url,
                    "fetched_at": ev.fetched_at,
                }
            )
        results = checks.run_all(ev, names, node.get('eosc_page', ''))
        # When the capture went two hops deep, also assess it as if it had not,
        # so the report can show what the second hop changed rather than
        # asserting it was worth it.
        shallow_results = None
        if ev.crawl_depth >= 2:
            shallow_results = checks.run_all(
                without_depth_2(ev), names, node.get('eosc_page', '')
            )
        run["nodes"].append(
            {
                "id": node["id"],
                "name": node["name"],
                "url": node["url"],
                "ad_hoc": node.get("ad_hoc", False),
                **(
                    {"configured_url": node["configured_url"]}
                    if node.get("configured_url")
                    else {}
                ),
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
                            "depth": c.depth,
                            "parent_url": c.parent_url,
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
                **(
                    {"results_depth_1": [asdict(r) for r in shallow_results]}
                    if shallow_results is not None
                    else {}
                ),
            }
        )

    for a in alternative:
        typer.secho(
            f"\n  {a['id']} was checked at an alternative URL, not its configured one:\n"
            f"    checked:    {a['url']}\n    configured: {a['configured_url']}\n"
            "  The report says so; it is not the node's assessment at its registered page.",
            fg=typer.colors.CYAN,
        )

    if url_mismatch:
        run["url_mismatch"] = url_mismatch
        lines = "\n".join(
            f"    {m['id']}: nodes file says {m['configured_url']}\n"
            f"    {' ' * len(m['id'])}  evidence is from {m['evidence_url']}"
            for m in url_mismatch
        )
        typer.secho(
            f"\n  {len(url_mismatch)} node(s) were assessed from evidence collected at a "
            f"different URL than the nodes file gives:\n{lines}\n  Collect them again, "
            "or assess with the node list the evidence was collected with (--nodes).",
            fg=typer.colors.YELLOW,
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
    return run


@app.command()
def run(
    nodes_file: Path = typer.Option(
        DEFAULT_NODES, "--nodes", "-n", help=H_NODES, show_default="nodes.yaml"
    ),
    results_dir: Path = typer.Option(None, "--results", help=H_RESULTS, show_default="results/"),
    only: str = typer.Option("", "--only", help=H_ONLY),
    skip: list[str] = typer.Option(
        None,
        "--skip",
        help=H_SKIP,
    ),
    url: list[str] = typer.Option(
        None,
        "--url",
        help=H_URL,
    ),
    eosc_page: str = typer.Option("", "--eosc-page", help=H_EOSC_PAGE),
    node: str = typer.Option("", "--node", help=H_NODE),
    checklist_file: Path = typer.Option(
        DEFAULT_CHECKLIST, "--checklist", "-c", help=H_CHECKLIST,
        show_default=DEFAULT_CHECKLIST_LABEL,
    ),
    approved_names: Path | None = typer.Option(
        None,
        "--approved-names",
        help=H_APPROVED_NAMES,
    ),
    no_approved_names: bool = typer.Option(
        False, "--no-approved-names", help=H_NO_APPROVED_NAMES
    ),
    strict_separators: bool = typer.Option(
        False,
        "--strict-separators",
        help=H_STRICT_SEPARATORS,
    ),
    run_id: str = typer.Option("", "--run", help=H_RUN),
    delay: float = typer.Option(2.0, "--delay", help=H_DELAY),
    depth: int = typer.Option(
        1,
        "--depth",
        min=0,
        max=2,
        help=H_DEPTH,
    ),
    fetch_budget: int = typer.Option(
        DEFAULT_FETCH_BUDGET,
        "--fetch-budget",
        min=0,
        help=H_FETCH_BUDGET,
    ),
):
    """collect, then assess, in one go. Contacts the nodes.

    Takes the options of both, except --max-children (always 8 here).
    """
    # Resolve once so both phases agree on the node list and the directory.
    nodes, reported, resolved = _resolve(
        url, nodes_file, only, results_dir, eosc_page, skip, node
    )
    _do_collect(nodes, resolved, delay, depth, MAX_CHILDREN, fetch_budget)
    _do_assess(
        reported, resolved, checklist_file, approved_names, run_id, no_approved_names,
        strict_separators=strict_separators,
        selection=_selection(only),
        skipped=_skipped(nodes_file, skip, url),
    )


@app.command()
def points(checklist_file: Path = typer.Option(
        DEFAULT_CHECKLIST, "--checklist", "-c", help=H_CHECKLIST,
        show_default=DEFAULT_CHECKLIST_LABEL,
    )):
    """Print the checklist points and whether each is machine-decidable. Offline."""
    checklist = yaml.safe_load(checklist_file.read_text())
    typer.echo(
        f"Checklist v{checklist.get('checklist_version', '?')} "
        f"({checklist.get('checklist_date', '?')}) from {checklist_file}"
    )
    if checklist.get("source_file"):
        typer.echo(
            f"  transcribed from checklist/{checklist['source_file']} "
            f"sha256:{str(checklist.get('source_sha256', ''))[:12]}…"
        )
    typer.echo("")
    for p in checklist["points"]:
        labels = {True: "by inspection", "partial": "partly", False: "human judgement"}
        dec = labels[p.get("decidable")]
        impl = p.get("implemented_by", "—")
        typer.echo(f"{p['id']:4} [{dec:15}] {impl:12} {p['title']}")


@app.command()
def show(
    node_id: str = typer.Argument(..., help="Node id, e.g. geant (see basic-check --help)."),
    results_dir: Path = typer.Option(
        DEFAULT_RESULTS, "--results", help="Results folder to read.", show_default="results/"
    ),
    one_off: bool = typer.Option(
        False, "--one-off", help="Read the --url or --node results in results/one-off/ instead."
    ),
):
    """Print one node's results from an existing run. Offline."""
    if one_off:
        results_dir = DEFAULT_ONEOFF
    data = json.loads((results_dir / "results.json").read_text())
    for node in data["nodes"]:
        if node["id"] == node_id:
            typer.echo(f"{node['name']} — {node['url']}")
            if node.get("configured_url"):
                typer.echo(f"  (alternative URL; configured: {node['configured_url']})")
            for res in node["results"]:
                typer.echo(f"\n  [{res['verdict']}] {res['point_id']} {res['title']}")
                typer.echo(f"      {' '.join(res['message'].split())}")
                for item in res.get("evidence", []):
                    typer.echo(f"      - {item}")
            return
    raise typer.BadParameter(f"no results for {node_id}")


if __name__ == "__main__":
    app()
