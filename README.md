# eosc-basic-compliance

Checks EOSC Node Landing Pages against the **Node Landing Page Verification
Checklist v3.0** (15 September 2026). One result per checklist point, per node.

**Deliberately light on the nodes' websites.** Each landing page is loaded once in
a headless browser. The tool then follows **at most one level** of links, and only
links that can actually settle a checklist point — a policy, a contact page, an
about page. Everything else is left alone. Across the twelve nodes assessed on
24 September 2026 that was **32 extra requests** at the default depth of 1,
spaced 1.2 s apart, with `robots.txt` honoured per host. Evidence is saved to disk and every check reads only that
saved evidence, so re-running the rules costs nothing.

Set `--depth 0` for the strict one-request-per-node behaviour, or `--depth 2` to
follow one further hop under a fixed budget.

👉 **[Installation, configuration and run guide](docs/GUIDE.md)** — start here if
you want to install and run it yourself.
([Word](docs/eosc-basic-compliance-guide.docx) · [PDF](docs/eosc-basic-compliance-guide.pdf))

👉 **[Test suite and configuration overview](docs/TEST-SUITE.md)** — what the 339
tests cover, every configuration option, the defects that earned a regression
test, and what the published figures do and do not say.
([Word](docs/eosc-basic-compliance-testsuite.docx) · [PDF](docs/eosc-basic-compliance-testsuite.pdf))

👉 **[Analysis workflow](docs/ANALYSIS-WORKFLOW.md)** — what the tool does once
running, step by step: the collection sequence, the evidence model, and the exact
conditions behind each of the ten checklist points.
([Word](docs/eosc-basic-compliance-analysis-workflow.docx) · [PDF](docs/eosc-basic-compliance-analysis-workflow.pdf))

The Word and PDF copies are built from the Markdown guides at commit `b2fb946`.
The Markdown is the source, so if the two differ, the Markdown is current.

👉 **[Latest results](results/results.md)** · [browsable HTML report](results/index.html)
· [checklist v3.0 explained](results/checklist-v3.0.html)
(download and open locally, or use the GitHub Pages link if enabled)

## What it found

> **The published report covers twelve of the thirteen configured nodes.** EOSC
> Node Italy was skipped by request (`--skip Italy`): on 24 September 2026
> `eosc.it` had no A or AAAA record and `www.eosc.it` did not resolve. The report
> says so in a "Skipped by request" banner. Italy is not counted as missing
> evidence, and it does not appear in any count below.

Twelve landing pages, all fetched 24 September 2026 at `--depth 1`, all
`HTTP 200` to an anonymous request. Run `live-2026-09-24-no-italy`, assessed
against the official unscoped names list.

The per-node results are **not reproduced here**. The full matrix, with the
evidence behind every verdict, is in the report linked above:
**[Latest results](results/results.md)**.

120 cells: 🟢 44 PASS · 🔴 6 FAIL · 🟠 70 review. These are the tool's verdicts after the
point 6 and 5b/5c fixes, re-assessed from the same evidence; the first assessment
of this run gave 45 / 6 / 69.

**The automated verdicts were reviewed by hand before publication.** The review
is published beside them as
**[results/REVIEW-2026-09-24.md](results/REVIEW-2026-09-24.md)**, and it does not
alter the tool's output. It records:

- three point 6 PASSes resting on link text alone: two were false, and
  BBMRI-ERIC's was upheld on the helpdesk mailboxes of its contact page;
- one AUP link, GÉANT's, that the tool missed (both have since been fixed in
  the checks, and the review's addendum shows the effect);
- the verification of Slovakia's AUP/UAP PDF;
- visual logo checks from the screenshots;
- proposed determinations for points 2 and 3.

Read it before quoting a cell.

> **Two rows describe a page, not a node.** CERN's configured URL is an INDIGO
> IAM sign-in form, and EBRAINS's is the general EBRAINS homepage, which does not
> mention EOSC. Both rows are published with that caveat, pending each node's
> registered Website address.

Compared with the previous published run (21 September 2026, nine nodes):

- **EOSC DTO** now links its own `eosc.eu` entry and a helpdesk. Points 4 and 6
  moved from `FAIL` to `PASS`.
- **GÉANT** was served this time, where on 21 September it got a Cloudflare
  `HTTP 403`. Points 1, 6 and 7 are now `PASS`, and point 4 is now `FAIL`.
- **CERN, Czechia and Slovakia** appear for the first time.
- **The point 6 and 5b/5c fixes** make GÉANT 5b a `PASS` and move EBRAINS 6
  from `PASS` to review.

No other verdict changed.

**The one clear, repeated finding is checklist point 4.** Every node has a
dedicated page under `eosc.eu/building-the-eosc-federation/` — the slugs were
read from the live index — but six of the twelve landing pages do not link to
their own:

- four (Data Terra, EOSC Finland, EGI, EBRAINS) link to nothing on `eosc.eu` at all;
- two (PaNOSC, GÉANT) link only to the federation index page, which the
  checklist explicitly excludes.

BBMRI-ERIC, Czechia, EOSC DTO, EUDAT and Slovakia link correctly. CERN's sign-in
page has no such link, but it is left to review rather than failed. Each failure
names the exact URL that is missing, so the fix is a one-line edit.

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
uv run basic-check run --skip Italy,Slovakia  # every node except these (ids or names)
uv run basic-check assess            # evidence -> results/{index.html,results.md,.csv,.json}
uv run basic-check run               # collect + assess
uv run basic-check run --depth 2     # follow one further hop (see below)
uv run basic-check show data-terra   # one node's results in the terminal
```

### Command-line options

`uv run basic-check --help` lists the commands, the node ids and some examples,
and `uv run basic-check <command> --help` lists that command's options. The
tables below give the same information. Only `collect` and `run` contact the
nodes; `assess`, `points` and `show` work offline.

| Command | What it does |
|---|---|
| `collect` | Fetches each landing page and saves the evidence, with personal data masked. The only step that sends requests to the nodes, together with `run`. |
| `assess` | Applies the checklist to the evidence already saved and writes `results.json`, `results.md`, `results.csv` and `index.html`. |
| `run` | `collect`, then `assess`, in one go. |
| `points` | Prints the ten checklist points and whether each can be decided by a script. |
| `show <node_id>` | Prints one node's results from an existing run. |

**Which nodes to check** (`collect`, `assess`, `run`)

| Option | What it's for |
|---|---|
| `--nodes`, `-n <path>` | A node list to use instead of `nodes.yaml`: a separate list of candidate nodes, or the list an old run was collected with, to rebuild it. |
| `--only <ids>` | Fetch only these nodes, as comma-separated ids (`egi,eudat`). Ids only, not names. Writing to `results/`, the report still covers every node and marks which were fetched again; with `--results DIR` it covers only these. |
| `--skip <ids or names>` | Leave these nodes out entirely: not fetched, not assessed, not in the report, which says they were skipped. An id or a name (`eosc-it`, `Italy`, `EOSC Node Italy`), in any case; comma-separated or repeated. A value that matches no node, or more than one, is an error. |
| `--url <url>` | Check a page that is not in `nodes.yaml`. Repeatable. Writes to `results/one-off/`, so the published run is never overwritten. Cannot be combined with `--only` or `--skip`. |
| `--eosc-page <url>` | With a single `--url`: the node's own `eosc.eu` page, so a point 4 failure names the exact missing link. |

**How much to fetch** (`collect`, `run`)

| Option | Default | What it's for |
|---|---|---|
| `--depth 0\|1\|2` | `1` | `0` fetches the landing page only. `1` also follows links that can settle a checklist point (policies, contact, about). `2` follows one more hop from those pages, and the report shows both depths side by side. |
| `--max-children <n>` | `8` | The most linked pages followed per node at depth 1. `collect` only; `run` always uses 8. |
| `--fetch-budget <n>` | `60` | Depth 2 only: a hard limit on second-hop requests for the whole run, shared across all nodes. |
| `--delay <seconds>` | `2.0` | The pause between hosts, to go easy on the servers. |

**How to assess** (`assess`, `run`)

| Option | What it's for |
|---|---|
| `--checklist`, `-c <path>` | A rules file to use instead of `checklist/v3.0.yaml`, for example a future v3.1. `points` takes it too. |
| `--approved-names <path>` | A list of approved node names for point 3, replacing `checklist/approved-names.txt`. `node-id: Name` ties a name to one node; a bare name counts for every node. |
| `--no-approved-names` | Use no name list at all; point 3's name requirement is then not assessed. |
| `--strict-separators` | Match the separators in approved names exactly. By default spaces, `\|`, `-`, `–`, `:`, `/` and `·` count as equivalent. |
| `--run <label>` | A label for the run, recorded in the report, such as `live-2026-09-24-no-italy`. By default, the current UTC time as `YYYY-MM-DD-HHMM`. |

**Where results go**

| Option | Commands | What it's for |
|---|---|---|
| `--results <path>` | `collect`, `assess`, `run`, `show` | A folder to write to or read from instead of `results/`, for example `/tmp/trial` for a scratch run. |
| `--one-off` | `show` | Read the `--url` results in `results/one-off/`. |

**Node ids.** Each node's id is the `id:` field in `nodes.yaml`, and
`basic-check --help` prints the current list:

| Id | Node | Id | Node |
|---|---|---|---|
| `bbmri-eric` | BBMRI-ERIC | `eudat` | EUDAT |
| `cern` | CERN | `egi` | EGI |
| `eosc-cz` | EOSC Node Czechia | `geant` | GÉANT |
| `eosc-dto` | EOSC DTO (D4Science) | `ebrains` | EBRAINS |
| `data-terra` | Data Terra | `eosc-it` | EOSC Node Italy |
| `eosc-fi` | EOSC Finland | `eosc-sk` | EOSC Node Slovakia |
| `panosc` | PaNOSC | | |

**Examples**

```bash
# Check only EGI and EUDAT, in a scratch folder, leaving results/ untouched
uv run basic-check run --only egi,eudat --results /tmp/trial

# Every node except Italy; --skip takes an id or a name
uv run basic-check run --skip Italy --results /tmp/trial

# Leave out two nodes, and fetch the landing pages only
uv run basic-check run --skip eosc-it,bbmri-eric --depth 0 --results /tmp/trial

# Re-assess Czechia from the evidence already in /tmp/trial, offline
uv run basic-check assess --only eosc-cz --results /tmp/trial

# One node's results from the published run
uv run basic-check show geant
```

### Adding a node

Three files change together, all at the repository root, all edited by hand:

| File | What to add |
|---|---|
| `nodes.yaml` | The entry: `id`, `name`, `url` (the landing page **as registered** in the EOSC EU Node Contributors Dashboard, "Website address", section 1.2 field 6) and `eosc_page` (the node's own entry on `eosc.eu`, copied from the [federation index](https://eosc.eu/building-the-eosc-federation/) — look the slug up, do not guess it). |
| `checklist/approved-names.txt` | The node's approved name, exactly as the Tripartite list writes it, `EOSC Node \| ` prefix included. |
| `checklist/approved-names-scoped.txt` | The same name, prefixed with the node id: `cern: EOSC Node \| CERN`. |

Then `uv run pytest -q` before running the checker: `tests/test_nodes.py` and
`tests/test_checklist.py` fail with the specific problem if the three files
disagree, in milliseconds and without touching the network. Then
`basic-check collect --only <new-id>` and `basic-check assess`.

Nothing else in the repository needs changing, and nothing is auto-discovered.
[docs/GUIDE.md](docs/GUIDE.md) section 3 covers each field, the failure modes,
and what does and does not carry over if you maintain a copy on another host
such as GitLab.

### Worked examples

Section 11 of [docs/GUIDE.md](docs/GUIDE.md) and of
[docs/TEST-SUITE.md](docs/TEST-SUITE.md), and section 8 of
[docs/ANALYSIS-WORKFLOW.md](docs/ANALYSIS-WORKFLOW.md), give every file and
command for the three changes that come up most:

1. **Adding a node** and publishing a run that includes it, contacting only the
   new node's site.
2. **Changing a node's URL.** Only the `url` line in `nodes.yaml` changes.
   Until that node is collected again, `assess` warns, and both reports carry an
   "Evidence from a different URL" banner.
3. **Moving to a new revision of the checklist.** There is no URL to change: the
   tool never downloads the checklist. Commit the new document, add a
   `checklist/vX.Y.yaml` for it, and change the one line `DEFAULT_CHECKLIST` in
   `src/basic_check/cli.py`.

### How deep to go: `--depth`

| `--depth` | What is fetched | Requests in the 21 Sep 2026 run |
|---|---|---|
| `0` | The landing page only. | 9 |
| `1` **(default)** | The landing page, plus links from it that could settle a checklist point — policy, contact, about pages. At most 8 per node, 2 per point. | 31 (9 + 22) |
| `2` | The above, plus one further hop from those pages: a policy *index* that links on to the actual policy, for instance. At most 2 per fetched page and 1 per point, and the whole run shares a single `--fetch-budget` (default 60 requests). | 45 (9 + 22 + 14) |

Depth 2 exists for the case where the answer is one click past where depth 1 stops. It is not the default, for two reasons. The first is other people's servers: every extra hop multiplies requests against production sites that did not ask to be tested, which is why the budget is a hard ceiling for the whole run rather than a per-node limit. The second is that, on this federation, it has not yet changed anything.

```bash
uv run basic-check run --depth 2                    # bounded by the default budget
uv run basic-check run --depth 2 --fetch-budget 20  # stricter ceiling
```

**A depth-2 run reports both depths.** The report renders two summary tables — *Results at depth 1* and *Results at depth 2* — followed by a *What the second hop changed* section listing every cell whose verdict differs, and a table of exactly which pages the second hop fetched and what each was followed for. Both tables are computed from the **same capture**: the shallow view is the deep evidence with the second-hop pages set aside, not a second run. So any difference between the two tables is the extra hop, not the page changing between runs.

On the 21 September 2026 run, the second hop made 14 extra requests and changed **no verdict at all** — all 90 cells landed exactly where depth 1 had them. An earlier depth-2 run the same day, with 18 second-hop requests, also changed nothing. That is a finding rather than a disappointment: the points still marked review turn on a judgement ("clearly state") or quantify over things no crawl enumerates ("all research resources offered by the Node"), and no amount of fetching settles either kind. Run it yourself before assuming the same holds for another federation or a later date.

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

`--only` narrows which sites are contacted, not what the report covers: a subset
run still writes a row for every configured node, reusing evidence on disk for the ones it did not
re-fetch, and labels itself **Mixed freshness** so the reused rows are not taken
for fresh ones. Pass an explicit `--results DIR` when a genuinely narrower report
is what you want.

`--skip` is the opposite: it leaves the named nodes out of the run entirely.
They are not fetched, not assessed and not in the report. It takes ids or names,
case-insensitively (`--skip Italy,Slovakia` or `--skip Italy --skip Slovakia`).
A skipped node does not count as missing evidence, so `assess` does not exit 2
for it. The report is shorter, so it says so: a **Skipped by request** banner,
and a `skipped` list in `results.json`. A value that matches no node is an
error rather than being ignored. See [the guide](docs/GUIDE.md) section 4.

`collect` and `assess` are separate on purpose: assessment is re-runnable offline
against saved evidence, so changing a check never means re-requesting the pages.
`assess` exits non-zero if any configured node has no evidence, so a short table
cannot quietly look complete.

Edit `nodes.yaml` to change the list of nodes.

The official Tripartite-approved node names, used by point 3, are committed at
[`checklist/approved-names.txt`](checklist/approved-names.txt) and are used
automatically — no flag needed. To check against a different list, or none:

```bash
uv run basic-check assess                                  # official list (default)
uv run basic-check assess --approved-names my-names.txt    # your list instead
uv run basic-check assess --no-approved-names              # no list at all
```

Every report states which list the run used, together with its SHA-256, so a
stale list is detectable without re-running. Prefix a name with a node id
(`bbmri-eric: EOSC Node - BBMRI-ERIC`) to tie it to one node; the official list
is unscoped, so a match shows the name is on the page but not that it is that
page's own name, and the report says so. A scoped variant is committed at
[`checklist/approved-names-scoped.txt`](checklist/approved-names-scoped.txt) for
when you want that stronger claim — it finds the same five nodes, which is
evidence the headline is not an artefact of names leaking between pages. Word
separators are matched flexibly by default; `--strict-separators` requires the
exact glyphs and the report states which rule was in force.

In the published run of 24 September 2026, the official list matches **5 of
the 12** nodes assessed (2 of 9 on 21 September). That is a finding to review, not a verdict — point 3 stays
`MANUAL_REVIEW` either way. See
[the guide](docs/GUIDE.md#the-approved-names-file----approved-names) for the
format, how matching works, and what each node shows.

## Scope and limits

- **A short, bounded walk, not a crawl.** One level by default; `--depth 2` adds a
  single further hop under a run-wide budget, and the tool never follows a link it
  cannot use. Point 1R still cannot be settled either way: it quantifies
  over *every* resource reachable from the page, which no bounded depth covers.
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
uv run pytest -q          # 339 tests, a few seconds, no network, no browser
uv run ruff check src tests
```

Full instructions, including what needs a browser and what does not, are in the
**[installation, configuration and run guide](docs/GUIDE.md)**.

The tests are hermetic — they construct page evidence directly, so the suite
never touches a node's website.

Five tests exist because of mistakes this tool actually made, and are worth
reading as documentation of them:

| Test | The mistake it prevents |
|---|---|
| `test_a_well_rendered_page_still_fails_when_the_link_is_genuinely_absent` | Reporting "no contact route of any kind was found" from a page that had not rendered. That describes the tool, not the node. Absence-based failures are now gated on the page having actually rendered — and this test stops that gate becoming a blanket excuse. |
| `test_point1_does_not_fail_on_403_with_no_login_offered` | Asserted `FAIL` originally. Inverted after GÉANT returned 403 purely in response to this tool's own request volume. |
| `test_run_does_not_pass_typer_descriptors_to_its_helpers` | `basic-check run` was documented here as working and crashed on every invocation: calling a Typer-decorated function from Python passes its option *descriptors*, not their values. Nothing tested the CLI, so the suite was green throughout. |
| `test_url_runs_are_written_somewhere_else_by_default` | A one-off `--url` check writing into `results/` would replace the committed federation report with a one-row table, since `assess` rewrites those files wholesale. |
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
