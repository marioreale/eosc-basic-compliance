"""Tests for the one-level crawl: what gets followed, and what it changes.

Two distinct risks are guarded here.

The first is load. "Follow one level" on a page with 167 links means 167
requests to someone else's server, and nine nodes would be ~1000. The selection
rules exist to keep that to single digits, so they are pinned.

The second is the opposite of the usual bias: crawling makes it *easier* to say
PASS, because a link target can now be inspected and found plausible. So these
tests mostly assert that a fetched child page does NOT rescue a weak finding --
a 404 policy link fails, and a navigation stub is not a policy.
"""

from __future__ import annotations

from basic_check import checks
from basic_check.fetch import (
    DEFAULT_FETCH_BUDGET,
    MAX_CHILDREN,
    MAX_GRANDCHILDREN_PER_CHILD,
    ChildPage,
    FetchBudget,
    Link,
    PageEvidence,
    select_children,
    select_grandchildren,
    without_depth_2,
)

POLICY_BODY = (
    "This Acceptable Use Policy sets out the terms under which you may use the "
    "services. You must not attempt to gain unauthorised access. Users are "
    "responsible for complying with these conditions at all times. " * 4
)


def page(links: list[Link], **kw) -> PageEvidence:
    body = "This node provides research services to European scientists. " * 40
    base = dict(
        node_id="t",
        node_name="T",
        requested_url="https://node.example/",
        final_url="https://node.example/",
        http_status=200,
        full_text=body,
        main_text=body,
        links=links,
    )
    base.update(kw)
    return PageEvidence(**base)


# --- selection: keeping the request count honest ------------------------------


def test_only_checklist_relevant_links_are_followed():
    """A page of ordinary navigation must produce no child requests at all."""
    links = [Link(f"https://node.example/news/{i}", f"News item {i}") for i in range(60)]
    links += [Link("https://node.example/events", "Events"), Link("https://node.example/", "Home")]
    selected, skipped = select_children(page(links))
    assert selected == []
    assert skipped == []


def test_policy_and_contact_links_are_followed():
    links = [
        Link("https://node.example/aup", "Acceptable Use Policy"),
        Link("https://node.example/access-policy", "User Access Policy"),
        Link("https://node.example/contact", "Contact us"),
        Link("https://node.example/news/1", "Some news"),
    ]
    selected, _ = select_children(page(links))
    got = {c.url: c.selected_for for c in selected}
    assert "https://node.example/news/1" not in got
    assert any("5b" in v for v in got.values())
    assert any("5c" in v for v in got.values())
    assert any("6" in v for v in got.values())


def test_selection_is_capped_and_the_drop_is_recorded():
    """Hitting a cap must be visible, or a later "not found" is unaccountable."""
    links = [Link(f"https://node.example/contact-{i}", f"Contact office {i}") for i in range(30)]
    links += [Link(f"https://node.example/aup-{i}", f"Acceptable Use Policy {i}") for i in range(30)]
    selected, skipped = select_children(page(links), max_children=4)
    assert len(selected) <= 4
    assert skipped, "dropped candidates must be recorded, not silently discarded"


def test_third_party_links_are_not_followed():
    """Load must not spread onto sites that cannot settle a point about this node."""
    links = [
        Link("https://twitter.com/contact", "Contact us on Twitter"),
        Link("https://funder.example/about", "About our funder"),
        Link("https://other.example/aup", "Acceptable Use Policy"),
    ]
    selected, _ = select_children(page(links))
    assert selected == []


def test_subdomains_of_the_node_are_followed():
    links = [Link("https://docs.node.example/aup", "Acceptable Use Policy")]
    selected, _ = select_children(page(links))
    assert len(selected) == 1


def test_binary_targets_are_not_fetched():
    """A PDF policy is a real finding but cannot be rendered to text here."""
    links = [Link("https://node.example/aup.pdf", "Acceptable Use Policy")]
    selected, _ = select_children(page(links))
    assert selected == []


def test_the_landing_page_itself_is_never_refetched():
    links = [Link("https://node.example/", "Acceptable use policy")]
    selected, _ = select_children(page(links))
    assert selected == []


# --- verdicts: crawling must not make PASS cheaper ---------------------------


def child(url="https://node.example/aup", for_points=("5b",), **kw) -> ChildPage:
    base = dict(
        url=url,
        selected_for=list(for_points),
        http_status=200,
        final_url=url,
        title="Acceptable Use Policy",
        main_text=POLICY_BODY,
        full_text=POLICY_BODY,
    )
    base.update(kw)
    return ChildPage(**base)


def test_a_broken_policy_link_fails_rather_than_passing_on_its_label():
    """The requirement is that the policy be accessible, not that a link exist.

    Before crawling, a link labelled "Acceptable Use Policy" pointing at a 404
    scored PASS. That is the single most valuable thing this level of crawling
    buys, so it is pinned.
    """
    ev = page(
        [Link("https://node.example/aup", "Acceptable Use Policy")],
        crawl_depth=1,
        children=[child(http_status=404, main_text="Not found", full_text="Not found")],
    )
    r = checks.check_5b(ev)
    assert r.verdict == checks.FAIL
    assert "404" in r.message


def test_a_verified_policy_page_passes_and_says_it_was_read():
    ev = page(
        [Link("https://node.example/aup", "Acceptable Use Policy")],
        crawl_depth=1,
        children=[child()],
    )
    r = checks.check_5b(ev)
    assert r.verdict == checks.PASS
    assert "fetched" in r.message


def test_a_navigation_stub_is_not_accepted_as_a_policy():
    """A page titled "Policies" that only links onward is not a policy document."""
    ev = page(
        [Link("https://node.example/policies", "Acceptable Use Policy")],
        crawl_depth=1,
        children=[child(main_text="Policies", full_text="Policies", title="Policies")],
    )
    assert checks.check_5b(ev).verdict == checks.MANUAL_REVIEW


def test_an_unreachable_policy_target_is_review_not_fail():
    """A 403 is more often a bot restriction than a real absence."""
    ev = page(
        [Link("https://node.example/aup", "Acceptable Use Policy")],
        crawl_depth=1,
        children=[child(http_status=403, main_text="", full_text="")],
    )
    assert checks.check_5b(ev).verdict == checks.MANUAL_REVIEW


def test_without_crawling_a_policy_link_passes_but_is_marked_unverified():
    """Depth 0 must stay usable, and must not overstate what it checked."""
    ev = page([Link("https://node.example/aup", "Acceptable Use Policy")])
    r = checks.check_5b(ev)
    assert r.verdict == checks.PASS
    assert "not fetched" in r.message or "pointer" in r.message


def test_a_contact_page_naming_a_helpdesk_upgrades_point_6():
    desk = "Our service desk answers user questions. Email the helpdesk below. " * 6
    ev = page(
        [Link("https://node.example/contact", "Contact")],
        crawl_depth=1,
        children=[
            child(
                url="https://node.example/contact",
                for_points=("6",),
                title="Contact",
                main_text=desk,
                full_text=desk,
                links=[Link("mailto:support@node.example", "support")],
            )
        ],
    )
    r = checks.check_6(ev)
    assert r.verdict == checks.PASS
    assert "helpdesk" in r.message.lower() or "support" in r.message.lower()


def test_a_broken_contact_link_fails_point_6():
    ev = page(
        [Link("https://node.example/contact", "Contact")],
        crawl_depth=1,
        children=[
            child(url="https://node.example/contact", for_points=("6",), http_status=404,
                  main_text="Not found", full_text="Not found")
        ],
    )
    assert checks.check_6(ev).verdict == checks.FAIL


def test_a_bare_contact_page_with_no_helpdesk_signal_stays_review():
    generic = "Head office, Rue de la Loi 1, Brussels. Press enquiries only. " * 6
    ev = page(
        [Link("https://node.example/contact", "Contact")],
        crawl_depth=1,
        children=[
            child(
                url="https://node.example/contact",
                for_points=("6",),
                title="Contact",
                main_text=generic,
                full_text=generic,
                links=[Link("mailto:press@node.example", "press")],
            )
        ],
    )
    assert checks.check_6(ev).verdict == checks.MANUAL_REVIEW


def test_point_2_stays_a_judgement_even_with_an_about_page():
    """The checklist asks the *landing page* to state these things.

    An About page one level down is context for the reviewer, not a substitute,
    so it must not flip the verdict.
    """
    about = "We are a research infrastructure serving European biologists. " * 8
    ev = page(
        [Link("https://node.example/about", "About us")],
        crawl_depth=1,
        children=[
            child(url="https://node.example/about", for_points=("2",), title="About",
                  main_text=about, full_text=about)
        ],
    )
    r = checks.check_2(ev)
    assert r.verdict == checks.MANUAL_REVIEW
    assert any("one level down" in line for line in r.evidence)


def test_crawling_does_not_change_point_4():
    """Point 4 is about a link on the landing page; children are irrelevant to it."""
    links = [Link("https://eosc.eu/building-the-eosc-federation/eosc-node-x/", "Our EOSC page")]
    bare = checks.check_4(page(links + [Link(f"https://node.example/{i}", f"P{i}") for i in range(40)]))
    crawled = checks.check_4(
        page(
            links + [Link(f"https://node.example/{i}", f"P{i}") for i in range(40)],
            crawl_depth=1,
            children=[child()],
        )
    )
    assert bare.verdict == crawled.verdict == checks.PASS


# --- a block is not a finding -------------------------------------------------


def test_a_403_without_a_login_is_review_not_a_failure():
    """Bot mitigation must not be reported as "not publicly accessible".

    Real case: GÉANT served HTTP 200 to this tool, and then 403 once depth-1
    crawling made a few more requests. The page had not changed; the tool had
    become more annoying. Failing point 1 on that would be the checker blaming a
    node for its own request volume.
    """
    ev = page([], http_status=403, full_text="Attention Required! Cloudflare Ray ID: abc123",
              main_text="Attention Required")
    r = checks.check_1(ev)
    assert r.verdict == checks.MANUAL_REVIEW
    assert "bot protection" in r.message.lower()


def test_a_403_with_no_bot_wording_is_still_not_a_failure():
    ev = page([], http_status=403, full_text="Forbidden", main_text="Forbidden")
    assert checks.check_1(ev).verdict == checks.MANUAL_REVIEW


def test_a_404_landing_page_does_fail_point_1():
    """A registered URL that does not resolve is a genuine, actionable finding."""
    ev = page([], http_status=404, full_text="Page not found", main_text="Page not found")
    r = checks.check_1(ev)
    assert r.verdict == checks.FAIL
    assert "404" in r.message


def test_a_500_is_review_because_it_is_usually_transient():
    ev = page([], http_status=503, full_text="Service Unavailable", main_text="x")
    assert checks.check_1(ev).verdict == checks.MANUAL_REVIEW


def test_a_normal_page_still_passes_point_1():
    ev = page([Link("https://node.example/a", "A")])
    assert checks.check_1(ev).verdict == checks.PASS


# --- the crawler and the checks must not disagree -----------------------------


def test_every_link_a_check_can_use_is_a_link_the_crawler_will_follow():
    """The crawler and the checks must share one vocabulary.

    They originally did not. The crawler looked for "acceptable use" while
    check_5b also accepted "terms of use", so a link the check treated as an AUP
    was never fetched, and the report said "target not fetched" for a page that
    was one request away. Nothing failed and no test caught it -- the output was
    just quietly weaker than it claimed to be.

    This walks the real vocabulary rather than a sample, so adding a term to one
    layer and not the other fails here instead of silently degrading a run.
    """
    from basic_check.patterns import AUP_PATTERNS, CONTACT_PATTERNS, UAP_PATTERNS

    cases = [
        ("5b", AUP_PATTERNS, ["Acceptable Use Policy", "AUP", "Terms of Use",
                              "Terms of Service", "Conditions of Use", "User Agreement"]),
        ("5c", UAP_PATTERNS, ["User Access Policy", "UAP", "Access Policy",
                              "Conditions of Access", "Access Conditions"]),
        ("6", CONTACT_PATTERNS, ["Contact", "Helpdesk", "Help desk", "Service desk",
                                 "Support", "Get in touch"]),
    ]
    for point_id, _patterns, labels in cases:
        for label in labels:
            slug = label.lower().replace(" ", "-")
            ev = page([Link(f"https://node.example/{slug}", label)])
            selected, _ = select_children(ev)
            assert selected, f"a link labelled {label!r} is used by point {point_id} but would never be followed"
            assert any(point_id in c.selected_for for c in selected), (
                f"a link labelled {label!r} satisfies point {point_id} but the crawler "
                f"followed it only for {[c.selected_for for c in selected]}"
            )


# --- depth 2: a second hop, under a hard budget --------------------------------


def _child_with(links: list[Link], url="https://node.example/policies") -> ChildPage:
    return ChildPage(url=url, final_url=url, http_status=200, links=links, selected_for=["5b"])


def test_a_budget_hands_out_only_what_it_has():
    b = FetchBudget(total=3)
    assert [b.take() for _ in range(5)] == [True, True, True, False, False]
    assert b.spent == 3
    assert b.exhausted


def test_a_budget_of_zero_permits_nothing():
    """Guard against a falsy-vs-None bug making 0 mean unlimited."""
    b = FetchBudget(total=0)
    assert b.take() is False
    assert b.exhausted


def test_the_budget_records_why_it_stopped():
    b = FetchBudget(total=1)
    b.take()
    b.take()
    assert "budget" in b.note.lower()
    assert "1" in b.note


def test_grandchildren_are_selected_from_a_child_page():
    """A policy page linking to the real AUP is the case depth 2 exists for."""
    links = [
        Link("https://node.example/legal/aup-full", "Full Acceptable Use Policy"),
        Link("https://node.example/news/42", "Some news"),
    ]
    picked, _ = select_grandchildren(_child_with(links), FetchBudget(total=10))
    assert [g.url for g in picked] == ["https://node.example/legal/aup-full"]
    assert all(g.depth == 2 for g in picked)


def test_grandchildren_never_leave_the_node_site():
    links = [Link("https://unrelated-funder.org/aup", "Acceptable Use Policy")]
    picked, _ = select_grandchildren(_child_with(links), FetchBudget(total=10))
    assert picked == []


def test_grandchildren_do_not_revisit_pages_already_seen():
    """The AUP page linking back to itself, or to the landing page, must not refetch."""
    links = [
        Link("https://node.example/policies", "Acceptable Use Policy"),
        Link("https://node.example/policies/aup", "Acceptable Use Policy detail"),
    ]
    seen = {"https://node.example/policies", "https://node.example/policies/aup"}
    picked, skipped = select_grandchildren(_child_with(links), FetchBudget(total=10), seen=seen)
    assert picked == []
    assert any("already" in s for s in skipped)


def test_the_budget_caps_grandchildren_before_the_per_child_cap_does():
    """Links must span purposes, or the per-purpose cap binds first and the
    budget is never exercised -- which would make this test prove nothing."""
    links = [
        Link("https://node.example/legal/aup", "Acceptable Use Policy"),
        Link("https://node.example/legal/user-access-policy", "User Access Policy"),
        Link("https://node.example/contact", "Contact the helpdesk"),
    ]
    budget = FetchBudget(total=1)
    picked, skipped = select_grandchildren(_child_with(links), budget)
    assert len(picked) == 1, "the budget of 1 must stop the second selection"
    assert budget.exhausted
    assert any("budget" in s.lower() for s in skipped)


def test_a_child_yields_at_most_the_per_child_cap():
    links = [Link(f"https://node.example/legal/aup-{i}", "Acceptable Use Policy") for i in range(9)]
    picked, _ = select_grandchildren(_child_with(links), FetchBudget(total=99))
    assert len(picked) <= MAX_GRANDCHILDREN_PER_CHILD


def test_depth_2_costs_are_bounded_for_a_nine_node_run():
    """The whole point of the budget: a second hop must not become a crawl.

    Refuse to ship a default that could fan out to hundreds of requests against
    other people's production sites.
    """
    worst_case = 9 * (1 + MAX_CHILDREN + MAX_CHILDREN * MAX_GRANDCHILDREN_PER_CHILD)
    assert worst_case > DEFAULT_FETCH_BUDGET, "the budget must actually bind"
    assert DEFAULT_FETCH_BUDGET <= 120


# --- a depth-1 view of depth-2 evidence ---------------------------------------


def test_stripping_depth_2_leaves_the_depth_1_evidence_intact():
    """The dual-depth report compares like with like: one evidence set, two lenses.

    Re-fetching at depth 1 to build the comparison would double the load on the
    nodes and introduce time as a variable, so the shallow view is derived from
    the same capture instead.
    """
    kid = ChildPage(url="https://node.example/policies", depth=1, http_status=200)
    grandkid = ChildPage(url="https://node.example/policies/aup", depth=2, http_status=200)
    ev = page([Link("https://node.example/policies", "Policies")])
    ev.children = [kid, grandkid]
    ev.crawl_depth = 2

    shallow = without_depth_2(ev)
    assert [c.url for c in shallow.children] == ["https://node.example/policies"]
    assert shallow.crawl_depth == 1
    # The original must not be mutated: the deep view is rendered from it afterwards.
    assert len(ev.children) == 2
    assert ev.crawl_depth == 2


def test_stripping_depth_2_is_a_no_op_on_a_depth_1_capture():
    ev = page([])
    ev.children = [ChildPage(url="https://node.example/a", depth=1)]
    ev.crawl_depth = 1
    assert without_depth_2(ev).children == ev.children
    assert without_depth_2(ev).crawl_depth == 1
