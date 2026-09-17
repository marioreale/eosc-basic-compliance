"""Results as a matrix: nodes down, checklist points across. Plus CSV and Markdown.

The matrix is the deliverable. One glance should answer "which node fails what",
and every cell should be clickable through to the evidence that produced it.
"""

from __future__ import annotations

import csv
import html
import json
from datetime import UTC, datetime
from pathlib import Path

VERDICT_STYLE = {
    "PASS": ("pass", "PASS", "✓"),
    "FAIL": ("fail", "FAIL", "✗"),
    "MANUAL_REVIEW": ("manual", "REVIEW", "?"),
    "ERROR": ("error", "ERROR", "!"),
}

CSS = """
:root{--bg:#fff;--fg:#1a1d21;--muted:#5b6470;--line:#e3e7ec;
--pass:#0f7b3f;--pass-bg:#e7f5ec;--fail:#b3261e;--fail-bg:#fdeceb;
--manual:#8a5a00;--manual-bg:#fdf3e0;--error:#5b21b6;--error-bg:#f3ecfd;}
*{box-sizing:border-box}
body{margin:0;padding:2.5rem 2rem 4rem;background:var(--bg);color:var(--fg);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1500px;margin:0 auto}
h1{font-size:1.65rem;margin:0 0 .3rem;letter-spacing:-.01em}
h2{font-size:1.15rem;margin:2.5rem 0 .75rem;padding-bottom:.35rem;border-bottom:1px solid var(--line)}
.sub{color:var(--muted);margin:0 0 1.5rem;font-size:.92rem}
.banner{border:1px solid #f0c98a;background:var(--manual-bg);border-left:4px solid #d98f00;
padding:.9rem 1.1rem;border-radius:6px;margin:0 0 1.75rem;font-size:.9rem}
.banner strong{color:#7a4f00}
.counts{display:flex;gap:.5rem;flex-wrap:wrap;margin:0 0 1.5rem}
.chip{border:1px solid var(--line);border-radius:999px;padding:.3rem .8rem;font-size:.82rem;
font-variant-numeric:tabular-nums}
.chip b{font-weight:650}
table{border-collapse:separate;border-spacing:0;width:100%;font-size:.88rem}
th,td{padding:.5rem .55rem;text-align:left;vertical-align:middle}
thead th{position:sticky;top:0;background:#fafbfc;border-bottom:2px solid var(--line);
font-size:.76rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:650}
.matrix tbody tr:nth-child(even){background:#fcfcfd}
.matrix td.node{font-weight:600;white-space:nowrap}
.matrix td.node a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
.matrix th.pt{text-align:center;width:4.6rem}
.matrix td.cell{text-align:center;padding:.35rem .3rem}
.v{display:inline-block;min-width:2.9rem;padding:.22rem .45rem;border-radius:4px;
font-size:.72rem;font-weight:700;letter-spacing:.02em}
.v.pass{color:var(--pass);background:var(--pass-bg)}
.v.fail{color:var(--fail);background:var(--fail-bg)}
.v.manual{color:var(--manual);background:var(--manual-bg)}
.v.error{color:var(--error);background:var(--error-bg)}
.legend{margin:.9rem 0 0;font-size:.84rem;color:var(--muted)}
.legend .v{margin-right:.3rem}
.legend div{margin:.3rem 0}
details.node{border:1px solid var(--line);border-radius:7px;margin:.6rem 0;overflow:hidden}
details.node>summary{padding:.7rem .9rem;cursor:pointer;background:#fafbfc;font-weight:600;
display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
details.node>summary::-webkit-details-marker{display:none}
summary .url{font-weight:400;color:var(--muted);font-size:.83rem;word-break:break-all}
.finding{padding:.75rem .9rem;border-top:1px solid var(--line)}
.finding .hd{display:flex;gap:.55rem;align-items:baseline;flex-wrap:wrap}
.finding .pid{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;
background:#f1f3f6;border-radius:3px;padding:.1rem .35rem;white-space:nowrap}
.finding .ti{font-weight:600;font-size:.9rem}
.finding .msg{margin:.45rem 0 0;font-size:.88rem}
.finding ul{margin:.45rem 0 0;padding-left:1.1rem;font-size:.83rem;color:var(--muted)}
.finding li{margin:.15rem 0;word-break:break-word}
.finding .act{margin:.5rem 0 0;font-size:.83rem;padding:.4rem .6rem;background:#f7f9fb;
border-left:3px solid #c9d3de;border-radius:0 4px 4px 0}
.finding .act b{color:var(--fg)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em}
.foot{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);
color:var(--muted);font-size:.82rem}
.foot a{color:#0b5fa5}
"""


def _point_titles(points: list[dict]) -> dict[str, str]:
    return {p["id"]: p["title"] for p in points}


def render_html(run: dict, out: Path) -> Path:
    points = run["checklist"]["points"]
    titles = _point_titles(points)
    order = [p["id"] for p in points]
    decidable = {p["id"]: p.get("decidable") for p in points}

    tally: dict[str, int] = {}
    for node in run["nodes"]:
        for res in node["results"]:
            tally[res["verdict"]] = tally.get(res["verdict"], 0) + 1

    head = "".join(
        f'<th class="pt" title="{html.escape(titles.get(pid, ""))}">{html.escape(pid)}</th>'
        for pid in order
    )
    rows = []
    for node in run["nodes"]:
        by_id = {r["point_id"]: r for r in node["results"]}
        cells = []
        for pid in order:
            res = by_id.get(pid)
            if not res:
                cells.append('<td class="cell">—</td>')
                continue
            cls, label, _ = VERDICT_STYLE.get(res["verdict"], ("manual", res["verdict"], "?"))
            tip = html.escape(res["message"][:300])
            cells.append(f'<td class="cell"><span class="v {cls}" title="{tip}">{label}</span></td>')
        rows.append(
            f'<tr><td class="node"><a href="#{html.escape(node["id"])}">'
            f'{html.escape(node["name"])}</a></td>{"".join(cells)}</tr>'
        )

    blocks = []
    for node in run["nodes"]:
        findings = []
        for res in node["results"]:
            cls, label, _ = VERDICT_STYLE.get(res["verdict"], ("manual", res["verdict"], "?"))
            ev_items = "".join(f"<li>{html.escape(str(e))}</li>" for e in res.get("evidence", []))
            act = (
                f'<p class="act"><b>Reviewer action:</b> {html.escape(res["reviewer_action"])}</p>'
                if res.get("reviewer_action")
                else ""
            )
            findings.append(
                f'<div class="finding"><div class="hd"><span class="v {cls}">{label}</span>'
                f'<span class="pid">{html.escape(res["point_id"])}</span>'
                f'<span class="ti">{html.escape(res["title"])}</span></div>'
                f'<p class="msg">{html.escape(res["message"])}</p>'
                f'{f"<ul>{ev_items}</ul>" if ev_items else ""}{act}</div>'
            )
        meta = node.get("fetch", {})
        status = meta.get("http_status")
        status_txt = f"HTTP {status}" if status else (meta.get("error") or "not fetched")
        blocks.append(
            f'<details class="node" id="{html.escape(node["id"])}"><summary>'
            f'{html.escape(node["name"])} <span class="url">{html.escape(node["url"])}</span>'
            f'<span class="url">· {html.escape(str(status_txt))}</span></summary>'
            f'{"".join(findings)}</details>'
        )

    chips = "".join(
        f'<span class="chip"><span class="v {VERDICT_STYLE[v][0]}">{VERDICT_STYLE[v][1]}</span> '
        f"<b>{tally.get(v, 0)}</b></span>"
        for v in ("PASS", "FAIL", "MANUAL_REVIEW", "ERROR")
        if tally.get(v)
    )

    auto = [pid for pid, d in decidable.items() if d is True]
    partial = [pid for pid, d in decidable.items() if d == "partial"]
    human = [pid for pid, d in decidable.items() if d is False]

    legend_rows = "".join(
        f'<div><span class="v {VERDICT_STYLE[v][0]}">{VERDICT_STYLE[v][1]}</span> {desc}</div>'
        for v, desc in [
            ("PASS", "Satisfied, and the tool can show why."),
            ("FAIL", "Violated, and the tool can show why."),
            (
                "MANUAL_REVIEW",
                "A human must decide. Either the checklist point turns on a judgement, or it "
                "quantifies over things one page request cannot see. Evidence is attached.",
            ),
            ("ERROR", "The tool could not assess the page at all."),
        ]
    )

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EOSC Node Landing Page compliance — checklist v{html.escape(run["checklist"]["checklist_version"])}</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>EOSC Node Landing Page compliance</h1>
<p class="sub">Node Landing Page Verification Checklist v{html.escape(run["checklist"]["checklist_version"])}
({html.escape(run["checklist"]["checklist_date"])}) · {len(run["nodes"])} nodes ·
run <code>{html.escape(run["run_id"])}</code> · {html.escape(run["generated_at"])}</p>

<div class="banner"><strong>This is not a compliance statement.</strong> Of the
{len(order)} checklist points, {len(auto)} can be settled by inspection
({", ".join(auto)}), {len(partial)} only partly ({", ".join(partial)}), and
{len(human)} require a human reading the page ({", ".join(human)}). Every
<span class="v manual">REVIEW</span> below is a point this tool deliberately
refuses to guess at. One page request per node was made; no links were followed.</div>

<div class="counts">{chips}</div>

<h2>Matrix</h2>
<table class="matrix"><thead><tr><th>Node</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>
<div class="legend">{legend_rows}</div>

<h2>Per-node detail</h2>
{"".join(blocks)}

<h2>Checklist points</h2>
<table><thead><tr><th style="width:3.5rem">Point</th><th>Requirement</th><th style="width:7rem">Decidable</th></tr></thead><tbody>
{"".join(
    f'<tr><td><code>{html.escape(p["id"])}</code></td><td><b>{html.escape(p["title"])}</b><br>'
    f'<span style="color:var(--muted);font-size:.86em">{html.escape(p["requirement"])}</span><br>'
    f'<span style="color:var(--muted);font-size:.83em"><i>{html.escape(p.get("decidable_note", ""))}</i></span></td>'
    f'<td>{"by inspection" if p.get("decidable") is True else ("partly" if p.get("decidable") == "partial" else "human")}</td></tr>'
    for p in points
)}
</tbody></table>

<p class="foot">Generated by <a href="https://github.com/marioreale/eosc-basic-compliance">eosc-basic-compliance</a>.
Points 1&nbsp;and&nbsp;1R correspond to the two paragraphs of checklist point&nbsp;1; 5a–5c to its
sub-points. Evidence for every verdict is in <code>results/evidence/</code>.</p>
</div></body></html>"""
    out.write_text(doc, encoding="utf-8")
    return out


def render_csv(run: dict, out: Path) -> Path:
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["node_id", "node_name", "url", "point_id", "point_title", "verdict", "message"])
        for node in run["nodes"]:
            for res in node["results"]:
                writer.writerow([
                    node["id"], node["name"], node["url"],
                    res["point_id"], res["title"], res["verdict"],
                    " ".join(res["message"].split()),
                ])
    return out


def render_markdown(run: dict, out: Path) -> Path:
    points = run["checklist"]["points"]
    order = [p["id"] for p in points]
    short = {"PASS": "PASS", "FAIL": "**FAIL**", "MANUAL_REVIEW": "review", "ERROR": "ERROR"}

    lines = [
        f"# EOSC Node Landing Page compliance — checklist v{run['checklist']['checklist_version']}",
        "",
        f"Run `{run['run_id']}` · {run['generated_at']} · {len(run['nodes'])} nodes · "
        "one page request per node, no crawling.",
        "",
        "> **This is not a compliance statement.** Points marked `review` are ones this tool "
        "refuses to guess at: they either turn on a judgement (\"clearly state\") or quantify "
        "over things a single page request cannot see (\"all research resources\").",
        "",
        "| Node | " + " | ".join(order) + " |",
        "|---|" + "---|" * len(order),
    ]
    for node in run["nodes"]:
        by_id = {r["point_id"]: r for r in node["results"]}
        cells = [short.get(by_id[p]["verdict"], "?") if p in by_id else "—" for p in order]
        lines.append(f"| {node['name']} | " + " | ".join(cells) + " |")

    lines += ["", "## Points", ""]
    for p in points:
        dec = (
            "decidable by inspection"
            if p.get("decidable") is True
            else ("partly decidable" if p.get("decidable") == "partial" else "needs a human")
        )
        lines.append(f"**{p['id']} — {p['title']}** ({dec})  ")
        lines.append(f"{' '.join(p['requirement'].split())}")
        lines.append("")

    lines += ["## Detail", ""]
    for node in run["nodes"]:
        lines.append(f"### {node['name']}")
        lines.append(f"<{node['url']}>")
        lines.append("")
        for res in node["results"]:
            lines.append(f"- **{res['point_id']}** {short.get(res['verdict'], res['verdict'])} — {' '.join(res['message'].split())}")
            for item in res.get("evidence", [])[:4]:
                lines.append(f"  - {item}")
            if res.get("reviewer_action"):
                lines.append(f"  - *Reviewer action:* {res['reviewer_action']}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_all(run: dict, results_dir: Path) -> dict[str, Path]:
    results_dir.mkdir(parents=True, exist_ok=True)
    run.setdefault("generated_at", datetime.now(UTC).isoformat(timespec="seconds"))
    paths = {
        "json": results_dir / "results.json",
        "html": results_dir / "index.html",
        "csv": results_dir / "results.csv",
        "md": results_dir / "results.md",
    }
    paths["json"].write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
    render_html(run, paths["html"])
    render_csv(run, paths["csv"])
    render_markdown(run, paths["md"])
    return paths
