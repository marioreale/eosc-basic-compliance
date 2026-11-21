"""Same-site embedded frames: reading the content a page loads into an <iframe>.

Every page of EOSC Scholarly Commons draws only its menu, footer and cookie
dialog itself and loads its content into a same-site <iframe> (a Joomla article
at /pages/?option=com_content&...). Reading the top document alone, the tool saw
the landing page's text on every page, and up to web-44 reported 5b and 5c as
FAIL although the "Terms & Policies" page publishes the node's AUP and UAP.
These tests pin the repair: which frames are read, how their content is merged,
and that the checks then find the policy.
"""

from __future__ import annotations

import asyncio
import os

import pytest

from basic_check import checks
from basic_check.fetch import (
    MAX_FRAMES,
    ChildPage,
    Link,
    PageEvidence,
    _extract,
    merge_frames,
    read_frames,
    same_site,
)

SITE = "https://sc.example"


def test_same_site_ignores_a_leading_www_and_nothing_else():
    assert same_site(f"{SITE}/pages/?id=29", f"{SITE}/terms-and-policies")
    assert same_site("https://www.sc.example/a", "https://sc.example/b")
    assert not same_site("https://www.youtube.com/embed/x", f"{SITE}/home")
    assert not same_site("https://helpdesk.sc.example/form", f"{SITE}/contact")
    assert not same_site("about:blank", f"{SITE}/home")


def test_frame_content_is_appended_after_the_page_own_text():
    shell = _extract(
        '<html lang="en"><head><title>Terms | Node</title></head><body>'
        '<nav><a href="/about">About</a></nav><iframe src="/pages/?id=29"></iframe>'
        "<footer>Cookie policy</footer></body></html>",
        f"{SITE}/terms-and-policies",
    )
    article = _extract(
        "<html><body><h2>Acceptable Use Policy</h2><p>By using the Services you accept this AUP.</p>"
        '<a href="https://operator.example/aup">Operator AUP</a></body></html>',
        f"{SITE}/pages/?id=29",
    )
    merged = merge_frames(shell, [article])
    assert merged["main_text"].startswith(shell["main_text"])
    assert "By using the Services you accept this AUP." in merged["main_text"]
    assert [lk.href for lk in merged["links"]] == [f"{SITE}/about", "https://operator.example/aup"]
    # The page keeps its own title and language.
    assert merged["title"] == "Terms | Node" and merged["lang_attr"] == "en"
    # Nothing to merge leaves the extraction as it was.
    assert merge_frames(shell, []) == shell


class _Box:
    def __init__(self, h):
        self.h = h

    async def bounding_box(self):
        return {"width": 800, "height": self.h} if self.h else None

    async def get_attribute(self, _name):
        return "Terms & Policies"


class _Frame:
    def __init__(self, url, html, parent, height=600):
        self.url, self.html, self.parent_frame, self._h = url, html, parent, height

    async def frame_element(self):
        return _Box(self._h)

    async def content(self):
        return self.html

    async def evaluate(self, _js):
        return len(self.html)

    async def wait_for_timeout(self, _ms):
        return None


class _Page:
    def __init__(self, children):
        self.main_frame = object()
        self.frames = [self.main_frame, *children]


def test_only_visible_same_site_frames_are_read_and_every_frame_is_recorded():
    page = _Page([])
    body = "<html><body><p>Article text.</p></body></html>"
    page.frames += [
        _Frame(f"{SITE}/pages/?id=29", body, page.main_frame),
        _Frame("https://www.youtube.com/embed/x", body, page.main_frame),
        _Frame(f"{SITE}/pages/?id=30", body, page.main_frame, height=0),
        _Frame("about:blank", body, page.main_frame),
    ]
    records, framed = asyncio.run(read_frames(page, f"{SITE}/terms-and-policies"))
    assert [r["outcome"] for r in records] == ["read", "not read: another site", "not read: not visible"]
    assert records[0]["title"] == "Terms & Policies" and records[0]["chars"] == len("Article text.")
    assert len(framed) == 1 and framed[0]["main_text"] == "Article text."


def test_frames_are_capped():
    page = _Page([])
    body = "<html><body><p>x</p></body></html>"
    page.frames += [_Frame(f"{SITE}/pages/?id={i}", body, page.main_frame) for i in range(MAX_FRAMES + 2)]
    records, framed = asyncio.run(read_frames(page, f"{SITE}/home"))
    assert len(framed) == MAX_FRAMES
    assert records[-1]["outcome"] == f"not read: more than {MAX_FRAMES} frames"


def test_a_policy_inside_a_frame_settles_5b():
    """The Scholarly Commons shape: the AUP is linked from the contact form, inside its frame."""
    ev = PageEvidence(node_id="sc", node_name="SC", requested_url=f"{SITE}/home",
                      final_url=f"{SITE}/home", http_status=200,
                      main_text="About Services Terms & Policies " * 20,
                      links=[Link(href=f"{SITE}/contact", text="Contact the Node team"),
                             Link(href=f"{SITE}/terms-and-policies", text="Terms & Policies")])
    ev.full_text = ev.main_text
    policy = ("Acceptable Use Policy and Conditions of Use. Version 1.0. This Acceptable Use Policy "
              "sets the rules and conditions for your access to and use of the Services. "
              "By accessing or using the Services, you accept this AUP. ") * 4
    contact = ChildPage(url=f"{SITE}/contact", selected_for=["6"], http_status=200,
                        final_url=f"{SITE}/contact", main_text="Contact the Node team Name Email",
                        links=[Link(href=f"{SITE}/terms-and-policies", text="Acceptable Use Policy")])
    terms = ChildPage(url=f"{SITE}/terms-and-policies", selected_for=["5p"], http_status=200,
                      final_url=f"{SITE}/terms-and-policies", main_text=policy, full_text=policy,
                      title="Terms & Policies")
    ev.children = [contact, terms]
    assert checks.check_5b(ev).verdict == checks.PASS
    # Before the repair the frame was not read, and the same pages do not pass.
    contact.links, terms.main_text, terms.full_text = [], ev.main_text, ev.main_text
    assert checks.check_5b(ev).verdict != checks.PASS


# Opens a real browser, so it is skipped by default.
# Run with BASIC_CHECK_BROWSER_TESTS=1 (and Chromium installed) to include it.

SHELL = """<!doctype html><html lang="en"><head><title>Terms | Node</title></head><body>
<nav><a href="/about">About</a></nav>
<iframe title="Terms" src="/pages/?id=29" style="width:800px;height:600px"></iframe>
<iframe src="https://video.example/embed" style="width:300px;height:200px"></iframe>
</body></html>"""
ARTICLE = """<!doctype html><html><body><h2>User Access Policy</h2>
<p>Resources are offered under wide access.</p></body></html>"""


@pytest.mark.skipif(
    os.environ.get("BASIC_CHECK_BROWSER_TESTS") != "1",
    reason="opens a browser; set BASIC_CHECK_BROWSER_TESTS=1 to run it",
)
def test_reading_a_same_site_frame_in_a_browser():
    pw = pytest.importorskip("playwright.async_api")

    async def run():
        async with pw.async_playwright() as p:
            try:
                browser = await p.chromium.launch()
            except Exception as exc:  # no browser binary on this machine
                pytest.skip(f"Chromium not available: {exc}")
            page = await browser.new_page()

            async def serve(route):
                url = route.request.url
                body = ARTICLE if "/pages/" in url else SHELL if "sc.example" in url else "<p>video</p>"
                await route.fulfill(status=200, content_type="text/html", body=body)

            await page.route("**/*", serve)
            await page.goto(f"{SITE}/terms-and-policies")
            await page.wait_for_timeout(500)
            result = await read_frames(page, f"{SITE}/terms-and-policies")
            await browser.close()
            return result

    records, framed = asyncio.run(run())
    assert [r["outcome"] for r in records] == ["read", "not read: another site"]
    assert records[0]["title"] == "Terms"
    assert "Resources are offered under wide access." in framed[0]["main_text"]
