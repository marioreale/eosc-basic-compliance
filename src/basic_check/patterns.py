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

HELPDESK_SPECIFIC = [
    r"(?i)\bhelpdesk\b",
    r"(?i)\bhelp\s?desk\b",
    r"(?i)\bservice\s+desk\b",
    r"(?i)\bsupport\b",
    r"(?i)\bticket",
]

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
