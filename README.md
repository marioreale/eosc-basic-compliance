# eosc-basic-compliance

Checks EOSC Node Landing Pages against the **Node Landing Page Verification
Checklist v3.0** (15 September 2026). One result per checklist point, per node.

**One HTTP request per node. No crawling.** Each landing page is loaded once in a
headless browser, evidence is saved to disk, and every check reads only that
saved evidence. Nothing else on the node's site is touched.

👉 **[Latest results](results/results.md)** · [browsable HTML report](results/index.html)
(download and open locally, or use the GitHub Pages link if enabled)

## What it found

Nine landing pages, 17 September 2026:

| Node | 1 | 1R | 2 | 3 | 4 | 5a | 5b | 5c | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|
| BBMRI-ERIC | PASS | review | review | review | PASS | review | review | PASS | PASS | PASS |
| EOSC DTO (D4Science) | PASS | review | review | review | review | review | PASS | review | review | PASS |
| Data Terra | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EOSC Finland | PASS | review | review | review | **FAIL** | review | PASS | review | PASS | PASS |
| PaNOSC | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EUDAT | PASS | review | review | review | review | review | PASS | review | review | PASS |
| EGI | PASS | review | review | review | **FAIL** | review | PASS | review | review | PASS |
| GÉANT | PASS | review | review | review | **FAIL** | review | review | review | review | PASS |
| EBRAINS | PASS | review | review | review | **FAIL** | review | review | review | PASS | PASS |

**The one clear, repeated finding is checklist point 4.** All nine nodes have a
dedicated page under `eosc.eu/building-the-eosc-federation/` — the slugs were read
from the live index — but only BBMRI-ERIC links to its own. Six nodes fail
outright: four link to nothing on `eosc.eu`, and PaNOSC and GÉANT link only to the
federation index page, which the checklist explicitly excludes. Each failure names
the exact URL that is missing, so the fix is a one-line edit.

Point 4 is also the checklist's sharpest point: it names a specific page and
excludes two specific near-misses, so it can be decided mechanically. Most of the
rest cannot be.

## Why so much "review"

Of the 10 points, **3 are decidable by inspection** (1, 4, 7), **4 only partly**
(3, 5b, 5c, 6), and **3 require a human reading the page** (1R, 2, 5a).

`review` is a deliberate verdict, not a gap. Point 2 asks whether the page
"clearly state[s]" scope, users and responsible organisation — "clearly" is a
judgement about a reader, and a tool that scored it would be inventing a
threshold the checklist does not set. Point 5 quantifies over "all research
resources offered by the Node", which a single page request cannot enumerate, and
the checklist permits the policies to live in the EOSC Catalogue rather than on
the page. So the tool extracts the relevant evidence, attaches it, and says who
must decide.

The asymmetry drives this: a false PASS is never investigated again, and a false
FAIL against a named organisation is expensive to retract. Where the tool cannot
be sure, it says so.

### Absence is not concluded from a page that did not render

Two pages in this run were not fully captured: the D4Science page is dominated by
a cookie-consent overlay (530 characters of main text), and the EUDAT portal
yielded only 10 links. Reporting "no contact route exists" from either would say
more about the tool than about the node. Both are downgraded to `review` with the
reason stated. A well-rendered page with a genuinely missing link still FAILs —
the gate is not a blanket excuse (`test_a_well_rendered_page_still_fails_when_the_link_is_genuinely_absent`).

## Verdicts

| | meaning |
|---|---|
| `PASS` | Satisfied, and the tool can show why. |
| `FAIL` | Violated, and the tool can show why. |
| `review` | A human must decide. Evidence is attached. |
| `ERROR` | The page could not be assessed at all. |

## Usage

```bash
uv sync
uv run playwright install chromium --with-deps

uv run basic-check points            # the checklist, and what is decidable
uv run basic-check collect           # one request per node -> results/evidence/
uv run basic-check assess            # evidence -> results/{index.html,results.md,.csv,.json}
uv run basic-check run               # collect + assess
uv run basic-check show data-terra   # one node's results in the terminal
```

`collect` and `assess` are separate on purpose: assessment is re-runnable offline
against saved evidence, so changing a check never means re-requesting the pages.
`assess` exits non-zero if any configured node has no evidence, so a short table
cannot quietly look complete.

Edit `nodes.yaml` to change the list of nodes. To check the official
Tripartite-approved node names (point 3), supply a list:

```bash
uv run basic-check assess --approved-names approved-names.txt
```

## Scope and limits

- **One request per node, no link following.** Point 1R (resources behind the
  landing page) and point 5 (per-resource policies) therefore cannot be settled
  here; the tool lists the external hosts it saw as a reviewer work list.
- **Logos** are detected from image markup. A logo delivered as a CSS background
  or an SVG sprite will be missed, so absence of logo markup is reported as *not
  proof of absence*.
- **AAI** compliance is verified during EEN enrolment, not by reading a page. The
  tool only reports whether a login affordance is visible.
- **AUP and UAP are kept distinct** (5b, 5c). They are different documents and
  are not treated as interchangeable.
- The registered NLP is whatever is in the EOSC EU Node Contributors Dashboard
  (§1.2, field 6). `nodes.yaml` is a local copy and can drift from it.

## Tests

```bash
uv run pytest -q          # 30 tests, ~0.1s, no network
uv run ruff check src tests
```

The tests are hermetic — they construct page evidence directly, so the suite
never touches a node's website.

Two of them exist because probing found real bugs in this code:

- `test_point4_rejects_domains_that_merely_end_in_eosc_eu` — the first version
  used `netloc.endswith("eosc.eu")`, so `myeosc.eu` and `not-eosc.eu` satisfied a
  requirement about `eosc.eu`.
- `test_consent_overlay_blocks_an_absence_based_fail` — the first version reported
  "no contact route of any kind was found" for a page where it had actually only
  captured a cookie banner.

## Source

Checklist: *Node Landing Page Verification Checklist v3.0*, 15 September 2026.
EOSC Federation node index: <https://eosc.eu/building-the-eosc-federation/>
