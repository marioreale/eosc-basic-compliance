"""The one place link and text vocabulary is defined.

These patterns are shared by two layers that must agree:

* `fetch` uses them to decide which links are worth following one level down;
* `checks` uses them to decide which links satisfy a checklist point.

They started out duplicated, with the crawler looking for "acceptable use" while
the check also accepted "terms of use". The result was a link the check treated
as an Acceptable Use Policy that the crawler never fetched, so the report said
"links to what appears to be an AUP -- target not fetched" for pages whose target
was sitting right there. Nothing failed and no test caught it; the output was
merely quietly weaker than it should have been.

A shared vocabulary makes that class of mismatch impossible: if a link can settle
a point, it is by construction a link the crawler will follow.

English-only, and that is a real limitation rather than an oversight: a node
serving a Dutch or Finnish contact page can be missed. Point 7 requires the
landing page to be in English, so for these points the bias is tolerable -- but
it is a bias.
"""

from __future__ import annotations

import re
from urllib.parse import unquote, urlparse

# Candidate wording: worth following a link for, NOT enough to settle point 6.
# "support" alone is the problem word. On 24 September 2026 it passed three
# pages that are not helpdesks: "National Support" (a funding programme),
# "EBRAINS Support for EuroHPC Applications" (a proposal service) and
# "Services & Support" (a service overview). It stays here so those links are
# still followed; HELPDESK_STRONG below decides whether a route is a helpdesk.
HELPDESK_SPECIFIC = [
    r"(?i)\bhelpdesk\b",
    r"(?i)\bhelp\s?desk\b",
    r"(?i)\bservice\s+desk\b",
    r"(?i)\bsupport\b",
    r"(?i)\bticket",
]

# Wording that does identify a helpdesk, in a link label, a link address or the
# text of a followed page. "support" counts only when it is qualified: a support
# team, request, portal or address, or support that is user, technical or
# contactable. Addresses are matched in their "[at]" / "(at)" disguises too,
# since that is how EGI publishes support[at]egi.eu.
HELPDESK_STRONG = [
    r"(?i)\bhelp\s?desk",
    r"(?i)\bservice\s?desk\b",
    r"(?i)\bticket(s|ing)?\b",
    r"(?i)\bsupport\s+(team|request|requests|portal|centre|center|desk|line|ticket|tickets)\b",
    r"(?i)\b(user|technical|customer|it)\s+support\b",
    r"(?i)\b(contact|get|ask|request)\s+(our\s+|the\s+)?support\b",
    r"(?i)\bsupport\s*(@|\[at\]|\(at\))\s*[a-z0-9-]+",
    r"(?i)\bservice-?now\b",
]

# The subset that settles point 6 from the body of a followed page. Qualified
# "support" phrases are left out on purpose: in a landing-page link label they
# name a route, but in page prose they describe services. EBRAINS's EuroHPC
# proposal page says "Technical Support" and "Application Support team" and is
# still not the node helpdesk. A helpdesk, service desk or ticket system, or a
# support mailbox, is unambiguous wherever it appears.
HELPDESK_ON_PAGE = [
    r"(?i)\bhelp\s?desk",
    r"(?i)\bservice\s?desk\b",
    r"(?i)\bticket(s|ing)?\b",
    r"(?i)\bsupport\s*(@|\[at\]|\(at\))\s*[a-z0-9-]+",
    r"(?i)\bservice-?now\b",
]

# First host labels that name a helpdesk or ticketing system: hd.eosc.sk,
# support.d4science.org, helpdesk.bbmri-eric.eu.
HELPDESK_HOST_LABELS = ("helpdesk", "hd", "support", "servicedesk", "ticket", "tickets")

# Mailbox local parts that name a helpdesk, as against info@ or contact@.
HELPDESK_MAILBOXES = re.compile(
    r"(?i)^(support|helpdesk|help|servicedesk|service-desk|user-support|[a-z0-9]+-helpdesk|[a-z0-9]+-support)$"
)


def link_haystack(text: str, href: str) -> str:
    """What a link is matched against: its label, its raw address, and the
    address with its separators turned into spaces.

    The last part is the fix. Patterns are written for words ("acceptable\\s+use
    polic"), and a URL spells them with hyphens: GEANT's AUP is linked with prose
    as its label and the words only in the address,
    /geant-node-acceptable-use-policy/, so on 24 September 2026 neither the
    crawler nor the check saw it. The raw address is kept as well, so every link
    that matched before still matches.
    """
    parsed = urlparse(href)
    words = re.sub(r"[-_/.+~=&?#:%]+", " ", unquote(f"{parsed.netloc} {parsed.path}"))
    return f"{text} {href} {words}"


def is_helpdesk_address(href: str) -> bool:
    """A mailto: whose mailbox or mail host names a helpdesk."""
    if not href.lower().startswith("mailto:"):
        return False
    addr = unquote(href[7:]).split("?")[0].strip()
    local, _, domain = addr.partition("@")
    if HELPDESK_MAILBOXES.match(local):
        return True
    return domain.lower().split(".")[0] in HELPDESK_HOST_LABELS


def is_helpdesk_host(href: str) -> bool:
    """An http(s) link to a host whose first label names a helpdesk."""
    parsed = urlparse(href)
    if parsed.scheme not in ("http", "https"):
        return False
    return parsed.netloc.lower().split(".")[0] in HELPDESK_HOST_LABELS


CONTACT_PATTERNS = [
    *HELPDESK_SPECIFIC,
    r"(?i)\bcontact\b",
    r"(?i)\bget\s+in\s+touch\b",
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

ABOUT_PATTERNS = [
    r"(?i)\babout\b",
    r"(?i)\bwho\s+we\s+are\b",
    r"(?i)\bour\s+mission\b",
    r"(?i)\bmission\b",
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

# Which checklist point each vocabulary can settle if the link is followed one
# level down, in descending order of how much a request buys. Consumed by
# fetch.select_children; the point ids match the ids the checks look up.
CRAWL_PURPOSES: list[tuple[str, list[str]]] = [
    ("5b", AUP_PATTERNS),
    ("5c", UAP_PATTERNS),
    ("6", CONTACT_PATTERNS),
    ("2", ABOUT_PATTERNS),
]
