"""The Tripartite-approved node name list, and how it is matched.

Checklist point 3 asks whether the page shows "the official Tripartite-approved
node name". There is no machine-readable source for those names, so the list is
an input the operator supplies. This module owns three things that were
previously done inline, badly:

1. **Parsing.** Comments and per-node scoping, so a name can be tied to the
   node it belongs to instead of floating free over the whole run.
2. **Scoping.** `for_node` returns only the names that may satisfy *that* node.
   An unscoped list is still accepted, and still applies everywhere, because
   that is what earlier runs did — but it is reported as unscoped so a reader
   knows the weaker claim is the one being made.
3. **Matching.** Boundary-aware and literal in the tokens, tolerant only of the
   separator between them. `EGI` no longer matches "strat**egi**c" or
   "Norw**egi**an", which it did on real node pages; `EOSC Node | X` still
   matches a page that writes `EOSC Node - X`, because the glyph between the
   words is typography, not identity.

File format, one entry per line::

    # comments and blank lines are ignored
    EOSC Node | EUDAT                   # applies to any node
    bbmri-eric: EOSC Node - BBMRI-ERIC  # applies to that node only

Write `\\#` for a literal hash in a name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["ApprovedNames", "NameMatch", "parse_approved_names"]

# A leading "<id>:" scopes the entry. Node ids are slugs — letters, digits,
# hyphens, underscores, dots — so a name containing a colon ("EOSC Node:
# Finland") is not mistaken for one.
_SCOPED = re.compile(r"^(?P<node>[A-Za-z0-9._-]+)\s*:\s*(?P<name>\S.*)$")

# An unescaped hash starts a trailing comment.
_COMMENT = re.compile(r"(?<!\\)#.*$")

# What may not touch a name: word characters, and a hyphen. The hyphen matters
# because "BBMRI" and "BBMRI-ERIC" are different names, so a page showing the
# second does not show the first.
_WORDISH = re.compile(r"[\w-]")

# Separator glyphs that node pages use interchangeably in a name lockup. The
# official list writes "EOSC Node | X"; of the nine nodes, one writes the pipe,
# one writes a hyphen and an en dash, and one writes nothing at all. Matching
# the pipe literally scored 0/9 against real pages.
_SEPS = "|\u2013\u2014\u2012\u2015:/\u00b7\u2022-"

# In a name, a separator glyph that stands alone (whitespace on at least one
# side) or a plain run of whitespace. A hyphen *inside* a token — BBMRI-ERIC —
# does not match this, and stays literal.
_NAME_GAP = re.compile(rf"\s+[{re.escape(_SEPS)}]\s*|\s*[{re.escape(_SEPS)}]\s+|\s+")

# What such a gap may match in the page: any run of whitespace and separators,
# or nothing at all where the page joins the words with a single space that the
# name spells as " | ". At least one character is required, so two tokens can
# never fuse: "EOSC Node" cannot match "EOSCNode".
_PAGE_GAP = rf"[\s{re.escape(_SEPS)}]+"


@dataclass(frozen=True)
class ApprovedNames:
    """Names that may satisfy point 3, optionally scoped per node."""

    unscoped: tuple[str, ...] = ()
    per_node: dict[str, tuple[str, ...]] = field(default_factory=dict)
    # Match separator glyphs literally instead of treating them as
    # interchangeable. Off by default, because the flexible rule is what makes
    # the official list match any page at all; on, for anyone who wants the
    # stricter reading. Carried on the list rather than passed to each call so
    # the report can state which rule was in force.
    strict_separators: bool = False

    @property
    def supplied(self) -> bool:
        """True when any name at all was supplied."""
        return bool(self.unscoped or self.per_node)

    @property
    def scoped(self) -> bool:
        """True when at least one name is tied to a specific node."""
        return bool(self.per_node)

    def for_node(self, node_id: str) -> list[str]:
        """Names that may satisfy `node_id`: its own first, then unscoped ones."""
        own = self.per_node.get(node_id.lower(), ())
        return [*own, *self.unscoped]

    def is_scoped_to(self, node_id: str, name: str) -> bool:
        """True when `name` was written against this node specifically."""
        return name in self.per_node.get(node_id.lower(), ())

    def find(self, text: str, node_id: str) -> NameMatch | None:
        """The first name, in file order, that appears in `text` for this node.

        Matching is case-insensitive and boundary-aware. Each token of the name
        is literal, so a name is never a fragment of a longer word. The gap
        between tokens is not: whitespace and the separator glyphs pages use in
        a name lockup are interchangeable, so a list written "EOSC Node | X"
        matches a page that writes "EOSC Node - X".

        Returns what the page actually shows as well as which approved name it
        satisfied, so a reviewer can see a variant rendering rather than being
        told only that something matched.
        """
        for name in self.for_node(node_id):
            if m := re.search(_pattern(name, self.strict_separators), text, re.I | re.S):
                return NameMatch(
                    name=name,
                    matched_text=" ".join(m.group(0).split()),
                    scoped=self.is_scoped_to(node_id, name),
                )
        return None

    def match(self, text: str, node_id: str) -> str | None:
        """The approved name that `text` satisfies, or None. See `find`."""
        m = self.find(text, node_id)
        return m.name if m else None

    def common_prefix(self, node_id: str) -> str:
        """The leading tokens every candidate name for this node shares.

        The official list writes all nine names as "EOSC Node | X", so the
        shared prefix is "EOSC Node". Derived rather than hardcoded, so a list
        using another convention gets the same treatment and a list with
        nothing in common gets none.
        """
        tokens = [[t for t in _NAME_GAP.split(n.strip()) if t] for n in self.for_node(node_id)]
        if len(tokens) < 2:
            return ""
        shared: list[str] = []
        for parts in zip(*tokens, strict=False):
            first = parts[0].casefold()
            if any(p.casefold() != first for p in parts):
                break
            shared.append(parts[0])
        return " ".join(shared)

    def prefix_hits(self, text: str, node_id: str) -> tuple[str, int]:
        """The shared prefix of the candidate names, and how often it occurs.

        "None of the approved names appear" is true but gives a reviewer
        nowhere to look, and seven of the nine node pages do show *a* name.
        This points at the phrase to search for and says how many times it is
        there, which is checkable, rather than quoting a guess at the name.

        An earlier version quoted the surrounding text. It produced "EOSC Node
        f" on one page (truncated at an ellipsis) and, on another, quoted a
        sentence about a *different* node as if it were that page's name. A
        confident wrong quote is worse than saying less, so it was removed.
        """
        prefix = self.common_prefix(node_id)
        if not prefix:
            return "", 0
        return prefix, len(re.findall(_pattern(prefix, self.strict_separators), text, re.I | re.S))

    # --- construction --------------------------------------------------------

    @classmethod
    def load(cls, path: Path | None, strict_separators: bool = False) -> ApprovedNames:
        """Parse `path`, or return an unsupplied list when `path` is None.

        A path that does not exist raises: the caller asked for a list, and
        proceeding without one would leave point 3 quietly unassessed.
        """
        if path is None:
            return cls()
        return parse_approved_names(
            Path(path).read_text(encoding="utf-8"), strict_separators=strict_separators
        )

    @classmethod
    def coerce(cls, value: ApprovedNames | list[str] | None) -> ApprovedNames:
        """Accept this class, a plain list of names, or None."""
        if value is None:
            return cls()
        if isinstance(value, ApprovedNames):
            return value
        return cls(unscoped=tuple(str(v).strip() for v in value if str(v).strip()))


@dataclass(frozen=True)
class NameMatch:
    """A name that matched, and the text on the page that satisfied it."""

    name: str
    matched_text: str
    scoped: bool

    @property
    def exact(self) -> bool:
        """True when the page writes the name as the approved list writes it.

        Case and the amount of whitespace are not differences worth reporting;
        a different separator glyph is, because it is the thing the reviewer
        would otherwise have to diff by eye.
        """
        return " ".join(self.name.split()).casefold() == self.matched_text.casefold()


def parse_approved_names(text: str, strict_separators: bool = False) -> ApprovedNames:
    """Parse the approved-names file format."""
    unscoped: list[str] = []
    per_node: dict[str, list[str]] = {}

    for raw in text.splitlines():
        line = _COMMENT.sub("", raw).replace("\\#", "#").strip()
        if not line:
            continue
        if m := _SCOPED.match(line):
            node = m.group("node").lower()
            per_node.setdefault(node, []).append(m.group("name").strip())
        else:
            unscoped.append(line)

    return ApprovedNames(
        unscoped=tuple(unscoped),
        per_node={k: tuple(v) for k, v in per_node.items()},
        strict_separators=strict_separators,
    )


def _pattern(name: str, strict_separators: bool = False) -> str:
    """A boundary-aware pattern: literal tokens, interchangeable separators.

    Under `strict_separators`, every character of the name is literal except the
    amount of whitespace: a name that wraps across two lines is still the same
    name, but a page writing a hyphen where the list writes a pipe is not.
    """
    if strict_separators:
        body = r"\s+".join(re.escape(t) for t in name.split())
    else:
        tokens = [t for t in _NAME_GAP.split(name.strip()) if t]
        body = _PAGE_GAP.join(re.escape(t) for t in tokens)
    # Guard only an edge that is itself word-like. "EGI" gets both guards, so
    # "strategic" cannot match. "(Finland)" ends in a paren, which is already a
    # boundary, so demanding another would reject a legitimate page.
    lead = r"(?<![\w-])" if name[:1] and _WORDISH.match(name[0]) else ""
    trail = r"(?![\w-])" if name[-1:] and _WORDISH.match(name[-1]) else ""
    return lead + body + trail
