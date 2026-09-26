"""Structural guards on `nodes.yaml`.

`nodes.yaml` is the file a human edits to add a node, and nothing in the run
path validates it: `collect` reads the entries and starts fetching. A malformed
entry therefore fails late, on the network, after the tool has already made
requests to other people's servers — or, worse, does not fail at all and
quietly weakens a verdict.

The specific hazard is `eosc_page`. Point 4 asks whether the landing page links
to the node's own entry on eosc.eu. `checks.run_all` is called with
`node.get('eosc_page', '')`, so an entry that omits it is not an error: point 4
still runs, but it can no longer name the URL it was looking for. A node added
without it gets a weaker check than the nine that have it, and the report does
not say so. These tests make that omission loud at collection time.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("id", "name", "url", "eosc_page")


def _nodes() -> list[dict]:
    return yaml.safe_load((ROOT / "nodes.yaml").read_text(encoding="utf-8"))["nodes"]


@pytest.fixture(scope="module")
def nodes() -> list[dict]:
    return _nodes()


def test_the_file_parses_and_is_not_empty(nodes):
    assert nodes, "nodes.yaml declares no nodes"


@pytest.mark.parametrize("field", REQUIRED)
def test_every_node_declares_every_required_field(nodes, field):
    """A missing `eosc_page` silently weakens point 4 rather than failing."""
    missing = [n.get("id", "<no id>") for n in nodes if not str(n.get(field, "")).strip()]
    assert not missing, f"node(s) with no {field}: {missing}"


def test_node_ids_are_unique(nodes):
    """Two entries sharing an id would overwrite each other's evidence file:
    evidence is written per node id, so one node's capture would be lost."""
    ids = [n["id"] for n in nodes]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"duplicate node id(s): {dupes}"


def test_node_ids_are_safe_as_filenames_and_cli_values(nodes):
    """Ids reach the filesystem as `results/evidence/<id>.json` and the CLI as
    `--only <id>`, so a slash, space or comma would break one or the other."""
    for n in nodes:
        nid = n["id"]
        assert nid == nid.lower(), f"{nid}: ids are matched lowercased, so declare them lowercase"
        assert nid.replace("-", "").replace("_", "").isalnum(), (
            f"{nid}: use only letters, digits, hyphen and underscore — "
            "an id becomes a filename and a --only value"
        )


def test_every_url_is_absolute_and_https(nodes):
    """A relative or scheme-less URL fails inside the browser, one node into a
    run that has already started fetching."""
    for n in nodes:
        for field in ("url", "eosc_page"):
            parsed = urlparse(n.get(field, ""))
            assert parsed.scheme == "https", f"{n['id']}.{field}: expected https, got {n[field]!r}"
            assert parsed.netloc, f"{n['id']}.{field}: no host in {n[field]!r}"


def test_landing_page_urls_are_unique(nodes):
    """Two nodes pointing at one page is far more likely a copy-paste slip than
    a real federation arrangement, and it would report the same evidence twice
    under two names."""
    urls = [n.get("url", "").rstrip("/") for n in nodes]
    dupes = {u for u in urls if urls.count(u) > 1}
    assert not dupes, f"shared landing page URL(s): {dupes}"


def test_eosc_pages_are_unique(nodes):
    """Each node has its own entry on eosc.eu. Two nodes sharing one is a
    copy-paste slip when adding similar entries, and it is not harmless: point 4
    would look for the wrong node's page, and a node could fail a requirement it
    satisfies. Every other guard passes on such a slip, so this one must exist."""
    pages = [n.get("eosc_page", "").rstrip("/") for n in nodes]
    dupes = {p for p in pages if pages.count(p) > 1}
    assert not dupes, f"shared eosc_page URL(s): {dupes}"


def test_every_eosc_page_is_on_eosc_eu(nodes):
    """Point 4 is specifically about the node's entry on eosc.eu. Pointing
    `eosc_page` anywhere else would make the check pass on the wrong link."""
    for n in nodes:
        host = urlparse(n.get("eosc_page", "")).netloc
        assert host.endswith("eosc.eu"), f"{n['id']}: eosc_page is not on eosc.eu: {host}"


def test_no_eosc_page_is_the_federation_index(nodes):
    """The index lists every node, so linking it satisfies nothing about *this*
    node — the checklist excludes it explicitly, and a run has already found a
    node linking the index instead of its own page.
    """
    for n in nodes:
        path = urlparse(n.get("eosc_page", "")).path.strip("/")
        assert path != "building-the-eosc-federation", (
            f"{n['id']}: eosc_page is the federation index, not this node's entry"
        )


def test_every_node_has_a_scoped_approved_name(nodes):
    """Kept here as well as in test_checklist.py because this is the file a
    person edits when adding a node, and the two files must move together."""
    from basic_check.names import parse_approved_names

    scoped = parse_approved_names(
        (ROOT / "checklist" / "approved-names-scoped.txt").read_text(encoding="utf-8")
    )
    missing = [n["id"] for n in nodes if not scoped.per_node.get(n["id"])]
    assert not missing, (
        f"node(s) with no name in checklist/approved-names-scoped.txt: {missing}"
    )


def test_shipped_default_is_the_committed_nodes_yaml():
    """--restore-default-config puts back src/basic_check/defaults/nodes.yaml.
    It must be exactly the nodes.yaml committed in this revision, so a restore
    gives what was downloaded from GitHub. Compared with the committed file
    (git HEAD), not the working copy, so a local --update-nlp does not fail
    the suite; skipped outside a git checkout (a zip download)."""
    import shutil
    import subprocess

    if shutil.which("git") is None or not (ROOT / ".git").exists():
        pytest.skip("not a git checkout")
    committed = subprocess.run(
        ["git", "show", "HEAD:nodes.yaml"], cwd=ROOT, capture_output=True, check=True
    ).stdout
    shipped = (ROOT / "src" / "basic_check" / "defaults" / "nodes.yaml").read_bytes()
    assert shipped == committed, (
        "src/basic_check/defaults/nodes.yaml differs from the committed nodes.yaml; "
        "copy nodes.yaml over it in the same commit"
    )
