# eosc-basic-compliance

Checks EOSC Node Landing Pages against the **Node Landing Page Verification
Checklist v3.0** (15 September 2026). One result per checklist point, per node.

**Deliberately light on the nodes' websites.** Each landing page is loaded once in
a headless browser. The tool then follows **at most one level** of links, and only
links that can actually settle a checklist point — a policy, a contact page, an
about page. Everything else is left alone. Across all nine nodes that is **25
extra requests in total**, roughly three per node, spaced 1.2 s apart, with
`robots.txt` honoured per host. Evidence is saved to disk and every check reads
only that saved evidence, so re-running the rules costs nothing.

Set `--depth 0` for the strict one-request-per-node behaviour.

👉 **[Latest results](results/results.md)** · [browsable HTML report](results/index.html)
· [checklist v3.0 explained](results/checklist-v3.0.html)
(download and open locally, or use the GitHub Pages link if enabled)

## What it found

Nine landing pages, all fetched 21 September 2026, 12:39–12:44 UTC, at `--depth 2`.
Every node responded `HTTP 200`. The same tally holds at depth 1 — see
[How deep to go](#how-deep-to-go---depth).

The per-node results are **not reproduced here**. The full matrix, with the
evidence behind every verdict, is in the report linked above:
**[Latest results](results/results.md)**.

90 cells: 🟢 31 PASS · 🔴 8 FAIL · 🟠 51 review.

`portal.eudat.eu` returned `HTTP 500` on 18 September and was unassessable that
day; it responded normally on 21 September and is fully assessed here.

**The one clear, repeated finding is checklist point 4.** All nine nodes have a
dedicated page under `eosc.eu/building-the-eosc-federation/` — the slugs were read
from the live index — but only BBMRI-ERIC and EUDAT link to their own. Seven nodes
fail outright: five link to nothing on `eosc.eu` at all, and PaNOSC and GÉANT link
only to the federation index page, which the checklist explicitly excludes. Each failure names
the exact URL that is missing, so the fix is a one-line edit.

Point 4 is also the checklist's sharpest point: it names a specific page and
excludes two specific near-misses, so it can be decided mechanically. Most of the
rest cannot be.

### What each column means

| Column | The question it answers | Can a tool decide it? |
|---|---|---|
| [`1`](results/checklist-v3.0.html#p1) | Is the landing page served to an anonymous visitor, or behind an EOSC AAI login? | yes, by inspection |
| [`1R`](results/checklist-v3.0.html#p1R) | Are the resources the page points to also public or behind EOSC AAI? | no, human judgement |
| [`2`](results/checklist-v3.0.html#p2) | Does the page itself say what the node is and what it offers? | no, human judgement |
| [`3`](results/checklist-v3.0.html#p3) | Does the page use the official Tripartite-approved node name? | partly |
| [`4`](results/checklist-v3.0.html#p4) | Does the page link to this node's own page on eosc.eu? | yes, by inspection |
| [`5a`](results/checklist-v3.0.html#p5a) | Does the page point to the policies governing its resources? | no, human judgement |
| [`5b`](results/checklist-v3.0.html#p5b) | Is there an Acceptable Use Policy, and does it actually load? | partly |
| [`5c`](results/checklist-v3.0.html#p5c) | Is there a User Access Policy, and does it actually load? | partly |
| [`6`](results/checklist-v3.0.html#p6) | Can a user find a support or helpdesk route? | partly |
| [`7`](results/checklist-v3.0.html#p7) | Is the page available in English? | yes, by inspection |

Full requirement text for every point, quoted from the source document, is in
**[checklist v3.0 explained](results/checklist-v3.0.html)** — generated from the same
`checklist/v3.0.yaml` the checks read, so the explanation cannot drift from the rules.

`1R` is not a numbered point in the source checklist. Point 1 has two sentences: the
landing page must be public or behind EOSC AAI, and so must *"all resources pointed by
the Node Landing Page, either directly or through links through intermediate pages"*.
Those are different questions with different answers, so they are scored as separate
columns. `1R` is always *review*: it quantifies over every resource reachable from the
page, and whether a login is genuinely EOSC AAI compliant is settled during EEN
enrolment, not by reading HTML. Splitting it out stops a node appearing to satisfy the
whole of point 1 when only the page itself was checked.

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
a cookie-consent overlay (530 characters of main text, 20 links), and the EUDAT
portal returned `HTTP 500` and yielded 61 characters and no links at all.
Reporting "no contact route exists" from either would say more about the tool, or
about a transient outage, than about the node. Both are downgraded to `review`
with the reason stated — which is exactly what happened to EUDAT here, rather
than its ten points turning into ten spurious failures. A well-rendered page with
a genuinely missing link still FAILs — the gate is not a blanket excuse
(`test_a_well_rendered_page_still_fails_when_the_link_is_genuinely_absent`).

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
uv run basic-check collect           # landing page + <=1 level of links -> results/evidence/
uv run basic-check collect --depth 0 # landing pages only, one request per node
uv run basic-check collect --max-children 4   # tighter cap (default 8 per node)
uv run basic-check collect --only egi,geant   # a subset, for a gentle re-run
uv run basic-check assess            # evidence -> results/{index.html,results.md,.csv,.json}
uv run basic-check run               # collect + assess
uv run basic-check run --depth 2     # follow one further hop (see below)
uv run basic-check show data-terra   # one node's results in the terminal
```

### How deep to go: `--depth`

| `--depth` | What is fetched | Requests in the 21 Sep 2026 run |
|---|---|---|
| `0` | The landing page only. | 9 |
| `1` **(default)** | The landing page, plus links from it that could settle a checklist point — policy, contact, about pages. At most 8 per node, 2 per point. | 34 (9 + 25) |
| `2` | The above, plus one further hop from those pages: a policy *index* that links on to the actual policy, for instance. At most 2 per fetched page and 1 per point, and the whole run shares a single `--fetch-budget` (default 60 requests). | 52 (9 + 25 + 18) |

Depth 2 exists for the case where the answer is one click past where depth 1 stops. It is not the default, for two reasons. The first is other people's servers: every extra hop multiplies requests against production sites that did not ask to be tested, which is why the budget is a hard ceiling for the whole run rather than a per-node limit. The second is that, on this federation, it has not yet changed anything.

```bash
uv run basic-check run --depth 2                    # bounded by the default budget
uv run basic-check run --depth 2 --fetch-budget 20  # stricter ceiling
```

**A depth-2 run reports both depths.** The report renders two summary tables — *Results at depth 1* and *Results at depth 2* — followed by a *What the second hop changed* section listing every cell whose verdict differs, and a table of exactly which pages the second hop fetched and what each was followed for. Both tables are computed from the **same capture**: the shallow view is the deep evidence with the second-hop pages set aside, not a second run. So any difference between the two tables is the extra hop, not the page changing between runs.

On the 21 September 2026 run, the second hop made 18 extra requests and changed **no verdict at all** — all 90 cells landed exactly where depth 1 had them. That is a finding rather than a disappointment: the points still marked review turn on a judgement ("clearly state") or quantify over things no crawl enumerates ("all research resources offered by the Node"), and no amount of fetching settles either kind. Run it yourself before assuming the same holds for another federation or a later date.

### Checking a page that is not in `nodes.yaml`

`--url` runs the full checklist against any page without editing configuration.
Repeatable, and it writes to `results/one-off/` so a published run is never
overwritten:

```bash
uv run basic-check run --url https://example.org/our-eosc-node/
uv run basic-check run --url https://a.example/ --url https://b.example/
uv run basic-check show example-org-our-eosc-node --one-off
```

Point 4 needs to know which `eosc.eu` page the node ought to link to. Without it
the point is still checked — a link to the federation index still fails — but the
message cannot name the URL that is missing. Supply it for a single URL with:

```bash
uv run basic-check run --url https://eosc.panosc.eu/ \
  --eosc-page https://eosc.eu/building-the-eosc-federation/eosc-node-panosc/
```

Reports from a `--url` run are titled **"Ad hoc page check (not a federation
run)"** and carry a marker at the top. They are otherwise identical in layout to
the real report, and a stray single-node file that looked official would be a
liability while a production decision is pending. `results/one-off/` is
git-ignored for the same reason.

`--url` cannot be combined with `--only`: `--only` filters ids in the nodes file,
and an ad hoc URL has no id there.

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

- **One level of links, not a crawl.** The tool never goes two levels deep and
  never follows a link it cannot use. Point 1R still cannot be settled: it quantifies
  over *every* resource reachable from the page, which one level does not cover.
  What one level does buy is that a policy link is checked rather than believed —
  a link labelled "Acceptable Use Policy" that 404s now **fails** point 5b instead
  of passing on the strength of its own label.
- **A block is not a finding.** A node that returns HTTP 403 to this tool is
  reported as *review*, never as a failure.  Turning that
  into "not publicly accessible" would be the checker blaming a node for its own
  request volume. Only 404/410 — a registered URL that does not resolve — fails
  point 1.
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
uv run pytest -q          # 83 tests, ~0.2s, no network
uv run ruff check src tests
```

The tests are hermetic — they construct page evidence directly, so the suite
never touches a node's website.

Five tests exist because of mistakes this tool actually made, and are worth
reading as documentation of them:

| Test | The mistake it prevents |
|---|---|
| `test_a_well_rendered_page_still_fails_when_the_link_is_genuinely_absent` | Reporting "no contact route of any kind was found" from a page that had not rendered. That describes the tool, not the node. Absence-based failures are now gated on the page having actually rendered — and this test stops that gate becoming a blanket excuse. |
| `test_point1_does_not_fail_on_403_with_no_login_offered` | Asserted `FAIL` originally. Inverted after GÉANT returned 403 purely in response to this tool's own request volume. |
| `test_run_does_not_pass_typer_descriptors_to_its_helpers` | `basic-check run` was documented here as working and crashed on every invocation: calling a Typer-decorated function from Python passes its option *descriptors*, not their values. Nothing tested the CLI, so the suite was green throughout. |
| `test_url_runs_are_written_somewhere_else_by_default` | A one-off `--url` check writing into `results/` would replace the committed nine-node report with a one-row table, since `assess` rewrites those files wholesale. |
| `test_every_link_a_check_can_use_is_a_link_the_crawler_will_follow` | The crawler looked for "acceptable use" while the check also accepted "terms of use", so links the checks relied on were never fetched. Four PASSes were weaker than they appeared. Nothing failed; the output was just quietly thinner than it claimed. |

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
