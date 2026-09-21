"""Tests for each checklist point, written as adversarial cases.

The bias these guard against: a checker that says PASS too easily is worse than
no checker, because a false PASS is never investigated. So most of these tests
assert that a plausible-looking page does NOT pass.
"""

from __future__ import annotations

from basic_check import checks
from basic_check.fetch import Control, Image, Link, PageEvidence
from basic_check.names import parse_approved_names


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


def test_point1_does_not_fail_on_403_with_no_login_offered():
    """This assertion was inverted deliberately, and the reason is worth keeping.

    It originally asserted FAIL: a 403 with no login means neither branch of
    point 1 is satisfied. That reasoning was wrong in practice. GÉANT served this
    tool HTTP 200, and then 403 once depth-1 crawling made a few more requests to
    the same host. Nothing about the node's accessibility had changed. Genuine
    access control redirects to a login page; a bare 403 to an automated client is
    usually bot mitigation, and says nothing about what a researcher would see.

    A tool must not turn its own request volume into a finding against a node.
    """
    r = checks.check_1(ev(http_status=403, full_text="Forbidden"))
    assert r.verdict == checks.MANUAL_REVIEW


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


def _logo_ev(**kw):
    return ev(images=[Image(src="https://cdn.example/eosc.svg", alt="EOSC")], **kw)


def test_point3_reports_when_no_approved_name_matches():
    r = checks.check_3(
        _logo_ev(full_text="Some Node" * 50),
        approved_names=["EOSC Node Poland", "EOSC Node Finland"],
    )
    assert any("NONE of the 2 approved name(s)" in e for e in r.evidence)


def test_point3_says_nothing_about_names_when_no_list_is_supplied():
    r = checks.check_3(_logo_ev(full_text="EOSC Node Finland"))
    assert not any("approved name" in e for e in r.evidence)


def test_point3_does_not_match_a_short_name_inside_a_longer_word():
    """Regression: "EGI" matched "strategic" on the BBMRI-ERIC page."""
    r = checks.check_3(
        _logo_ev(full_text="one of Europe's strategic research priorities"),
        approved_names=["EGI"],
    )
    assert any("NONE of the" in e for e in r.evidence)


def test_point3_marks_an_unscoped_match_as_not_establishing_ownership():
    r = checks.check_3(
        _logo_ev(full_text="Welcome to the EGI Node"),
        approved_names=["EGI Node"],
    )
    note = next(e for e in r.evidence if "approved name" in e)
    assert "unscoped" in note
    assert "does not establish" in note


def test_point3_reports_a_scoped_match_plainly():
    names = parse_approved_names("t: EGI Node\n")  # the test evidence has node_id "t"
    r = checks.check_3(_logo_ev(full_text="Welcome to the EGI Node"), approved_names=names)
    assert any("scoped to this node" in e for e in r.evidence)


def test_point3_will_not_borrow_another_nodes_scoped_name():
    """Regression: any name matching any page satisfied that page."""
    names = parse_approved_names("somewhere-else: EGI Node\n")
    r = checks.check_3(_logo_ev(full_text="Welcome to the EGI Node"), approved_names=names)
    assert any("no approved name was supplied for this node" in e for e in r.evidence)


def test_point3_verdict_is_unchanged_by_the_name_list():
    """The list adds evidence for a reviewer; it never decides the point."""
    page = _logo_ev(full_text="Welcome to the EGI Node")
    assert checks.check_3(page).verdict == checks.check_3(page, ["EGI Node"]).verdict
    assert checks.check_3(page, ["Nothing Like It"]).verdict == checks.MANUAL_REVIEW


def test_point3_names_are_reported_even_when_no_logo_is_found():
    r = checks.check_3(ev(images=[], full_text="Welcome to the EGI Node"), approved_names=["EGI Node"])
    assert any("approved name matched" in e for e in r.evidence)


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


# --- the render gate: distrusting absence without excusing it ----------------


def _consent_heavy_but_fully_rendered() -> PageEvidence:
    """The EOSC DTO landing page, as actually measured on 18 September 2026.

    20 links, 14 images, 34 controls, 530 chars of main text, 4328 of full text.
    A consent banner suppresses the *visible* text; the DOM is complete. Verified
    against the live page: the raw HTML carries exactly 20 anchors, the rendered
    DOM carries 21, clicking "Accept All" changes nothing, and none of them
    points at eosc.eu.
    """
    return ev(
        links=[Link(f"https://eosc-dto.d4science.org/p{i}", f"Item {i}") for i in range(20)],
        images=[Image(f"/img/{i}.png") for i in range(14)],
        controls=[Control(f"Button {i}") for i in range(34)],
        main_text="We value your privacy This website uses cookies Accept All Reject All",
        full_text="We value your privacy This website uses cookies Accept All Reject All " * 62,
    )


def test_a_consent_banner_does_not_excuse_a_missing_link():
    """Regression: EOSC DTO point 4 was MANUAL_REVIEW when it should have been FAIL.

    A consent overlay hides text, not anchors. Gating a *link*-absence verdict on
    a *text*-length signal let a verified absence escape as "cannot conclude".
    Confirmed against the live page before changing the rule.
    """
    page = _consent_heavy_but_fully_rendered()
    assert checks.link_collection_warning(page) == ""
    assert checks.check_4(page).verdict == checks.FAIL
    assert checks.check_6(page).verdict == checks.FAIL


def test_a_sparse_page_is_not_treated_as_unrendered():
    """20 links is the whole document on a compact portal page, not a truncation."""
    page = _consent_heavy_but_fully_rendered()
    assert "20 links" not in checks.link_collection_warning(page)


def test_absence_is_still_distrusted_when_nothing_was_collected():
    """EUDAT during its HTTP 500: 0 links, 0 images, 0 controls, 61 chars.

    This is the case the gate exists for, and it must keep working.
    """
    page = ev(links=[], images=[], controls=[], main_text="x" * 61, full_text="x" * 61)
    assert checks.link_collection_warning(page)
    assert checks.check_4(page).verdict == checks.MANUAL_REVIEW
    assert checks.check_6(page).verdict == checks.MANUAL_REVIEW


def test_an_empty_document_with_stray_links_is_still_distrusted():
    """A shell that rendered a nav but no document should not ground a FAIL."""
    page = ev(links=[Link("https://n.example/a", "A")], images=[], controls=[],
              main_text="Loading", full_text="Loading")
    assert checks.link_collection_warning(page)
    assert checks.check_4(page).verdict == checks.MANUAL_REVIEW


def test_point3_does_not_claim_a_name_is_absent_from_a_page_it_never_read():
    """GEANT answers 403 with no body: "none appear" would be a claim about nothing."""
    r = checks.check_3(ev(full_text="", http_status=403), approved_names=["EOSC Node - GEANT"])
    note = next(e for e in r.evidence if "approved name" in e)
    assert "not looked for" in note
    assert "403" in note
    assert "NONE" not in note


# --- point 3: the logo match must not be satisfied by the site's own hostname --


def test_the_logo_match_ignores_eosc_in_the_sites_own_hostname():
    """The defect this guards: on the real eosc-dto node, 7 of 8 "EOSC-referencing
    image asset(s)" matched only because the page is served from
    eosc-dto.d4science.org. One of them was an EU funding badge named
    FundedbytheEU.png. The host is a property of the site, not of the image, so
    it cannot be evidence that an EOSC logo is shown.
    """
    images = [
        Image(src="https://eosc-dto.example.org/documents/FundedbytheEU.png"),
        Image(src="https://eosc-dto.example.org/image/layout_icon?img_id=1"),
    ]
    res = checks.check_3(ev(images=images, final_url="https://eosc-dto.example.org/"))
    assert "none referencing EOSC" in " ".join(res.evidence), res.evidence


def test_an_image_actually_served_from_eosc_eu_still_counts():
    """The mirror case: a logo loaded cross-host from eosc.eu is a real signal,
    and at least one node in the set does exactly that.
    """
    images = [Image(src="https://eosc.eu/sites/default/files/logo-x.svg")]
    res = checks.check_3(ev(images=images, final_url="https://node.example/"))
    assert "image asset(s): 1" in " ".join(res.evidence), res.evidence


def test_a_lookalike_domain_does_not_count_as_eosc_eu():
    images = [Image(src="https://myeosc.example/logo.svg")]
    res = checks.check_3(ev(images=images, final_url="https://node.example/"))
    assert "none referencing EOSC" in " ".join(res.evidence), res.evidence


def test_eosc_inside_a_longer_word_does_not_count():
    """"geoscience" contains "eosc". The same class of bug as EGI matching
    "strategic", which was fixed in the name match but not here.
    """
    images = [
        Image(src="https://node.example/img/geoscience-banner.png", alt="Geoscience data"),
    ]
    res = checks.check_3(ev(images=images, final_url="https://node.example/"))
    assert "none referencing EOSC" in " ".join(res.evidence), res.evidence


def test_eosc_in_the_filename_still_counts():
    images = [Image(src="https://node.example/themes/images/eosc-node-final.webp")]
    res = checks.check_3(ev(images=images, final_url="https://node.example/"))
    assert "image asset(s): 1" in " ".join(res.evidence), res.evidence


def test_eosc_in_the_alt_text_still_counts():
    images = [Image(src="https://cdn.example/x.png", alt="EOSC Node Finland")]
    res = checks.check_3(ev(images=images, final_url="https://node.example/"))
    assert "image asset(s): 1" in " ".join(res.evidence), res.evidence


def test_a_camelcase_eosc_lockup_filename_still_counts():
    """A defect in the boundary fix above, caught by regenerating the real
    report: requiring a non-word character after "eosc" rejected
    EOSCNode_Finland-1-1-scaled.jpg and EOSCNodeBBMRIERIC_ColourPos.png — the
    actual EOSC Node lockups, which several nodes name with no separator at all.
    The Finnish node's only EOSC asset disappeared, flipping its point 3 evidence
    from "asset present" to "none found". An uppercase letter is a word boundary
    to a human reading CamelCase, so it is treated as one here.
    """
    for src in (
        "https://research.csc.fi/app/uploads/EOSCNode_Finland-1-1-scaled.jpg",
        "https://i0.wp.com/x/EOSCNodeBBMRIERIC_ColourPos-1-scaled.png",
        "https://node.example/EOSCNodeDataTerra_ColourPos-scaled.jpg",
    ):
        res = checks.check_3(ev(images=[Image(src=src)], final_url="https://node.example/"))
        assert "image asset(s): 1" in " ".join(res.evidence), src


def test_geoscience_is_still_not_a_logo():
    """The word that motivated the boundary in the first place. Blocked by the
    *leading* guard — "eosc" there is preceded by a letter — which is why
    allowing an uppercase letter after it is safe, including for "GEOSCIENCE".
    """
    for src in ("/img/geoscience.png", "/img/GEOSCIENCE-BANNER.png", "/img/neoscope.png"):
        res = checks.check_3(ev(images=[Image(src=src)], final_url="https://node.example/"))
        assert "none referencing EOSC" in " ".join(res.evidence), src
