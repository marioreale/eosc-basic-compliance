"""The approved-names file: parsing, scoping, and boundary-aware matching.

Point 3's name half is only as trustworthy as this module. Every test here
started as a defect observed against the committed evidence.
"""

import pytest

from basic_check.names import ApprovedNames, parse_approved_names

# --- parsing -----------------------------------------------------------------


def test_plain_lines_are_unscoped_names():
    an = parse_approved_names("EOSC Node EUDAT\nEGI Node\n")
    assert an.supplied
    assert not an.scoped
    assert an.for_node("anything") == ["EOSC Node EUDAT", "EGI Node"]


def test_blank_lines_and_surrounding_whitespace_are_ignored():
    an = parse_approved_names("\n  EOSC Node EUDAT  \n\n\tEGI Node\t\n\n")
    assert an.for_node("x") == ["EOSC Node EUDAT", "EGI Node"]


def test_comment_lines_are_comments_not_node_names():
    """Previously a leading '#' line was read as a name to search for."""
    an = parse_approved_names("# Tripartite-approved, 21 Sep 2026\nEGI Node\n")
    assert an.for_node("x") == ["EGI Node"]


def test_trailing_comments_are_stripped():
    an = parse_approved_names("EGI Node  # as written on the page\n")
    assert an.for_node("x") == ["EGI Node"]


def test_a_name_containing_a_hash_can_be_escaped():
    an = parse_approved_names("Node \\# 4\n")
    assert an.for_node("x") == ["Node # 4"]


def test_an_empty_file_is_not_supplied():
    an = parse_approved_names("# only a comment\n\n")
    assert not an.supplied
    assert an.for_node("x") == []


# --- scoping -----------------------------------------------------------------


def test_id_prefixed_lines_scope_a_name_to_one_node():
    an = parse_approved_names("bbmri-eric: EOSC Node - BBMRI-ERIC\negi: EGI Node\n")
    assert an.scoped
    assert an.for_node("bbmri-eric") == ["EOSC Node - BBMRI-ERIC"]
    assert an.for_node("egi") == ["EGI Node"]


def test_a_scoped_name_is_not_offered_to_another_node():
    """The defect: any name matching any page satisfied that page."""
    an = parse_approved_names("bbmri-eric: EOSC Node - BBMRI-ERIC\n")
    assert an.for_node("egi") == []


def test_unscoped_names_apply_to_every_node_alongside_scoped_ones():
    an = parse_approved_names("bbmri-eric: EOSC Node - BBMRI-ERIC\nEOSC Node\n")
    assert an.for_node("bbmri-eric") == ["EOSC Node - BBMRI-ERIC", "EOSC Node"]
    assert an.for_node("egi") == ["EOSC Node"]


def test_several_names_may_be_scoped_to_one_node():
    an = parse_approved_names("egi: EGI Node\negi: EGI Federation\n")
    assert an.for_node("egi") == ["EGI Node", "EGI Federation"]


def test_a_url_is_not_mistaken_for_a_scoped_entry():
    """A colon inside a name must not be read as an id separator."""
    an = parse_approved_names("EOSC Node: Finland\n")
    assert not an.scoped
    assert an.for_node("x") == ["EOSC Node: Finland"]


def test_node_ids_are_matched_case_insensitively():
    an = parse_approved_names("BBMRI-ERIC: EOSC Node - BBMRI-ERIC\n")
    assert an.for_node("bbmri-eric") == ["EOSC Node - BBMRI-ERIC"]


# --- matching ----------------------------------------------------------------


def test_a_short_name_does_not_match_inside_a_longer_word():
    """The defect: 'EGI' matched 'strategic' and 'Norwegian'."""
    an = parse_approved_names("EGI\n")
    assert an.match("of Europe's strategic priorities", "egi") is None
    assert an.match("Nepali NKo Norwegian Nuer", "egi") is None


def test_the_same_short_name_still_matches_when_it_stands_alone():
    an = parse_approved_names("EGI\n")
    assert an.match("Operated by the EGI Foundation", "egi") == "EGI"


def test_matching_is_case_insensitive():
    an = parse_approved_names("EGI Node\n")
    assert an.match("welcome to the egi node", "egi") == "EGI Node"


def test_whitespace_in_the_name_matches_any_run_of_whitespace():
    """Page text may wrap or double-space where the official name does not."""
    an = parse_approved_names("EOSC Node EUDAT\n")
    assert an.match("the EOSC  Node\nEUDAT landing page", "eudat") == "EOSC Node EUDAT"


def test_a_standalone_separator_is_no_longer_required_to_be_present():
    """This reverses an earlier decision, deliberately.

    The rule used to be that every character of the name had to appear, so
    "EOSC Node - X" did not match a page writing "EOSC Node X". Run against the
    nine real pages with the official list, that rule matched none of them:
    the pages disagree about the glyph, not about the name. A separator between
    tokens is now optional; punctuation *inside* a token is still required, as
    the next test pins.
    """
    an = parse_approved_names("EOSC Node - BBMRI-ERIC\n")
    assert an.match("EOSC Node - BBMRI-ERIC", "b") == "EOSC Node - BBMRI-ERIC"
    assert an.match("EOSC Node BBMRI-ERIC", "b") == "EOSC Node - BBMRI-ERIC"


def test_a_name_ending_in_punctuation_matches_at_a_boundary():
    an = parse_approved_names("EOSC Node (Finland)\n")
    assert an.match("the EOSC Node (Finland) team", "fi") == "EOSC Node (Finland)"


def test_a_name_is_not_matched_inside_a_longer_hyphenated_token():
    """"BBMRI" is not shown on a page that shows "BBMRI-ERIC" — a different name."""
    an = parse_approved_names("BBMRI\n")
    assert an.match("BBMRI-ERIC operates", "b") is None
    assert an.match("BBMRI operates", "b") == "BBMRI"


def test_a_hyphen_inside_the_name_itself_is_matched_normally():
    an = parse_approved_names("EOSC Node - BBMRI-ERIC\n")
    assert an.match("the EOSC Node - BBMRI-ERIC page", "b") == "EOSC Node - BBMRI-ERIC"


def test_a_name_following_a_dash_in_the_page_text_still_matches():
    an = parse_approved_names("EGI Node\n")
    assert an.match("Home - EGI Node - EGI", "egi") == "EGI Node"


def test_the_first_name_in_file_order_wins_when_several_match():
    an = parse_approved_names("EGI Node\nEGI Federation\n")
    assert an.match("EGI Federation runs the EGI Node", "egi") == "EGI Node"


def test_regex_metacharacters_in_a_name_are_literal():
    an = parse_approved_names("Node (EU) [pilot]\n")
    assert an.match("the Node (EU) [pilot] page", "x") == "Node (EU) [pilot]"


def test_matching_against_a_node_with_no_names_returns_none():
    an = parse_approved_names("bbmri-eric: EOSC Node - BBMRI-ERIC\n")
    assert an.match("EOSC Node - BBMRI-ERIC appears here", "egi") is None


# --- file loading ------------------------------------------------------------


def test_load_reads_a_file(tmp_path):
    p = tmp_path / "approved-names.txt"
    p.write_text("# header\negi: EGI Node\n", encoding="utf-8")
    an = ApprovedNames.load(p)
    assert an.scoped
    assert an.for_node("egi") == ["EGI Node"]


def test_load_of_none_is_an_unsupplied_list():
    an = ApprovedNames.load(None)
    assert not an.supplied
    assert an.for_node("x") == []


def test_a_missing_file_is_an_error_not_a_silent_empty_list(tmp_path):
    """Silently proceeding would leave point 3 unassessed without saying so."""
    with pytest.raises(FileNotFoundError):
        ApprovedNames.load(tmp_path / "nope.txt")


def test_a_plain_list_is_accepted_for_backward_compatibility():
    an = ApprovedNames.coerce(["EGI Node"])
    assert an.supplied
    assert not an.scoped
    assert an.for_node("x") == ["EGI Node"]


def test_coerce_passes_an_existing_object_through():
    an = parse_approved_names("EGI Node\n")
    assert ApprovedNames.coerce(an) is an


def test_coerce_of_none_is_unsupplied():
    assert not ApprovedNames.coerce(None).supplied


def test_a_bad_path_is_a_clean_cli_error_not_a_traceback(tmp_path):
    from typer.testing import CliRunner

    from basic_check.cli import app

    res = CliRunner().invoke(app, ["assess", "--approved-names", str(tmp_path / "nope.txt")])
    assert res.exit_code != 0
    assert "approved-names file not found" in (res.output + str(res.exception))


# --- the separator between "EOSC Node" and the node part ---------------------
#
# The official list writes every name as "EOSC Node | X". Real pages do not:
# of the nine, BBMRI-ERIC writes a hyphen and an en dash, European DTO writes
# the pipe, and EUDAT writes no separator at all. Matching the pipe literally
# scored 0/9 against the committed evidence, which would have published a
# finding against every node for what is a typographic difference.


@pytest.mark.parametrize(
    "page_text",
    [
        "EOSC Node | BBMRI-ERIC",
        "EOSC Node - BBMRI-ERIC",
        "EOSC Node – BBMRI-ERIC",  # en dash, as BBMRI-ERIC's own page writes it
        "EOSC Node — BBMRI-ERIC",  # em dash
        "EOSC Node: BBMRI-ERIC",
        "EOSC Node BBMRI-ERIC",  # no separator, as EUDAT's page writes it
        "EOSC  Node   |   BBMRI-ERIC",  # wrapped across lines
    ],
)
def test_a_standalone_separator_matches_any_of_the_usual_separators(page_text):
    an = parse_approved_names("EOSC Node | BBMRI-ERIC\n")
    assert an.match(page_text, "bbmri-eric") == "EOSC Node | BBMRI-ERIC"


def test_a_hyphen_inside_a_word_stays_literal():
    """Only a separator standing alone is flexible.

    "BBMRI-ERIC" is one token, so its hyphen is part of the name. Relaxing it
    would undo the boundary rule that stops BBMRI matching BBMRI-ERIC.
    """
    an = parse_approved_names("EOSC Node | BBMRI-ERIC\n")
    assert an.match("EOSC Node | BBMRI ERIC", "bbmri-eric") is None


def test_the_separator_does_not_let_a_name_match_across_unrelated_words():
    an = parse_approved_names("EOSC Node | EGI\n")
    assert an.match("EOSC Node for the Earth system and EGI is elsewhere", "x") is None


def test_the_matched_text_is_reported_so_a_variant_can_be_seen():
    an = parse_approved_names("EOSC Node | BBMRI-ERIC\n")
    m = an.find("the page says EOSC Node – BBMRI-ERIC here", "bbmri-eric")
    assert m.name == "EOSC Node | BBMRI-ERIC"
    assert m.matched_text == "EOSC Node – BBMRI-ERIC"
    assert not m.exact


def test_an_identical_rendering_is_reported_as_exact():
    an = parse_approved_names("EOSC Node | European DTO\n")
    m = an.find("... EOSC Node | European DTO ...", "eosc-dto")
    assert m.exact


def test_case_and_whitespace_differences_alone_still_count_as_exact():
    an = parse_approved_names("EOSC Node | EUDAT\n")
    assert an.find("eosc  node | eudat", "eudat").exact


def test_find_returns_none_when_nothing_matches():
    an = parse_approved_names("EOSC Node | EGI\n")
    assert an.find("nothing here", "egi") is None


# --- the committed default list ---------------------------------------------


def _run_assess(tmp_path, *extra):
    """Assess the committed evidence into a scratch dir, and return results.json.

    The node list is narrowed to the nodes the committed evidence actually
    covers. `assess` exits 2 when a configured node has no evidence — correctly,
    since an unassessed node must not pass silently — so without this these
    name tests would break every time a node is added to nodes.yaml ahead of
    its first collection, which is exactly the order a node gets added in.
    """
    import json
    import shutil

    import yaml
    from typer.testing import CliRunner

    from basic_check.cli import ROOT, app

    out = tmp_path / "results"
    shutil.copytree(ROOT / "results" / "evidence", out / "evidence")
    nodes_file = _nodes_with_evidence(tmp_path, out / "evidence", ROOT, yaml)
    res = CliRunner().invoke(
        app,
        ["assess", "--results", str(out), "--nodes", str(nodes_file), *extra],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    return json.loads((out / "results.json").read_text())


def _nodes_with_evidence(tmp_path, evidence_dir, root, yaml):
    """A nodes.yaml holding only the nodes with an evidence file on disk."""
    have = {p.stem for p in evidence_dir.glob("*.json")}
    all_nodes = yaml.safe_load((root / "nodes.yaml").read_text(encoding="utf-8"))["nodes"]
    kept = [n for n in all_nodes if n["id"] in have]
    assert kept, f"no committed evidence matched nodes.yaml (found {sorted(have)})"
    path = tmp_path / "nodes-with-evidence.yaml"
    path.write_text(yaml.safe_dump({"nodes": kept}, allow_unicode=True), encoding="utf-8")
    return path


def test_the_official_list_is_committed_and_parses():
    from basic_check.cli import DEFAULT_APPROVED_NAMES

    assert DEFAULT_APPROVED_NAMES.exists(), "the official list must be in the repository"
    an = ApprovedNames.load(DEFAULT_APPROVED_NAMES)
    # Derived from the file rather than pinned to a number, so adding a node to
    # the Tripartite list does not fail this test. What is being guarded is that
    # every meaningful line becomes its own name — a parser regression that
    # collapsed the file into one entry, or dropped the last line, would show
    # here — not how many nodes the federation currently has.
    meaningful = [
        line
        for line in DEFAULT_APPROVED_NAMES.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert len(an.unscoped) + sum(len(v) for v in an.per_node.values()) == len(meaningful)
    assert len(meaningful) > 1, "a one-entry list would make the matching tests vacuous"


def test_with_no_flag_the_committed_default_is_used(tmp_path):
    run = _run_assess(tmp_path)
    assert run["approved_names"]["supplied"]
    assert run["approved_names"]["default_used"]
    from basic_check.cli import DEFAULT_APPROVED_NAMES

    assert run["approved_names"]["count"] == len(
        ApprovedNames.load(DEFAULT_APPROVED_NAMES).unscoped
    )


def test_a_user_file_overrides_the_default(tmp_path):
    mine = tmp_path / "mine.txt"
    mine.write_text("egi: Only This One\n", encoding="utf-8")
    run = _run_assess(tmp_path, "--approved-names", str(mine))
    assert run["approved_names"]["count"] == 1
    assert not run["approved_names"]["default_used"]
    assert run["approved_names"]["scoped"]


def test_the_default_can_be_turned_off(tmp_path):
    """A one-off check of a page that is not an EOSC node needs this."""
    run = _run_assess(tmp_path, "--no-approved-names")
    assert not run["approved_names"]["supplied"]
    assert not run["approved_names"]["default_used"]


def test_the_default_still_errors_clearly_if_the_user_file_is_missing(tmp_path):
    """Falling back to the default here would check something unasked for."""
    from typer.testing import CliRunner

    from basic_check.cli import app

    res = CliRunner().invoke(app, ["assess", "--approved-names", str(tmp_path / "nope.txt")])
    assert res.exit_code != 0
    assert "approved-names file not found" in (res.output + str(res.exception))


def test_the_official_names_match_the_nodes_that_show_them(tmp_path):
    """Pinned against the committed evidence, so a matching change is visible.

    Four of the pages carry their approved name in the body, all with a
    separator the official list does not use ("EOSC Node - BBMRI-ERIC",
    "EOSC Node Czechia", "EOSC Node EUDAT", "EOSC Node Slovakia"). This asserts
    the real-world outcome, not a synthetic one. Evidence of runs web-4, web-5, web-6 and web-8, 26
    September 2026. GÉANT's page also carries its name ("EOSC Node GÉANT", as
    matched on 24 September), but on 26 September it answered with the
    Cloudflare challenge, so there was no body to match; on 21 September only
    BBMRI-ERIC and EUDAT matched, for the same reason and because Czechia and
    Slovakia were not collected.
    """
    run = _run_assess(tmp_path)
    matched = {
        n["id"]
        for n in run["nodes"]
        for r in n["results"]
        if r["point_id"] == "3"
        for e in r["evidence"]
        if "approved name matched" in e
    }
    assert matched == {"bbmri-eric", "eosc-cz", "eudat", "eosc-sk"}


# --- what the page calls itself, when nothing matched ------------------------


def test_the_shared_prefix_of_the_official_list_is_found():
    from basic_check.cli import DEFAULT_APPROVED_NAMES

    an = ApprovedNames.load(DEFAULT_APPROVED_NAMES)
    assert an.common_prefix("egi") == "EOSC Node"


def test_a_list_with_nothing_in_common_has_no_prefix():
    an = parse_approved_names("Alpha Thing\nBeta Other\n")
    assert an.common_prefix("x") == ""


def test_a_single_name_yields_no_prefix_to_hunt_for():
    """One name is its own prefix; quoting it back as a near miss is noise."""
    an = parse_approved_names("EOSC Node | EGI\n")
    assert an.common_prefix("egi") == ""


def test_the_shared_phrase_is_counted_when_no_name_matched():
    """A count is checkable; a quoted guess at the name was not.

    The first attempt quoted the text after the prefix. On the real pages that
    produced "EOSC Node f", cut at an ellipsis, and on another page quoted a
    sentence about a different node. This reports only what can be verified.
    """
    an = parse_approved_names("EOSC Node | EGI\nEOSC Node | EUDAT\n")
    assert an.prefix_hits("the EOSC Node for Sweden, an EOSC Node", "x") == ("EOSC Node", 2)


def test_nothing_is_offered_when_the_shared_phrase_is_absent():
    an = parse_approved_names("EOSC Node | EGI\nEOSC Node | EUDAT\n")
    assert an.prefix_hits("a page about something else entirely", "x") == ("EOSC Node", 0)


def test_the_default_source_is_recorded_repo_relative_not_absolute(tmp_path):
    """The committed report is published; a sandbox path in it is a leak."""
    run = _run_assess(tmp_path)
    assert run["approved_names"]["source"] == "checklist/approved-names.txt"


# --- the separator loosening must be reversible from the command line ---------


def test_strict_separators_restores_the_literal_match():
    """The flexible separator rule is a judgement call, not a fact: it was
    adopted because matching the pipe literally scored 0 of 9 against the real
    pages. Anyone who disagrees must be able to see the strict result without
    editing this module, so the reversal is a flag rather than a code change.
    """
    lax = parse_approved_names("EOSC Node | EUDAT")
    strict = parse_approved_names("EOSC Node | EUDAT", strict_separators=True)
    page = "Welcome to the EOSC Node - EUDAT service catalogue."
    assert lax.match(page, "eudat") == "EOSC Node | EUDAT"
    assert strict.match(page, "eudat") is None


def test_strict_separators_still_matches_the_exact_form():
    strict = parse_approved_names("EOSC Node | EUDAT", strict_separators=True)
    assert strict.match("shown as EOSC Node | EUDAT here", "eudat") == "EOSC Node | EUDAT"


def test_strict_separators_still_tolerates_the_amount_of_whitespace():
    """A page that wraps the name across two lines writes the same name. That is
    whitespace normalisation, not a different separator, so strict mode keeps it.
    """
    strict = parse_approved_names("EOSC Node | EUDAT", strict_separators=True)
    assert strict.match("EOSC  Node\n|\tEUDAT", "eudat") == "EOSC Node | EUDAT"


def test_strict_separators_is_recorded_so_a_report_can_state_it():
    assert parse_approved_names("X", strict_separators=True).strict_separators is True
    assert parse_approved_names("X").strict_separators is False


# --- provenance: which bytes were used ----------------------------------------


def test_the_run_records_the_hash_of_the_list_it_used(tmp_path):
    """The tool cannot know whether the approved-names file is current. It can
    say exactly which bytes it used, which is what makes staleness detectable at
    all: a reader comparing two runs, or a run against the circulated file, has
    something to compare. Same reasoning as source_sha256 on the checklist.
    """
    import hashlib

    from basic_check.cli import DEFAULT_APPROVED_NAMES

    run = _run_assess(tmp_path)
    expected = hashlib.sha256(DEFAULT_APPROVED_NAMES.read_bytes()).hexdigest()
    assert run["approved_names"]["sha256"] == expected


def test_a_user_supplied_list_is_hashed_too(tmp_path):
    import hashlib

    mine = tmp_path / "mine.txt"
    mine.write_text("egi: EOSC Node | EGI\n", encoding="utf-8")
    run = _run_assess(tmp_path, "--approved-names", str(mine))
    assert run["approved_names"]["sha256"] == hashlib.sha256(mine.read_bytes()).hexdigest()


def test_no_list_means_no_hash_rather_than_the_hash_of_nothing(tmp_path):
    """sha256("") is a real-looking hex string, and would read as a list that was
    used. An absent list must be absent, not empty.
    """
    run = _run_assess(tmp_path, "--no-approved-names")
    assert run["approved_names"]["sha256"] == ""


def test_the_separator_rule_in_force_is_recorded(tmp_path):
    """Separate directories: _run_assess copies the evidence tree in, so two
    calls on one tmp_path fail on the copy rather than on the assertion.
    """
    lax = _run_assess(tmp_path / "lax")
    strict = _run_assess(tmp_path / "strict", "--strict-separators")
    assert lax["approved_names"]["strict_separators"] is False
    assert strict["approved_names"]["strict_separators"] is True
