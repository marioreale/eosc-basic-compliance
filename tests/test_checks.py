"""Tests for each checklist point, written as adversarial cases.

The bias these guard against: a checker that says PASS too easily is worse than
no checker, because a false PASS is never investigated. So most of these tests
assert that a plausible-looking page does NOT pass.
"""

from __future__ import annotations

from basic_check import checks
from basic_check.fetch import Image, Link, PageEvidence


def realistic(links: list[Link], **kw) -> PageEvidence:
    """A page with enough substance that the render-quality gate stays silent.

    Absence-based verdicts are deliberately suppressed on thin pages, so a test
    about rule logic must supply a page that looks genuinely rendered -- otherwise
    it tests the gate by accident.
    """
    padding = [Link(f"https://node.example/section-{i}", f"Section {i}") for i in range(40)]
    body = "This node provides research services to European scientists. " * 40
    base = dict(links=links + padding, full_text=body, main_text=body)
    base.update(kw)
    return ev(**base)


def ev(**kw) -> PageEvidence:
    base = dict(
        node_id="t",
        node_name="Test Node",
        requested_url="https://node.example/eosc/",
        final_url="https://node.example/eosc/",
        http_status=200,
        full_text="x" * 500,
        main_text="x" * 500,
        lang_attr="en",
    )
    base.update(kw)
    return PageEvidence(**base)


# --- point 1 -----------------------------------------------------------------


def test_point1_passes_when_content_is_served_anonymously():
    assert checks.check_1(ev()).verdict == checks.PASS


def test_point1_fails_on_403_with_no_login_offered():
    r = checks.check_1(ev(http_status=403, full_text="Forbidden"))
    assert r.verdict == checks.FAIL


def test_point1_is_manual_when_403_but_a_login_exists():
    """Branch (b) may apply, but only the EEN can confirm it is EOSC AAI."""
    r = checks.check_1(ev(http_status=403, full_text="Please log in to continue" * 20))
    assert r.verdict == checks.MANUAL_REVIEW
    assert "EOSC AAI" in r.message


def test_point1_does_not_pass_an_empty_shell():
    """A 200 with no content is a broken render, not a compliant page."""
    r = checks.check_1(ev(full_text="", main_text=""))
    assert r.verdict == checks.MANUAL_REVIEW


# --- point 4: the sharpest point in the checklist ----------------------------


def test_point4_passes_on_a_specific_node_entry():
    r = checks.check_4(
        ev(links=[Link("https://eosc.eu/building-the-eosc-federation/eosc-node-poland", "Our EOSC page")])
    )
    assert r.verdict == checks.PASS


def test_point4_fails_on_the_index_page_which_the_checklist_excludes():
    r = checks.check_4(
        ev(links=[Link("https://eosc.eu/building-the-eosc-federation", "EOSC Federation")])
    )
    assert r.verdict == checks.FAIL
    assert "index" in r.message.lower()


def test_point4_fails_on_the_eosc_homepage():
    r = checks.check_4(ev(links=[Link("https://eosc.eu/", "EOSC")]))
    assert r.verdict == checks.FAIL


def test_point4_fails_when_no_eosc_link_at_all():
    r = checks.check_4(realistic([Link("https://node.example/about", "About")]))
    assert r.verdict == checks.FAIL


def test_point4_is_not_fooled_by_a_lookalike_domain():
    """`eosc.eu.evil.example` must not satisfy a requirement about eosc.eu."""
    r = checks.check_4(
        realistic([Link("https://eosc.eu.evil.example/building-the-eosc-federation/x", "EOSC")])
    )
    assert r.verdict == checks.FAIL


# --- point 3 -----------------------------------------------------------------


def test_point3_never_claims_pass_without_the_approved_name_list():
    """The Tripartite-approved name cannot be checked without the list."""
    r = checks.check_3(ev(images=[Image(src="https://cdn.example/eosc-logo.svg", alt="EOSC")]))
    assert r.verdict == checks.MANUAL_REVIEW
    assert "Tripartite" in r.message


def test_point3_absence_of_logo_markup_is_not_stated_as_proof():
    r = checks.check_3(ev(images=[Image(src="https://cdn.example/hero.jpg", alt="Lab")]))
    assert r.verdict == checks.MANUAL_REVIEW
    assert "NOT proof of absence" in r.message


def test_point3_reports_when_no_approved_name_matches():
    r = checks.check_3(
        ev(images=[Image(src="https://cdn.example/eosc.svg", alt="EOSC")], full_text="Some Node" * 50),
        approved_names=["EOSC Node Poland", "EOSC Node Finland"],
    )
    assert any("NONE of the supplied approved names" in e for e in r.evidence)


# --- point 5b / 5c: AUP and UAP are distinct documents -----------------------


def test_aup_and_uap_are_not_conflated():
    """An Acceptable Use Policy is not a User Access Policy."""
    only_aup = ev(links=[Link("https://node.example/aup", "Acceptable Use Policy")])
    assert checks.check_5b(only_aup).verdict == checks.PASS
    assert checks.check_5c(only_aup).verdict == checks.MANUAL_REVIEW

    only_uap = ev(links=[Link("https://node.example/access", "User Access Policy")])
    assert checks.check_5c(only_uap).verdict == checks.PASS
    assert checks.check_5b(only_uap).verdict == checks.MANUAL_REVIEW


def test_missing_policy_is_manual_review_not_fail():
    """The checklist allows the policy to live in the resource's Catalogue entry."""
    r = checks.check_5b(ev(links=[Link("https://node.example/about", "About")]))
    assert r.verdict == checks.MANUAL_REVIEW
    assert "Catalogue" in r.message


# --- point 6 -----------------------------------------------------------------


def test_point6_passes_on_a_helpdesk_route():
    r = checks.check_6(ev(links=[Link("https://node.example/support", "User Support")]))
    assert r.verdict == checks.PASS


def test_point6_flags_a_generic_contact_rather_than_passing_it():
    """The checklist asks for the helpdesk, not a press office."""
    r = checks.check_6(ev(links=[Link("mailto:press@node.example", "Contact us")]))
    assert r.verdict == checks.MANUAL_REVIEW
    assert "helpdesk" in r.message


def test_point6_fails_when_no_contact_route_exists():
    r = checks.check_6(realistic([Link("https://node.example/science", "Science")]))
    assert r.verdict == checks.FAIL


# --- point 7 -----------------------------------------------------------------


def test_point7_passes_english_content():
    text = (
        "This node provides open access to biobanking data and services for researchers "
        "across Europe, supporting discovery and reuse of biological samples. " * 4
    )
    r = checks.check_7(ev(main_text=text, lang_attr="en-GB"))
    assert r.verdict == checks.PASS


def test_point7_handles_regional_english_tags():
    """en-GB, en-US and similar must count as English."""
    text = "The service offers federated access to research data for scientists. " * 8
    assert checks.check_7(ev(main_text=text, lang_attr="en-US")).verdict == checks.PASS


def test_point7_fails_non_english_content():
    text = (
        "Ce noeud fournit un acces ouvert aux donnees de recherche pour les scientifiques "
        "europeens, avec un accompagnement personnalise et des services varies. " * 4
    )
    r = checks.check_7(ev(main_text=text, lang_attr="fr"))
    assert r.verdict == checks.FAIL


def test_point7_english_content_with_wrong_lang_attribute_still_passes():
    """Point 7 is about the content served, not the metadata."""
    text = "This node offers computing and storage services to researchers everywhere. " * 6
    r = checks.check_7(ev(main_text=text, lang_attr="fi"))
    assert r.verdict == checks.PASS
    assert "inconsistency" in r.message


def test_point7_is_manual_when_there_is_too_little_text():
    r = checks.check_7(ev(main_text="Home", full_text="Home"))
    assert r.verdict == checks.MANUAL_REVIEW


# --- points that must never silently pass ------------------------------------


def test_judgement_points_are_never_auto_passed():
    """1R, 2, 5a turn on judgement or on data one request cannot see."""
    page = ev(
        links=[Link("https://x.example/a", "Resource A")],
        full_text="Our node serves researchers. " * 40,
        main_text="Our node serves researchers. " * 40,
    )
    for result in (checks.check_1R(page), checks.check_2(page), checks.check_5a(page)):
        assert result.verdict == checks.MANUAL_REVIEW
        assert result.reviewer_action, f"{result.point_id} must tell the reviewer what to do"


def test_run_all_returns_exactly_one_result_per_checklist_point():
    from pathlib import Path

    import yaml

    checklist = yaml.safe_load((Path(__file__).parents[1] / "checklist" / "v3.0.yaml").read_text())
    expected = [p["id"] for p in checklist["points"]]
    got = [r.point_id for r in checks.run_all(ev())]
    assert got == expected, "results must be one per point, in checklist order"


def test_every_result_carries_a_message():
    for r in checks.run_all(ev()):
        assert r.message.strip(), f"{r.point_id} produced no explanation"


def test_unreachable_page_errors_rather_than_failing_every_point():
    """A tool outage must not be recorded as the node's non-compliance."""
    broken = ev(error="TimeoutError: navigation timed out", http_status=None)
    results = checks.run_all(broken)
    assert all(r.verdict == checks.ERROR for r in results)
    assert not any(r.verdict == checks.FAIL for r in results)


def test_point4_rejects_domains_that_merely_end_in_eosc_eu():
    """`myeosc.eu` is not eosc.eu.

    The first implementation used netloc.endswith("eosc.eu"), so any domain
    ending in those characters satisfied the requirement. Found by probing the
    check with lookalike hosts rather than by the original tests.
    """
    for bad in (
        "https://myeosc.eu/building-the-eosc-federation/x",
        "https://not-eosc.eu/building-the-eosc-federation/x",
        "https://eosc.eu.evil.example/building-the-eosc-federation/x",
        "https://xeosc.eu/building-the-eosc-federation/x",
    ):
        r = checks.check_4(realistic([Link(bad, "EOSC page")]))
        assert r.verdict == checks.FAIL, f"{bad} must not satisfy point 4"

    for good in (
        "https://eosc.eu/building-the-eosc-federation/node-x",
        "https://www.eosc.eu/building-the-eosc-federation/node-x",
        "https://EOSC.EU/building-the-eosc-federation/node-x",
        "https://eosc.eu:443/building-the-eosc-federation/node-x",
    ):
        r = checks.check_4(realistic([Link(good, "EOSC page")]))
        assert r.verdict == checks.PASS, f"{good} must satisfy point 4"


# --- absence must not be concluded from a page that did not render -----------


def test_consent_overlay_blocks_an_absence_based_fail():
    """A cookie wall means the tool saw a banner, not the node's landing page.

    Observed on a real node: 530 characters of main text, all of it consent
    wording, 20 links. Reporting "no contact route exists" from that would be an
    accusation caused by the tool's own blind spot.
    """
    page = ev(
        full_text="We value your privacy This website uses cookies Accept All Reject All " * 8,
        main_text="We value your privacy Accept All",
        links=[Link("https://node.example/cookie-policy", "Read More")],
    )
    assert checks.render_warning(page)
    assert checks.check_6(page).verdict == checks.MANUAL_REVIEW
    assert checks.check_4(page).verdict == checks.MANUAL_REVIEW


def test_a_well_rendered_page_still_fails_when_the_link_is_genuinely_absent():
    """The gate must not become a blanket excuse that hides real findings."""
    links = [Link(f"https://node.example/p{i}", f"Page {i}") for i in range(60)]
    page = ev(links=links, full_text="Real content. " * 200, main_text="Real content. " * 200)
    assert checks.render_warning(page) == ""
    assert checks.check_4(page).verdict == checks.FAIL
    assert checks.check_6(page).verdict == checks.FAIL


def test_render_warning_flags_a_thin_shell():
    page = ev(links=[Link("https://n.example/a", "A")], main_text="Loading", full_text="Loading")
    assert "main text" in checks.render_warning(page)
