"""The per-node limit: a node that hangs is abandoned, recorded as ERROR, and the
run goes on. Uses a fake browser, so nothing here touches the network.

Background: in run web-29 (19 October 2026) one node's collection stalled after
its screenshot and held the GitHub job until its 30-minute limit; the nodes
after it were never reached.
"""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

import pytest

from basic_check import checks, fetch

NODE = {"id": "slow", "name": "Slow node", "url": "https://slow.example/"}
HTML = "<html lang='en'><head><title>T</title></head><body><main>Hello</main></body></html>"


class FakeResponse:
    status = 200


class FakePage:
    def __init__(self, hang_on: str | None):
        self.hang_on = hang_on
        self.url = NODE["url"]

    def on(self, *_a, **_k):
        pass

    async def _maybe_hang(self, step: str):
        if self.hang_on == step:
            await asyncio.sleep(3600)

    async def goto(self, url, **_k):
        await self._maybe_hang("goto")
        self.url = url
        return FakeResponse()

    async def wait_for_load_state(self, *_a, **_k):
        pass

    async def wait_for_timeout(self, *_a, **_k):
        pass

    async def content(self):
        await self._maybe_hang("content")
        return HTML

    async def screenshot(self, **_k):
        pass

    async def close(self):
        pass


class FakeContext:
    def __init__(self, hang_on, hang_close=False):
        self.hang_on, self.hang_close, self.closed = hang_on, hang_close, False

    async def new_page(self):
        return FakePage(self.hang_on)

    async def close(self):
        if self.hang_close:
            await asyncio.sleep(3600)
        self.closed = True


class FakeBrowser:
    def __init__(self, hang_on=None, hang_close=False):
        self.contexts: list[FakeContext] = []
        self.hang_on, self.hang_close = hang_on, hang_close

    async def new_context(self, **_k):
        ctx = FakeContext(self.hang_on, self.hang_close)
        self.contexts.append(ctx)
        return ctx


@pytest.fixture(autouse=True)
def no_robots(monkeypatch):
    monkeypatch.setattr(fetch, "_robots", lambda url: (True, "test: robots not read"))
    monkeypatch.setattr(fetch, "_robots_ok", lambda url: True)
    monkeypatch.setattr(fetch, "CANCEL_GRACE_S", 0.2)
    monkeypatch.setattr(fetch, "CLOSE_TIMEOUT_S", 0.2)


def _run(browser, tmp_path: Path, timeout_s):
    return asyncio.run(
        fetch.fetch_with_limit(browser, NODE, tmp_path, depth=0, timeout_s=timeout_s)
    )


def test_a_node_that_finishes_is_untouched(tmp_path):
    ev, timed_out = _run(FakeBrowser(), tmp_path, 5)
    assert not timed_out
    assert ev.error == ""
    assert ev.http_status == 200


@pytest.mark.parametrize("step", ["goto", "content"])
def test_a_hung_node_is_abandoned_at_the_limit(tmp_path, step):
    browser = FakeBrowser(hang_on=step)
    t0 = time.monotonic()
    ev, timed_out = _run(browser, tmp_path, 0.3)
    elapsed = time.monotonic() - t0
    assert timed_out
    assert elapsed < 3, "the limit must fire, not wait for the hung call"
    assert ev.error.startswith("TimeoutError: node collection did not finish within 0.3 s")
    assert ev.node_id == "slow" and ev.requested_url == NODE["url"]
    assert "per-node limit" in ev.crawl_note
    # The cancelled work still closed its browser context.
    assert browser.contexts and browser.contexts[0].closed


def test_partial_evidence_survives_the_timeout(tmp_path):
    # Hangs after the landing page was read: what was gathered is kept as
    # evidence, but the error means it is not assessed.
    ev, timed_out = _run(FakeBrowser(hang_on=None), tmp_path, 5)
    assert not timed_out and ev.title == "T"

    async def hang_after_landing(browser, node, shots, depth, max_children, budget, ev=None):
        ev.http_status, ev.title = 200, "T"
        await asyncio.sleep(3600)

    orig = fetch._fetch_one
    fetch._fetch_one = hang_after_landing
    try:
        ev, timed_out = _run(FakeBrowser(), tmp_path, 0.2)
    finally:
        fetch._fetch_one = orig
    assert timed_out and ev.title == "T" and ev.http_status == 200
    assert ev.error.startswith("TimeoutError")


def test_a_hung_context_close_does_not_become_the_hang(tmp_path):
    browser = FakeBrowser(hang_on="content", hang_close=True)
    t0 = time.monotonic()
    ev, timed_out = _run(browser, tmp_path, 0.3)
    assert timed_out and time.monotonic() - t0 < 3


def test_zero_means_no_limit(tmp_path):
    ev, timed_out = _run(FakeBrowser(), tmp_path, 0)
    assert not timed_out and ev.error == ""


def test_a_timed_out_node_reads_error_on_every_point(tmp_path):
    ev, _ = _run(FakeBrowser(hang_on="content"), tmp_path, 0.2)
    results = checks.run_all(ev, None, "", True)
    assert len(results) == 10
    assert all(r.verdict == checks.ERROR for r in results)


def test_the_default_limit_is_finite_and_generous():
    # Several times the slowest node seen in a full run (about a minute), and
    # far below the 30-minute job limit it exists to protect.
    assert 120 <= fetch.NODE_TIMEOUT_S <= 600


def test_the_run_continues_after_a_hung_node(tmp_path, monkeypatch, capsys):
    import playwright.async_api as pa

    launched: list[FakeBrowser] = []

    class HangsOnSecondNode(FakeBrowser):
        async def new_context(self, **k):
            ctx = await super().new_context(**k)
            if len(launched) == 1 and len(self.contexts) == 2:
                ctx.hang_on = "content"
            return ctx

        async def close(self):
            pass

    class FakeChromium:
        async def launch(self, **_k):
            b = HangsOnSecondNode()
            launched.append(b)
            return b

    class FakePW:
        chromium = FakeChromium()

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

    monkeypatch.setattr(pa, "async_playwright", lambda: FakePW())
    nodes = [dict(NODE, id=f"n{i}", url=f"https://n{i}.example/") for i in range(3)]
    results = asyncio.run(
        fetch.collect_all(nodes, tmp_path / "ev", delay_s=0, depth=0, node_timeout_s=0.3)
    )
    assert [ev.node_id for ev in results] == ["n0", "n1", "n2"]
    assert results[0].error == "" and results[2].error == ""
    assert results[1].error.startswith("TimeoutError")
    assert len(launched) == 2, "the browser is restarted after a timeout"
    assert (tmp_path / "ev" / "n1.json").exists()
    out = capsys.readouterr().out
    assert "n1" in out and "per-node limit" in out
