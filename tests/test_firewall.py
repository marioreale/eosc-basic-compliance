"""The FIREWALL outcome: the site answered, but with a bot-protection challenge.

The challenge page (Cloudflare's "Performing security verification") shows
that the server is up and responding, and nothing else. Every point is
FIREWALL rather than review, and in particular point 7 no longer passes on the
challenge page's own English.
"""

from __future__ import annotations

import json

from basic_check import checks, report
from basic_check.cli import ROOT
from basic_check.fetch import Link, PageEvidence

CHALLENGE_TEXT = (
    "eosc.lv Performing security verification This website uses a security service to "
    "protect against malicious bots. This page is displayed while the website verifies you "
    "are not a bot. Verification successful. Waiting for eosc.lv to respond Ray ID: "
    "a58bf1662a10a66d Performance and Security by Cloudflare Privacy"
)


def ev(**kw) -> PageEvidence:
    base = dict(
        node_id="t", node_name="Test Node",
        requested_url="https://node.example/", final_url="https://node.example/",
        http_status=403, title="Just a moment...",
        full_text=CHALLENGE_TEXT, main_text=CHALLENGE_TEXT, lang_attr="en",
        links=[Link("https://www.cloudflare.com/", "Cloudflare")],
    )
    base.update(kw)
    return PageEvidence(**base)


def test_a_cloudflare_challenge_makes_every_point_firewall():
    results = checks.run_all(ev())
    assert len(results) == 10
    assert {r.verdict for r in results} == {checks.FIREWALL}
    assert [r.point_id for r in results] == ["1", "1R", "2", "3", "4", "5a", "5b", "5c", "6", "7"]
    first = results[0]
    assert "up and responding" in first.message and "nothing can be asserted" in first.message
    assert any("Performing security verification" in e for e in first.evidence)


def test_the_challenge_url_marker_counts_as_cloudflare():
    """GÉANT's challenge redirects to ?ki-cf-botcl=1; the URL alone is a Cloudflare marker."""
    text = "geant.org Performing security verification This page is displayed while the website verifies you are not a bot."
    results = checks.run_all(ev(full_text=text, main_text=text, final_url="https://geant.org/x/?ki-cf-botcl=1"))
    assert {r.verdict for r in results} == {checks.FIREWALL}


def test_a_plain_403_is_not_a_firewall():
    """No challenge wording: an access refusal, still reviewed as before."""
    text = "403 Forbidden nginx"
    results = checks.run_all(ev(title="403 Forbidden", full_text=text, main_text=text))
    assert checks.FIREWALL not in {r.verdict for r in results}
    assert results[0].verdict == checks.MANUAL_REVIEW


def test_a_served_page_that_mentions_cloudflare_is_not_a_firewall():
    text = "Our node is protected by Cloudflare. Just a moment of your time: " + "content " * 60
    results = checks.run_all(ev(http_status=200, title="EOSC Node", full_text=text, main_text=text))
    assert checks.FIREWALL not in {r.verdict for r in results}


def test_challenge_wording_without_a_cloudflare_marker_is_not_a_firewall():
    text = "Performing security verification. Please wait."
    results = checks.run_all(ev(full_text=text, main_text=text, links=[]))
    assert checks.FIREWALL not in {r.verdict for r in results}


def test_a_fetch_error_stays_an_error():
    results = checks.run_all(ev(http_status=None, error="TimeoutError"))
    assert checks.FIREWALL not in {r.verdict for r in results}


def _run():
    point = {"id": "1", "title": "Point 1", "requirement": "", "implemented_by": "check_1", "decidable": True}
    node = {
        "id": "lv", "name": "EOSC Node Latvia", "url": "https://eosc.lv/en/",
        "results": [{"point_id": "1", "title": "Point 1", "verdict": "FIREWALL", "message": "challenge", "evidence": []}],
        "fetch": {"crawl_depth": 1, "children": []},
    }
    return {"run_id": "t", "generated_at": "2026-11-11T00:00:00+00:00",
            "checklist": {"checklist_version": "3.2", "checklist_date": "2026-09-28", "points": [point]},
            "nodes": [node]}


def test_the_markdown_report_has_its_own_icon_and_tally(tmp_path):
    md = report.render_markdown(_run(), tmp_path / "r.md").read_text(encoding="utf-8")
    assert "🧱 **Firewall**" in md
    assert report._tally_line({"PASS": 1, "FIREWALL": 10}).endswith("🧱 10 firewall")
    assert "🟣" not in md.split("| Node |")[1].split("\n\n")[0]  # not drawn as ERROR in the matrix


def test_the_html_report_draws_it_red_and_distinct_from_fail_and_error(tmp_path):
    page = report.render_html(_run(), tmp_path / "i.html").read_text(encoding="utf-8")
    assert 'class="v firewall"' in page
    assert ".v.firewall{color:var(--firewall);background:var(--firewall-bg);white-space:nowrap}" in page
    assert "--firewall-bg:#c62828" in page
    assert report.VERDICT_STYLE["FIREWALL"][0] not in (report.VERDICT_STYLE["FAIL"][0], report.VERDICT_STYLE["ERROR"][0])


def test_the_published_run_has_latvia_and_geant_behind_the_firewall():
    """Pinned to the committed evidence: the two nodes whose screenshots show the challenge."""
    run = json.loads((ROOT / "results" / "results.json").read_text(encoding="utf-8"))
    behind = {n["id"] for n in run["nodes"] if all(r["verdict"] == "FIREWALL" for r in n["results"])}
    anywhere = {n["id"] for n in run["nodes"] if any(r["verdict"] == "FIREWALL" for r in n["results"])}
    assert behind == anywhere == {"eosc-lv", "geant"}
