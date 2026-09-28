"""One check function per checklist point. Exactly one result each.

Verdict vocabulary, and why it is not just pass/fail:

    PASS           the point is satisfied, and a script can show why
    FAIL           the point is violated, and a script can show why
    MANUAL_REVIEW  a human must decide; evidence is attached to make that quick
    ERROR          the tool could not assess (page unreachable, etc.)

MANUAL_REVIEW is the important one. Several checklist points turn on words like
"clearly state" or quantify over "all Node Exchange research resources offered by
the Node" —
neither is settleable by inspecting one page. Emitting PASS or FAIL on those
would be a guess dressed as a verdict, and a wrong FAIL against a node is
expensive to retract. Where the tool cannot know, it says so and hands over the
evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from .fetch import BINARY_SUFFIXES, Image, PageEvidence, _related_host
from .names import ApprovedNames
from .patterns import (
    AAI_HINTS,
    AUP_PATTERNS,
    CONTACT_PATTERNS,
    HELPDESK_ON_PAGE,
    HELPDESK_STRONG,
    LICENCE_PATTERNS,
    LOGIN_PATTERNS,
    POLICY_INDEX_PATTERNS,
    SERVICE_INDEX_PATTERNS,
    UAP_PATTERNS,
    is_helpdesk_address,
    is_helpdesk_host,
    link_haystack,
)

PASS = "PASS"
FAIL = "FAIL"
MANUAL_REVIEW = "MANUAL_REVIEW"
ERROR = "ERROR"


@dataclass
class Result:
    point_id: str
    title: str
    verdict: str
    message: str
    evidence: list[str] = field(default_factory=list)
    # What a reviewer should do next when the tool cannot decide.
    reviewer_action: str = ""


# --- shared vocabulary -------------------------------------------------------

# Defined in patterns.py, which the crawler also reads. See that module for why
# these must not be duplicated here.


def _match(text: str, patterns: list[str]) -> list[str]:
    hits = []
    for pattern in patterns:
        found = re.search(pattern, text)
        if found:
            hits.append(found.group(0))
    return hits


def _link_hits(ev: PageEvidence, patterns: list[str]) -> list:
    out = []
    for link in ev.links:
        haystack = link_haystack(link.text, link.href)
        if any(re.search(p, haystack) for p in patterns):
            out.append(link)
    return out


def _fmt(link) -> str:
    label = link.text.strip() or "(no label)"
    return f'"{label}" -> {link.href}'


CONSENT_MARKERS = [
    r"(?i)we value your privacy",
    r"(?i)this website uses cookies",
    r"(?i)cookie\s+(consent|preferences|settings)",
    r"(?i)accept\s+all\b",
    r"(?i)reject\s+all\b",
    r"(?i)manage\s+(your\s+)?(cookies|preferences)",
]


def render_warning(ev: PageEvidence) -> str:
    """Return a reason to distrust absence on this page, or "".

    A consent overlay can hold back the real document, and a client-side app can
    serve a shell. In both cases the tool sees a page that is technically HTTP
    200 but substantially unrendered -- and "I found no contact link" then says
    more about the tool than about the node.

    Concluding absence from incomplete collection is the single most damaging
    mistake this kind of checker can make, because the output is an accusation
    against a named organisation. So absence-based FAILs are gated on this.
    """
    reasons = []
    consent = _match(ev.full_text, CONSENT_MARKERS)
    if consent and len(ev.main_text) < 1200:
        reasons.append(
            f"a cookie-consent overlay dominates the captured text "
            f"(main text only {len(ev.main_text)} chars; markers: {', '.join(sorted(set(consent))[:3])})"
        )
    if len(ev.links) < 25:
        reasons.append(f"only {len(ev.links)} links captured, low for a landing page")
    if len(ev.main_text) < 600:
        reasons.append(f"only {len(ev.main_text)} characters of main text captured")
    return "; ".join(reasons)


# A landing page that rendered at all yields anchors, images and buttons. When
# almost none of that survives, collection -- not the node -- is the problem.
DOM_ELEMENT_FLOOR = 10
EMPTY_DOCUMENT_CHARS = 500


def link_collection_warning(ev: PageEvidence) -> str:
    """Return a reason to distrust the *absence of a link*, or "".

    This is deliberately not `render_warning`. That function asks "did the page
    render enough to read?", which is the right question for a text judgement and
    the wrong one for a link. A consent overlay suppresses visible text while
    leaving every anchor in the DOM, so gating a link-absence FAIL on a text
    length let a verified absence escape as "cannot conclude".

    Observed on EOSC DTO: 530 chars of main text behind a cookie banner, but 20
    anchors -- exactly the 20 in the server's HTML, and 21 in the rendered DOM
    both before and after accepting consent. The absence of an eosc.eu link there
    is a fact about the node, not an artefact of collection.

    So the question here is only whether the DOM arrived. Text length is not
    evidence about that; a small page is not a truncated one.
    """
    if not ev.links:
        return "no links were captured at all, so the page yielded no link evidence"
    structure = len(ev.links) + len(ev.images) + len(ev.controls)
    if structure < DOM_ELEMENT_FLOOR:
        return (
            f"only {structure} DOM element(s) captured "
            f"({len(ev.links)} link(s), {len(ev.images)} image(s), {len(ev.controls)} control(s)) "
            "— too little structure to treat the document as delivered"
        )
    if len(ev.full_text) < EMPTY_DOCUMENT_CHARS:
        return f"the document is essentially empty ({len(ev.full_text)} chars of text in total)"
    return ""


def _render_note(ev: PageEvidence) -> list[str]:
    """Disclose page-quality caveats alongside a FAIL.

    The gate no longer suppresses the verdict, but the reviewer should still be
    told a consent banner was in the way, so the finding can be spot-checked.
    """
    note = render_warning(ev)
    return [f"note: {note} — the DOM was nonetheless complete, so absence stands"] if note else []


def _is_host(netloc: str, domain: str) -> bool:
    """Exact host match or a true subdomain of it.

    A naive `netloc.endswith("eosc.eu")` also matches `myeosc.eu` and
    `not-eosc.eu`, which would let an unrelated domain satisfy a requirement
    about eosc.eu. Caught by probing the check with lookalike hosts.
    """
    host = netloc.lower().split(":")[0].rstrip(".")
    domain = domain.lower()
    return host == domain or host.endswith("." + domain)


# --- point 1 -----------------------------------------------------------------


def check_1(ev: PageEvidence) -> Result:
    """Anonymously accessible, or reachable via EOSC AAI login."""
    if ev.error:
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            ERROR,
            f"The page could not be fetched: {ev.error}",
            reviewer_action="Retry; if it persists, check the URL registered in the Contributors Dashboard.",
        )

    status = ev.http_status
    if status is not None and 200 <= status < 300 and len(ev.full_text) > 200:
        ev_list = [f"HTTP {status} anonymously, {len(ev.full_text)} characters of text rendered"]
        if ev.redirect_chain:
            ev_list.append(f"redirects followed: {len(ev.redirect_chain)}")
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            PASS,
            "Served content to an anonymous request, satisfying branch (a).",
            ev_list,
        )

    if status in (401, 403):
        logins = _match(ev.full_text, LOGIN_PATTERNS) + _match(ev.final_url, AAI_HINTS)
        if logins:
            return Result(
                "1",
                "NLP publicly accessible or via EOSC AAI",
                MANUAL_REVIEW,
                f"HTTP {status} anonymously, and a login affordance is present. "
                "Branch (b) may apply, but whether that login is EOSC AAI cannot be "
                "confirmed from the page.",
                [f"HTTP {status}", f"login indicators: {', '.join(logins[:4])}"],
                reviewer_action=
                "Confirm that the node's login is EOSC AAI compliant, as verified under requirement [P.2] of the Production 1.0 Checklist.",
            )
        # A 403 with no login in sight is weak evidence about public accessibility.
        # Genuine access control almost always redirects to a login page; a bare
        # 403 to an automated client is far more often bot mitigation, which says
        # nothing about what a researcher with a browser would see. This was not
        # hypothetical: a node here served HTTP 200 to this tool and then 403 once
        # the crawl made a handful more requests. Reporting that as "not publicly
        # accessible" would have been the tool blaming a node for its own
        # rate-limiting, so it is a review item, never a FAIL.
        wall = _match(ev.full_text + " " + ev.title, BOT_WALL_PATTERNS)
        detail = (
            f"bot-protection wording seen: {', '.join(sorted(set(wall))[:4])}"
            if wall
            else "no login affordance and no explicit bot-protection wording"
        )
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            MANUAL_REVIEW,
            f"HTTP {status} to this tool's anonymous request, with no login affordance found. "
            "This is most likely bot protection reacting to an automated client rather than an "
            "access policy, so it is not treated as a failure: a browser may well be served "
            "normally. It could not be verified either way.",
            [f"HTTP {status}", detail, f"final URL: {ev.final_url}"],
            reviewer_action="Open the URL in a normal browser. If it loads, this point passes and "
            "the block was bot protection. If it demands a login, confirm that the login is EOSC "
            "AAI compliant, as verified under requirement [P.2] of the Production 1.0 Checklist.",
        )

    if status in DEAD_STATUSES:
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            FAIL,
            f"The landing page returned HTTP {status}: the registered URL does not resolve to a "
            "page, so it cannot be accessible by either branch.",
            [f"HTTP {status}", f"final URL: {ev.final_url}"],
            reviewer_action="Check the URL registered in the EOSC EU Node Contributors Dashboard.",
        )

    if status is not None and status >= 500:
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            MANUAL_REVIEW,
            f"The landing page returned HTTP {status}, a server-side error. This is often "
            "transient, so it is not recorded as a checklist failure without a retry.",
            [f"HTTP {status}", f"final URL: {ev.final_url}"],
            reviewer_action="Retry later; if it persists, raise it with the node.",
        )

    if status is not None and status >= 400:
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            MANUAL_REVIEW,
            f"The landing page returned HTTP {status} to this tool.",
            [f"HTTP {status}", f"final URL: {ev.final_url}"],
            reviewer_action="Open the URL in a browser to see what a researcher would get.",
        )

    return Result(
        "1",
        "NLP publicly accessible or via EOSC AAI",
        MANUAL_REVIEW,
        f"HTTP {status} but only {len(ev.full_text)} characters rendered. "
        "The page may require JavaScript the tool did not execute, or may be a shell.",
        [f"HTTP {status}", f"text length: {len(ev.full_text)}"],
        reviewer_action="Open the page in a browser and confirm content is served anonymously.",
    )


# --- point 1R ----------------------------------------------------------------


def check_1R(ev: PageEvidence) -> Result:
    """Resources behind the NLP are public or behind EOSC AAI. Not decidable here."""
    if ev.error:
        return Result("1R", "Linked resources public or via EOSC AAI", ERROR, f"Page not fetched: {ev.error}")

    host = urlparse(ev.final_url or ev.requested_url).netloc.lower()
    external = []
    for link in ev.links:
        netloc = urlparse(link.href).netloc.lower()
        if netloc and netloc != host and not _is_host(netloc, "eosc.eu"):
            external.append(link)

    # Deduplicate by host so the reviewer sees distinct destinations.
    by_host: dict[str, list] = {}
    for link in external:
        by_host.setdefault(urlparse(link.href).netloc.lower(), []).append(link)

    aai = _match(ev.full_text, AAI_HINTS) + _match(
        " ".join(link.href for link in ev.links), AAI_HINTS
    )
    lines = [f"{len(by_host)} distinct external host(s) linked from the landing page"]
    for netloc, links in sorted(by_host.items())[:12]:
        labels = ", ".join(sorted({link.text.strip() for link in links if link.text.strip()})[:3])
        lines.append(f"{netloc}{f' ({labels})' if labels else ''}")
    if aai:
        lines.append(f"EOSC AAI indicators seen: {', '.join(sorted(set(aai))[:4])}")

    if ev.crawl_depth >= 1 and ev.children:
        reached = [c for c in ev.children if c.ok]
        blocked = [c for c in ev.children if not c.ok and c.robots_allowed is not False]
        lines.append(
            f"depth 1: {len(reached)} of {len(ev.children)} followed page(s) were served "
            f"anonymously, so those are publicly accessible"
        )
        for child in blocked[:5]:
            detail = child.error or f"HTTP {child.http_status}"
            lines.append(f"not served anonymously: {child.url} -> {detail}")

    return Result(
        "1R",
        "Linked resources public or via EOSC AAI",
        MANUAL_REVIEW,
        "Not assessable in full: it quantifies over every Node Exchange resource reachable "
        "through the landing page, including through intermediate pages, and whether a given "
        "login is genuinely EOSC AAI compliant is settled under requirement [P.2] of the "
        "Production 1.0 Checklist rather than by reading HTML. One level of crawling narrows "
        "this but cannot close it.",
        lines,
        reviewer_action="Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.",
    )


# --- point 2 -----------------------------------------------------------------


def check_2(ev: PageEvidence) -> Result:
    """Scope, intended users, responsible organisation. A judgement, not a match."""
    if ev.error:
        return Result("2", "Scope, users and responsible organisation stated", ERROR, f"Page not fetched: {ev.error}")

    snippet = ev.main_text[:600] or ev.full_text[:600]
    lines = []
    if ev.meta_description:
        lines.append(f'meta description: "{ev.meta_description[:200]}"')
    if snippet:
        lines.append(f'opening main text: "{snippet[:400]}..."')

    # Organisation candidates: legal-entity suffixes are a genuine signal.
    orgs = sorted(
        set(
            re.findall(
                r"\b(?:[A-Z][A-Za-z0-9&.\-]{1,30}\s+){0,4}"
                r"(?:ERIC|e\.V\.|GmbH|Ltd|Foundation|Institute|Institut|University|Universit[eéà]|"
                r"Consortium|Association|Council|Agency|Centre|Center|CNRS|CNR|CSC)\b",
                ev.full_text,
            )
        )
    )
    if orgs:
        lines.append(f"organisation-like names found: {'; '.join(o.strip() for o in orgs[:6])}")
    else:
        lines.append("no organisation-like names matched by pattern")

    about = _verify_child(ev, "2", [])
    if about is not None and about.ok:
        # The checklist asks the landing page to state these things, so an About
        # page cannot satisfy it on the page's behalf. It is offered as context
        # for the reviewer, clearly marked as one level down.
        lines.append(
            f'about page one level down: {about.url} (HTTP {about.http_status}) '
            f'opening text: "{(about.main_text or about.full_text)[:260]}..."'
        )

    return Result(
        "2",
        "Scope, users and responsible organisation stated",
        MANUAL_REVIEW,
        'Requires reading the page: "clearly state" is a judgement about whether the prose '
        "conveys scope, intended users, and the responsible organisation to a researcher. "
        "Evidence is extracted below so the decision is quick.",
        lines,
        reviewer_action="Read the extracted text and confirm all three elements are present and clear.",
    )


# --- point 3 -----------------------------------------------------------------


@dataclass(frozen=True)
class _NameNote:
    """What the name list established, as both a state and an evidence line.

    The state exists so that a summary sentence and the evidence line beside it
    are derived from one decision. They were previously written independently,
    and drifted: the summary said no list of approved names existed while the
    evidence line under it recorded a successful match against one.
    """

    state: str  # absent | unscoped-for-node | no-body | not-found | matched | matched-unscoped
    line: str = ""

    @property
    def supplied(self) -> bool:
        return self.state != "absent"


def _approved_name_note(
    ev: PageEvidence,
    approved_names: ApprovedNames | list[str] | None,
) -> _NameNote:
    """What a supplied list of approved names established for this page.

    `line` is one evidence line, empty when no list was supplied. It states
    which name matched and whether that name was written against this node. An
    unscoped list cannot establish that the name found is this node's own, so
    the line says so rather than implying more.
    """
    names = ApprovedNames.coerce(approved_names)
    if not names.supplied:
        return _NameNote("absent")

    candidates = names.for_node(ev.node_id)
    if not candidates:
        return _NameNote(
            "unscoped-for-node",
            "no approved name was supplied for this node "
            f"(the list is scoped, and has no entry for {ev.node_id})",
        )

    # Absence of the name is only meaningful if there was a body to look in. On a
    # bot-blocked node (GEANT returns HTTP 403 with no body) "none appear" would
    # be a claim about a page that was never read.
    if not ev.full_text.strip():
        return _NameNote(
            "no-body",
            f"{len(candidates)} approved name(s) were supplied for this node, but no page body "
            f"was captured (HTTP {ev.http_status}), so the name was not looked for",
        )

    found = names.find(ev.full_text, ev.node_id)
    if found is None:
        # Point at where to look. Bare absence is true but gives a reviewer
        # nothing to check; naming the phrase the approved names share, and how
        # often the page uses it, is verifiable without guessing at the name.
        prefix, hits = names.prefix_hits(ev.full_text, ev.node_id)
        times = "once" if hits == 1 else f"{hits} times"
        instead = (
            f' — the phrase "{prefix}" does occur {times}, but never followed by an '
            "approved name"
            if hits
            else ""
        )
        return _NameNote(
            "not-found",
            f"NONE of the {len(candidates)} approved name(s) for this node appear in the page "
            f"body{instead} — note the <title> is not searched",
        )

    # A different separator glyph is not a failure, but it is the one difference
    # a reviewer would otherwise have to spot by eye, so it is shown.
    how = "" if found.exact else f' (the page writes it "{found.matched_text}")'
    if found.scoped:
        return _NameNote(
            "matched",
            f'approved name matched, scoped to this node: "{found.name}"{how}',
        )
    return _NameNote(
        "matched-unscoped",
        f'approved name matched from the unscoped list: "{found.name}"{how} — the list does '
        "not say which name belongs to which node, so this does not establish it is this "
        "node's own name",
    )


# The name half of point 3, as one sentence for the summary. Each clause is
# written to be true of the state it belongs to and false of the others, so a
# reader of the summary alone is never told the tool did less than it did.
_NAME_CLAUSE = {
    "absent": (
        "whether the node name on the page is the official Tripartite-approved one — no "
        "approved-names list was supplied, so the tool did not check it (pass --approved-names "
        "to have it checked)"
    ),
    "unscoped-for-node": (
        "whether the node name on the page is the official Tripartite-approved one — the list "
        "supplied holds no approved name for this node, so the tool did not check it"
    ),
    "no-body": (
        "whether the node name on the page is the official Tripartite-approved one — approved "
        "names were supplied for this node, but the page body was not captured, so the name "
        "could not be looked for"
    ),
    "not-found": (
        "whether the node name on the page is the official Tripartite-approved one — it was "
        "looked for and not found in the page body, which is not proof of absence, since the "
        "<title> is not searched"
    ),
    "matched": (
        "whether the page shows it as the official form — an approved name written against this "
        "node was found in the page body (see the evidence below)"
    ),
    "matched-unscoped": (
        "whether the name found is this node's own — an approved name was found in the page "
        "body, but the list supplied is unscoped, so it does not say which node the name "
        "belongs to"
    ),
}

# What a reviewer should actually do, which differs once the tool has already
# compared the page against a list.
_NAME_ACTION = {
    "matched": "The node name matched the approved list, so only how the page renders it needs a look.",
    "matched-unscoped": "Confirm the matched name is this node's own; the list supplied does not say.",
}
_NAME_ACTION_DEFAULT = "check the node name against the Tripartite-approved list"


# "eosc" as a token, not a fragment of a longer word. "geoscience" contains it;
# so does "neoscope". The same class of bug as EGI matching "strategic", which
# was fixed in the name match before it was fixed here.
#
# The trailing guard allows an uppercase letter, unlike the leading one. Nodes
# name the official lockup with no separator at all — EOSCNode_Finland.jpg,
# EOSCNodeBBMRIERIC_ColourPos.png, EOSCNodeDataTerra.jpg — and a strict
# trailing guard rejected every one of them, which cost the Finnish node its
# only EOSC asset. CamelCase reads as a word break to a human, so it is one
# here. The asymmetry is safe: "geoscience" and "GEOSCIENCE" are both stopped
# by the *leading* guard, since a letter precedes the "eosc" in each.
_EOSC_TOKEN = re.compile(r"(?<![A-Za-z0-9])[Ee][Oo][Ss][Cc](?![a-z0-9])")


def _references_eosc(img: Image) -> bool:
    """Whether an image asset genuinely references EOSC.

    The hostname of `src` is deliberately excluded from the text searched. On
    the real eosc-dto node, 7 of the 8 assets reported as "EOSC-referencing"
    matched only because the page is served from `eosc-dto.d4science.org` —
    among them an EU funding badge called `FundedbytheEU.png`. The host is a
    property of the site, and the site is already known to be an EOSC node;
    it says nothing about the image, so counting it inflates the evidence for
    exactly the nodes that need no help.

    A host of `eosc.eu` itself is the opposite case and does count: at least one
    node in the set loads its logo cross-host from eosc.eu, which is a real
    signal about that image. A lookalike such as `myeosc.eu` does not, per
    `_is_host`.
    """
    parsed = urlparse(img.src)
    # The path and query survive, so a file named "eosc-node-final.webp" still
    # counts however it is hosted.
    src_without_host = img.src.replace(parsed.netloc, " ", 1) if parsed.netloc else img.src
    haystack = f"{src_without_host} {img.alt} {img.aria_label} {img.title} {img.css_class}"
    if _EOSC_TOKEN.search(haystack):
        return True
    return _is_host(parsed.netloc, "eosc.eu")


def check_3(
    ev: PageEvidence,
    approved_names: ApprovedNames | list[str] | None = None,
) -> Result:
    """EOSC logo present, and the official Tripartite-approved node name."""
    if ev.error:
        return Result("3", "EOSC logo and official node name visible", ERROR, f"Page not fetched: {ev.error}")

    logo_hits = []
    for img in ev.images:
        if _references_eosc(img):
            kind = "inline SVG" if img.inline_svg else "img"
            label = img.alt or img.aria_label or img.title or img.src.rsplit("/", 1)[-1]
            logo_hits.append(f"{kind}: {label[:120]}")

    name_note = _approved_name_note(ev, approved_names)

    if logo_hits:
        lines = [f"EOSC-referencing image asset(s): {len(logo_hits)}"] + logo_hits[:5]
        if name_note.line:
            lines.append(name_note.line)
        extra = _NAME_ACTION.get(name_note.state)
        action = (
            f"Confirm the EOSC logo is visible without scrolling. {extra}"
            if extra
            else f"Confirm the logo is visible without scrolling, and {_NAME_ACTION_DEFAULT}."
        )
        return Result(
            "3",
            "EOSC logo and official node name visible",
            MANUAL_REVIEW,
            "An EOSC-referencing image asset is present, so the logo requirement is likely met. "
            'Two things remain human judgements: whether it is "clearly and visibly" shown, and '
            f"{_NAME_CLAUSE[name_note.state]}.",
            lines,
            reviewer_action=action,
        )

    return Result(
        "3",
        "EOSC logo and official node name visible",
        MANUAL_REVIEW,
        "No EOSC-referencing image asset was found in the markup. This is NOT proof of absence: "
        "a logo shown as a CSS background image, an SVG sprite reference, or a file named without "
        '"eosc" would all be missed by this check.',
        [
            f"{len(ev.images)} image/SVG element(s) examined, none referencing EOSC",
            "mentions of EOSC in page text: " + str(len(re.findall(r"(?i)eosc", ev.full_text))),
        ]
        + ([name_note.line] if name_note.line else []),
        reviewer_action="Look at the page (or its screenshot) and confirm whether an EOSC logo is visibly displayed.",
    )


# --- point 4 -----------------------------------------------------------------


def check_4(ev: PageEvidence, expected_page: str = "") -> Result:
    """Link to the node's own dedicated page under eosc.eu/building-the-eosc-federation."""
    if ev.error:
        return Result("4", "Link to the node's page on eosc.eu", ERROR, f"Page not fetched: {ev.error}")

    # Naming the exact page a node should link to turns "something is absent" into
    # a one-line fix the node operator can action.
    expected_note = (
        [f"the node's dedicated page exists at {expected_page} but is not linked from here"]
        if expected_page
        else []
    )

    node_pages, index_only, other_eosc = [], [], []
    for link in ev.links:
        parsed = urlparse(link.href)
        if not _is_host(parsed.netloc, "eosc.eu"):
            continue
        path = parsed.path.rstrip("/")
        if "building-the-eosc-federation" in path:
            tail = path.split("building-the-eosc-federation", 1)[1].strip("/")
            (node_pages if tail else index_only).append(link)
        else:
            other_eosc.append(link)

    if node_pages:
        return Result(
            "4",
            "Link to the node's page on eosc.eu",
            PASS,
            "Links to a specific node entry under eosc.eu/building-the-eosc-federation.",
            [_fmt(link) for link in node_pages[:3]],
        )

    if index_only:
        return Result(
            "4",
            "Link to the node's page on eosc.eu",
            FAIL,
            "Links only to the building-the-eosc-federation index, which the checklist "
            "explicitly excludes. The node's own dedicated entry is required.",
            [_fmt(link) for link in index_only[:3]] + expected_note,
        )

    if other_eosc:
        return Result(
            "4",
            "Link to the node's page on eosc.eu",
            FAIL,
            "Links to eosc.eu but not to the node's dedicated page under "
            "building-the-eosc-federation. The checklist excludes the homepage.",
            [_fmt(link) for link in other_eosc[:4]] + expected_note,
        )

    warning = link_collection_warning(ev)
    if warning:
        return Result(
            "4",
            "Link to the node's page on eosc.eu",
            MANUAL_REVIEW,
            "No link to eosc.eu was found, but the page yielded too little to conclude "
            "absence: " + warning,
            [f"{len(ev.links)} link(s) examined, none pointing to eosc.eu"] + expected_note,
            reviewer_action="Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.",
        )
    return Result(
        "4",
        "Link to the node's page on eosc.eu",
        FAIL,
        "No link to eosc.eu was found on the landing page.",
        [f"{len(ev.links)} link(s) examined, none pointing to eosc.eu"]
        + expected_note
        + _render_note(ev),
    )


# --- point 5 -----------------------------------------------------------------


def check_5a(ev: PageEvidence, on_nlp: bool = True) -> Result:
    """Purpose descriptions. `on_nlp` selects the item 5 wording in force.

    Checklist v3.2 (28 September 2026) requires the information of item 5 "both on
    the NLP presenting the resource to the users (directly on the NLP itself or via
    intermediate web pages linked by the NLP) and via the link to the resource's
    entry in the EOSC Catalogue"; v3.0 and v3.1 asked for either.
    For 5a the verdict does not change -- judging whether a description states a
    purpose is reading, and the resources cannot be enumerated from the page --
    but the message and the reviewer's work list do.
    """
    if ev.error:
        return Result("5a", "Purpose description for research resources", ERROR, f"Page not fetched: {ev.error}")
    if on_nlp:
        return Result(
            "5a",
            "Purpose description for research resources",
            MANUAL_REVIEW,
            'Quantifies over "all Node Exchange research resources offered by the Node", which cannot be '
            "enumerated from the landing page alone. Since checklist v3.2 each resource's purpose "
            "description must be on the NLP that presents it (directly or on a page the NLP links to) and "
            "in the resource's metadata in the EOSC Catalogue; the tool reads neither the resource list "
            "nor the Catalogue.",
            [
                f"{len(ev.links)} outbound link(s) on the landing page",
                f"main text length: {len(ev.main_text)} characters",
            ],
            reviewer_action="List the node's Node Exchange resources, then confirm each has an English purpose "
            "description on the NLP (or a page it links to) and in its EOSC Catalogue metadata.",
        )
    return Result(
        "5a",
        "Purpose description for research resources",
        MANUAL_REVIEW,
        'Quantifies over "all Node Exchange research resources offered by the Node", which cannot be '
        "enumerated from the landing page alone. The checklist also allows the description "
        "to live in the resource's EOSC Catalogue entry rather than on this page.",
        [
            f"{len(ev.links)} outbound link(s) on the landing page",
            f"main text length: {len(ev.main_text)} characters",
        ],
        reviewer_action="List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.",
    )


# Wording that a genuine policy document contains, used to tell a real policy
# page apart from a navigation stub that merely has "policy" in its link text.
POLICY_BODY_PATTERNS = [
    r"(?i)\bmust not\b", r"(?i)\byou (?:may|must|shall|agree)\b", r"(?i)\bpermitted\b",
    r"(?i)\bprohibit", r"(?i)\bterms\b", r"(?i)\bpolicy\b", r"(?i)\bconditions\b",
    r"(?i)\bresponsib", r"(?i)\bcomply\b", r"(?i)\bauthorised\b", r"(?i)\bauthorized\b",
]
DEAD_STATUSES = (404, 410)

# Signals that a 403 came from bot mitigation rather than from an access policy.
BOT_WALL_PATTERNS = [
    r"(?i)just a moment", r"(?i)attention required", r"(?i)cloudflare",
    r"(?i)access denied", r"(?i)captcha", r"(?i)are you a (?:human|robot)",
    r"(?i)enable javascript and cookies", r"(?i)unusual traffic",
    r"(?i)request (?:was )?blocked", r"(?i)ray id", r"(?i)akamai", r"(?i)incapsula",
    r"(?i)perimeterx", r"(?i)forbidden",
]


def _verify_child(ev: PageEvidence, point: str, patterns: list[str]):
    """Return the fetched child page that was followed for this point, or None."""
    for child in ev.children_for(point):
        return child
    return None


def _why_not_fetched(ev: PageEvidence, links: list, what: str) -> tuple[str, str]:
    """Say why a matching link has no fetched target, and what to do about it.

    The reviewer action used to say "re-run with --depth 1" in every case,
    including runs that were already at depth 1 and links to a PDF, which no
    depth will fetch. Advice that cannot work wastes the reviewer's time and
    tempts a re-run that puts load on the node for nothing.
    """
    confirm = f"Open the link and confirm the target really is {what}, in English."
    if ev.crawl_depth < 1:
        return ("this run did not follow links",
                confirm + " Re-run with --depth 1 to have the tool check it.")
    page_host = urlparse(ev.final_url or ev.requested_url).netloc.lower()
    for link in links:
        parsed = urlparse(link.href)
        if parsed.path.lower().endswith(BINARY_SUFFIXES):
            kind = parsed.path.rsplit(".", 1)[-1].upper()
            return (f"it is a {kind} document, which the tool does not download or read",
                    f"Open the {kind} and confirm it is {what}, in English. "
                    "No --depth setting will fetch it.")
    skipped = " ".join(ev.children_skipped)
    if any(link.href in skipped for link in links):
        return ("a per-node or per-point cap was reached before it",
                confirm + " Raising --max-children would let the tool fetch it.")
    for link in links:
        host = urlparse(link.href).netloc.lower()
        if host and host != page_host and not _related_host(host, page_host):
            return ("it is on another site, which the tool does not follow",
                    confirm + " No --depth setting will fetch it.")
    return ("it was not selected when this evidence was collected",
            confirm + " Collecting the evidence again would fetch it.")


def _policy_check(
    ev: PageEvidence,
    point: str,
    title: str,
    patterns: list[str],
    what: str,
    on_nlp: bool = True,
    other_patterns: list[str] | None = None,
    other_what: str = "",
) -> Result:
    """Points 5b and 5c.

    `on_nlp` is True under checklist v3.2, whose item 5 requires the AUP and the
    UAP "both on the NLP presenting the resource to the users (directly on the
    NLP itself or via intermediate web pages linked by the NLP) and via the link
    to the resource's entry in the EOSC Catalogue". Under v3.0 and v3.1 the
    requirement was "either directly or via" the Catalogue, so a landing page
    without a pointer could not fail: the policy might be in the Catalogue.

    Under v3.2 a pointer on any linked page the tool read counts as on the NLP.
    Absence is a FAIL only when nothing else keeps a human in the loop:

    * the NLP links to the *other* policy: "AUP and UAP can be provided through
      the same, single document";
    * the landing page links to a licence: "AUP/UAP can be provided via specific
      product licenses in the case of datasets, archives, software";
    * the DOM did not arrive (`link_collection_warning`), as for point 4;
    * the landing page links to a policies, legal, services or resources page
      the tool did not read, which may be where the pointers are.

    A pointer found on the NLP settles only the NLP half. The Catalogue half is
    not read by this tool, and the reviewer action says so.
    """
    if ev.error:
        return Result(point, title, ERROR, f"Page not fetched: {ev.error}")

    links = _link_hits(ev, patterns)
    text_hits = _match(ev.full_text, patterns)

    if links:
        child = _verify_child(ev, point, patterns)

        # Without a level of crawling the tool can only say a link exists. That is
        # weaker than it looks: a link labelled "Acceptable Use Policy" pointing at
        # a 404 satisfies the letter of "there is a link" while failing the actual
        # requirement, which is that the policy be *accessible*.
        if child is None:
            why, action = _why_not_fetched(ev, links, what)
            return Result(
                point,
                title,
                PASS,
                f"The landing page links to what appears to be {what}. "
                f"The link target was not fetched ({why}), so this is a pointer, not a verified document.",
                [_fmt(link) for link in links[:4]],
                reviewer_action=action + (_CATALOGUE_HALF if on_nlp else ""),
            )

        if child.http_status in DEAD_STATUSES:
            return Result(
                point,
                title,
                FAIL,
                f"The landing page links to {what}, but that link is broken "
                f"(HTTP {child.http_status}), so the policy is not accessible.",
                [_fmt(link) for link in links[:2]] + [f"followed: {child.url} -> HTTP {child.http_status}"],
                reviewer_action="Fix or repoint the link.",
            )

        if not child.ok:
            return Result(
                point,
                title,
                MANUAL_REVIEW,
                f"The landing page links to what appears to be {what}, but the tool could not "
                f"read the target, so it is unverified. This may be a bot restriction rather "
                f"than a real problem.",
                [_fmt(link) for link in links[:2]]
                + [f"followed: {child.url} -> {child.error or f'HTTP {child.http_status}'}"],
                reviewer_action="Open the link manually and confirm the policy is reachable.",
            )

        body = _match(child.main_text or child.full_text, POLICY_BODY_PATTERNS)
        if len(child.main_text) < 400 or not body:
            return Result(
                point,
                title,
                MANUAL_REVIEW,
                f"The link target was fetched but does not read like {what}: "
                f"{len(child.main_text)} characters of main text and "
                f"{'no policy-like wording' if not body else 'little substance'}. "
                "It may be a landing stub that points further on.",
                [f"followed: {child.url} -> HTTP {child.http_status}",
                 f"title: {child.title or '(none)'}"],
                reviewer_action=f"Open the target and find where {what} is actually published.",
            )

        return Result(
            point,
            title,
            PASS,
            f"The landing page links to {what}, and the target was fetched and reads like a "
            f"policy document.",
            [_fmt(link) for link in links[:2]]
            + [f"followed: {child.url} -> HTTP {child.http_status}, "
               f"{len(child.main_text)} chars, title: {child.title or '(none)'}",
               f"policy wording found: {', '.join(sorted(set(body))[:4])}"],
            reviewer_action="Confirm it covers all the node's resources and is in English."
            + (_CATALOGUE_HALF if on_nlp else ""),
        )

    if text_hits and not on_nlp:
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"{what.capitalize()} is mentioned in the page text but not as a followable link.",
            [f"text mentions: {', '.join(sorted(set(text_hits))[:4])}"],
            reviewer_action=f"Find where {what} is actually published and confirm it is reachable.",
        )

    if not on_nlp:
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"No pointer to {what} was found on the landing page. This is deliberately not a FAIL: "
            "the checklist permits the policy to be reached via each resource's entry in the EOSC "
            "Catalogue, which this tool does not follow.",
            [f"{len(ev.links)} link(s) examined, none matching {what}"],
            reviewer_action=f"Check the node's resource entries in the EOSC Catalogue for {what}.",
        )

    # Checklist v3.2: "directly on the NLP itself or via intermediate web pages
    # linked by the NLP". Every linked page the tool read counts.
    read = [c for c in ev.children if c.ok]
    via = _linked_page_hits(read, patterns)
    if via:
        page, link = via[0]
        target = _fetched(ev, link.href)
        if target is not None and target.http_status in DEAD_STATUSES:
            return Result(
                point,
                title,
                FAIL,
                f"The landing page links to {page.url}, which links to {what}, but that link is "
                f"broken (HTTP {target.http_status}), so the policy is not accessible.",
                [f"via {page.url}: {_fmt(link)}", f"followed: {target.url} -> HTTP {target.http_status}"],
                reviewer_action="Fix or repoint the link.",
            )
        return Result(
            point,
            title,
            PASS,
            f"The landing page does not link to {what} itself, but a page it links to does. "
            "Checklist v3.2 accepts the policy on the NLP or on intermediate pages linked by the NLP. "
            + ("The policy page was fetched too." if target is not None and target.ok
               else "The policy page itself was not fetched, so this is a pointer, not a verified document."),
            [f"landing page -> {page.url} (\"{page.link_text.strip() or page.title}\")"]
            + [f"via {pg.url}: {_fmt(lk)}" for pg, lk in via[:3]],
            reviewer_action="Confirm the policy covers every Node Exchange resource the landing page "
            "presents, and is in English." + _CATALOGUE_HALF,
        )

    looked = [f"{len(ev.links)} link(s) on the landing page examined, none matching {what}"]
    if read:
        looked.append(
            f"{len(read)} linked page(s) read, none linking to {what}: "
            + ", ".join(c.url for c in read[:5]) + (" ..." if len(read) > 5 else "")
        )
    if text_hits:
        # Naming the AUP in prose ("based on the ... AUP") does not make it
        # accessible; the mention is kept as evidence so a reviewer can see it.
        looked.append(f"named in the text without a link: {', '.join(sorted(set(text_hits))[:4])}")
    other = _link_hits(ev, other_patterns) if other_patterns else []
    other_via = _linked_page_hits(read, other_patterns) if other_patterns else []
    if other or other_via:
        shown = [f"{other_what}: {_fmt(link)}" for link in other[:2]]
        shown += [f"{other_what} via {pg.url}: {_fmt(lk)}" for pg, lk in other_via[: 2 - len(shown[:2])]]
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"No pointer to {what} was found on the NLP, but it links to {other_what}. "
            "Checklist v3.2 allows the AUP and the UAP to be provided through the same, single "
            "document, so this may satisfy the point.",
            looked + shown,
            reviewer_action=f"Open the linked {other_what} and confirm it also serves as {what} "
            "for every Node Exchange resource the page presents." + _CATALOGUE_HALF,
        )
    licences = _link_hits(ev, LICENCE_PATTERNS)
    if licences:
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"No pointer to {what} was found on the NLP, but the landing page links to a licence. "
            "Checklist v3.2 allows the AUP and UAP of datasets, archives and software to be "
            "provided through their product licences, which a reviewer must match to resources.",
            looked + [f"licence: {_fmt(link)}" for link in licences[:2]],
            reviewer_action="Confirm which resources the licence covers, and that every service "
            f"resource has {what} on the NLP or a page it links to." + _CATALOGUE_HALF,
        )
    warning = link_collection_warning(ev)
    if warning:
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"No pointer to {what} was found, but the page yielded too little to conclude "
            "absence: " + warning,
            looked,
            reviewer_action=f"Open the page, dismiss any consent banner, and look for {what} "
            "linked for each resource the page presents.",
        )
    unread = _unread_intermediate_links(ev)
    if unread:
        # A policies index or a services page the tool did not read may hold the
        # pointers. Concluding absence without reading it would blame the node
        # for the tool's own blind spot.
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"No pointer to {what} was found on the pages the tool read, but the landing page links "
            "to pages that may carry it (a policies, legal, services or resources page) which were "
            "not read. Checklist v3.2 accepts the policy on intermediate pages linked by the NLP.",
            looked + [f"not read: {_fmt(link)}" for link in unread[:3]],
            reviewer_action=f"Open those pages and look for {what} for each resource. "
            "Collecting the evidence again at depth 1 or more would read them.",
        )
    return Result(
        point,
        title,
        FAIL,
        (f"{what.capitalize()} is named in the page text, but no link to it was found. "
         if text_hits else f"No pointer to {what} was found on the landing page. ")
        + (f"None of the {len(read)} linked page(s) the tool read links to it either, and the landing "
           "page links to no other policies, legal, services or resources page. " if read else
           "The landing page links to no policies, legal, services or resources page that could carry it. ")
        + "Checklist v3.2 requires it on the NLP, directly or via intermediate pages linked by the NLP, "
        "for every Node Exchange resource the page presents, as well as in each resource's EOSC "
        "Catalogue metadata; being in the Catalogue alone is not enough.",
        looked + _render_note(ev),
        reviewer_action=f"Confirm on the live page, then ask the node to link {what} from the NLP or "
        "a page it links to, for each of its resources (one document may cover all of them, and may "
        "be the same as the other policy).",
    )


def _linked_page_hits(pages: list, patterns: list[str]) -> list:
    """(page, link) pairs: links on already-read linked pages matching `patterns`.

    A linked page that is itself the policy (its title names it) counts as a
    hit too, represented by a link to itself.
    """
    from .fetch import Link

    out = []
    for page in pages:
        title_hit = _match(f"{page.title} {page.link_text}", patterns)
        if title_hit and _match(page.main_text or page.full_text, POLICY_BODY_PATTERNS):
            out.append((page, Link(page.final_url or page.url, page.title or page.link_text)))
            continue
        for link in page.links:
            if link.href.lower().startswith(("mailto:", "tel:", "javascript:")):
                continue
            if any(re.search(p, link_haystack(link.text, link.href)) for p in patterns):
                out.append((page, link))
                break
    return out


def _fetched(ev: PageEvidence, href: str):
    key = href.split("#")[0].rstrip("/")
    for c in ev.children:
        if key in (c.url.split("#")[0].rstrip("/"), (c.final_url or "").split("#")[0].rstrip("/")):
            return c
    return None


def _unread_intermediate_links(ev: PageEvidence) -> list:
    """Same-site landing-page links to a policies or services page not read."""
    page_host = urlparse(ev.final_url or ev.requested_url).netloc.lower()
    home = (ev.final_url or ev.requested_url).split("#")[0].rstrip("/")
    out, seen = [], set()
    for link in ev.links:
        parsed = urlparse(link.href)
        if parsed.scheme not in ("http", "https") or parsed.path.lower().endswith(BINARY_SUFFIXES):
            continue
        host = parsed.netloc.lower()
        if not (host == page_host or _related_host(host, page_host)):
            continue
        key = link.href.split("#")[0].rstrip("/")
        if key == home or key in seen:
            continue
        hay = link_haystack(link.text, parsed.path)
        if not any(re.search(p, hay) for p in POLICY_INDEX_PATTERNS + SERVICE_INDEX_PATTERNS):
            continue
        seen.add(key)
        if _fetched(ev, link.href) is None:
            out.append(link)
    return out


_CATALOGUE_HALF = (
    " Checklist v3.2 also requires it in each resource's metadata in the EOSC Catalogue,"
    " which this tool does not read."
)


def check_5b(ev: PageEvidence, on_nlp: bool = True) -> Result:
    return _policy_check(
        ev, "5b", "Acceptable Use Policy (AUP) accessible", AUP_PATTERNS, "an Acceptable Use Policy",
        on_nlp, UAP_PATTERNS, "a User Access Policy",
    )


def check_5c(ev: PageEvidence, on_nlp: bool = True) -> Result:
    return _policy_check(
        ev, "5c", "User Access Policy (UAP) accessible", UAP_PATTERNS, "a User Access Policy",
        on_nlp, AUP_PATTERNS, "an Acceptable Use Policy",
    )


# --- point 6 -----------------------------------------------------------------


def _strong_link(link) -> bool:
    """A landing-page link that by itself identifies a helpdesk."""
    if is_helpdesk_address(link.href) or is_helpdesk_host(link.href):
        return True
    return bool(_match(link_haystack(link.text, link.href), HELPDESK_STRONG))


def check_6(ev: PageEvidence) -> Result:
    """Means of contacting the node helpdesk.

    A PASS needs something that identifies a helpdesk, not a link that merely
    says "support". Any of these is enough:

    * a landing-page link labelled or addressed as a helpdesk, service desk,
      ticket system, support team or request (HELPDESK_STRONG), or to a
      helpdesk host (hd., support., helpdesk.);
    * a mailto: whose mailbox or mail host names a helpdesk (support@...,
      it@helpdesk...);
    * a followed contact or support page that names a helpdesk, service desk
      or ticket system, or gives a helpdesk address (HELPDESK_ON_PAGE; page
      prose about "support" does not count).

    A bare "support" link is followed, but settles nothing by its label.
    """
    title = "Means of contacting the node helpdesk"
    if ev.error:
        return Result("6", title, ERROR, f"Page not fetched: {ev.error}")

    mailtos = [link for link in ev.links if link.href.lower().startswith("mailto:")]
    contact_links = _link_hits(ev, CONTACT_PATTERNS)
    strong = [link for link in contact_links + mailtos if _strong_link(link)]

    if strong:
        return Result(
            "6",
            title,
            PASS,
            "The landing page links to a route identified as a helpdesk or user support.",
            [_fmt(link) for link in strong[:4]],
            reviewer_action="Confirm the route reaches the node's user support. A helpdesk "
            "behind a sign-in form is still a means of contact, but note it.",
        )

    if contact_links or mailtos:
        followed = ev.children_for("6")
        live = [c for c in followed if c.ok]
        # A "Contact" or "Support" link is ambiguous on its own. The page behind
        # it usually is not: it either names a helpdesk or gives a helpdesk
        # address, or it does not. Every followed page is read, not just the
        # first: BBMRI-ERIC's helpdesk addresses are on the second.
        for child in live:
            text = child.main_text or child.full_text
            desk = _match(text, HELPDESK_ON_PAGE)
            desk_mail = [ln.href for ln in child.links if is_helpdesk_address(ln.href)]
            if desk or desk_mail:
                return Result(
                    "6",
                    title,
                    PASS,
                    "A page reached from the landing page identifies a helpdesk or user "
                    "support route.",
                    [_fmt(link) for link in (contact_links + mailtos)[:2]]
                    + [f"followed: {child.url} -> HTTP {child.http_status}"]
                    + ([f"helpdesk wording on that page: {', '.join(sorted(set(desk))[:4])}"]
                       if desk else [])
                    + [f"helpdesk address given: {h}" for h in desk_mail[:3]],
                    reviewer_action="Confirm the route reaches the node's user support.",
                )

        weak = [link for link in contact_links if re.search(r"(?i)\bsupport\b", link.text)]
        skipped6 = [s for s in ev.children_skipped if "point 6" in s]
        evidence = [_fmt(link) for link in (contact_links + mailtos)[:3]]
        evidence += [f"followed: {c.url} -> HTTP {c.http_status}" for c in followed[:3]]
        for child in live:
            evidence += [f"address given: {ln.href}" for ln in child.links
                         if ln.href.lower().startswith("mailto:")][:2]
        evidence += [f"not followed: {s}" for s in skipped6[:2]]
        weak_note = (
            ' A link labelled "support" was found, but that word alone does not identify '
            "a helpdesk: it also labels funding programmes and service catalogues."
            if weak else ""
        )

        if live:
            offers = any(
                any(ln.href.lower().startswith("mailto:") for ln in c.links)
                or _match(c.main_text or c.full_text, [r"(?i)contact\s*form", r"(?i)<?\bsubmit\b"])
                for c in live
            )
            summary = (
                "A contact page exists and offers a way to get in touch, but nothing on it "
                "identifies a helpdesk specifically."
                if offers else
                "The contact or support pages reached from the landing page do not identify "
                "a helpdesk."
            )
            return Result(
                "6",
                title,
                MANUAL_REVIEW,
                summary + weak_note + " The checklist asks for the node helpdesk, and general "
                "enquiries may not satisfy that.",
                evidence,
                reviewer_action="Confirm whether any route reaches the node's user support, not a "
                "general mailbox or an unrelated service.",
            )

        dead = [c for c in followed if c.http_status in DEAD_STATUSES]
        if followed and len(dead) == len(followed):
            child = dead[0]
            return Result(
                "6",
                title,
                FAIL,
                f"The landing page's contact link is broken (HTTP {child.http_status}), so no "
                "working means of contact is offered by that route.",
                [_fmt(link) for link in contact_links[:2]]
                + [f"followed: {child.url} -> HTTP {child.http_status}"],
                reviewer_action="Fix or repoint the contact link.",
            )

        return Result(
            "6",
            title,
            MANUAL_REVIEW,
            "A contact route exists, but nothing identifies it as a helpdesk." + weak_note
            + " The checklist asks specifically for the node helpdesk, and a general enquiries "
            "or press address does not obviously satisfy that.",
            evidence,
            reviewer_action="Confirm this contact route reaches the node's user support, not a general mailbox.",
        )

    warning = link_collection_warning(ev)
    if warning:
        return Result(
            "6",
            title,
            MANUAL_REVIEW,
            "No contact route was found, but the page yielded too little to conclude "
            "absence: " + warning,
            [f"{len(ev.links)} link(s) examined"],
            reviewer_action="Open the page, dismiss any consent banner, and look for a helpdesk or support contact.",
        )
    return Result(
        "6",
        title,
        FAIL,
        "No contact route of any kind was found among the landing page's links: "
        "no mailto:, and no link labelled or addressed as contact, support or helpdesk.",
        [f"{len(ev.links)} link(s) examined"] + _render_note(ev),
    )


# --- point 7 -----------------------------------------------------------------


def check_7(ev: PageEvidence) -> Result:
    """The page is in English."""
    if ev.error:
        return Result("7", "The page is in English", ERROR, f"Page not fetched: {ev.error}")

    text = ev.main_text or ev.full_text
    declared = (ev.lang_attr or "").strip()
    lines = [f'declared lang attribute: "{declared or "(none)"}"']

    if len(text) < 120:
        return Result(
            "7",
            "The page is in English",
            MANUAL_REVIEW,
            f"Only {len(text)} characters of text were available — too little to detect a language.",
            lines,
            reviewer_action="Open the page and confirm its content is in English.",
        )

    detected, confidence = None, 0.0
    try:
        from lingua import LanguageDetectorBuilder

        detector = LanguageDetectorBuilder.from_all_languages_with_latin_script().build()
        sample = text[:4000]
        best = detector.compute_language_confidence_values(sample)[0]
        detected = best.language.iso_code_639_1.name.lower()
        confidence = round(best.value, 2)
        lines.append(f"detected language: {detected} (confidence {confidence})")
    except ImportError:
        lines.append("lingua not installed; relying on the declared attribute alone")
        if declared.lower().startswith("en"):
            return Result("7", "The page is in English", PASS,
                          "Declares English. Statistical detection unavailable.", lines,
                          reviewer_action="Install the lingua extra for a content-based check.")
        return Result("7", "The page is in English", MANUAL_REVIEW,
                      "Cannot detect language and the page does not declare English.", lines,
                      reviewer_action="Confirm by reading the page.")

    is_english = detected == "en"
    declares_english = declared.lower().startswith("en")

    if is_english and declares_english:
        return Result("7", "The page is in English", PASS,
                      "The main content is English and the page declares English.", lines)
    if is_english and not declares_english:
        return Result(
            "7", "The page is in English", PASS,
            f'The main content is English. The page declares "{declared or "nothing"}", which is '
            "a metadata inconsistency worth fixing but does not breach point 7.",
            lines,
            reviewer_action="Suggest the node correct its lang attribute.",
        )
    if not is_english and declares_english:
        return Result(
            "7", "The page is in English", MANUAL_REVIEW,
            f"The page declares English but the main text detects as {detected} "
            f"(confidence {confidence}). Mixed-language pages and short navigation-heavy text "
            "both cause this.",
            lines,
            reviewer_action="Read the page and decide whether an EOSC researcher is served in English.",
        )
    return Result(
        "7", "The page is in English", FAIL,
        f"The main content detects as {detected} (confidence {confidence}), not English, "
        f'and the page declares "{declared or "nothing"}".',
        lines,
        reviewer_action="Confirm; if an English version exists, the registered URL may need to point at it.",
    )


def run_all(
    ev: PageEvidence,
    approved_names: ApprovedNames | list[str] | None = None,
    expected_eosc_page: str = "",
    item5_on_nlp: bool = True,
) -> list[Result]:
    """Every checklist point, in checklist order, exactly one result each.

    `item5_on_nlp` selects the item 5 rule: True for checklist v3.2 and later
    (the information must be on the NLP and in the Catalogue), False for v3.0 and
    v3.1 (on the NLP or in the Catalogue). The CLI reads it from the checklist
    file (`item5_on_nlp`), so rebuilding an older run applies that run's rule.
    """
    return [
        check_1(ev),
        check_1R(ev),
        check_2(ev),
        check_3(ev, approved_names),
        check_4(ev, expected_eosc_page),
        check_5a(ev, item5_on_nlp),
        check_5b(ev, item5_on_nlp),
        check_5c(ev, item5_on_nlp),
        check_6(ev),
        check_7(ev),
    ]
