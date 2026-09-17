"""One check function per checklist point. Exactly one result each.

Verdict vocabulary, and why it is not just pass/fail:

    PASS           the point is satisfied, and a script can show why
    FAIL           the point is violated, and a script can show why
    MANUAL_REVIEW  a human must decide; evidence is attached to make that quick
    ERROR          the tool could not assess (page unreachable, etc.)

MANUAL_REVIEW is the important one. Several checklist points turn on words like
"clearly state" or quantify over "all research resources offered by the Node" —
neither is settleable by inspecting one page. Emitting PASS or FAIL on those
would be a guess dressed as a verdict, and a wrong FAIL against a node is
expensive to retract. Where the tool cannot know, it says so and hands over the
evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from .fetch import PageEvidence

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

# English-only, and that is a real limitation: a node serving a Dutch or Finnish
# contact page can be missed. Point 7 requires English, so for these particular
# points the bias is tolerable — but it is a bias, not an absence of one.
CONTACT_PATTERNS = [
    r"(?i)\bhelpdesk\b",
    r"(?i)\bhelp\s?desk\b",
    r"(?i)\bservice\s+desk\b",
    r"(?i)\bsupport\b",
    r"(?i)\bcontact\b",
    r"(?i)\bget\s+in\s+touch\b",
    r"(?i)\bticket",
]
HELPDESK_SPECIFIC = [
    r"(?i)\bhelpdesk\b",
    r"(?i)\bhelp\s?desk\b",
    r"(?i)\bservice\s+desk\b",
    r"(?i)\bsupport\b",
    r"(?i)\bticket",
]
AUP_PATTERNS = [
    r"(?i)\bacceptable\s+use\s+polic",
    r"(?i)\bAUP\b",
    r"(?i)\bterms\s+of\s+(use|service)\b",
    r"(?i)\bconditions\s+of\s+use\b",
    r"(?i)\buser\s+agreement\b",
]
UAP_PATTERNS = [
    r"(?i)\buser\s+access\s+polic",
    r"(?i)\bUAP\b",
    r"(?i)\baccess\s+polic",
    r"(?i)\bconditions\s+of\s+access\b",
    r"(?i)\baccess\s+conditions\b",
]
LOGIN_PATTERNS = [
    r"(?i)\blog\s?in\b",
    r"(?i)\bsign\s?in\b",
    r"(?i)\bmy\s+account\b",
    r"(?i)\bauthenticate\b",
    r"(?i)\bsso\b",
]
# Markers that a login is EOSC AAI specifically, not a local IdP. Presence is
# suggestive only; the checklist says this is verified during EEN enrolment.
AAI_HINTS = [
    r"(?i)eosc[\s\-]?aai",
    r"(?i)aai\.eosc",
    r"(?i)\bmyaccessid\b",
    r"(?i)\begi\s+check-?in\b",
    r"(?i)aai\.egi\.eu",
    r"(?i)\blife\s?science\s+(ri|login)\b",
    r"(?i)\bmyaccess\b",
    r"(?i)proxy\.aai",
]


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
        haystack = f"{link.text} {link.href}"
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
                reviewer_action="Confirm with the EEN that the node's login is EOSC AAI compliant.",
            )
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            FAIL,
            f"HTTP {status} to an anonymous request, with no login affordance found. "
            "Neither branch (a) nor (b) is satisfied.",
            [f"HTTP {status}"],
        )

    if status is not None and status >= 400:
        return Result(
            "1",
            "NLP publicly accessible or via EOSC AAI",
            FAIL,
            f"The landing page returned HTTP {status}.",
            [f"HTTP {status}", f"final URL: {ev.final_url}"],
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

    return Result(
        "1R",
        "Linked resources public or via EOSC AAI",
        MANUAL_REVIEW,
        "Not assessable without following every resource link and confirming each login "
        "is EOSC AAI. This tool makes one request per node by design, and AAI compliance "
        "is verified during EEN enrolment rather than by reading a page.",
        lines,
        reviewer_action="Walk the external hosts above; for each resource, confirm it is either anonymous or behind EOSC AAI.",
    )


# --- point 2 -----------------------------------------------------------------


def check_2(ev: PageEvidence) -> Result:
    """Scope, intended users, responsible organization. A judgement, not a match."""
    if ev.error:
        return Result("2", "Scope, users and responsible organization stated", ERROR, f"Page not fetched: {ev.error}")

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

    return Result(
        "2",
        "Scope, users and responsible organization stated",
        MANUAL_REVIEW,
        'Requires reading the page: "clearly state" is a judgement about whether the prose '
        "conveys scope, intended users, and the responsible organisation to a researcher. "
        "Evidence is extracted below so the decision is quick.",
        lines,
        reviewer_action="Read the extracted text and confirm all three elements are present and clear.",
    )


# --- point 3 -----------------------------------------------------------------


def check_3(ev: PageEvidence, approved_names: list[str] | None = None) -> Result:
    """EOSC logo present, and the official Tripartite-approved node name."""
    if ev.error:
        return Result("3", "EOSC logo and official node name visible", ERROR, f"Page not fetched: {ev.error}")

    logo_hits = []
    for img in ev.images:
        haystack = f"{img.src} {img.alt} {img.aria_label} {img.title} {img.css_class}"
        if re.search(r"(?i)eosc", haystack):
            kind = "inline SVG" if img.inline_svg else "img"
            label = img.alt or img.aria_label or img.title or img.src.rsplit("/", 1)[-1]
            logo_hits.append(f"{kind}: {label[:120]}")

    name_note = ""
    if approved_names:
        found = [n for n in approved_names if re.search(re.escape(n), ev.full_text, re.I)]
        name_note = (
            f"approved name matched: {found[0]}"
            if found
            else "NONE of the supplied approved names appear on the page"
        )

    if logo_hits:
        lines = [f"EOSC-referencing image asset(s): {len(logo_hits)}"] + logo_hits[:5]
        if name_note:
            lines.append(name_note)
        return Result(
            "3",
            "EOSC logo and official node name visible",
            MANUAL_REVIEW,
            "An EOSC-referencing image asset is present, so the logo requirement is likely met. "
            'Two things remain human judgements: whether it is "clearly and visibly" shown, and '
            "whether the node name on the page is the official Tripartite-approved one — the tool "
            "has no authoritative list of approved names.",
            lines,
            reviewer_action="Confirm the logo is visible without scrolling, and check the node name against the Tripartite-approved list.",
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
        + ([name_note] if name_note else []),
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

    warning = render_warning(ev)
    if warning:
        return Result(
            "4",
            "Link to the node's page on eosc.eu",
            MANUAL_REVIEW,
            "No link to eosc.eu was found, but the page did not fully render, so absence "
            "cannot be concluded: " + warning,
            [f"{len(ev.links)} link(s) examined, none pointing to eosc.eu"] + expected_note,
            reviewer_action="Open the page, dismiss any consent banner, and look for a link to the node's entry under eosc.eu/building-the-eosc-federation.",
        )
    return Result(
        "4",
        "Link to the node's page on eosc.eu",
        FAIL,
        "No link to eosc.eu was found on the landing page.",
        [f"{len(ev.links)} link(s) examined, none pointing to eosc.eu"] + expected_note,
    )


# --- point 5 -----------------------------------------------------------------


def check_5a(ev: PageEvidence) -> Result:
    if ev.error:
        return Result("5a", "Purpose description for research resources", ERROR, f"Page not fetched: {ev.error}")
    return Result(
        "5a",
        "Purpose description for research resources",
        MANUAL_REVIEW,
        'Quantifies over "all research resources offered by the Node", which cannot be '
        "enumerated from the landing page alone. The checklist also allows the description "
        "to live in the resource's EOSC Catalogue entry rather than on this page.",
        [
            f"{len(ev.links)} outbound link(s) on the landing page",
            f"main text length: {len(ev.main_text)} characters",
        ],
        reviewer_action="List the node's research resources, then confirm each has an English purpose description here or in its Catalogue entry.",
    )


def _policy_check(ev: PageEvidence, point: str, title: str, patterns: list[str], what: str) -> Result:
    if ev.error:
        return Result(point, title, ERROR, f"Page not fetched: {ev.error}")

    links = _link_hits(ev, patterns)
    text_hits = _match(ev.full_text, patterns)

    if links:
        return Result(
            point,
            title,
            PASS,
            f"The landing page links to what appears to be {what}.",
            [_fmt(link) for link in links[:4]],
            reviewer_action=f"Confirm the target really is {what}, is in English, and covers all the node's resources.",
        )

    if text_hits:
        return Result(
            point,
            title,
            MANUAL_REVIEW,
            f"{what.capitalize()} is mentioned in the page text but not as a followable link.",
            [f"text mentions: {', '.join(sorted(set(text_hits))[:4])}"],
            reviewer_action=f"Find where {what} is actually published and confirm it is reachable.",
        )

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


def check_5b(ev: PageEvidence) -> Result:
    return _policy_check(
        ev, "5b", "Acceptable Use Policy (AUP) accessible", AUP_PATTERNS, "an Acceptable Use Policy"
    )


def check_5c(ev: PageEvidence) -> Result:
    return _policy_check(
        ev, "5c", "User Access Policy (UAP) accessible", UAP_PATTERNS, "a User Access Policy"
    )


# --- point 6 -----------------------------------------------------------------


def check_6(ev: PageEvidence) -> Result:
    """Means of contacting the node helpdesk."""
    if ev.error:
        return Result("6", "Means of contacting the node helpdesk", ERROR, f"Page not fetched: {ev.error}")

    mailtos = [link for link in ev.links if link.href.lower().startswith("mailto:")]
    contact_links = _link_hits(ev, CONTACT_PATTERNS)
    specific = [
        link
        for link in contact_links + mailtos
        if any(re.search(p, f"{link.text} {link.href}") for p in HELPDESK_SPECIFIC)
    ]

    if specific:
        return Result(
            "6",
            "Means of contacting the node helpdesk",
            PASS,
            "A support or helpdesk contact route is present.",
            [_fmt(link) for link in specific[:4]],
        )

    if contact_links or mailtos:
        return Result(
            "6",
            "Means of contacting the node helpdesk",
            MANUAL_REVIEW,
            "A contact route exists, but nothing identifies it as a helpdesk. The checklist asks "
            "specifically for the node helpdesk, and a general enquiries or press address does "
            "not obviously satisfy that.",
            [_fmt(link) for link in (contact_links + mailtos)[:4]],
            reviewer_action="Confirm this contact route reaches the node's user support, not a general mailbox.",
        )

    warning = render_warning(ev)
    if warning:
        return Result(
            "6",
            "Means of contacting the node helpdesk",
            MANUAL_REVIEW,
            "No contact route was found, but the page did not fully render, so absence cannot "
            "be concluded: " + warning,
            [f"{len(ev.links)} link(s) examined"],
            reviewer_action="Open the page, dismiss any consent banner, and look for a helpdesk or support contact.",
        )
    return Result(
        "6",
        "Means of contacting the node helpdesk",
        FAIL,
        "No contact route of any kind was found among the landing page's links: "
        "no mailto:, and no link labelled or addressed as contact, support or helpdesk.",
        [f"{len(ev.links)} link(s) examined"],
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
    approved_names: list[str] | None = None,
    expected_eosc_page: str = "",
) -> list[Result]:
    """Every checklist point, in checklist order, exactly one result each."""
    return [
        check_1(ev),
        check_1R(ev),
        check_2(ev),
        check_3(ev, approved_names),
        check_4(ev, expected_eosc_page),
        check_5a(ev),
        check_5b(ev),
        check_5c(ev),
        check_6(ev),
        check_7(ev),
    ]
