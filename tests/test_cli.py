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
    replace the committed nine-node report with a one-row table."""
    _, out = cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "", None)
    assert out == cli.DEFAULT_ONEOFF
    assert out != cli.DEFAULT_RESULTS


def test_the_configured_run_still_writes_to_the_normal_place():
    nodes, out = cli._resolve(None, cli.DEFAULT_NODES, "", None)
    assert out == cli.DEFAULT_RESULTS
    assert len(nodes) > 1


def test_an_explicit_results_dir_still_wins_for_a_url_run():
    _, out = cli._resolve(["https://a.example/"], cli.DEFAULT_NODES, "", Path("/tmp/custom"))
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
    nodes, out = cli._resolve(["", "  "], cli.DEFAULT_NODES, "", None)
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
