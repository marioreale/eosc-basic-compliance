"""Tests for the rendered report.

report.py was the least-covered module in the project and the dual-depth tables
are the first thing a reader of a `--depth=2` run actually sees, so they are
tested here rather than eyeballed once and trusted.
"""

from __future__ import annotations

import re

from basic_check import report


def _point(pid: str) -> dict:
    return {
        "id": pid,
        "title": f"Point {pid}",
        "requirement": "The node must do the thing.",
        "decidable": True,
    }


def _result(pid: str, verdict: str) -> dict:
    return {
        "point_id": pid,
        "title": f"Point {pid}",
        "verdict": verdict,
        "message": "because of the evidence",
        "evidence": [],
    }


def run_dict(nodes: list[dict]) -> dict:
    return {
        "run_id": "test-run",
        "generated_at": "2026-09-21T12:00:00+00:00",
        "checklist": {"checklist_version": "3.0", "checklist_date": "2026-09-10", "points": [_point("4"), _point("6")]},
        "nodes": nodes,
    }


def _node(name: str, deep: list[tuple[str, str]], shallow=None, children=None) -> dict:
    n = {
        "id": name.lower(),
        "name": name,
        "url": f"https://{name.lower()}.example/",
        "results": [_result(p, v) for p, v in deep],
        "fetch": {"crawl_depth": 2 if shallow else 1, "children": children or []},
    }
    if shallow is not None:
        n["results_depth_1"] = [_result(p, v) for p, v in shallow]
    return n


def render(run, tmp_path) -> str:
    return report.render_markdown(run, tmp_path / "r.md").read_text(encoding="utf-8")


# --- a depth-1 run is unchanged ----------------------------------------------


def test_a_depth_1_run_renders_a_single_table(tmp_path):
    run = run_dict([_node("Alpha", [("4", "PASS"), ("6", "FAIL")])])
    md = render(run, tmp_path)
    assert "Results at depth 1" not in md
    assert "Results at depth 2" not in md
    assert md.count("| Node | 4 | 6 |") == 1


# --- a depth-2 run reports both ----------------------------------------------


def test_a_depth_2_run_renders_both_tables_and_both_sections(tmp_path):
    run = run_dict(
        [_node("Alpha", [("4", "FAIL"), ("6", "PASS")], shallow=[("4", "FAIL"), ("6", "PASS")])]
    )
    md = render(run, tmp_path)
    assert "### Results at depth 1" in md
    assert "### Results at depth 2" in md
    assert "### What the second hop changed" in md
    assert md.count("| Node | 4 | 6 |") == 2, "one matrix header per depth"


def test_the_two_tables_show_their_own_verdicts(tmp_path):
    """The shallow table must not silently render the deep results."""
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "FAIL"), ("6", "PASS")],
                shallow=[("4", "MANUAL_REVIEW"), ("6", "PASS")],
            )
        ]
    )
    md = render(run, tmp_path)
    d1 = md.split("### Results at depth 1")[1].split("### Results at depth 2")[0]
    d2 = md.split("### Results at depth 2")[1].split("### What the second hop changed")[0]
    row1 = next(ln for ln in d1.splitlines() if ln.startswith("| Alpha"))
    row2 = next(ln for ln in d2.splitlines() if ln.startswith("| Alpha"))
    assert "review" in row1 and "FAIL" not in row1
    assert "FAIL" in row2 and "review" not in row2


def test_a_changed_verdict_is_listed_with_both_values(tmp_path):
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "MANUAL_REVIEW"), ("6", "PASS")],
            )
        ]
    )
    md = render(run, tmp_path)
    changed = md.split("### What the second hop changed")[1]
    assert "1 cell(s) differ" in changed
    assert "| Alpha | 4 |" in changed
    assert "| Alpha | 6 |" not in changed, "an unchanged cell must not be listed"


def test_no_change_is_reported_as_a_finding_not_silence(tmp_path):
    run = run_dict(
        [_node("Alpha", [("4", "FAIL"), ("6", "PASS")], shallow=[("4", "FAIL"), ("6", "PASS")])]
    )
    md = render(run, tmp_path)
    changed = md.split("### What the second hop changed")[1]
    assert "No verdict changed" in changed
    assert "not a failure of the deeper crawl" in changed


def test_the_tallies_are_computed_per_depth(tmp_path):
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "FAIL"), ("6", "FAIL")],
                shallow=[("4", "MANUAL_REVIEW"), ("6", "MANUAL_REVIEW")],
            )
        ]
    )
    md = render(run, tmp_path)
    d1 = md.split("### Results at depth 1")[1].split("### Results at depth 2")[0]
    d2 = md.split("### Results at depth 2")[1].split("### What the second hop changed")[0]
    assert "🔴 0 FAIL" in d1 and "🟠 2 review" in d1
    assert "🔴 2 FAIL" in d2 and "🟠 0 review" in d2


def test_second_hop_pages_are_listed_with_their_purpose(tmp_path):
    child = {
        "url": "https://alpha.example/legal/aup",
        "depth": 2,
        "selected_for": ["5b"],
        "http_status": 200,
    }
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=[{"url": "https://alpha.example/legal", "depth": 1}, child],
            )
        ]
    )
    md = render(run, tmp_path)
    assert "Pages the second hop fetched" in md
    assert "https://alpha.example/legal/aup" in md
    assert "| Alpha | 5b |" in md
    assert "https://alpha.example/legal>" not in md, "a depth-1 child is not a second hop"


def test_a_pipe_in_a_url_cannot_break_the_table(tmp_path):
    """A stray pipe would add a column and silently misalign every later cell."""
    child = {
        "url": "https://alpha.example/a|b",
        "depth": 2,
        "selected_for": ["6"],
        "http_status": 200,
    }
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=[child],
            )
        ]
    )
    md = render(run, tmp_path)
    row = next(ln for ln in md.splitlines() if "alpha.example/a" in ln)
    assert row.count("|") == 5, f"expected 4 columns, got a misaligned row: {row}"


def test_a_failed_second_hop_is_shown_rather_than_dropped(tmp_path):
    child = {
        "url": "https://alpha.example/timeout",
        "depth": 2,
        "selected_for": ["6"],
        "http_status": None,
        "error": "TimeoutError",
    }
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=[child],
            )
        ]
    )
    md = render(run, tmp_path)
    assert "alpha.example/timeout" in md
    assert "error" in md.split("Pages the second hop fetched")[1]


def test_the_scope_line_separates_the_two_hops(tmp_path):
    children = [
        {"url": "https://alpha.example/a", "depth": 1},
        {"url": "https://alpha.example/b", "depth": 2, "selected_for": ["6"], "http_status": 200},
    ]
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=children,
            )
        ]
    )
    md = render(run, tmp_path)
    assert "1 followed link(s)" in md
    assert "1 second-hop page(s) (depth 2)" in md


# --- the HTML page ------------------------------------------------------------


def _html(run, tmp_path) -> str:
    return report.render_html(run, tmp_path / "i.html").read_text(encoding="utf-8")


def test_a_depth_1_html_page_keeps_its_single_matrix_heading(tmp_path):
    run = run_dict([_node("Alpha", [("4", "PASS"), ("6", "FAIL")])])
    out = _html(run, tmp_path)
    assert "<h2>Matrix</h2>" in out
    assert "Results at depth 1" not in out
    assert out.count('<table class="matrix"') == 1


def test_a_depth_2_html_page_has_two_matrices_and_no_stray_heading(tmp_path):
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "FAIL")],
                shallow=[("4", "MANUAL_REVIEW"), ("6", "FAIL")],
                children=[
                    {
                        "url": "https://alpha.example/x",
                        "depth": 2,
                        "selected_for": ["4"],
                        "http_status": 200,
                    }
                ],
            )
        ]
    )
    out = _html(run, tmp_path)
    assert "<h2>Matrix</h2>" not in out, "the generic heading is replaced by the two depth ones"
    assert out.count('<table class="matrix"') == 2
    assert "Results at depth 1" in out and "Results at depth 2" in out
    assert "What the second hop changed" in out
    assert "Pages the second hop fetched" in out


def test_the_html_header_does_not_count_second_hop_pages_as_first_hop(tmp_path):
    """Lumping both hops together overstates how shallow the crawl was."""
    children = [
        {"url": "https://alpha.example/a", "depth": 1},
        {"url": "https://alpha.example/b", "depth": 2, "selected_for": ["6"], "http_status": 200},
        {"url": "https://alpha.example/c", "depth": 2, "selected_for": ["6"], "http_status": 200},
    ]
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=children,
            )
        ]
    )
    out = _html(run, tmp_path)
    assert "plus 1 checklist-relevant link one level down" in out
    assert "then 2 pages one hop further out" in out
    assert "depth 0" not in out, "no node here was collected at depth 0"


# --- the approved-name list is reported, including its absence ---------------


def _with_names(info) -> dict:
    run = run_dict([_node("A", [("4", "PASS"), ("6", "PASS")])])
    if info is not None:
        run["approved_names"] = info
    return run


def test_an_absent_name_list_is_stated_not_left_to_be_inferred(tmp_path):
    """A REVIEW on point 3 must not be read as "the name was checked and is fine"."""
    run = _with_names({"supplied": False, "scoped": False, "count": 0, "source": ""})
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "No approved-name list was used" in out
        assert "not assessed at all" in out


def test_a_scoped_list_is_described_as_tied_to_nodes(tmp_path):
    run = _with_names({"supplied": True, "scoped": True, "count": 9, "source": "n.txt"})
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "9 approved node name(s) were used, from a list supplied for this run, tied to specific nodes" in out


def test_an_unscoped_list_is_reported_with_its_weaker_claim(tmp_path):
    run = _with_names({"supplied": True, "scoped": False, "count": 3, "source": "n.txt"})
    assert "not that it is that node's own name" in render(run, tmp_path)
    # The HTML renderer escapes the apostrophe, so match the part either shares.
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "unscoped list" in out
        assert "own name" in out


def test_an_older_result_file_without_the_detail_still_renders(tmp_path):
    """Result files written before this field existed must not crash the renderer."""
    run = _with_names(None)
    run["approved_names_supplied"] = True
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "approved node name(s) were used" in out


def test_a_result_file_with_no_name_information_at_all_still_renders(tmp_path):
    run = _with_names(None)
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "No approved-name list was used" in out


def test_the_sentence_says_when_the_committed_default_was_used(tmp_path):
    """Which list was in force is part of the finding, not run metadata."""
    run = _with_names({"supplied": True, "scoped": False, "count": 9, "default_used": True})
    for out in (render(run, tmp_path), _html(run, tmp_path)):
        assert "official list committed with the checklist" in out


def test_the_sentence_distinguishes_an_operator_supplied_list(tmp_path):
    run = _with_names(
        {"supplied": True, "scoped": True, "count": 2, "default_used": False, "source": "m.txt"}
    )
    out = render(run, tmp_path)
    assert "a list supplied for this run" in out
    assert "official list committed" not in out


# --- a mixed-freshness report must say so -------------------------------------


def _mixed_run():
    """A run where only one node was re-fetched, as --only now produces."""
    egi = _node("EGI", [("4", "PASS"), ("6", "PASS")])
    egi["id"] = "egi"
    egi["fetch"] = {**egi.get("fetch", {}), "fetched_at": "2026-09-21T10:00:00+00:00"}
    eudat = _node("EUDAT", [("4", "PASS"), ("6", "PASS")])
    eudat["id"] = "eudat"
    eudat["fetch"] = {**eudat.get("fetch", {}), "fetched_at": "2026-08-01T10:00:00+00:00"}
    run = run_dict([egi, eudat])
    run["selection"] = ["egi"]
    return run


def test_a_partially_refetched_report_names_what_was_refetched(tmp_path):
    """--only now narrows the fetch without narrowing the report, which is what
    stops it destroying the nine-node table. The cost is that rows no longer
    share a capture date, and the header states a single run timestamp. Left
    unsaid, the report would imply every row is as fresh as the newest.
    """
    md = (tmp_path / "r.md")
    report.render_markdown(_mixed_run(), md)
    text = md.read_text()
    assert "egi" in text
    assert "not re-fetched" in text or "reused" in text, text[:1500]


def test_a_full_run_makes_no_such_claim(tmp_path):
    md = (tmp_path / "r.md")
    report.render_markdown(run_dict([_node("EGI", [("4", "PASS")])]), md)
    assert "reused" not in md.read_text()


def test_the_html_report_also_states_it(tmp_path):
    out = (tmp_path / "i.html")
    report.render_html(_mixed_run(), out)
    text = out.read_text()
    assert "reused" in text or "not re-fetched" in text


# --- the report must state the provenance of the name list --------------------


def test_the_report_states_the_hash_of_the_name_list(tmp_path):
    run = run_dict([_node("EGI", [("4", "PASS")])])
    run["approved_names"] = {
        "supplied": True, "scoped": False, "count": 9,
        "source": "checklist/approved-names.txt", "default_used": True,
        "sha256": "abcdef1234567890" + "0" * 48, "strict_separators": False,
    }
    md = (tmp_path / "r.md")
    report.render_markdown(run, md)
    assert "abcdef123456" in md.read_text()


def test_the_report_states_when_separators_were_matched_strictly(tmp_path):
    run = run_dict([_node("EGI", [("4", "PASS")])])
    run["approved_names"] = {
        "supplied": True, "scoped": False, "count": 9,
        "source": "checklist/approved-names.txt", "default_used": True,
        "sha256": "a" * 64, "strict_separators": True,
    }
    md = (tmp_path / "r.md")
    report.render_markdown(run, md)
    text = md.read_text()
    assert "interchangeable" not in text, "the lax rule must not be claimed when strict was used"
    assert "literal" in text or "strictly" in text, text[:1200]


# --- table-breaking and list-breaking input -----------------------------------
#
# Every string below reaches the Markdown renderer from a fetched page, a
# checklist file or a name list, so none of it is under this module's control.
# A pipe adds a column and silently misaligns every cell after it; a newline
# ends the row or the list item early. Both corrupt the report without raising,
# which is the reason these are tested rather than assumed.


def _columns(row: str) -> int:
    """Cells in a Markdown table row, counting only unescaped delimiters.

    A `\\|` inside a cell is literal text, not a column break, so counting raw
    pipes would call a correctly escaped row misaligned.
    """
    return len(re.findall(r"(?<!\\)\|", row)) - 1


def _pipe_node(name: str = "Alpha | Beta") -> dict:
    return _node(name, [("4", "PASS"), ("6", "FAIL")])


def test_a_pipe_in_a_node_name_cannot_break_the_matrix(tmp_path):
    md = render(run_dict([_pipe_node()]), tmp_path)
    row = next(ln for ln in md.splitlines() if "Alpha" in ln and ln.startswith("|"))
    assert _columns(row) == 3, f"expected 3 columns, got a misaligned row: {row}"


def test_a_pipe_in_a_node_name_survives_as_text(tmp_path):
    """Escaping must not silently delete the character from the name."""
    md = render(run_dict([_pipe_node()]), tmp_path)
    assert "Alpha \\| Beta" in md


def test_a_pipe_in_a_node_name_cannot_break_the_depth_change_table(tmp_path):
    run = run_dict(
        [
            _node(
                "Alpha | Beta",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "FAIL"), ("6", "PASS")],
            )
        ]
    )
    md = render(run, tmp_path)
    row = next(ln for ln in md.splitlines() if "Alpha" in ln and " 4 " in ln)
    assert _columns(row) == 4, f"expected 4 columns, got a misaligned row: {row}"


def test_a_pipe_in_a_followed_reason_cannot_break_the_second_hop_table(tmp_path):
    """`selected_for` is joined into a cell; a pipe in a point id would split it."""
    child = {
        "url": "https://alpha.example/x",
        "depth": 2,
        "selected_for": ["6|7"],
        "http_status": 200,
    }
    run = run_dict(
        [
            _node(
                "Alpha",
                [("4", "PASS"), ("6", "PASS")],
                shallow=[("4", "PASS"), ("6", "PASS")],
                children=[child],
            )
        ]
    )
    md = render(run, tmp_path)
    row = next(ln for ln in md.splitlines() if "alpha.example/x" in ln)
    assert _columns(row) == 4, f"expected 4 columns, got a misaligned row: {row}"


def test_a_pipe_in_a_point_title_cannot_break_the_column_table(tmp_path):
    """The column table falls back to the point title for an id with no gloss.

    Every id in checklist v3.0 has one, so this is the path a future checklist
    version would take — which is exactly when nobody would be watching for it.
    """
    run = run_dict([_node("Alpha", [("8z", "PASS"), ("6", "PASS")])])
    run["checklist"]["points"][0] = _point("8z")
    run["checklist"]["points"][0]["title"] = "Links | to EOSC"
    md = render(run, tmp_path)
    row = next(ln for ln in md.splitlines() if "Links" in ln and ln.startswith("|"))
    assert _columns(row) == 3, f"expected 3 columns, got a misaligned row: {row}"
    assert "Links \\| to EOSC" in row


def test_a_newline_in_a_point_title_stays_on_one_line(tmp_path):
    run = run_dict([_node("Alpha", [("4", "PASS"), ("6", "PASS")])])
    run["checklist"]["points"][0]["title"] = "Links\nto EOSC"
    md = render(run, tmp_path)
    assert "**4 — Links to EOSC**" in md
    for ln in md.splitlines():
        assert ln != "to EOSC", "the title split across two lines"


def test_a_newline_in_an_evidence_string_stays_one_list_item(tmp_path):
    node = _node("Alpha", [("4", "FAIL"), ("6", "PASS")])
    node["results"][0]["evidence"] = ["first line\nsecond line"]
    md = render(run_dict([node]), tmp_path)
    assert "  - first line second line" in md
    assert "\nsecond line" not in md, "the newline escaped the list item"


def test_a_newline_in_a_reviewer_action_stays_one_list_item(tmp_path):
    node = _node("Alpha", [("4", "MANUAL_REVIEW"), ("6", "PASS")])
    node["results"][0]["reviewer_action"] = "Open the page.\nCheck the footer."
    md = render(run_dict([node]), tmp_path)
    assert "  - *Reviewer action:* Open the page. Check the footer." in md


def test_a_newline_in_a_node_name_cannot_break_the_detail_heading(tmp_path):
    md = render(run_dict([_node("Alpha\nBeta", [("4", "PASS"), ("6", "PASS")])]), tmp_path)
    assert "### Alpha Beta" in md
    for ln in md.splitlines():
        assert ln != "Beta", "the node name split across two lines"


def test_collapsing_whitespace_does_not_mangle_ordinary_evidence(tmp_path):
    """The fix must not reflow text that was already fine."""
    node = _node("Alpha", [("4", "FAIL"), ("6", "PASS")])
    node["results"][0]["evidence"] = ["6 link(s) examined, none pointing to eosc.eu"]
    md = render(run_dict([node]), tmp_path)
    assert "  - 6 link(s) examined, none pointing to eosc.eu" in md
