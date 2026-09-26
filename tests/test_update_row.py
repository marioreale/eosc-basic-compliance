"""--update-results-for-node: replace one row of the stored results, keep the rest.

Every test works on a copy of the committed results/ directory in tmp_path, so
neither results/ nor any node website is touched. The `run` path is exercised
with `_do_collect` replaced by a stand-in that writes evidence into the staging
directory it is given, exactly where the real collector would.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from basic_check import cli

PUBLISHED = cli.DEFAULT_RESULTS


@pytest.fixture
def stored(tmp_path) -> Path:
    """A copy of the published run: results.json, reports and evidence."""
    out = tmp_path / "results"
    shutil.copytree(PUBLISHED, out, ignore=shutil.ignore_patterns("one-off"))
    return out


def _load(results: Path) -> dict:
    return json.loads((results / "results.json").read_text(encoding="utf-8"))


def _tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(root).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _invoke(*args):
    return CliRunner().invoke(cli.app, list(args), env={"COLUMNS": "200"})


def _fake_collect(evidence: dict, monkeypatch, calls: list | None = None):
    """Replace the collector: write `evidence` for the one node it is asked for."""

    def fake(nodes, results_dir, *a, **k):
        assert len(nodes) == 1, "an update must collect exactly one node"
        if calls is not None:
            calls.append((nodes[0]["id"], Path(results_dir)))
        ev_dir = Path(results_dir) / "evidence"
        (ev_dir / "screenshots").mkdir(parents=True, exist_ok=True)
        data = dict(evidence, node_id=nodes[0]["id"], node_name=nodes[0]["name"])
        (ev_dir / f"{nodes[0]['id']}.json").write_text(json.dumps(data), encoding="utf-8")
        if data.get("screenshot"):
            (ev_dir / "screenshots" / data["screenshot"]).write_bytes(b"new png")

    monkeypatch.setattr(cli, "_do_collect", fake)


def _egi_evidence(stored: Path, **changes) -> dict:
    ev = json.loads((stored / "evidence" / "egi.json").read_text(encoding="utf-8"))
    ev.update(changes)
    return ev


def test_published_results_are_the_run_these_tests_copy():
    """The fixture relies on the committed run: rows and evidence for 12 nodes."""
    run = _load(PUBLISHED)
    assert len(run["nodes"]) == 12 and run["skipped"] == ["eosc-it"]
    assert "row_updates" not in run


def test_assess_update_replaces_only_that_row_and_keeps_the_others(stored, monkeypatch):
    monkeypatch.setattr(cli, "_do_collect", lambda *a, **k: pytest.fail("assess must not fetch"))
    before = _load(stored)
    review = (stored / "REVIEW-2026-09-24.md").read_bytes()
    res = _invoke("assess", "--update-results-for-node", "EGI", "--results", str(stored))
    assert res.exit_code == 0, res.output
    after = _load(stored)
    assert [n["id"] for n in after["nodes"]] == [n["id"] for n in before["nodes"]]
    for old, new in zip(before["nodes"], after["nodes"], strict=True):
        # Same evidence, same rules: even the re-judged row comes out identical.
        assert old == new, old["id"]
    assert after["run_id"] == before["run_id"]
    assert after["generated_at"] == before["generated_at"]
    (update,) = after["row_updates"]
    assert update["id"] == "egi" and update["how"].startswith("assess")
    assert update["previous"]["verdicts"]["4"] == "FAIL"
    assert (stored / "REVIEW-2026-09-24.md").read_bytes() == review


def test_the_reports_gain_an_updated_rows_banner_and_nothing_else(stored):
    old_md = (stored / "results.md").read_text(encoding="utf-8").splitlines()
    assert _invoke("assess", "--update-results-for-node", "egi", "--results", str(stored)).exit_code == 0
    new_md = (stored / "results.md").read_text(encoding="utf-8").splitlines()
    added = [line for line in new_md if line not in old_md]
    assert [line for line in old_md if line not in new_md] == []
    assert len(added) == 1 and added[0].startswith("> **Updated rows.** This row was updated")
    assert "egi on " in added[0] and "neither re-fetched nor re-judged" in added[0]
    assert "Updated rows." in (stored / "index.html").read_text(encoding="utf-8")


def test_run_update_fetches_one_node_and_merges_its_new_evidence(stored, monkeypatch):
    calls: list = []
    new = _egi_evidence(
        stored, fetched_at="2026-09-26T04:00:00+00:00", title="EGI Node, new page"
    )
    _fake_collect(new, monkeypatch, calls)
    before = _load(stored)
    res = _invoke("run", "--update-results-for-node", "egi", "--results", str(stored))
    assert res.exit_code == 0, res.output
    (node_id, staging), = calls
    assert node_id == "egi" and stored not in staging.parents and staging != stored
    assert not staging.exists(), "the scratch directory is removed after a merge"
    after = _load(stored)
    egi = next(n for n in after["nodes"] if n["id"] == "egi")
    assert egi["fetch"]["fetched_at"] == "2026-09-26T04:00:00+00:00"
    ev = json.loads((stored / "evidence" / "egi.json").read_text(encoding="utf-8"))
    assert ev["title"] == "EGI Node, new page"
    assert (stored / "evidence" / "screenshots" / "egi.png").read_bytes() == b"new png"
    for old, cur in zip(before["nodes"], after["nodes"], strict=True):
        if old["id"] != "egi":
            assert old == cur, old["id"]
    assert after["row_updates"][-1]["how"].startswith("run")


def test_a_new_capture_without_a_screenshot_removes_the_old_one(stored, monkeypatch):
    _fake_collect(_egi_evidence(stored, screenshot=""), monkeypatch)
    assert (stored / "evidence" / "screenshots" / "egi.png").exists()
    assert _invoke("run", "--update-results-for-node", "egi", "--results", str(stored)).exit_code == 0
    assert not (stored / "evidence" / "screenshots" / "egi.png").exists()


def test_a_failed_fetch_changes_nothing_unless_accepted(stored, monkeypatch):
    failed = _egi_evidence(stored, http_status=None, error="net::ERR_NAME_NOT_RESOLVED")
    _fake_collect(failed, monkeypatch)
    digest = _tree_digest(stored)
    res = _invoke("run", "--update-results-for-node", "egi", "--results", str(stored))
    assert res.exit_code == 1
    assert "Nothing was changed" in res.output and "--accept-error" in res.output
    assert _tree_digest(stored) == digest

    res = _invoke(
        "run", "--update-results-for-node", "egi", "--accept-error", "--results", str(stored)
    )
    assert res.exit_code == 0, res.output
    egi = next(n for n in _load(stored)["nodes"] if n["id"] == "egi")
    assert egi["fetch"]["error"] == "net::ERR_NAME_NOT_RESOLVED"


def test_a_node_the_run_skipped_is_inserted_in_nodes_yaml_order(stored, monkeypatch):
    italy = _egi_evidence(stored, requested_url="https://eosc.it/", final_url="https://eosc.it/")
    italy["screenshot"] = "eosc-it.png"
    _fake_collect(italy, monkeypatch)
    res = _invoke("run", "--update-results-for-node", "Italy", "--results", str(stored))
    assert res.exit_code == 0, res.output
    after = _load(stored)
    ids = [n["id"] for n in after["nodes"]]
    assert ids[ids.index("eosc-it") - 1 : ids.index("eosc-it") + 2] == ["ebrains", "eosc-it", "eosc-sk"]
    assert after["skipped"] == []
    assert after["row_updates"][-1]["previous"] is None


def test_evidence_from_another_url_is_flagged_on_that_row(stored):
    """bbmri-eric's stored evidence is from the old URL; nodes.yaml has the new one."""
    assert _invoke(
        "assess", "--update-results-for-node", "bbmri-eric", "--results", str(stored)
    ).exit_code == 0
    after = _load(stored)
    (m,) = after["url_mismatch"]
    assert m["id"] == "bbmri-eric" and m["evidence_url"].startswith("https://www.bbmri-eric.eu/")
    assert "Evidence from a different URL" in (stored / "results.md").read_text(encoding="utf-8")


def test_refuses_without_stored_results(tmp_path):
    with pytest.raises(typer.BadParameter, match="no stored results"):
        cli._update_results_for_node(
            "egi", tmp_path, cli.DEFAULT_NODES, cli.DEFAULT_CHECKLIST, None, False, False,
            fetch=False,
        )


def test_refuses_a_different_checklist(stored, tmp_path):
    other = tmp_path / "v9.yaml"
    text = cli.DEFAULT_CHECKLIST.read_text(encoding="utf-8")
    assert 'checklist_version: "3.0"' in text
    other.write_text(text.replace('checklist_version: "3.0"', 'checklist_version: "9.9"'), encoding="utf-8")
    digest = _tree_digest(stored)
    with pytest.raises(typer.BadParameter, match="not the checklist"):
        cli._update_results_for_node(
            "egi", stored, cli.DEFAULT_NODES, other, None, False, False, fetch=False
        )
    assert _tree_digest(stored) == digest


@pytest.mark.parametrize(
    "names_args",
    [
        {"no_approved_names": True},
        {"approved_names": cli.SCOPED_APPROVED_NAMES},
        {"strict_separators": True},
    ],
)
def test_refuses_a_different_approved_name_list(stored, names_args):
    kwargs = {"approved_names": None, "no_approved_names": False, "strict_separators": False}
    kwargs.update(names_args)
    digest = _tree_digest(stored)
    with pytest.raises(typer.BadParameter, match="approved-name list differs"):
        cli._update_results_for_node(
            "egi", stored, cli.DEFAULT_NODES, cli.DEFAULT_CHECKLIST,
            kwargs["approved_names"], kwargs["no_approved_names"], kwargs["strict_separators"],
            fetch=False,
        )
    assert _tree_digest(stored) == digest


def test_refuses_an_unknown_node(stored):
    with pytest.raises(typer.BadParameter, match="no node matches"):
        cli._update_results_for_node(
            "atlantis", stored, cli.DEFAULT_NODES, cli.DEFAULT_CHECKLIST, None, False, False,
            fetch=False,
        )


def test_refuses_an_alternative_url_trial(stored):
    run = _load(stored)
    run["alternative_url"] = [{"id": "egi", "configured_url": "x", "url": "y"}]
    (stored / "results.json").write_text(json.dumps(run), encoding="utf-8")
    with pytest.raises(typer.BadParameter, match="alternative-URL trial"):
        cli._update_results_for_node(
            "egi", stored, cli.DEFAULT_NODES, cli.DEFAULT_CHECKLIST, None, False, False,
            fetch=False,
        )


@pytest.mark.parametrize(
    "extra",
    [["--only", "cern"], ["--skip", "cern"], ["--url", "https://x.example/"],
     ["--node", "cern"], ["--run", "r1"]],
)
def test_refuses_options_that_select_other_nodes_or_another_run(stored, extra, monkeypatch):
    monkeypatch.setattr(cli, "_do_collect", lambda *a, **k: pytest.fail("must not fetch"))
    digest = _tree_digest(stored)
    for command in ("run", "assess"):
        res = _invoke(command, "--update-results-for-node", "egi", *extra, "--results", str(stored))
        assert res.exit_code == 2, (command, res.output)
    assert _tree_digest(stored) == digest


def test_accept_error_needs_update_results_for_node(monkeypatch):
    monkeypatch.setattr(cli, "_do_collect", lambda *a, **k: pytest.fail("must not fetch"))
    assert _invoke("run", "--accept-error", "--only", "egi").exit_code == 2


def test_both_commands_document_the_option():
    for command in ("run", "assess"):
        res = _invoke(command, "--help")
        assert "--update-results-for-node" in re.sub(r"\x1b\[[0-9;]*m", "", res.output)
