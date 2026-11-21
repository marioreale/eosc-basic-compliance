"""Clickable items without an href: finding where they lead.

EOSC Life Sciences Connect is a JavaScript application. Its footer item "AUP and
UAP" is an <a> with no href and its menu item "Contact Us" a <span>; the app
changes the address only when they are clicked. Reading a[href] alone, the tool
saw the words but no link, and in web-42 and web-43 reported the node's AUP,
UAP and contact route as missing. These tests pin the repair: which items are
clicked, how the clicks become links, and that the checks then read them.
"""

from __future__ import annotations

import asyncio
import os
import re

import pytest

from basic_check import checks
from basic_check.fetch import (
    MAX_SCRIPTED_CLICKS,
    ChildPage,
    Link,
    PageEvidence,
    _wait_for_render,
    resolve_scripted_links,
    scripted_labels_to_click,
    scripted_records_to_links,
    select_children,
)
from basic_check.patterns import HELPDESK_ON_PAGE

LANDING = "https://lsc.example/home"
LSC_LABELS = ["HOME", "ABOUT", "CONTACT US", "CATALOGUE", "Log in", "Home", "About", "AUP and UAP"]


def test_only_labels_that_can_settle_a_point_are_clicked():
    chosen = scripted_labels_to_click(LSC_LABELS, [])
    assert chosen == ["ABOUT", "CONTACT US", "CATALOGUE", "AUP and UAP"]
    # Cookie and login buttons are never clicked.
    assert scripted_labels_to_click(["Accept all", "Reject all", "Login", "Settings"], []) == []


def test_a_label_already_on_a_real_link_is_not_clicked():
    links = [Link("https://lsc.example/about", "About")]
    assert "ABOUT" not in scripted_labels_to_click(LSC_LABELS, links)


def test_clicks_are_capped():
    labels = [f"Contact office {i}" for i in range(20)]
    assert len(scripted_labels_to_click(labels, [])) == MAX_SCRIPTED_CLICKS


def test_clicks_that_opened_a_page_become_links_once():
    records = [
        {"text": "AUP and UAP", "href": "https://lsc.example/aup-and-uap", "outcome": "x"},
        {"text": "CONTACT US", "href": "https://lsc.example/contact-information", "outcome": "x"},
        {"text": "CATALOGUE", "href": "https://lsc.example/catalogue", "outcome": "x"},
        {"text": "ABOUT", "href": "", "outcome": "clicking it did not open a page"},
        {"text": "HOME", "href": LANDING, "outcome": "x"},
    ]
    existing = [Link("https://lsc.example/catalogue", "service catalogue")]
    links = scripted_records_to_links(records, LANDING, existing)
    assert [(lnk.text, lnk.href) for lnk in links] == [
        ("AUP and UAP", "https://lsc.example/aup-and-uap"),
        ("CONTACT US", "https://lsc.example/contact-information"),
    ]


def _lsc_evidence(children: list[ChildPage]) -> PageEvidence:
    body = "The EOSC Life Sciences Connect Node brings together research infrastructures. " * 20
    links = scripted_records_to_links(
        [
            {"text": "AUP and UAP", "href": "https://lsc.example/aup-and-uap", "outcome": ""},
            {"text": "CONTACT US", "href": "https://lsc.example/contact-information",
             "outcome": ""},
        ],
        LANDING,
    )
    return PageEvidence(
        node_id="lsc", node_name="LSC", requested_url=LANDING, final_url=LANDING,
        http_status=200, full_text=body + " Home About AUP and UAP", main_text=body,
        links=links, crawl_depth=1, children=children,
    )


def test_the_resolved_links_are_followed_and_settle_5b_5c_and_6():
    policy = (
        "Life Sciences Connect – Acceptable Use Policy. By accessing or using services "
        "provided through the Node, users agree to use the services exclusively for lawful "
        "purposes. Life Sciences Connect – User Access Policy. Access is granted to "
        "registered users who accept these conditions. " * 3
    )
    contact = "Contact us General information and questions: Contact us via help@lsc.example"
    ev = _lsc_evidence([])
    selected, _ = select_children(ev)
    assert {c.url for c in selected} == {
        "https://lsc.example/aup-and-uap", "https://lsc.example/contact-information",
    }
    by_url = {"https://lsc.example/aup-and-uap": policy,
              "https://lsc.example/contact-information": contact}
    for c in selected:
        c.http_status, c.final_url = 200, c.url
        c.full_text = c.main_text = by_url[c.url]
        c.title = "AUP" if "aup" in c.url else "Contact"
    ev.children = selected
    assert checks.check_5b(ev).verdict == checks.PASS
    assert checks.check_5c(ev).verdict == checks.PASS
    assert checks.check_6(ev).verdict == checks.PASS


def test_a_help_mailbox_in_page_text_names_a_helpdesk():
    def hit(s: str) -> bool:
        return any(re.search(p, s) for p in HELPDESK_ON_PAGE)

    assert hit("Contact us via help@eosc-lifesciences-connect.eu")
    assert hit("write to help [at] node.example")
    assert not hit("self-help@node.example")
    assert not hit("we are here to help @ any time")


class _GrowingPage:
    """A fake page whose visible text grows as an application draws it."""

    def __init__(self, lengths: list[int]) -> None:
        self.lengths, self.reads = lengths, 0

    async def evaluate(self, _js):
        n = self.lengths[min(self.reads, len(self.lengths) - 1)]
        self.reads += 1
        return n

    async def wait_for_timeout(self, _ms):
        return None


def test_a_linked_page_is_read_only_once_its_text_has_settled():
    page = _GrowingPage([0, 0, 0, 1200, 3700, 3756, 3756])
    asyncio.run(_wait_for_render(page))
    assert page.reads == 6  # stops at 3756, within 2% of 3700, not at the empty shell


def test_the_render_wait_is_bounded_for_a_page_that_never_draws():
    page = _GrowingPage([0])
    asyncio.run(_wait_for_render(page, max_ms=2_000))
    assert page.reads == 5


# --- in a real browser: opt-in, so the default suite opens no browser --------
# Run with BASIC_CHECK_BROWSER_TESTS=1 (and Chromium installed) to include it.

APP = """<!doctype html><html lang="en"><body>
<nav><span style="cursor:pointer" onclick="history.pushState({}, '', '/contact')">Contact Us</span>
<button>Accept all</button></nav>
<main><p>Landing page text.</p></main>
<footer><a class="MuiLink-root" onclick="history.pushState({}, '', '/aup-and-uap')">AUP and UAP</a>
<a class="MuiLink-root" onclick="void 0">Terms of use</a></footer>
</body></html>"""


@pytest.mark.skipif(
    os.environ.get("BASIC_CHECK_BROWSER_TESTS") != "1",
    reason="opens a browser; set BASIC_CHECK_BROWSER_TESTS=1 to run it",
)
def test_clicking_scripted_items_in_a_browser_records_their_addresses():
    pw = pytest.importorskip("playwright.async_api")

    async def run():
        async with pw.async_playwright() as p:
            try:
                browser = await p.chromium.launch()
            except Exception as exc:  # no browser binary on this machine
                pytest.skip(f"Chromium not available: {exc}")
            page = await browser.new_page()

            async def serve(route):
                await route.fulfill(status=200, content_type="text/html", body=APP)

            await page.route("https://app.example/**", serve)
            await page.goto("https://app.example/home")
            records = await resolve_scripted_links(page, "https://app.example/home", [])
            await browser.close()
            return records

    records = asyncio.run(run())
    got = {r["text"]: r["href"] for r in records}
    assert got["Contact Us"] == "https://app.example/contact"
    assert got["AUP and UAP"] == "https://app.example/aup-and-uap"
    assert got["Terms of use"] == ""
    assert "Accept all" not in got
