"""Mask personal data before anything is written to disk.

Collected pages sometimes name individuals: a media officer's address and mobile
number on a contact page, for instance. The checklist needs none of that. Point 6
asks for a means of contacting the node helpdesk, and a helpdesk is a role, not a
person. So the evidence files and the reports keep role mailboxes as they are
(support@, info@, it@helpdesk.example.org) and mask everything that could
identify a person:

- **Email addresses.** A personal local part becomes ``XXXXX`` and the domain
  stays, so ``jane.doe@example.org`` becomes ``XXXXX@example.org``. The reader
  can still see which organisation the address belongs to. Obfuscated forms
  (``jane.doe [at] example.org``) are masked the same way.
- **Phone numbers.** Only the international prefix stays, so
  ``+31 20 123 4567`` becomes ``+31 XXXXXX``. A number written without a prefix
  is masked only when a label such as "phone:" or "tel." introduces it, because
  a bare run of digits is as likely to be a date, a grant number or a price.
  A labelled number dialled with "00" keeps its country the same way
  (``tel:0043…`` becomes ``tel:+43 XXXXXX``). Office switchboards are masked
  too: nothing in a number says whether it rings a person or a reception desk.
- **The name beside a masked address.** When ``skrickova@…`` is masked,
  "Skřičková" is masked where it appears near the address, together with
  a capitalised given name directly before it. Titles such as "Mgr." or "Dr."
  are left alone, because they end in a full stop, and so are all-capital
  words, which are acronyms (EBRAINS) rather than surnames. A mailbox named
  after its own domain (``geant@geant.org``) is the organisation's, not a
  person's.

The rule is deliberately one-sided. An address is kept only when it is
recognisably a role, and anything unrecognised is masked. A role mailbox masked
by mistake costs a reviewer one click on the live page. A personal address
published by mistake cannot be taken back.

This does not reach into screenshots, which are images of the landing page as
served.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

MASK = "XXXXX"
PHONE_MASK = "XXXXXX"

# Words that make a local part a role mailbox rather than a person. Compared
# against the local part split on ".", "-", "_" and "+", so "elsi-helpdesk" and
# "eudat.support" both qualify.
ROLE_WORDS = frozenset(
    [
        "abuse",
        "base",
        "business",
        "cert",
        "csirt",
        "dih",
        "incident",
        "incidents",
        "infra",
        "infrastructure",
        "innovation",
        "noc",
        "partnerships",
        "report",
        "resources",
        "sit",
        "soc",
        "strategy",
        "vulnerability",
        "access",
        "accounting",
        "accounts",
        "admin",
        "administration",
        "applications",
        "ask",
        "board",
        "careers",
        "comms",
        "communication",
        "communications",
        "contact",
        "contacts",
        "coordination",
        "customer",
        "data",
        "desk",
        "dpo",
        "editor",
        "editorial",
        "email",
        "enquiries",
        "enquiry",
        "eosc",
        "event",
        "events",
        "feedback",
        "finance",
        "gdpr",
        "general",
        "hello",
        "help",
        "helpdesk",
        "helpline",
        "hd",
        "hr",
        "ict",
        "info",
        "information",
        "inquiries",
        "inquiry",
        "it",
        "jobs",
        "legal",
        "library",
        "mail",
        "mailbox",
        "management",
        "marketing",
        "media",
        "membership",
        "news",
        "newsletter",
        "no-reply",
        "node",
        "noreply",
        "office",
        "operations",
        "ops",
        "outreach",
        "partners",
        "policy",
        "postmaster",
        "press",
        "privacy",
        "project",
        "projects",
        "questions",
        "reception",
        "registration",
        "request",
        "requests",
        "research",
        "sales",
        "secretariat",
        "security",
        "service",
        "servicedesk",
        "services",
        "social",
        "staff",
        "support",
        "team",
        "tech",
        "technical",
        "ticket",
        "tickets",
        "training",
        "user",
        "users",
        "web",
        "webmaster",
        "welcome",
    ]
)

# A host label that makes every mailbox under it a role mailbox:
# it@helpdesk.bbmri-eric.eu, rd@helpdesk.bbmri-eric.eu.
ROLE_HOST_LABELS = frozenset({"helpdesk", "hd", "support", "servicedesk", "ticket", "tickets"})

_LOCAL = r"[A-Za-z0-9!#$%&'*+=?^_`{|}~.-]+"
# Labels, then an alphabetic top-level domain: "52.3326" in a map link is not a domain.
_DOMAIN = r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?![A-Za-z0-9-])"
_AT = r"(?:@|\s*[\[(]\s*at\s*[\])]\s*)"
EMAIL_RE = re.compile(
    rf"(?<![A-Za-z0-9._%+-])(?P<local>{_LOCAL})(?P<at>{_AT})(?P<domain>{_DOMAIN})"
)

# E.164 country codes are prefix-free: +1 and +7 are one digit, these are two,
# and every other code is three.
_TWO_DIGIT_CODES = frozenset(
    [
        "20",
        "27",
        "30",
        "31",
        "32",
        "33",
        "34",
        "36",
        "39",
        "40",
        "41",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "81",
        "82",
        "84",
        "86",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "98",
    ]
)

# "+", then digits with the separators people actually use: spaces, dots,
# hyphens, slashes and a "(0)" trunk prefix. At least 8 digits in all, so
# "+1000 users" and "+30%" stay as they are.
_INTL_RE = re.compile(r"(?<![\w+])\+\s?(?P<num>\d(?:[\d\s./-]|\(\d{1,4}\)){6,}\d)")
_LABEL_RE = re.compile(
    r"(?P<label>\b(?:phone|telephone|tel|mobile|mob|cell|fax|gsm|call)\b\.?\s*:?\s*)"
    r"(?P<num>\(?\d(?:[\d\s./-]|\(\d{1,4}\)){5,}\d)",
    re.IGNORECASE,
)
_MIN_DIGITS_INTL = 8
_MIN_DIGITS_LABEL = 6


def _fold(word: str) -> str:
    """Lowercase, with accents removed, so "Skřičková" compares equal to "skrickova"."""
    decomposed = unicodedata.normalize("NFKD", word)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).casefold()


def is_role_address(local: str, domain: str) -> bool:
    """True if the mailbox is a role or function rather than a person."""
    first_label = domain.split(".", 1)[0].casefold()
    if first_label in ROLE_HOST_LABELS:
        return True
    tokens = [t for t in re.split(r"[._+-]", local.casefold()) if t]
    if local.casefold() in ROLE_WORDS:
        return True
    if any(t in ROLE_WORDS for t in tokens):
        return True
    # The organisation's own mailbox: bbmri@bbmri-eric.eu, geant@geant.org.
    domain_parts = set(re.split(r"[.-]", domain.casefold()))
    return bool(tokens) and all(t in domain_parts for t in tokens)


def _name_tokens(local: str) -> set[str]:
    """Parts of a personal local part long enough to be a name: "jane.doe" -> {jane, doe}."""
    return {_fold(t) for t in re.split(r"[._+-]", local) if len(t) >= 3 and t.isalpha()}


def _is_personal(m: re.Match[str]) -> bool:
    local, domain = m.group("local"), m.group("domain")
    return local != MASK and not is_role_address(local, domain)


def _mask_email(m: re.Match[str]) -> str:
    if not _is_personal(m):
        return m.group(0)
    return f"{MASK}{m.group('at')}{m.group('domain')}"


def country_code(digits: str) -> str:
    """The E.164 country code at the start of an international number's digits."""
    if digits[:1] in ("1", "7"):
        return digits[:1]
    if digits[:2] in _TWO_DIGIT_CODES:
        return digits[:2]
    return digits[:3]


def _mask_intl(m: re.Match[str]) -> str:
    digits = re.sub(r"\D", "", m.group("num"))
    if len(digits) < _MIN_DIGITS_INTL:
        return m.group(0)
    return f"+{country_code(digits)} {PHONE_MASK}"


def _mask_labelled(m: re.Match[str]) -> str:
    digits = re.sub(r"\D", "", m.group("num"))
    if len(digits) < _MIN_DIGITS_LABEL:
        return m.group(0)
    # "00" is the international prefix dialled from most of Europe: keep the
    # country it names, as for a number written with "+".
    if digits.startswith("00") and len(digits) >= _MIN_DIGITS_INTL + 2:
        return f"{m.group('label')}+{country_code(digits[2:])} {PHONE_MASK}"
    return f"{m.group('label')}{PHONE_MASK}"


# How far from a personal address a name is looked for. "Mgr. Bc. Lucie
# Skřičková correspondence Address: skrickova@…" puts the name 40 characters
# before it. Looking only nearby keeps an address from masking an ordinary word
# that happens to share its spelling somewhere else on the page.
NAME_WINDOW = 120

_WORD_RE = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*\.?")


def _mask_names(text: str) -> str:
    """Mask the name of the person behind each personal address, near that address."""
    spans: list[tuple[int, int, set[str]]] = []
    for m in EMAIL_RE.finditer(text):
        if _is_personal(m):
            tokens = _name_tokens(m.group("local"))
            if tokens:
                spans.append((m.start() - NAME_WINDOW, m.end() + NAME_WINDOW, tokens))
    if not spans:
        return text
    words = list(_WORD_RE.finditer(text))
    hits: set[int] = set()
    for i, w in enumerate(words):
        word = w.group(0)
        # A title ends in a full stop (Mgr., Dr.); an all-capitals word is an
        # acronym (EBRAINS); a word straight after "/" or "." is part of a URL.
        if word.endswith(".") or (word.isupper() and len(word) > 1):
            continue
        if w.start() > 0 and text[w.start() - 1] in "/.@":
            continue
        near = [t for a, b, t in spans if a <= w.start() <= b]
        if not any(_fold(word) in t for t in near):
            continue
        hits.add(i)
        # A capitalised given name directly before the surname, but not a
        # title: "Mgr. Bc. Lucie Skřičková" keeps "Mgr. Bc." and masks the rest.
        if i > 0:
            prev = words[i - 1].group(0)
            gap = text[words[i - 1].end() : w.start()]
            if (
                prev[:1].isupper()
                and not prev.endswith(".")
                and not prev.isupper()
                and not gap.strip()
            ):
                hits.add(i - 1)
    if not hits:
        return text
    out, pos = [], 0
    for i in sorted(hits):
        w = words[i]
        out.append(text[pos : w.start()])
        out.append(MASK)
        pos = w.end()
    out.append(text[pos:])
    return "".join(out)


def mask_text(text: str) -> str:
    """Mask personal email addresses, phone numbers and the names beside the addresses."""
    text = _mask_names(text)
    text = EMAIL_RE.sub(_mask_email, text)
    text = _LABEL_RE.sub(_mask_labelled, text)
    return _INTL_RE.sub(_mask_intl, text)


def mask_data(obj: Any) -> Any:
    """A copy of a JSON-like structure with every string value masked. Keys are left alone."""
    if isinstance(obj, str):
        return mask_text(obj)
    if isinstance(obj, dict):
        return {k: mask_data(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [mask_data(v) for v in obj]
    return obj
