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
3. **Matching.** Boundary-aware and literal. `EGI` no longer matches
   "strat**egi**c" or "Norw**egi**an", which it did on real node pages.

File format, one entry per line::

    # comments and blank lines are ignored
    EOSC Node EUDAT                     # applies to any node
    bbmri-eric: EOSC Node - BBMRI-ERIC  # applies to that node only

Write `\\#` for a literal hash in a name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["ApprovedNames", "parse_approved_names"]

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


@dataclass(frozen=True)
class ApprovedNames:
    """Names that may satisfy point 3, optionally scoped per node."""

    unscoped: tuple[str, ...] = ()
    per_node: dict[str, tuple[str, ...]] = field(default_factory=dict)

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

    def match(self, text: str, node_id: str) -> str | None:
        """The first name, in file order, that appears in `text` for this node.

        Matching is literal, case-insensitive and boundary-aware: internal
        whitespace in a name matches any run of whitespace in the text, so a
        name that wraps across a line still matches, but a name must not be a
        fragment of a longer word.
        """
        for name in self.for_node(node_id):
            if re.search(_pattern(name), text, re.I | re.S):
                return name
        return None

    # --- construction --------------------------------------------------------

    @classmethod
    def load(cls, path: Path | None) -> ApprovedNames:
        """Parse `path`, or return an unsupplied list when `path` is None.

        A path that does not exist raises: the caller asked for a list, and
        proceeding without one would leave point 3 quietly unassessed.
        """
        if path is None:
            return cls()
        return parse_approved_names(Path(path).read_text(encoding="utf-8"))

    @classmethod
    def coerce(cls, value: ApprovedNames | list[str] | None) -> ApprovedNames:
        """Accept this class, a plain list of names, or None."""
        if value is None:
            return cls()
        if isinstance(value, ApprovedNames):
            return value
        return cls(unscoped=tuple(str(v).strip() for v in value if str(v).strip()))


def parse_approved_names(text: str) -> ApprovedNames:
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
    )


def _pattern(name: str) -> str:
    """A literal, boundary-aware, whitespace-tolerant pattern for `name`."""
    body = r"\s+".join(re.escape(part) for part in name.split())
    # Guard only an edge that is itself word-like. "EGI" gets both guards, so
    # "strategic" cannot match. "(Finland)" ends in a paren, which is already a
    # boundary, so demanding another would reject a legitimate page.
    lead = r"(?<![\w-])" if name[:1] and _WORDISH.match(name[0]) else ""
    trail = r"(?![\w-])" if name[-1:] and _WORDISH.match(name[-1]) else ""
    return lead + body + trail
