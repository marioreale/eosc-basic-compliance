"""Tests for the command line surface.

The rest of the suite tests rules against in-memory evidence and never touches
the CLI. That gap hid a real bug: `basic-check run` crashed with "'OptionInfo'
object has no attribute 'read_text'" for every invocation, because calling a
Typer-decorated function from Python passes its option *descriptors* rather than
their values. It was documented in the README as a working command and shipped
broken. These tests exercise argument handling and the command wiring, still
without any network access.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from basic_check import cli

# --- id derivation ------------------------------------------------------------


def test_slug_includes_the_path_so_shared_hosts_do_not_collide():
    """Several node pages can live on one host; a hostname-only id would make
    two different pages overwrite each other's evidence file."""
    assert cli._slug("https://eosc.eu/node-a/") != cli._slug("https://eosc.eu/node-b/")


def test_slug_ignores_www_and_trailing_slash():
    assert cli._slug("https://www.eosc.eu/a") == cli._slug("https://eosc.eu/a/")


def test_slug_is_filesystem_safe():
    slug = cli._slug("https://ex.org/a b/c?d=1&e=2")
    assert all(c.isalnum() or c == "-" for c in slug), slug


# --- building nodes from bare URLs --------------------------------------------


def test_a_url_becomes_a_node_record():
    (node,) = cli._nodes_from_urls(["https://www.example.org/eosc/"])
    assert node["url"] == "https://www.example.org/eosc/"
    assert node["name"] == "example.org"
    assert node["ad_hoc"] is True


def test_ad_hoc_is_flagged_so_reports_can_say_so():
    """A one-off report otherwise looks identical to the federation run, and this
    one gets circulated before a production decision."""
    nodes = cli._nodes_from_urls(["https://a.example/"])
    assert all(n["ad_hoc"] for n in nodes)


@pytest.mark.parametrize(
    "bad", ["notaurl", "example.org", "ftp://example.org/x", "/local/path", "", "https://"]
)
def test_non_http_urls_are_rejected(bad):
    with pytest.raises(typer.BadParameter):
        cli._nodes_from_urls([bad])


def test_the_same_page_twice_is_rejected_rather_than_silently_deduplicated():
    """Two --url flags but one row in the report would be a quietly short table."""
    with pytest.raises(typer.BadParameter):
        cli._nodes_from_urls(["https://a.example/x", "https://www.a.example/x/"])


def test_eosc_page_is_carried_through_so_point_4_can_name_the_missing_url():
    (node,) = cli._nodes_from_urls(
        ["https://a.example/"], eosc_page="https://eosc.eu/building-the-eosc-federation/x/"
    )
    assert node["eosc_page"].endswith("/x/")


def test_eosc_page_with_several_urls_is_rejected():
    """One expected eosc.eu page cannot apply to several different nodes."""
    with pytest.raises(typer.BadParameter):
        cli._nodes_from_urls(["https://a.example/", "https://b.example/"], eosc_page="https://eosc.eu/x")


# --- resolution: what gets checked, and where it is written -------------------


def test_url_runs_are_written_somewhere_else_by_default():
    """The decisive property. assess() rewrites results.md, index.html and
    results.json wholesale, so a one-off check sharing the directory would
    replace the committed multi-node report with a one-row table."""
    _, _, out = cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "", None)
    assert out == cli.DEFAULT_ONEOFF
    assert out != cli.DEFAULT_RESULTS


def test_the_configured_run_still_writes_to_the_normal_place():
    nodes, reported, out = cli._resolve(None, cli.DEFAULT_NODES, "", None)
    assert out == cli.DEFAULT_RESULTS
    assert len(nodes) > 1
    assert nodes == reported


def test_an_explicit_results_dir_still_wins_for_a_url_run():
    _, _, out = cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "", Path("/tmp/custom"))
    assert out == Path("/tmp/custom")


def test_url_and_only_together_are_rejected():
    """--only filters ids in the nodes file; an ad hoc URL has no id there, so
    combining them can only mean the user misunderstood one of the two."""
    with pytest.raises(typer.BadParameter):
        cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "egi", None)


def test_eosc_page_without_url_is_rejected():
    with pytest.raises(typer.BadParameter):
        cli._resolve(None, cli.DEFAULT_NODES, "", None, eosc_page="https://eosc.eu/x")


def test_blank_urls_do_not_count_as_a_url_run():
    nodes, _reported, out = cli._resolve(["", "  "], cli.DEFAULT_NODES, "", None)
    assert out == cli.DEFAULT_RESULTS
    assert len(nodes) > 1


# --- the wiring bug that shipped ---------------------------------------------


def test_run_does_not_pass_typer_descriptors_to_its_helpers():
    """`run` must call the plain _do_* functions, not the decorated commands.

    Calling a Typer command from Python hands it OptionInfo objects for every
    argument the caller omitted, which then fail on first real use. That is what
    broke `basic-check run`.
    """
    import ast
    import inspect
    import textwrap

    tree = ast.parse(textwrap.dedent(inspect.getsource(cli.run)))
    called = {
        n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    }
    assert {"_do_collect", "_do_assess"} <= called, called
    assert not ({"collect", "assess"} & called), (
        f"run calls the Typer command(s) {sorted({'collect', 'assess'} & called)} directly, "
        "which passes OptionInfo descriptors instead of values"
    )


def test_the_do_helpers_have_no_typer_defaults():
    """A plain default of typer.Option(...) would reintroduce the same bug."""
    import inspect

    for fn in (cli._do_collect, cli._do_assess):
        for name, param in inspect.signature(fn).parameters.items():
            assert not isinstance(param.default, type(typer.Option(None))), (
                f"{fn.__name__}({name}=...) carries a Typer default"
            )


# --- --only must not overwrite the published report with a subset -------------


def _full_results_dir(tmp_path):
    """A stand-in for the committed results/ dir, with evidence for all nodes."""
    import shutil

    from basic_check.cli import ROOT

    out = tmp_path / "results"
    shutil.copytree(ROOT / "results" / "evidence", out / "evidence")
    return out


def _nodes_covering(tmp_path, results_dir):
    """A nodes.yaml listing exactly the nodes `results_dir` has evidence for.

    Keeps these tests about `--only` rather than about how many nodes are
    configured: a node added to nodes.yaml before its first `collect` has no
    evidence, and `assess` then exits 2 by design.
    """
    import yaml

    from basic_check.cli import ROOT

    have = {p.stem for p in (results_dir / "evidence").glob("*.json")}
    all_nodes = yaml.safe_load((ROOT / "nodes.yaml").read_text(encoding="utf-8"))["nodes"]
    kept = [n for n in all_nodes if n["id"] in have]
    path = tmp_path / "nodes-covered.yaml"
    path.write_text(yaml.safe_dump({"nodes": kept}, allow_unicode=True), encoding="utf-8")
    return path, len(kept)


def test_only_does_not_shrink_the_report_in_the_published_directory(monkeypatch, tmp_path):
    """The defect: `assess --only egi` rewrote results/results.md, index.html and
    results.json wholesale with a single row, so the published multi-node report
    was replaced by a one-node report that looked complete. --only exists to
    limit which sites get fetched, not to narrow what is reported.
    """
    import json

    from basic_check import cli

    out = _full_results_dir(tmp_path)
    nodes_file, expected = _nodes_covering(tmp_path, out)
    monkeypatch.setattr(cli, "DEFAULT_RESULTS", out)
    res = CliRunner().invoke(
        cli.app,
        ["assess", "--only", "egi", "--nodes", str(nodes_file)],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    data = json.loads((out / "results.json").read_text())
    assert len(data["nodes"]) == expected, [n["id"] for n in data["nodes"]]
    assert expected > 1, "the test is vacuous unless several nodes could be dropped"


def test_only_is_recorded_so_a_reader_knows_what_was_refetched(monkeypatch, tmp_path):
    import json

    from basic_check import cli

    out = _full_results_dir(tmp_path)
    monkeypatch.setattr(cli, "DEFAULT_RESULTS", out)
    CliRunner().invoke(cli.app, ["assess", "--only", "egi"], catch_exceptions=False)
    assert json.loads((out / "results.json").read_text())["selection"] == ["egi"]


def test_an_explicit_results_dir_still_allows_a_deliberate_subset(tmp_path):
    """Writing somewhere else is the deliberate case: nothing published is at
    risk, so --only narrows the report as before.
    """
    import json

    from basic_check.cli import app

    out = _full_results_dir(tmp_path)
    res = CliRunner().invoke(
        app, ["assess", "--only", "egi", "--results", str(out)], catch_exceptions=False
    )
    assert res.exit_code == 0, res.output
    assert len(json.loads((out / "results.json").read_text())["nodes"]) == 1


def test_a_full_run_records_no_selection(monkeypatch, tmp_path):
    import json

    from basic_check import cli

    out = _full_results_dir(tmp_path)
    monkeypatch.setattr(cli, "DEFAULT_RESULTS", out)
    CliRunner().invoke(cli.app, ["assess"], catch_exceptions=False)
    assert json.loads((out / "results.json").read_text())["selection"] == []


def test_only_narrows_the_fetch_but_not_the_report_in_the_published_dir():
    """The two lists _resolve returns are the fetch list and the report list."""
    import yaml

    configured = yaml.safe_load(cli.DEFAULT_NODES.read_text(encoding="utf-8"))["nodes"]
    fetched, reported, out = cli._resolve(None, cli.DEFAULT_NODES, "egi", None)
    assert out == cli.DEFAULT_RESULTS
    assert [n["id"] for n in fetched] == ["egi"]
    # Every configured node, not a fixed count: the report must not shrink to
    # the selection, however many nodes nodes.yaml happens to list.
    assert len(reported) == len(configured)
    assert len(reported) > 1


def test_an_unknown_id_is_still_rejected_rather_than_quietly_widened():
    """Since --only no longer narrows the report, a typo could now look like it
    worked: the full report would be produced and nothing fetched.
    """
    with pytest.raises(typer.BadParameter):
        cli._resolve(None, cli.DEFAULT_NODES, "not-a-node", None)


# --- --skip: leave named nodes out of a run, and say so ------------------------


def _ids(nodes):
    return [n["id"] for n in nodes]


@pytest.mark.parametrize(
    "skip",
    [
        ["eosc-it,eosc-sk"],  # one comma-separated value
        ["eosc-it", "eosc-sk"],  # the option repeated
        ["Italy, Slovakia"],  # short names, with a space after the comma
        ["italy", "SLOVAKIA"],  # case does not matter
        ["EOSC Node Italy", "eosc-sk"],  # full name and id mixed
    ],
    ids=["comma", "repeated", "short-names", "case", "full-name-and-id"],
)
def test_skip_removes_nodes_from_both_the_fetch_and_the_report(skip):
    fetched, reported, _ = cli._resolve(None, cli.DEFAULT_NODES, "", None, skip=skip)
    for ids in (_ids(fetched), _ids(reported)):
        assert "eosc-it" not in ids and "eosc-sk" not in ids, ids
        assert "egi" in ids  # and nothing else went with them


def test_an_unknown_skip_value_is_rejected_rather_than_ignored():
    """A typo that skipped nothing would run the node the user meant to leave
    out, which is exactly the request --skip exists to prevent."""
    with pytest.raises(typer.BadParameter, match="Itlay"):
        cli._resolve(None, cli.DEFAULT_NODES, "", None, skip=["Itlay"])


def test_an_ambiguous_skip_value_is_rejected(tmp_path):
    import yaml

    f = tmp_path / "nodes.yaml"
    f.write_text(yaml.safe_dump({"nodes": [
        {"id": "a", "name": "EOSC Node Twin", "url": "https://a.example/", "eosc_page": ""},
        {"id": "b", "name": "EOSC Twin", "url": "https://b.example/", "eosc_page": ""},
        {"id": "c", "name": "Other", "url": "https://c.example/", "eosc_page": ""},
    ]}))
    with pytest.raises(typer.BadParameter, match="more than one"):
        cli._resolve(None, f, "", None, skip=["Twin"])


def test_skipping_every_node_is_rejected():
    import yaml

    every = [n["id"] for n in yaml.safe_load(cli.DEFAULT_NODES.read_text())["nodes"]]
    with pytest.raises(typer.BadParameter, match="nothing left"):
        cli._resolve(None, cli.DEFAULT_NODES, "", None, skip=[",".join(every)])


def test_skip_and_url_together_are_rejected():
    with pytest.raises(typer.BadParameter):
        cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "", None, skip=["egi"])


def test_skip_applies_after_only():
    fetched, _, _ = cli._resolve(None, cli.DEFAULT_NODES, "egi,eudat", None, skip=["egi"])
    assert _ids(fetched) == ["eudat"]


def test_no_skip_changes_nothing():
    assert cli._resolve(None, cli.DEFAULT_NODES, "", None, skip=[]) == cli._resolve(
        None, cli.DEFAULT_NODES, "", None
    )


def test_skipped_nodes_do_not_count_as_missing_evidence_and_are_recorded(tmp_path):
    """The use case: nodes.yaml lists nodes with no evidence yet (Italy's domain
    does not resolve), and a run over the rest should be able to complete
    without exit 2 — but the result must still say who was left out."""
    import json

    out = _full_results_dir(tmp_path)
    have = {p.stem for p in (out / "evidence").glob("*.json")}
    configured = _ids(__import__("yaml").safe_load(cli.DEFAULT_NODES.read_text())["nodes"])
    absent = sorted(set(configured) - have)
    assert absent, "the test is vacuous unless some configured node lacks evidence"
    res = CliRunner().invoke(
        cli.app,
        ["assess", "--results", str(out), *[a for i in absent for a in ("--skip", i)]],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    data = json.loads((out / "results.json").read_text())
    assert data["skipped"] == absent
    assert "missing_evidence" not in data
    assert not set(_ids(data["nodes"])) & set(absent)


def test_the_reports_state_which_nodes_were_skipped(tmp_path):
    """A shorter table must not look like a complete one: that was the whole
    reason --only stopped narrowing the published report."""
    out = _full_results_dir(tmp_path)
    nodes_file, _ = _nodes_covering(tmp_path, out)
    CliRunner().invoke(
        cli.app,
        ["assess", "--results", str(out), "--nodes", str(nodes_file), "--skip", "egi,eudat"],
        catch_exceptions=False,
    )
    md = (out / "results.md").read_text()
    html_ = (out / "index.html").read_text()
    for text in (md, html_):
        assert "Skipped by request" in text
        assert "egi" in text.split("Skipped by request", 1)[1][:300]
        assert "eudat" in text.split("Skipped by request", 1)[1][:300]


def test_a_run_without_skip_records_an_empty_list_and_no_banner(tmp_path):
    import json

    out = _full_results_dir(tmp_path)
    nodes_file, _ = _nodes_covering(tmp_path, out)
    CliRunner().invoke(
        cli.app, ["assess", "--results", str(out), "--nodes", str(nodes_file)],
        catch_exceptions=False,
    )
    assert json.loads((out / "results.json").read_text())["skipped"] == []
    assert "Skipped by request" not in (out / "results.md").read_text()


@pytest.mark.parametrize("command", ["collect", "run"])
def test_collect_and_run_do_not_fetch_skipped_nodes(monkeypatch, tmp_path, command):
    """Nothing is sent to a skipped node's website."""
    seen = {}
    monkeypatch.setattr(cli, "_do_collect", lambda nodes, *a, **k: seen.setdefault("ids", _ids(nodes)))
    monkeypatch.setattr(cli, "_do_assess", lambda *a, **k: None)
    res = CliRunner().invoke(
        cli.app, [command, "--results", str(tmp_path), "--skip", "Italy", "--skip", "Slovakia"],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    assert "eosc-it" not in seen["ids"] and "eosc-sk" not in seen["ids"]
    assert "egi" in seen["ids"]


# --- help text ----------------------------------------------------------------


def _options(command) -> list:
    return [p for p in command.params if p.param_type_name == "option"]


def test_every_option_of_every_command_has_help_text():
    """The README's option reference mirrors --help, so an option added
    without a help string would be undocumented in both places."""
    group = typer.main.get_command(cli.app)
    missing = [
        f"{name} {opt.opts[0]}"
        for name, command in group.commands.items()
        for opt in _options(command)
        if not (opt.help or "").strip()
    ]
    assert not missing, missing


def test_a_shared_option_is_described_the_same_way_by_every_command():
    """collect, assess and run once described --skip and --depth each in their
    own words; one shared text per option keeps them from drifting apart."""
    group = typer.main.get_command(cli.app)
    texts: dict[str, set[str]] = {}
    for name in ("collect", "assess", "run"):
        for opt in _options(group.commands[name]):
            texts.setdefault(opt.opts[0], set()).add(opt.help)
    differing = {o: t for o, t in texts.items() if len(t) > 1}
    assert not differing, differing


def test_top_level_help_lists_the_configured_node_ids():
    import yaml

    ids = [n["id"] for n in yaml.safe_load(cli.DEFAULT_NODES.read_text())["nodes"]]
    res = CliRunner().invoke(cli.app, ["--help"], env={"COLUMNS": "400"})
    assert res.exit_code == 0
    for node_id in ids:
        assert node_id in res.output, node_id


def test_help_still_prints_when_the_node_list_is_unreadable(tmp_path):
    assert "nodes.yaml" in cli._node_ids(tmp_path / "missing.yaml")


# --- a URL change must not relabel old evidence silently ----------------------


def _nodes_from_evidence(tmp_path, results_dir, **url_overrides):
    """A nodes file whose URLs are the ones the evidence was collected from,
    with optional per-id replacements standing in for a URL change."""
    import json

    import yaml

    have = {}
    for p in (results_dir / "evidence").glob("*.json"):
        have[p.stem] = json.loads(p.read_text())["requested_url"]
    all_nodes = yaml.safe_load(cli.DEFAULT_NODES.read_text(encoding="utf-8"))["nodes"]
    kept = [
        {**n, "url": url_overrides.get(n["id"], have[n["id"]])}
        for n in all_nodes
        if n["id"] in have
    ]
    path = tmp_path / "nodes-from-evidence.yaml"
    path.write_text(yaml.safe_dump({"nodes": kept}, allow_unicode=True), encoding="utf-8")
    return path


def test_evidence_from_another_url_is_flagged_in_every_report(tmp_path):
    """The defect: after editing a node's url in nodes.yaml, a bare `assess`
    labelled the old page's verdicts with the new address, and nothing said so."""
    import json

    out = _full_results_dir(tmp_path)
    new_url = "https://www.egi.eu/a-new-landing-page/"
    nodes = _nodes_from_evidence(tmp_path, out, egi=new_url)
    res = CliRunner().invoke(
        cli.app, ["assess", "--results", str(out), "--nodes", str(nodes)], catch_exceptions=False
    )
    assert res.exit_code == 0, res.output
    assert "different URL" in res.output and new_url in res.output
    data = json.loads((out / "results.json").read_text())
    assert [m["id"] for m in data["url_mismatch"]] == ["egi"]
    assert data["url_mismatch"][0]["configured_url"] == new_url
    assert data["url_mismatch"][0]["evidence_url"] == "https://www.egi.eu/egi-node"
    for name in ("results.md", "index.html"):
        text = (out / name).read_text()
        assert "Evidence from a different URL." in text, name
        assert "https://www.egi.eu/egi-node" in text, name


def test_evidence_from_the_configured_url_adds_no_warning(tmp_path):
    """The rebuild of a published run with the node list it was collected with
    must stay identical: no mismatch, no banner, no new key in results.json."""
    import json

    out = _full_results_dir(tmp_path)
    nodes = _nodes_from_evidence(tmp_path, out)
    res = CliRunner().invoke(
        cli.app, ["assess", "--results", str(out), "--nodes", str(nodes)], catch_exceptions=False
    )
    assert res.exit_code == 0, res.output
    assert "different URL" not in res.output
    assert "url_mismatch" not in json.loads((out / "results.json").read_text())
    assert "Evidence from a different URL" not in (out / "results.md").read_text()


# --- --node: one configured node at an alternative landing page URL -----------

ALT = "https://alt.example.org/eosc-node-bbmri-eric/"


def test_node_keeps_the_configured_identity_but_fetches_the_alternative_url():
    """The point of --node over a bare --url: the id, name and eosc_page stay the
    node's own, so its scoped approved name applies and the row is comparable
    with the federation run. Only the page fetched changes."""
    import yaml

    configured = {
        n["id"]: n for n in yaml.safe_load(cli.DEFAULT_NODES.read_text())["nodes"]
    }["bbmri-eric"]
    fetched, reported, out = cli._resolve([ALT], cli.DEFAULT_NODES, "", None, node="bbmri-eric")
    assert fetched == reported
    (n,) = fetched
    assert n["id"] == "bbmri-eric" and n["name"] == configured["name"]
    assert n["url"] == ALT
    assert n["configured_url"] == configured["url"]
    assert n["eosc_page"] == configured["eosc_page"]
    assert not n.get("ad_hoc")
    assert out == cli.DEFAULT_ONEOFF


@pytest.mark.parametrize("value", ["bbmri-eric", "BBMRI-ERIC", "bbmri-ERIC"])
def test_node_accepts_an_id_or_name_in_any_case(value):
    (n,), _, _ = cli._resolve([ALT], cli.DEFAULT_NODES, "", None, node=value)
    assert n["id"] == "bbmri-eric"


def test_node_with_eosc_page_replaces_the_configured_one():
    page = "https://eosc.eu/building-the-eosc-federation/eosc-node-x/"
    (n,), _, _ = cli._resolve([ALT], cli.DEFAULT_NODES, "", None, page, node="bbmri-eric")
    assert n["eosc_page"] == page
    assert n["configured_eosc_page"].endswith("/eosc-node-bbmri-eric/")


def test_node_never_writes_into_the_published_results_dir():
    """The evidence file is named after the node id: writing into results/ would
    replace the reviewed evidence for that node with a page that is not its
    registered one. Refused, not silently redirected."""
    with pytest.raises(typer.BadParameter, match="published run"):
        cli._resolve([ALT], cli.DEFAULT_NODES, "", cli.DEFAULT_RESULTS, node="bbmri-eric")


def test_node_honours_another_explicit_results_dir(tmp_path):
    _, _, out = cli._resolve([ALT], cli.DEFAULT_NODES, "", tmp_path, node="bbmri-eric")
    assert out == tmp_path


@pytest.mark.parametrize(
    ("urls", "only", "skip", "match"),
    [
        ([], "", None, "exactly one --url"),
        ([ALT, "https://b.example/"], "", None, "exactly one --url"),
        ([ALT], "egi", None, "drop --only"),
        ([ALT], "", ["Italy"], "--skip"),
        (["alt.example.org/x"], "", None, "absolute http"),
    ],
    ids=["no-url", "two-urls", "with-only", "with-skip", "not-a-url"],
)
def test_node_rejects_combinations_it_cannot_honour(urls, only, skip, match):
    with pytest.raises(typer.BadParameter, match=match):
        cli._resolve(urls, cli.DEFAULT_NODES, only, None, skip=skip, node="bbmri-eric")


def test_an_unknown_node_is_rejected_and_the_ids_are_listed():
    with pytest.raises(typer.BadParameter, match="ids are: .*bbmri-eric"):
        cli._resolve([ALT], cli.DEFAULT_NODES, "", None, node="no-such-node")


def test_an_ambiguous_node_is_rejected(tmp_path):
    nodes = tmp_path / "nodes.yaml"
    nodes.write_text(
        "nodes:\n"
        "  - {id: a, name: EOSC Node Twin, url: 'https://a.example/', eosc_page: ''}\n"
        "  - {id: b, name: Twin, url: 'https://b.example/', eosc_page: ''}\n"
    )
    with pytest.raises(typer.BadParameter, match="more than one node"):
        cli._resolve([ALT], nodes, "", None, node="Twin")


@pytest.mark.parametrize("command", ["collect", "run"])
def test_collect_and_run_with_node_fetch_only_the_alternative_page(monkeypatch, tmp_path, command):
    """Nothing is sent to the configured URL or to any other node."""
    seen = {}
    monkeypatch.setattr(cli, "_do_collect", lambda nodes, out, *a, **k: seen.update(nodes=nodes, out=out))
    monkeypatch.setattr(cli, "_do_assess", lambda *a, **k: None)
    res = CliRunner().invoke(
        cli.app,
        [command, "--node", "bbmri-eric", "--url", ALT, "--results", str(tmp_path)],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    assert [(n["id"], n["url"]) for n in seen["nodes"]] == [("bbmri-eric", ALT)]
    assert seen["out"] == tmp_path


def test_a_node_run_says_in_every_report_that_the_url_is_not_the_configured_one(tmp_path):
    """The row keeps the node's id and name, so without a banner it would read as
    the node's assessment at its registered page."""
    import json

    import yaml

    configured = {
        n["id"]: n for n in yaml.safe_load(cli.DEFAULT_NODES.read_text())["nodes"]
    }["egi"]["url"]
    alt = "https://alt.example.org/egi-node/"
    out = tmp_path / "trial"
    (out / "evidence").mkdir(parents=True)
    ev = json.loads((cli.ROOT / "results" / "evidence" / "egi.json").read_text())
    ev["requested_url"] = alt
    (out / "evidence" / "egi.json").write_text(json.dumps(ev))

    res = CliRunner().invoke(
        cli.app,
        ["assess", "--node", "egi", "--url", alt, "--results", str(out)],
        catch_exceptions=False,
    )
    assert res.exit_code == 0, res.output
    assert "alternative URL" in res.output and "different URL" not in res.output
    data = json.loads((out / "results.json").read_text())
    assert data["alternative_url"] == [{"id": "egi", "configured_url": configured, "url": alt}]
    (node,) = data["nodes"]
    assert (node["id"], node["url"], node["configured_url"]) == ("egi", alt, configured)
    assert "url_mismatch" not in data
    for name in ("results.md", "index.html"):
        text = (out / name).read_text()
        assert "Alternative URL, not a federation run." in text, name
        assert alt in text and configured in text, name
    assert (out / "results.md").read_text().startswith("# Alternative URL check (not a federation run)")

    shown = CliRunner().invoke(cli.app, ["show", "egi", "--results", str(out)])
    assert shown.exit_code == 0 and f"configured: {configured}" in shown.output


def test_assessing_node_evidence_at_the_configured_url_still_flags_the_mismatch(tmp_path):
    """Evidence collected with --node, then assessed without it, must not be
    labelled as the configured page: the existing URL-mismatch warning covers it."""
    import json

    out = tmp_path / "trial"
    (out / "evidence").mkdir(parents=True)
    ev = json.loads((cli.ROOT / "results" / "evidence" / "egi.json").read_text())
    ev["requested_url"] = "https://alt.example.org/egi-node/"
    (out / "evidence" / "egi.json").write_text(json.dumps(ev))
    res = CliRunner().invoke(
        cli.app, ["assess", "--only", "egi", "--results", str(out)], catch_exceptions=False
    )
    assert res.exit_code == 0, res.output
    assert "different URL" in res.output
    assert "alternative_url" not in json.loads((out / "results.json").read_text())
