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

from .privacy import mask_data

VERDICT_STYLE = {
    "PASS": ("pass", "PASS", "✓"),
    "FAIL": ("fail", "FAIL", "✗"),
    "MANUAL_REVIEW": ("manual", "REVIEW", "?"),
    "ERROR": ("error", "ERROR", "!"),
}

# GitHub renders Markdown through a sanitiser that strips style attributes and
# CSS, so the HTML report's colours do not survive there. A coloured disc is the
# only colour primitive that renders consistently in a Markdown table on GitHub,
# so the Markdown and CSV outputs carry one alongside the word. The word is kept
# because colour alone fails for colour-blind readers and in plain-text diffs.
VERDICT_MD = {
    "PASS": "🟢 PASS",
    "FAIL": "🔴 **FAIL**",
    "MANUAL_REVIEW": "🟠 review",
    "ERROR": "🟣 ERROR",
}

# One line per checklist point, for readers who will not open the checklist PDF.
# This is what the matrix columns mean in practice, as opposed to the formal
# requirement text, which lives in checklist/v3.0.yaml and the generated
# checklist HTML page.
COLUMN_GLOSS = {
    "1": "Is the landing page itself reachable without logging in (or via EOSC AAI)?",
    "1R": "Are the resources the landing page points to also public or behind EOSC AAI?",
    "2": "Does the page state the node's scope, its intended users, and who runs it?",
    "3": "Is the EOSC logo shown, together with the official Tripartite-approved node name?",
    "4": "Does the page link to this node's own entry on eosc.eu (not the homepage or the index)?",
    "5a": "Is there an English purpose description for the node's research resources?",
    "5b": "Is an Acceptable Use Policy (AUP) reachable for those resources?",
    "5c": "Is a User Access Policy (UAP) reachable for those resources?",
    "6": "Is there a way to contact the node's helpdesk?",
    "7": "Is the landing page in English?",
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
.adhoc{border:1px solid #d9b8e8;background:#f9f2fd;border-left:4px solid #8e44ad;
padding:.85rem 1rem;border-radius:0 5px 5px 0;margin:0 0 1rem;font-size:.92rem;color:#4a2560}
thead th.pt a{color:inherit;text-decoration:none;border-bottom:1px dotted #b9c2cd}
thead th.pt a:hover{color:#0b5fa5;border-bottom-color:#0b5fa5}
.cols{margin:1.6rem 0 0}
.cols table{width:100%;border-collapse:collapse;font-size:.88rem}
.cols th,.cols td{text-align:left;padding:.42rem .6rem;border-bottom:1px solid var(--line);
vertical-align:top}
.cols thead th{font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;
color:var(--muted);background:#fafbfc}
.cols td.k{font:600 .82rem ui-monospace,SFMono-Regular,Menlo,monospace;white-space:nowrap}
.cols td.d{white-space:nowrap;font-size:.8rem;color:var(--muted)}
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


def _freshness_note(run: dict) -> str:
    """A sentence when the rows of a report do not share a capture date.

    `--only` narrows which sites a run re-fetches, but the report still covers
    every node — that is what stops a subset run replacing the published table
    with a shorter one that looks complete. The cost is mixed freshness under a
    single run timestamp in the header, which would otherwise imply every row is
    as fresh as the newest. Returns "" for a full run, so the ordinary report
    gains no caveat it does not need.
    """
    selection = run.get("selection") or []
    if not selection:
        return ""
    reused = [n for n in run["nodes"] if n["id"] not in selection]
    if not reused:
        return ""
    dates = sorted(
        {(n.get("fetch") or {}).get("fetched_at", "")[:10] for n in reused} - {""}
    )
    when = f" (captured {dates[0]})" if len(dates) == 1 else (
        f" (captured between {dates[0]} and {dates[-1]})" if dates else ""
    )
    named = ", ".join(sorted(selection))
    return (
        f"**Mixed freshness.** Only {named} {'was' if len(selection) == 1 else 'were'} "
        f"re-fetched in this run. The other {len(reused)} node(s) were not re-fetched; "
        f"their rows are reused from evidence already on disk{when}. The run timestamp "
        "above is this assessment, not their capture."
    )


def _skipped_note(run: dict) -> str:
    """A sentence naming the nodes --skip left out of this run, or "".

    A shorter table must not pass for a complete one. That is why --only never
    narrows the published report; --skip does narrow it, by request, and this
    sentence is what keeps the omission visible. Plain text (no Markdown), so
    each report can apply its own emphasis to the lead-in.
    """
    skipped = run.get("skipped") or []
    if not skipped:
        return ""
    return (
        f"{', '.join(skipped)} {'was' if len(skipped) == 1 else 'were'} left out of "
        "this run with --skip: not fetched, not assessed and not shown below. "
        "This table does not cover every configured node."
    )


def _alternative_url_note(run: dict) -> str:
    """A sentence naming nodes checked with --node at a page other than their
    configured one, or "".

    Such a row keeps the node's id and name, so without this it would read as
    the node's assessment. Plain text, like _skipped_note.
    """
    alternative = run.get("alternative_url") or []
    if not alternative:
        return ""
    parts = [
        f"{a['id']} was checked at {a['url']}, not at its configured landing page "
        f"{a['configured_url']}"
        for a in alternative
    ]
    one = len(alternative) == 1
    return (
        "; ".join(parts)
        + ". This is a trial of an alternative URL requested with --node, not "
        + ("the node's" if one else "those nodes'")
        + " assessment at the registered page, and it should not be quoted as one."
    )


def _url_mismatch_note(run: dict) -> str:
    """A sentence naming nodes whose evidence came from another URL, or "".

    `assess` labels each row with the URL in the nodes file, but judges the
    evidence on disk. After a URL change the two can describe different pages;
    this sentence keeps the row heading from passing for what was fetched.
    Plain text, like _skipped_note.
    """
    mismatches = run.get("url_mismatch") or []
    if not mismatches:
        return ""
    parts = [
        f"{m['id']} is configured as {m['configured_url']}, but its evidence was "
        f"collected from {m['evidence_url']} ({(m.get('fetched_at') or '')[:10] or 'date unknown'})"
        for m in mismatches
    ]
    one = len(mismatches) == 1
    return (
        "; ".join(parts)
        + (". That row shows" if one else ". Those rows show")
        + " the verdicts for the page the evidence came from, not for the configured "
        + ("URL. Collect it again before treating the row as current." if one else
           "URLs. Collect them again before treating the rows as current.")
    )


def _names_sentence(run: dict) -> str:
    """Plain prose about the approved-name list behind point 3.

    Absence is the common case and the one that misleads, so it is stated
    rather than left to be inferred from a missing evidence line.
    """
    info = run.get("approved_names") or {}
    if not info:  # result files written before the list was recorded in detail
        info = {"supplied": run.get("approved_names_supplied", False), "scoped": False, "count": 0}
    if not info.get("supplied"):
        return (
            "No approved-name list was used, so the name half of point 3 was not "
            "assessed at all: a REVIEW there says nothing about the node name."
        )
    n = info.get("count", 0)
    # Which list was in force is part of the finding. A reader must not have to
    # assume that the run's operator reviewed the names it was checked against.
    which = (
        "the official list committed with the checklist"
        if info.get("default_used")
        else "a list supplied for this run"
    )
    # The bytes actually read. The tool cannot judge whether the list is
    # current; naming its digest is what lets a reader check that for themselves.
    digest = info.get("sha256") or ""
    prov = f" (`{info.get('source', '')}`, sha256 `{digest[:12]}…`)" if digest else ""
    # Never claim the lax rule when the strict one was in force.
    rule = (
        " Separator glyphs were matched literally (`--strict-separators`), so a page "
        "writing “EOSC Node - X” does NOT satisfy a list writing “EOSC Node | X”."
        if info.get("strict_separators")
        else " Separator glyphs are treated as interchangeable, so a page writing "
        "“EOSC Node - X” satisfies a list writing “EOSC Node | X”."
    )
    if info.get("scoped"):
        return (
            f"{n} approved node name(s) were used, from {which}{prov}, tied to specific "
            f"nodes. A name is only matched against the node it was written for.{rule}"
        )
    return (
        f"{n} approved node name(s) were used, from {which}{prov}, as an unscoped list: a "
        "match shows the name appears on the page but not that it is that node's own "
        f"name.{rule}"
    )


def render_html(run: dict, out: Path) -> Path:
    points = run["checklist"]["points"]
    titles = _point_titles(points)
    order = [p["id"] for p in points]
    decidable = {p["id"]: p.get("decidable") for p in points}

    tally: dict[str, int] = {}
    for node in run["nodes"]:
        for res in node["results"]:
            tally[res["verdict"]] = tally.get(res["verdict"], 0) + 1

    version = run["checklist"].get("checklist_version", "3.0")
    checklist_href = f"checklist-v{version}.html"
    head = "".join(
        f'<th class="pt" title="{html.escape(pid)} — {html.escape(titles.get(pid, ""))}: '
        f'{html.escape(COLUMN_GLOSS.get(pid, ""))}">'
        f'<a href="{checklist_href}#p{html.escape(pid)}">{html.escape(pid)}</a></th>'
        for pid in order
    )
    def _rows_for(key: str) -> list[str]:
        out = []
        for node in run["nodes"]:
            by_id = {r["point_id"]: r for r in node.get(key, node["results"])}
            cs = []
            for pid in order:
                res = by_id.get(pid)
                if not res:
                    cs.append('<td class="cell">—</td>')
                    continue
                cls, label, _ = VERDICT_STYLE.get(res["verdict"], ("manual", res["verdict"], "?"))
                tip = html.escape(res["message"][:300])
                cs.append(
                    f'<td class="cell"><span class="v {cls}" title="{tip}">{label}</span></td>'
                )
            out.append(
                f'<tr><td class="node"><a href="#{html.escape(node["id"])}">'
                f'{html.escape(node["name"])}</a></td>{"".join(cs)}</tr>'
            )
        return out

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

    # A depth-2 run is reported twice from one capture: what the default depth
    # would have concluded, and what the extra hop concluded. Showing only the
    # deeper result would hide whether the extra requests changed anything.
    dual = _dual_depth(run)
    dual_block = dual_after = ""
    matrix_heading = "<h2>Matrix</h2>"
    if dual:
        changes = _depth_changes(run)
        d1 = _tally(run, "results_depth_1")
        d2 = _tally(run, "results")
        pages = _depth_2_pages(run)
        shallow_rows = "".join(_rows_for("results_depth_1"))
        chips1 = "".join(
            f'<span class="chip"><span class="v {VERDICT_STYLE[v][0]}">{VERDICT_STYLE[v][1]}</span> '
            f"<b>{d1.get(v, 0)}</b></span>"
            for v in ("PASS", "FAIL", "MANUAL_REVIEW", "ERROR")
            if d1.get(v)
        )
        chips2 = "".join(
            f'<span class="chip"><span class="v {VERDICT_STYLE[v][0]}">{VERDICT_STYLE[v][1]}</span> '
            f"<b>{d2.get(v, 0)}</b></span>"
            for v in ("PASS", "FAIL", "MANUAL_REVIEW", "ERROR")
            if d2.get(v)
        )
        if changes:
            rows_ch = "".join(
                f"<tr><td>{html.escape(n)}</td><td>{html.escape(pid)}</td>"
                f'<td><span class="v {VERDICT_STYLE.get(w, ("manual", w, ""))[0]}">'
                f'{VERDICT_STYLE.get(w, ("manual", w, ""))[1]}</span></td>'
                f'<td><span class="v {VERDICT_STYLE.get(g, ("manual", g, ""))[0]}">'
                f'{VERDICT_STYLE.get(g, ("manual", g, ""))[1]}</span></td></tr>'
                for n, pid, w, g in changes
            )
            changed_html = (
                f"<p>{len(changes)} cell(s) differ between the two depths. The deeper "
                "verdict is the one shown in the per-node detail below.</p>"
                '<table><thead><tr><th>Node</th><th>Point</th><th>At depth 1</th>'
                f"<th>At depth 2</th></tr></thead><tbody>{rows_ch}</tbody></table>"
            )
        else:
            changed_html = (
                f"<p><b>No verdict changed.</b> The second hop fetched {len(pages)} "
                f"page(s) and left all {sum(d2.values())} cells exactly as depth 1 had "
                "them. That is a finding rather than a failure of the deeper crawl: the "
                "points still marked <i>review</i> turn on a judgement, or quantify over "
                "things no crawl enumerates, so fetching more pages cannot settle them. "
                "This is why depth 1 remains the default.</p>"
            )
        pages_html = ""
        if pages:
            prows = "".join(
                f"<tr><td>{html.escape(n)}</td>"
                f'<td>{html.escape(", ".join(c.get("selected_for", [])) or "—")}</td>'
                f'<td><a href="{html.escape(str(c.get("url", "")))}">'
                f'{html.escape(_ellipsis(str(c.get("url", "")), 78))}</a></td>'
                f'<td>{html.escape(str(c.get("http_status") or ("error" if c.get("error") else "—")))}</td></tr>'
                for n, c in pages
            )
            pages_html = (
                "<h3>Pages the second hop fetched</h3><table><thead><tr><th>Node</th>"
                "<th>Followed for</th><th>Page</th><th>Served</th></tr></thead>"
                f"<tbody>{prows}</tbody></table>"
            )
        dual_block = (
            '<div class="note"><b>This run was collected at depth 2, and is reported '
            "twice.</b> Both tables come from the same capture — the shallow view is the "
            "deep evidence with the second-hop pages set aside, not a separate run — so "
            "any difference between them is the extra hop and not the passage of time."
            "</div>"
            "<h2>Results at depth 1</h2>"
            "<p>Landing page plus links that can settle a checklist point. This is the "
            f'default the tool ships with.</p><div class="chips">{chips1}</div>'
            f'<table class="matrix"><thead><tr><th>Node</th>{head}</tr></thead>'
            f"<tbody>{shallow_rows}</tbody></table>"
            "<h2>Results at depth 2</h2>"
            f"<p>The same evidence plus {len(pages)} page(s) reached one hop further out, "
            "under a shared run budget.</p>"
            f'<div class="chips">{chips2}</div>'
        )
        dual_after = f"<h3>What the second hop changed</h3>{changed_html}{pages_html}"
        # The two depth headings replace the single "Matrix" heading.
        matrix_heading = ""

    # Rendered as a banner rather than folded into the node-names one: it is a
    # claim about the whole table's freshness, not about point 3.
    fresh = _freshness_note(run)
    freshness_block = (
        f'\n<div class="banner">{html.escape(fresh)}</div>\n' if fresh else ""
    )
    skipped = _skipped_note(run)
    if skipped:
        freshness_block += (
            f'\n<div class="banner"><strong>Skipped by request.</strong> '
            f"{html.escape(skipped)}</div>\n"
        )
    alternative = _alternative_url_note(run)
    if alternative:
        freshness_block += (
            f'\n<div class="adhoc"><strong>Alternative URL, not a federation run.</strong> '
            f"{html.escape(alternative)}</div>\n"
        )
    mismatch = _url_mismatch_note(run)
    if mismatch:
        freshness_block += (
            f'\n<div class="banner"><strong>Evidence from a different URL.</strong> '
            f"{html.escape(mismatch)}</div>\n"
        )

    chips = "".join(
        f'<span class="chip"><span class="v {VERDICT_STYLE[v][0]}">{VERDICT_STYLE[v][1]}</span> '
        f"<b>{tally.get(v, 0)}</b></span>"
        for v in ("PASS", "FAIL", "MANUAL_REVIEW", "ERROR")
        if tally.get(v)
    )

    dec_label = {
        True: ("pass", "by inspection"),
        "partial": ("manual", "partly"),
        False: ("error", "human judgement"),
    }
    cols_rows = "".join(
        f'<tr><td class="k"><a href="{checklist_href}#p{html.escape(p["id"])}">'
        f'{html.escape(p["id"])}</a></td>'
        f'<td>{html.escape(COLUMN_GLOSS.get(p["id"], p["title"]))}</td>'
        f'<td class="d"><span class="v {dec_label.get(p.get("decidable"), ("manual", "?"))[0]}">'
        f'{dec_label.get(p.get("decidable"), ("manual", "?"))[1]}</span></td></tr>'
        for p in points
    )

    # Describe the requests actually made, computed from the evidence rather than
    # written by hand. A hand-written "no links were followed" survived the commit
    # that started following links, and a report that misdescribes its own method
    # is worse than one that says less.
    # A one-off --url check produces a report with the same title and layout as
    # the committed federation run. Those must not be confusable: this report gets
    # circulated before a production decision, and a stray single-node file that
    # looks official is a real hazard. Ad hoc runs say so at the top.
    ad_hoc = [n for n in run["nodes"] if n.get("ad_hoc")]
    ad_hoc_banner = (
        '<div class="adhoc"><strong>Ad hoc check, not a federation run.</strong> '
        f'{"This page was" if len(ad_hoc) == 1 else "These pages were"} checked via '
        "<code>--url</code> and {} not part of the configured node list. No registered "
        "Node Landing Page was involved, so nothing here should be quoted as a node's "
        "assessment.</div>".format("is" if len(ad_hoc) == 1 else "are")
        if ad_hoc
        else ""
    )

    fetches = [n.get("fetch", {}) for n in run["nodes"]]
    depths = {f.get("crawl_depth", 0) for f in fetches}
    kids = sum(len(f.get("children", []) or []) for f in fetches)
    if kids == 0:
        crawl_sentence = (
            "One page request per node was made and no links were followed, so every "
            "verdict rests on the landing page alone."
        )
    else:
        # `kids` counts every followed page, at whatever depth. Reporting all of
        # them as "one level down" would overstate the shallow crawl, so the two
        # hops are counted separately.
        deep_pages = len(_depth_2_pages(run))
        first_hop = kids - deep_pages
        mixed = " (some nodes were collected at depth 0)" if 0 in depths else ""
        second = (
            f", then {deep_pages} page{'s' if deep_pages != 1 else ''} one hop "
            "further out"
            if deep_pages
            else ""
        )
        crawl_sentence = (
            f"{len(run['nodes'])} landing pages were requested, plus {first_hop} "
            f"checklist-relevant link{'s' if first_hop != 1 else ''} one level down "
            f"({first_hop / max(len(run['nodes']), 1):.1f} per node on average)"
            f"{second}{mixed}. "
            "Links were followed only where the target could settle a point, so a "
            "policy link is verified rather than taken on the strength of its label."
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
                "quantifies over more than this tool collects. Evidence is attached.",
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

{ad_hoc_banner}
<div class="banner"><strong>This is not a compliance statement.</strong> Of the
{len(order)} checklist points, {len(auto)} can be settled by inspection
({", ".join(auto)}), {len(partial)} only partly ({", ".join(partial)}), and
{len(human)} require a human reading the page ({", ".join(human)}). Every
<span class="v manual">REVIEW</span> below is a point this tool deliberately
refuses to guess at. {crawl_sentence}</div>

<div class="banner"><strong>Node names.</strong> {html.escape(_names_sentence(run))}</div>
{freshness_block}
<div class="counts">{chips}</div>

{matrix_heading}{dual_block}
<table class="matrix"><thead><tr><th>Node</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>
{dual_after}
<div class="legend">{legend_rows}</div>

<div class="cols"><table>
<thead><tr><th>Column</th><th>The question this column answers</th><th>Can a tool decide it?</th></tr></thead>
<tbody>{cols_rows}</tbody></table>
<p class="legend">Full requirement text for every point, as written in the checklist:
<a href="{checklist_href}">checklist v{html.escape(version)} explained</a>.</p></div>

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


CHECKLIST_CSS = """
:root{--bg:#fff;--fg:#1a1d21;--muted:#5b6470;--line:#e3e7ec;--accent:#0b5fa5;
--yes:#0f7b3f;--yes-bg:#e7f5ec;--part:#8a5a00;--part-bg:#fdf3e0;--no:#5b21b6;--no-bg:#f3ecfd;}
*{box-sizing:border-box}
body{margin:0;padding:2.5rem 2rem 4rem;background:var(--bg);color:var(--fg);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:860px;margin:0 auto}
h1{font-size:1.7rem;margin:0 0 .3rem;letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 1.6rem;font-size:.92rem}
h2{font-size:1.12rem;margin:2.2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}
a{color:var(--accent)}
.note{border:1px solid #cfe0f0;background:#f2f8fd;border-left:4px solid var(--accent);
padding:.85rem 1rem;border-radius:0 5px 5px 0;margin:0 0 1.8rem;font-size:.93rem}
.toc{margin:0 0 2rem;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:.4rem}
.toc a{display:inline-block;border:1px solid var(--line);border-radius:20px;
padding:.2rem .7rem;text-decoration:none;font-size:.86rem;font-weight:600}
.point{border:1px solid var(--line);border-radius:7px;margin:0 0 1.1rem;overflow:hidden}
.point>.hd{background:#fafbfc;padding:.7rem .95rem;border-bottom:1px solid var(--line);
display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap}
.point>.hd .pid{font:600 .82rem ui-monospace,SFMono-Regular,Menlo,monospace;
background:#eef1f5;border-radius:4px;padding:.12rem .45rem}
.point>.hd .ti{font-weight:650}
.point>.bd{padding:.85rem .95rem}
.q{font-size:.95rem;margin:0 0 .8rem}
.req{margin:0 0 .8rem;padding:.6rem .8rem;background:#fbfcfd;border-left:3px solid #c9d3de;
border-radius:0 4px 4px 0;font-size:.92rem}
.req b{display:block;font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;
color:var(--muted);margin-bottom:.25rem}
.dec{display:inline-block;font-size:.75rem;font-weight:700;letter-spacing:.03em;
border-radius:4px;padding:.16rem .5rem;text-transform:uppercase}
.dec.yes{color:var(--yes);background:var(--yes-bg)}
.dec.part{color:var(--part);background:var(--part-bg)}
.dec.no{color:var(--no);background:var(--no-bg)}
.why{margin:.7rem 0 0;font-size:.9rem;color:#3c4551}
.why b{color:var(--fg)}
.foot{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);
color:var(--muted);font-size:.86rem}
"""


def _provenance(checklist: dict) -> str:
    """State which bytes this transcription was made from, and from what.

    A reader who wants to check the transcription against the source needs to
    know the source is in the repository and which copy it is. Saying only the
    document's name invites the assumption that the name was verified.
    """
    name = checklist.get("source_file")
    digest = checklist.get("source_sha256", "")
    if not name:
        return ""
    return (
        f' · transcribed from <code>checklist/{html.escape(str(name))}</code>'
        f' (sha256 <code>{html.escape(str(digest)[:12])}…</code>), a PDF rendering'
        " of the source document, committed so the transcription can be audited"
    )


def render_checklist_html(checklist: dict, out: Path) -> Path:
    """A standalone, readable page explaining checklist v3.0 and each column.

    Generated from the same YAML the checks read, so the explanation cannot drift
    away from the rules actually applied. A hand-written description of a
    checklist sitting next to code that implements it differently is worse than
    none, because it is trusted.
    """
    version = checklist.get("checklist_version", "?")
    points = checklist["points"]
    dec_meta = {
        True: ("yes", "Decidable by inspection"),
        "partial": ("part", "Partly decidable"),
        False: ("no", "Needs human judgement"),
    }

    toc = "".join(
        f'<li><a href="#p{html.escape(p["id"])}">{html.escape(p["id"])}</a></li>' for p in points
    )

    blocks = []
    for p in points:
        cls, label = dec_meta.get(p.get("decidable"), ("part", "Unknown"))
        gloss = COLUMN_GLOSS.get(p["id"], "")
        why = " ".join(p.get("decidable_note", "").split())
        blocks.append(
            f'<div class="point" id="p{html.escape(p["id"])}">'
            f'<div class="hd"><span class="pid">{html.escape(p["id"])}</span>'
            f'<span class="ti">{html.escape(p["title"])}</span>'
            f'<span class="dec {cls}">{label}</span></div>'
            f'<div class="bd">'
            + (f'<p class="q"><b>In the results matrix, this column asks:</b> {html.escape(gloss)}</p>' if gloss else "")
            + f'<div class="req"><b>Requirement, as written in the checklist</b>'
            f'{html.escape(" ".join(p["requirement"].split()))}</div>'
            + (f'<p class="why"><b>How this tool treats it, and why:</b> {html.escape(why)}</p>' if why else "")
            + "</div></div>"
        )

    return _write(
        out,
        f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Node Landing Page Verification Checklist v{html.escape(version)} — explained</title>
<style>{CHECKLIST_CSS}</style></head><body><div class="wrap">
<h1>Node Landing Page Verification Checklist v{html.escape(version)}</h1>
<p class="sub">Dated {html.escape(str(checklist.get("checklist_date", "")))} ·
source document <code>{html.escape(str(checklist.get("source_document", "")))}</code> ·
{len(points)} points · this page is generated from
<code>checklist/v{html.escape(version)}.yaml</code>{_provenance(checklist)}</p>

<div class="note">This page explains what each column of the results matrix means, quotes the
requirement it comes from, and states plainly whether a script can settle it. Three of the
{len(points)} points cannot be settled by a tool at all, and four only partly. Those are reported
as <b>review</b> with the evidence attached rather than guessed at, because a confident wrong
verdict about a named node costs more to retract than an honest &ldquo;a human must look&rdquo;.</div>

<p><b>Jump to a point:</b></p>
<ul class="toc">{toc}</ul>

<h2>The points</h2>
{"".join(blocks)}

<div class="foot">The abbreviation <b>NLP</b> in the source checklist means <i>Node Landing
Page</i>: the URL registered for the node in the EOSC EU Node Contributors Dashboard
(section 1.2, field 6, &ldquo;Website address&rdquo;). Point <b>1R</b> is not a separate numbered
point in the source document &mdash; it is the second sentence of point 1, which extends the same
access requirement from the landing page to every resource the page points to. It is scored as its
own column because it is a different question with a different answer.<br><br>
Back to the <a href="index.html">results matrix</a>.</div>
</div></body></html>""",
    )


def _write(out: Path, doc: str) -> Path:
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


def _ellipsis(s: str, n: int) -> str:
    """Truncate visibly, so a shortened URL is not mistaken for the real one."""
    return s if len(s) <= n else s[: n - 1] + "…"


def _md_text(value: object) -> str:
    """Flatten a string to one line for inline Markdown.

    Node names, verdict messages, evidence lines and reviewer actions all come
    from fetched pages or from the checklist transcription, so any of them may
    contain a newline. In a list item or a heading a newline ends the element
    early and the remainder is rendered as body text, which corrupts the report
    without raising. Collapsing runs of whitespace is deliberate: it leaves
    ordinary single-spaced text untouched.
    """
    return " ".join(str(value).split())


def _md_cell(value: object) -> str:
    """Prepare a value for a Markdown table cell.

    A literal `|` opens a new column, so every cell after it in that row shifts
    left and the table silently misaligns. Escaping keeps the character visible
    in the rendered output rather than dropping it, because a pipe in a node
    name is information. Newlines are flattened for the same reason as in
    `_md_text`: they would end the row.
    """
    return _md_text(value).replace("|", "\\|")


def _dual_depth(run: dict) -> bool:
    """True when the run carries both a depth-1 and a depth-2 assessment."""
    return any("results_depth_1" in n for n in run["nodes"])


def _matrix_rows(run: dict, order: list[str], key: str) -> list[str]:
    rows = []
    for node in run["nodes"]:
        by_id = {r["point_id"]: r for r in node.get(key, node["results"])}
        cells = [VERDICT_MD.get(by_id[p]["verdict"], "?") if p in by_id else "—" for p in order]
        rows.append(f"| {_md_cell(node['name'])} | " + " | ".join(cells) + " |")
    return rows


def _tally(run: dict, key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in run["nodes"]:
        for r in node.get(key, node["results"]):
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    return counts


def _tally_line(counts: dict[str, int]) -> str:
    total = sum(counts.values())
    return (
        f"{total} cells: 🟢 {counts.get('PASS', 0)} PASS · "
        f"🔴 {counts.get('FAIL', 0)} FAIL · 🟠 {counts.get('MANUAL_REVIEW', 0)} review"
        + (f" · 🟣 {counts['ERROR']} error" if counts.get("ERROR") else "")
    )


def _depth_changes(run: dict) -> list[tuple[str, str, str, str]]:
    """Cells whose verdict differs between the depth-1 and depth-2 assessments."""
    out = []
    for node in run["nodes"]:
        shallow = {r["point_id"]: r["verdict"] for r in node.get("results_depth_1", [])}
        for r in node["results"]:
            was = shallow.get(r["point_id"])
            if was is not None and was != r["verdict"]:
                out.append((node["name"], r["point_id"], was, r["verdict"]))
    return out


def _depth_2_pages(run: dict) -> list[tuple[str, dict]]:
    out = []
    for node in run["nodes"]:
        for c in node.get("fetch", {}).get("children", []):
            if c.get("depth") == 2:
                out.append((node["name"], c))
    return out


def render_markdown(run: dict, out: Path) -> Path:
    points = run["checklist"]["points"]
    order = [p["id"] for p in points]
    short = VERDICT_MD
    depths = {n.get("fetch", {}).get("crawl_depth", 0) for n in run["nodes"]}
    followed = sum(len(n.get("fetch", {}).get("children", [])) for n in run["nodes"])
    dual = _dual_depth(run)
    deepest = max(depths, default=0)
    second_hop = len(_depth_2_pages(run))
    if deepest >= 2:
        scope = (
            f"one page request per node plus {followed - second_hop} followed link(s), "
            f"then {second_hop} second-hop page(s) (depth 2)"
        )
    elif deepest >= 1:
        scope = f"one page request per node plus {followed} followed link(s) in total (depth 1)"
    else:
        scope = "one page request per node, no crawling"

    ad_hoc = [n for n in run["nodes"] if n.get("ad_hoc")]
    title = "EOSC Node Landing Page compliance"
    if ad_hoc and len(ad_hoc) == len(run["nodes"]):
        title = "Ad hoc page check (not a federation run)"
    alternative = run.get("alternative_url") or []
    if alternative and len(alternative) == len(run["nodes"]):
        title = "Alternative URL check (not a federation run)"

    lines = [
        f"# {title} — checklist v{run['checklist']['checklist_version']}",
        "",
    ]
    if alternative:
        lines += [f"> **Alternative URL, not a federation run.** {_alternative_url_note(run)}", ""]
    if ad_hoc:
        lines += [
            "> **Ad hoc check, not a federation run.** "
            f"{len(ad_hoc)} page(s) here were checked via `--url` and are not part of the "
            "configured node list. Nothing here should be quoted as a node's assessment.",
            "",
        ]
    lines += [
        f"Run `{run['run_id']}` · {run['generated_at']} · {len(run['nodes'])} nodes · {scope}.",
        "",
        "> **This is not a compliance statement.** Points marked 🟠 review are ones this tool "
        "refuses to guess at: they either turn on a judgement (\"clearly state\") or quantify "
        "over things this tool does not enumerate (\"all research resources\").",
        "",
        f"**Node names.** {_names_sentence(run)}",
        "",
        *([f"> {_freshness_note(run)}", ""] if _freshness_note(run) else []),
        *([f"> **Skipped by request.** {_skipped_note(run)}", ""] if _skipped_note(run) else []),
        *(
            [f"> **Evidence from a different URL.** {_url_mismatch_note(run)}", ""]
            if _url_mismatch_note(run)
            else []
        ),
        "🟢 PASS — satisfied, with evidence · 🔴 **FAIL** — violated, with evidence · "
        "🟠 review — a human must decide · 🟣 ERROR — could not be assessed",
        "",
    ]

    header = ["| Node | " + " | ".join(order) + " |", "|---|" + "---|" * len(order)]

    if not dual:
        lines += header + _matrix_rows(run, order, "results")
    else:
        changes = _depth_changes(run)
        d1, d2 = _tally(run, "results_depth_1"), _tally(run, "results")
        lines += [
            "This run was collected at `--depth=2`, so it is reported twice: once using "
            "only the landing page and its direct links, and once using the second hop as "
            "well. Both tables come from the **same capture** — the shallow view is the "
            "deep evidence with the second-hop pages set aside, not a separate run — so "
            "any difference between them is the hop itself and not the passage of time.",
            "",
            "### Results at depth 1",
            "",
            "Landing page plus links that can settle a checklist point (policies, contact, "
            "about). This is the default the tool ships with.",
            "",
            f"{_tally_line(d1)}.",
            "",
        ]
        lines += header + _matrix_rows(run, order, "results_depth_1")
        lines += [
            "",
            "### Results at depth 2",
            "",
            f"The same evidence plus {second_hop} page(s) reached one further hop out, "
            "under a shared run budget.",
            "",
            f"{_tally_line(d2)}.",
            "",
        ]
        lines += header + _matrix_rows(run, order, "results")
        lines += ["", "### What the second hop changed", ""]
        if not changes:
            lines += [
                f"**No verdict changed.** The second hop fetched {second_hop} page(s) and "
                "left all " + str(sum(d2.values())) + " cells exactly as depth 1 had them.",
                "",
                "That is a finding, not a failure of the deeper crawl. The points still "
                "marked 🟠 review are not shallow-crawl artefacts: they turn on a judgement "
                "(\"clearly state\") or quantify over things no crawl enumerates (\"all "
                "research resources offered by the Node\"). Fetching more pages cannot "
                "settle either kind, which is why depth 1 remains the default.",
                "",
            ]
        else:
            lines += [
                f"{len(changes)} cell(s) differ. The depth-2 verdict is the one carried in "
                "the detail section below.",
                "",
                "| Node | Point | At depth 1 | At depth 2 |",
                "|---|---|---|---|",
            ]
            for name, pid, was, now in changes:
                lines.append(
                    f"| {_md_cell(name)} | {_md_cell(pid)} | "
                    f"{short.get(was, was)} | {short.get(now, now)} |"
                )
            lines.append("")
        pages = _depth_2_pages(run)
        if pages:
            lines += [
                "#### Pages the second hop fetched",
                "",
                "| Node | Point it was followed for | Page | Served |",
                "|---|---|---|---|",
            ]
            for name, c in pages:
                status = c.get("http_status") or ("error" if c.get("error") else "—")
                purpose = ", ".join(c.get("selected_for", [])) or "—"
                # A pipe in a URL is percent-encoded rather than backslash-escaped:
                # inside an autolink a backslash is not an escape and would be
                # taken as part of the address.
                url = str(c.get("url", "")).replace("|", "%7C")
                lines.append(
                    f"| {_md_cell(name)} | {_md_cell(purpose)} | <{url}> | {status} |"
                )
            lines.append("")

    lines += [
        "",
        "## What each column means",
        "",
        "Full requirement text and the reasoning behind each verdict: "
        "[checklist v" + run["checklist"]["checklist_version"] + " explained]"
        "(checklist-v" + run["checklist"]["checklist_version"] + ".html).",
        "",
        "| Column | Question it answers | Can a tool decide it? |",
        "|---|---|---|",
    ]
    dec_label = {True: "yes, by inspection", "partial": "partly", False: "no, human judgement"}
    for p in points:
        gloss = COLUMN_GLOSS.get(p["id"], p["title"])
        lines.append(
            f"| **{_md_cell(p['id'])}** | {_md_cell(gloss)} | "
            f"{dec_label.get(p.get('decidable'), '?')} |"
        )

    lines += ["", "## Points in full", ""]
    for p in points:
        dec = (
            "decidable by inspection"
            if p.get("decidable") is True
            else ("partly decidable" if p.get("decidable") == "partial" else "needs a human")
        )
        lines.append(f"**{_md_text(p['id'])} — {_md_text(p['title'])}** ({dec})  ")
        lines.append(_md_text(p["requirement"]))
        lines.append("")
        if p.get("decidable_note"):
            lines.append(f"> {_md_text(p['decidable_note'])}")
            lines.append("")

    lines += ["## Detail", ""]
    for node in run["nodes"]:
        lines.append(f"### {_md_text(node['name'])}")
        lines.append(f"<{_md_text(node['url'])}>")
        lines.append("")
        for res in node["results"]:
            lines.append(
                f"- **{_md_text(res['point_id'])}** "
                f"{short.get(res['verdict'], res['verdict'])} — {_md_text(res['message'])}"
            )
            for item in res.get("evidence", [])[:4]:
                lines.append(f"  - {_md_text(item)}")
            if res.get("reviewer_action"):
                lines.append(f"  - *Reviewer action:* {_md_text(res['reviewer_action'])}")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_all(run: dict, results_dir: Path) -> dict[str, Path]:
    """Write every report format. Personal data is masked first (see privacy.py),
    so nothing below can publish it, whatever the evidence it was built from."""
    results_dir.mkdir(parents=True, exist_ok=True)
    run.setdefault("generated_at", datetime.now(UTC).isoformat(timespec="seconds"))
    run = mask_data(run)
    paths = {
        "json": results_dir / "results.json",
        "html": results_dir / "index.html",
        "csv": results_dir / "results.csv",
        "md": results_dir / "results.md",
    }
    version = run["checklist"].get("checklist_version", "3.0")
    paths["checklist"] = results_dir / f"checklist-v{version}.html"
    paths["json"].write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")
    render_html(run, paths["html"])
    render_checklist_html(run["checklist"], paths["checklist"])
    render_csv(run, paths["csv"])
    render_markdown(run, paths["md"])
    return paths
