"""One polite, rendered fetch per node landing page. No crawling.

Deliberate constraints:

* Exactly one page request per node, plus one robots.txt. Nothing else is
  touched. These are other institutions' servers and the checklist only asks
  about the landing page itself.
* The page is rendered in a real browser rather than fetched as HTML. Several of
  these landing pages are client-side rendered, and a plain HTTP fetch would see
  an empty shell and report a node non-compliant for having no content. That
  would be a false accusation caused by the tool, not a finding about the node.
* Evidence is written to disk and the checks read only that. So a verdict can be
  re-derived, argued with, and re-run after the checklist is reinterpreted,
  without going back to the node's server.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import urllib.robotparser as robotparser
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from selectolax.parser import HTMLParser

UA = (
    "eosc-basic-compliance/0.1 (EOSC Node Landing Page checklist v3.0 verification; "
    "+https://github.com/marioreale/eosc-basic-compliance)"
)
NAV_TIMEOUT_MS = 45_000
# Institutional sites carry consent banners and analytics that never let the
# network settle, so networkidle is given a short bounded chance and then we take
# whatever has rendered. The checklist asks about markup, which is already there.
NETWORKIDLE_MS = 2_500
SETTLE_MS = 1_200


@dataclass
class Link:
    href: str
    text: str
    visible: bool = True


@dataclass
class Image:
    src: str
    alt: str = ""
    aria_label: str = ""
    title: str = ""
    css_class: str = ""
    inline_svg: bool = False


@dataclass
class Control:
    """A clickable thing: button, link styled as a button, input submit."""

    text: str
    href: str = ""
    tag: str = ""
    visible: bool = True


@dataclass
class PageEvidence:
    node_id: str
    node_name: str
    requested_url: str
    fetched_at: str = ""
    final_url: str = ""
    http_status: int | None = None
    redirect_chain: list[str] = field(default_factory=list)
    robots_allowed: bool | None = None
    robots_note: str = ""
    title: str = ""
    lang_attr: str = ""
    main_text: str = ""
    full_text: str = ""
    links: list[Link] = field(default_factory=list)
    images: list[Image] = field(default_factory=list)
    controls: list[Control] = field(default_factory=list)
    meta_description: str = ""
    error: str = ""
    screenshot: str = ""

    def to_json(self) -> dict:
        return asdict(self)


def _robots(url: str) -> tuple[bool, str]:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    try:
        resp = httpx.get(
            base + "/robots.txt", timeout=15, follow_redirects=True, headers={"User-Agent": UA}
        )
    except Exception as exc:  # network failure is not permission to proceed blindly
        return True, f"robots.txt unreachable ({type(exc).__name__}); proceeding with one request"
    if resp.status_code != 200:
        return True, f"no robots.txt (HTTP {resp.status_code}); nothing disallowed"
    parser = robotparser.RobotFileParser()
    parser.parse(resp.text.splitlines())
    allowed = parser.can_fetch(UA, url)
    return allowed, "robots.txt consulted" if allowed else "robots.txt disallows this URL"


def _extract(html: str, base_url: str) -> dict:
    tree = HTMLParser(html)
    for tag in ("script", "style", "noscript", "template"):
        for node in tree.css(tag):
            node.decompose()

    body = tree.css_first("body")
    full_text = " ".join((body.text(separator=" ") if body else "").split())

    # Main text excludes chrome so language detection is not swayed by a
    # cookie banner or a language switcher.
    main_node = (
        tree.css_first("main")
        or tree.css_first("[role=main]")
        or tree.css_first("article")
        or tree.css_first("#content")
        or tree.css_first(".content")
        or body
    )
    main_text = " ".join((main_node.text(separator=" ") if main_node else "").split())

    links: list[Link] = []
    for a in tree.css("a[href]"):
        href = (a.attributes.get("href") or "").strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        text = " ".join(a.text(separator=" ").split())
        if not text:
            # A wrapping link often carries its label on a nested image.
            img = a.css_first("img")
            if img:
                text = (img.attributes.get("alt") or "").strip()
        links.append(Link(href=urljoin(base_url, href), text=text[:300]))

    images: list[Image] = []
    for img in tree.css("img"):
        images.append(
            Image(
                src=urljoin(base_url, (img.attributes.get("src") or "").strip()),
                alt=(img.attributes.get("alt") or "").strip()[:300],
                aria_label=(img.attributes.get("aria-label") or "").strip()[:300],
                title=(img.attributes.get("title") or "").strip()[:300],
                css_class=(img.attributes.get("class") or "").strip()[:300],
            )
        )
    for svg in tree.css("svg"):
        label = " ".join(svg.text(separator=" ").split())
        images.append(
            Image(
                src="",
                alt=label[:300],
                aria_label=(svg.attributes.get("aria-label") or "").strip()[:300],
                title=(svg.attributes.get("title") or "").strip()[:300],
                css_class=(svg.attributes.get("class") or "").strip()[:300],
                inline_svg=True,
            )
        )

    controls: list[Control] = []
    for sel in ("button", "a[href]", "input[type=submit]", "[role=button]"):
        for node in tree.css(sel):
            text = " ".join(node.text(separator=" ").split())
            aria = (node.attributes.get("aria-label") or "").strip()
            value = (node.attributes.get("value") or "").strip()
            label = text or aria or value
            if not label:
                continue
            controls.append(
                Control(
                    text=label[:300],
                    href=urljoin(base_url, (node.attributes.get("href") or "").strip()),
                    tag=node.tag,
                )
            )

    meta = ""
    for node in tree.css("meta"):
        if (node.attributes.get("name") or "").lower() == "description":
            meta = (node.attributes.get("content") or "").strip()
            break

    html_node = tree.css_first("html")
    title_node = tree.css_first("title")
    return {
        "title": " ".join((title_node.text() if title_node else "").split())[:300],
        "lang_attr": (html_node.attributes.get("lang") or "").strip() if html_node else "",
        "main_text": main_text,
        "full_text": full_text,
        "links": links,
        "images": images,
        "controls": controls,
        "meta_description": meta[:500],
    }


async def _fetch_one(browser, node: dict, shots: Path) -> PageEvidence:
    ev = PageEvidence(
        node_id=node["id"],
        node_name=node["name"],
        requested_url=node["url"],
        fetched_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )
    allowed, note = _robots(node["url"])
    ev.robots_allowed, ev.robots_note = allowed, note
    if not allowed:
        ev.error = "not fetched: robots.txt disallows it"
        return ev

    context = await browser.new_context(
        user_agent=UA,
        viewport={"width": 1440, "height": 1000},
        locale="en-GB",
        # Ask for English. The checklist's point 7 is about what the page serves
        # an EOSC user, and content negotiation is part of that.
        extra_http_headers={"Accept-Language": "en-GB,en;q=0.9"},
    )
    page = await context.new_page()
    redirects: list[str] = []
    page.on("response", lambda r: redirects.append(r.url) if 300 <= r.status < 400 else None)
    try:
        resp = await page.goto(node["url"], wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        with contextlib.suppress(Exception):
            await page.wait_for_load_state("networkidle", timeout=NETWORKIDLE_MS)
        await page.wait_for_timeout(SETTLE_MS)
        ev.http_status = resp.status if resp else None
        ev.final_url = page.url
        ev.redirect_chain = redirects[:10]
        html = await page.content()
        parsed = _extract(html, ev.final_url or node["url"])
        for key, value in parsed.items():
            setattr(ev, key, value)
        shot = shots / f"{node['id']}.png"
        with contextlib.suppress(Exception):
            await page.screenshot(path=str(shot), full_page=False)
            ev.screenshot = shot.name
    except Exception as exc:
        ev.error = f"{type(exc).__name__}: {exc}"
    finally:
        await context.close()
    return ev


async def collect_all(nodes: list[dict], out_dir: Path, delay_s: float = 2.0) -> list[PageEvidence]:
    """Fetch every landing page once, sequentially, with a gap between hosts."""
    from playwright.async_api import async_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    shots = out_dir / "screenshots"
    shots.mkdir(exist_ok=True)
    results: list[PageEvidence] = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--disable-dev-shm-usage"])
        try:
            for i, node in enumerate(nodes):
                ev = await _fetch_one(browser, node, shots)
                results.append(ev)
                (out_dir / f"{node['id']}.json").write_text(
                    json.dumps(ev.to_json(), indent=2, ensure_ascii=False)
                )
                status = ev.error or f"HTTP {ev.http_status}"
                print(f"  [{i + 1}/{len(nodes)}] {node['id']:12} {status}")
                if i < len(nodes) - 1:
                    await asyncio.sleep(delay_s)
        finally:
            await browser.close()
    return results


def load_evidence(out_dir: Path, node_id: str) -> PageEvidence:
    data = json.loads((out_dir / f"{node_id}.json").read_text())
    data["links"] = [Link(**x) for x in data.get("links", [])]
    data["images"] = [Image(**x) for x in data.get("images", [])]
    data["controls"] = [Control(**x) for x in data.get("controls", [])]
    return PageEvidence(**data)
