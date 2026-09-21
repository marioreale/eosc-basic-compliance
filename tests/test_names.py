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


def test_punctuation_in_the_name_must_still_be_present():
    an = parse_approved_names("EOSC Node - BBMRI-ERIC\n")
    assert an.match("EOSC Node - BBMRI-ERIC", "b") == "EOSC Node - BBMRI-ERIC"
    assert an.match("EOSC Node BBMRI-ERIC", "b") is None


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
