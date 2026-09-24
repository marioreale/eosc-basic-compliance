"""Polite, rendered fetches: the landing page, plus at most one level below it.

Deliberate constraints:

* Depth is capped at 1 and breadth is capped hard. A landing page here carries
  84-167 links, so "follow one level" taken literally would mean ~1000 requests
  across every node. Instead only links that can actually settle a checklist
  point are followed -- an Acceptable Use Policy, a contact page -- up to
  MAX_CHILDREN per node. Everything else is recorded as seen-but-not-followed,
  so the report can distinguish "checked and absent" from "never looked".
* robots.txt is consulted for every host before any request to it, not just for
  the landing page.
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
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from selectolax.parser import HTMLParser

from .patterns import CRAWL_PURPOSES, link_haystack

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

# Child pages are read for their text and their policy links, not judged on
# visual presentation, so they get a lighter load than the landing page: no
# networkidle wait and no screenshot. This keeps a federation-wide run to minutes.
CHILD_NAV_TIMEOUT_MS = 25_000
CHILD_SETTLE_MS = 600
MAX_CHILDREN = 8
MAX_PER_PURPOSE = 2
CHILD_DELAY_S = 1.2

# Depth 2 exists for one shape of page: a policies index that links on to the
# actual policy. It is deliberately meaner than depth 1 -- one link per purpose
# per child, and a run-wide ceiling -- because a second hop multiplies rather
# than adds. Nine nodes at depth 1 is ~22 child requests; the same fan-out
# unbounded at depth 2 would be several hundred against other people's
# production servers, which is a crawl, not a check.
MAX_GRANDCHILDREN_PER_CHILD = 2
MAX_PER_PURPOSE_D2 = 1
DEFAULT_FETCH_BUDGET = 60
GRANDCHILD_DELAY_S = 1.5

# Which links are worth following is defined in patterns.py, shared with the
# checks so the two cannot disagree about what a policy link looks like.


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
class ChildPage:
    """A page one level below the landing page, fetched because it may settle a point."""

    url: str
    selected_for: list[str] = field(default_factory=list)
    link_text: str = ""
    depth: int = 1
    parent_url: str = ""
    http_status: int | None = None
    final_url: str = ""
    title: str = ""
    lang_attr: str = ""
    main_text: str = ""
    full_text: str = ""
    links: list[Link] = field(default_factory=list)
    robots_allowed: bool | None = None
    error: str = ""

    @property
    def ok(self) -> bool:
        return not self.error and self.http_status is not None and 200 <= self.http_status < 300


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
    crawl_depth: int = 0
    children: list[ChildPage] = field(default_factory=list)
    # Links that matched a purpose but were not fetched because a cap was hit.
    # Without this a reader cannot tell a checked absence from an unchecked one.
    children_skipped: list[str] = field(default_factory=list)
    crawl_note: str = ""

    def to_json(self) -> dict:
        return asdict(self)

    def children_for(self, point_id: str) -> list[ChildPage]:
        return [c for c in self.children if point_id in c.selected_for]


_ROBOTS_CACHE: dict[str, robotparser.RobotFileParser | None] = {}


def _robots_ok(url: str) -> bool:
    """robots.txt check for a child URL, one fetch per host per run.

    Following links means touching hosts the landing page never named, so each
    host is asked for permission rather than inheriting the landing page's.
    """
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    if base not in _ROBOTS_CACHE:
        try:
            resp = httpx.get(
                base + "/robots.txt", timeout=10, follow_redirects=True,
                headers={"User-Agent": UA},
            )
            if resp.status_code == 200:
                rp = robotparser.RobotFileParser()
                rp.parse(resp.text.splitlines())
                _ROBOTS_CACHE[base] = rp
            else:
                _ROBOTS_CACHE[base] = None
        except Exception:
            _ROBOTS_CACHE[base] = None
    rp = _ROBOTS_CACHE[base]
    if rp is None:
        return True
    try:
        return rp.can_fetch(UA, url)
    except Exception:
        return True


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


BINARY_SUFFIXES = (
    ".pdf", ".zip", ".tar", ".gz", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".mp3", ".ics", ".rss", ".xml",
)


class FetchBudget:
    """A hard ceiling on requests made below the landing pages, for a whole run.

    Per-node caps bound each page's fan-out but not the product of them, and it
    is the product that lands on someone else's server. This is one counter
    shared across every node so the total is knowable before the run starts, not
    discovered afterwards from their access logs.

    `take()` is the only way to spend, and it returns False rather than raising
    so a caller stops collecting instead of losing the evidence gathered so far.
    """

    def __init__(self, total: int = DEFAULT_FETCH_BUDGET) -> None:
        self.total = max(0, int(total))
        self.spent = 0
        self.refused = 0

    def take(self) -> bool:
        if self.spent >= self.total:
            self.refused += 1
            return False
        self.spent += 1
        return True

    @property
    def exhausted(self) -> bool:
        return self.spent >= self.total

    @property
    def note(self) -> str:
        if not self.refused:
            return f"fetch budget: {self.spent} of {self.total} used"
        return (
            f"fetch budget exhausted: {self.spent} of {self.total} used, "
            f"{self.refused} further page(s) not fetched"
        )


def select_grandchildren(
    child: ChildPage,
    budget: FetchBudget,
    seen: set[str] | None = None,
    node_host: str = "",
) -> tuple[list[ChildPage], list[str]]:
    """Choose links on an already-fetched child worth one more hop.

    Same relevance rule as depth 1, three extra restraints: one link per purpose
    instead of two, a small per-child cap, and the shared run budget. `seen`
    carries every URL already fetched for this node so a policies page that
    links back to the landing page, or to a sibling already queued, costs
    nothing.

    Host containment is measured against `node_host` -- the *landing page's*
    host -- not the child's. Measuring against the child would let each hop
    redefine "same site" and walk the crawl off the node.
    """
    seen = seen or set()
    base_host = (node_host or urlparse(child.final_url or child.url).netloc).lower()
    chosen: dict[str, ChildPage] = {}
    skipped: list[str] = []
    per_purpose: dict[str, int] = {}

    for point_id, patterns in CRAWL_PURPOSES:
        for link in child.links:
            href = link.href
            parsed = urlparse(href)
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.path.lower().endswith(BINARY_SUFFIXES):
                continue
            host = parsed.netloc.lower()
            if not (host == base_host or _related_host(host, base_host)):
                continue
            haystack = link_haystack(link.text, parsed.path)
            if not _match_any(haystack, patterns):
                continue
            key = href.split("#")[0].rstrip("/")
            if key in seen or key in chosen:
                if key in seen:
                    skipped.append(f"{href} (already fetched at depth 1)")
                continue
            if per_purpose.get(point_id, 0) >= MAX_PER_PURPOSE_D2:
                skipped.append(f"{href} (depth 2 cap for point {point_id})")
                continue
            if len(chosen) >= MAX_GRANDCHILDREN_PER_CHILD:
                skipped.append(f"{href} (depth 2 per-page cap)")
                continue
            if not budget.take():
                skipped.append(f"{href} (run fetch budget exhausted)")
                return list(chosen.values()), skipped
            per_purpose[point_id] = per_purpose.get(point_id, 0) + 1
            chosen[key] = ChildPage(
                url=href,
                selected_for=[point_id],
                link_text=link.text,
                depth=2,
                parent_url=child.final_url or child.url,
            )

    return list(chosen.values()), skipped


def select_children(
    ev: PageEvidence, max_children: int = MAX_CHILDREN
) -> tuple[list[ChildPage], list[str]]:
    """Choose which links to follow one level down, and record what was dropped.

    A landing page here has 84-167 links. Following all of them would be a
    hundredfold increase in load on someone else's server for no gain, so a link
    is followed only when its text or URL suggests it can settle a specific
    checklist point.

    Returns (selected, skipped). `skipped` exists so a later "not found" verdict
    can say whether the tool actually looked. Reporting absence without knowing
    that is how a checker ends up accusing a node of the tool's own blind spot.
    """
    page_host = urlparse(ev.final_url or ev.requested_url).netloc.lower()
    chosen: dict[str, ChildPage] = {}
    skipped: list[str] = []
    per_purpose: dict[str, int] = {}

    for point_id, patterns in CRAWL_PURPOSES:
        for link in ev.links:
            href = link.href
            parsed = urlparse(href)
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.path.lower().endswith(BINARY_SUFFIXES):
                # A PDF policy is a real finding, but the browser cannot render it
                # to text here. Point 5 already treats a pointer as evidence.
                continue
            # Stay on the node's own site or an obvious subdomain of it. Following
            # a link to twitter.com or a funder's site cannot settle a point about
            # the node and would spread load onto unrelated third parties.
            host = parsed.netloc.lower()
            same_site = host == page_host or _related_host(host, page_host)
            if not same_site:
                continue
            haystack = link_haystack(link.text, parsed.path)
            if not _match_any(haystack, patterns):
                continue
            key = href.split("#")[0].rstrip("/")
            if key == (ev.final_url or ev.requested_url).split("#")[0].rstrip("/"):
                continue
            if key in chosen:
                if point_id not in chosen[key].selected_for:
                    chosen[key].selected_for.append(point_id)
                continue
            if per_purpose.get(point_id, 0) >= MAX_PER_PURPOSE:
                skipped.append(f"{href} (cap for point {point_id})")
                continue
            if len(chosen) >= max_children:
                skipped.append(f"{href} (per-node cap of {max_children})")
                continue
            per_purpose[point_id] = per_purpose.get(point_id, 0) + 1
            chosen[key] = ChildPage(url=href, selected_for=[point_id], link_text=link.text)

    return list(chosen.values()), skipped


def _related_host(host: str, page_host: str) -> bool:
    """True when two hosts share a registrable-looking base, e.g. www.x.eu and docs.x.eu."""

    def base(h: str) -> str:
        parts = [x for x in h.split(".") if x]
        if len(parts) > 2 and len(parts[-2]) <= 3:
            return ".".join(parts[-3:])
        return ".".join(parts[-2:])

    return bool(host) and bool(page_host) and base(host) == base(page_host)


def _match_any(text: str, patterns: list[str]) -> bool:
    import re

    return any(re.search(pat, text) for pat in patterns)


async def _fetch_child(context, child: ChildPage) -> ChildPage:
    """Fetch one child page. Lighter than the landing page: text and links only."""
    if not _robots_ok(child.url):
        child.robots_allowed = False
        child.error = "not fetched: robots.txt disallows it"
        return child
    child.robots_allowed = True
    page = await context.new_page()
    try:
        resp = await page.goto(
            child.url, wait_until="domcontentloaded", timeout=CHILD_NAV_TIMEOUT_MS
        )
        await page.wait_for_timeout(CHILD_SETTLE_MS)
        child.http_status = resp.status if resp else None
        child.final_url = page.url
        parsed = _extract(await page.content(), child.final_url or child.url)
        child.title = parsed["title"]
        child.lang_attr = parsed["lang_attr"]
        # Child text is capped: it is read for keywords and policy pointers, and
        # every node's full page text would bloat the committed evidence files.
        child.main_text = parsed["main_text"][:20_000]
        child.full_text = parsed["full_text"][:20_000]
        child.links = parsed["links"][:150]
    except Exception as exc:
        child.error = f"{type(exc).__name__}: {exc}"
    finally:
        with contextlib.suppress(Exception):
            await page.close()
    return child


async def _fetch_one(
    browser,
    node: dict,
    shots: Path,
    depth: int = 0,
    max_children: int = MAX_CHILDREN,
    budget: FetchBudget | None = None,
) -> PageEvidence:
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

        if depth >= 1:
            ev.crawl_depth = 1
            selected, skipped = select_children(ev, max_children)
            ev.children_skipped = skipped[:50]
            node_host = urlparse(ev.final_url or node["url"]).netloc.lower()
            # Every URL fetched for this node, so a second hop never pays twice
            # for a page already on disk.
            seen = {(ev.final_url or node["url"]).split("#")[0].rstrip("/")}
            seen |= {c.url.split("#")[0].rstrip("/") for c in selected}
            for i, child in enumerate(selected):
                await _fetch_child(context, child)
                ev.children.append(child)
                if i < len(selected) - 1:
                    await asyncio.sleep(CHILD_DELAY_S)

            grandchildren: list[ChildPage] = []
            if depth >= 2 and budget is not None:
                ev.crawl_depth = 2
                for child in selected:
                    if not child.ok:
                        # A child that did not render has no trustworthy links;
                        # following them would spend budget on guesswork.
                        continue
                    picked, gskipped = select_grandchildren(
                        child, budget, seen=seen, node_host=node_host
                    )
                    ev.children_skipped.extend(gskipped[:10])
                    for g in picked:
                        seen.add(g.url.split("#")[0].rstrip("/"))
                        await _fetch_child(context, g)
                        ev.children.append(g)
                        grandchildren.append(g)
                        await asyncio.sleep(GRANDCHILD_DELAY_S)
                    if budget.exhausted:
                        break

            ev.crawl_note = (
                f"depth {ev.crawl_depth}: {len(ev.links)} link(s) on the landing page, "
                f"{len(selected)} followed because they matched a checklist point, "
                f"{len(skipped)} matched but dropped by a cap, "
                f"the rest not relevant to any point"
            )
            if depth >= 2:
                ev.crawl_note += (
                    f"; depth 2 added {len(grandchildren)} page(s)"
                    + (f"; {budget.note}" if budget is not None else "")
                )
            ev.children_skipped = ev.children_skipped[:60]
        else:
            ev.crawl_note = "depth 0: the landing page only, no links followed"
    except Exception as exc:
        ev.error = f"{type(exc).__name__}: {exc}"
    finally:
        await context.close()
    return ev


def without_depth_2(ev: PageEvidence) -> PageEvidence:
    """A shallow copy of `ev` as if the run had stopped at depth 1.

    Used to show, from a single capture, what the second hop actually bought.
    Re-fetching at depth 1 for the comparison would double the load on the nodes
    and let the page change between the two runs, so the same evidence is read
    through two lenses instead. The original is left untouched -- the deep view
    is rendered from it immediately afterwards.
    """
    shallow = replace(
        ev,
        children=[c for c in ev.children if c.depth <= 1],
        crawl_depth=min(ev.crawl_depth, 1),
    )
    return shallow


async def collect_all(
    nodes: list[dict],
    out_dir: Path,
    delay_s: float = 2.0,
    depth: int = 0,
    max_children: int = MAX_CHILDREN,
    fetch_budget: int = DEFAULT_FETCH_BUDGET,
) -> list[PageEvidence]:
    """Fetch every landing page, sequentially, with a gap between hosts.

    At depth 1 a bounded set of child pages is fetched too -- see select_children
    for how few, and why.

    At depth 2 one `FetchBudget` is shared by every node, so the ceiling is on
    the run and not on each page. Earlier nodes can therefore consume budget that
    later ones then do not get: that is deliberate, and the note in each
    evidence file records what was left, so a thin result is visible as a budget
    effect rather than mistaken for a node with nothing to find.
    """
    from playwright.async_api import async_playwright

    out_dir.mkdir(parents=True, exist_ok=True)
    shots = out_dir / "screenshots"
    shots.mkdir(exist_ok=True)
    results: list[PageEvidence] = []
    budget = FetchBudget(fetch_budget) if depth >= 2 else None
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--disable-dev-shm-usage"])
        try:
            for i, node in enumerate(nodes):
                ev = await _fetch_one(browser, node, shots, depth, max_children, budget)
                results.append(ev)
                (out_dir / f"{node['id']}.json").write_text(
                    json.dumps(ev.to_json(), indent=2, ensure_ascii=False)
                )
                status = ev.error or f"HTTP {ev.http_status}"
                extra = ""
                if depth >= 1:
                    ok = sum(1 for c in ev.children if c.ok)
                    extra = f"  +{ok}/{len(ev.children)} child page(s)"
                    if depth >= 2:
                        g = sum(1 for c in ev.children if c.depth == 2)
                        extra += f" ({g} at depth 2)"
                print(f"  [{i + 1}/{len(nodes)}] {node['id']:12} {status}{extra}")
                if i < len(nodes) - 1:
                    await asyncio.sleep(delay_s)
        finally:
            await browser.close()
    if budget is not None:
        print(f"\n  {budget.note}")
    return results


def load_evidence(out_dir: Path, node_id: str) -> PageEvidence:
    data = json.loads((out_dir / f"{node_id}.json").read_text())
    data["links"] = [Link(**x) for x in data.get("links", [])]
    data["images"] = [Image(**x) for x in data.get("images", [])]
    data["controls"] = [Control(**x) for x in data.get("controls", [])]
    children = []
    for raw in data.get("children", []):
        raw = dict(raw)
        raw["links"] = [Link(**x) for x in raw.get("links", [])]
        children.append(ChildPage(**raw))
    data["children"] = children
    return PageEvidence(**data)
