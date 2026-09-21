# Installation, configuration and run guide

`eosc-basic-compliance` checks EOSC Node Landing Pages against the
**Node Landing Page Verification Checklist v3.0** (15 September 2026) and writes
a report: a matrix of nodes against checklist points, with the evidence behind
every verdict.

This guide covers installing it, configuring it for your own nodes, running it,
reading what comes out, and running the test suite. Every command below was
executed against a clean clone of the repository on 21 September 2026, and every
figure in it — test counts, verdict tallies, request counts, disk sizes — was
re-measured rather than carried over; where a command's behaviour is surprising,
that is noted rather than smoothed over.

**What this tool will not do:** it does not produce a compliance statement. Of
the ten checklist points, three can be settled by inspection, four only partly,
and three require a human reading the page. The tool returns `MANUAL_REVIEW`
rather than guessing, and roughly 60% of cells land there by design. A checker
that returned PASS/FAIL on every line would look more useful and be worth less.

👉 **[Analysis workflow](ANALYSIS-WORKFLOW.md)** — the companion to this guide. This
one tells you how to run the tool; that one tells you what it does once running:
the collection sequence, the evidence model, and for each of the ten checklist
points the exact branch conditions and the verdict each one yields. Read it when
you want to predict a verdict, argue with one, or change a check.

---

## 1. Requirements

| | |
|---|---|
| Python | 3.12 or newer (the project is developed on 3.14) |
| Package manager | [`uv`](https://docs.astral.sh/uv/) |
| Browser | Chromium, via Playwright — **only needed to collect evidence** |
| Disk | ~500 MB for the virtualenv, ~660 MB more for Chromium (see the note below) |
| Network | Outbound HTTPS to the node websites, for collection only |

Installing `uv`, if you do not have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh    # macOS / Linux
```

You do not need to create a virtualenv or run `pip install`. `uv` manages the
environment from `uv.lock`, so everyone gets identical dependency versions.

**On the disk figures.** Both were measured with `du -sh`, not estimated. The
500 MB is `.venv` in the project directory (490 MB in a fresh clone, rising to
about 510 MB once caches accumulate). The 660 MB is one Playwright install
— Chromium (393 MB), the headless shell (261 MB) and ffmpeg (5 MB) — and it does
**not** live in the project: Playwright puts browsers in a shared cache at
`~/.cache/ms-playwright`, so a second project on the same machine reuses it and
costs nothing. That cache can nonetheless grow well past 660 MB, because each
Playwright version keeps its own browser build; the machine this was measured on
held two versions and so 1.3 GB in total. Delete the whole directory and re-run
`playwright install` to reclaim it.

---

## 2. Installation

```bash
git clone https://github.com/marioreale/eosc-basic-compliance.git
cd eosc-basic-compliance
uv sync --locked
```

This creates `.venv/` and installs exactly the versions pinned in the committed
`uv.lock` — 27 packages. Expect it to take under a minute. A plain `uv sync`
also works, but it will silently re-resolve if the lockfile and
`pyproject.toml` ever disagree; `--locked` fails instead, which is what you want
when the point is to reproduce someone else's result. CI uses `--locked` for the
same reason (section 8).

At this point you can already run the test suite, read the checklist, and
regenerate the committed nine-node report from the evidence in the repository.
To **fetch pages**, you also need a browser:

```bash
uv run playwright install chromium --with-deps
```

This downloads roughly 660 MB (see the note in section 1). On Linux,
`--with-deps` also installs system libraries and will ask for `sudo`. If you
only want to re-render reports from evidence already in the repository, skip
this step.

### What needs a browser, and what does not

This distinction saves a large download in CI and on review machines:

| Command | Browser | Network | What it does |
|---|---|---|---|
| `points` | no | no | Prints the checklist and what is machine-decidable |
| `assess` | no | no | Applies the checklist to evidence already on disk |
| `show` | no | no | Prints one node's results in the terminal |
| `collect` | **yes** | **yes** | Fetches pages and saves evidence |
| `run` | **yes** | **yes** | `collect`, then `assess` |
| `pytest` | no | no | The whole test suite is offline |

Verified: with `PLAYWRIGHT_BROWSERS_PATH` pointed at an empty directory, all
111 tests still pass, while `collect` fails with Playwright's
`Executable doesn't exist … run playwright install`.

### Verifying the installation

```bash
uv run pytest -q                  # expect: 111 passed
uv run ruff check src tests       # expect: All checks passed!
uv run basic-check points         # prints the ten checklist points
```

If `pytest` passes, the checklist transcription, the check logic and the report
renderer are all working. No network access is involved.

---

## 3. Configuration

Two files control what is checked, and a third optional one supplies an input
the repository cannot ship. The two are plain YAML and both are meant to be
edited; the third is a plain text list you write yourself.

### `nodes.yaml` — which pages to check

```yaml
nodes:
  - id: bbmri-eric
    name: BBMRI-ERIC
    url: https://www.bbmri-eric.eu/eosc-node-bbmri-eric/
    eosc_page: https://eosc.eu/building-the-eosc-federation/eosc-node-bbmri-eric/
```

| Field | Meaning |
|---|---|
| `id` | Short slug. Used for evidence filenames and for `--only` / `show`. |
| `name` | Display name in the report. |
| `url` | **The URL registered in the EOSC EU Node Contributors Dashboard** ("Website address", section 1.2 field 6). That registered URL is what the checklist defines as the Node Landing Page. If the URL here differs from the registered value, the registered value wins — correct this file. |
| `eosc_page` | The node's dedicated entry on `eosc.eu`, which checklist point 4 requires the landing page to link to. |

`eosc_page` is what lets a point 4 failure name the exact URL that is missing,
rather than reporting a bare absence. The slugs in the committed file were read
from the live index at
[eosc.eu/building-the-eosc-federation/](https://eosc.eu/building-the-eosc-federation/).
If you add a node, look its slug up there rather than guessing it from the name.

### `checklist/v3.0.yaml` — the rules

One entry per checklist point. The `requirement` text is quoted verbatim from
the source document so a reader can audit the rule without a diff, and
`decidable` records whether a script can settle the point at all:

- `true` — decidable by inspection (points 1, 4, 7)
- `partial` — partly decidable; the tool gathers evidence and defers (3, 5b, 5c, 6)
- `false` — needs a human reading the page (1R, 2, 5a)

The file also pins its own provenance: `source_file` names the committed PDF the
transcription was made from and `source_sha256` is that file's hash, asserted by
`tests/test_checklist.py`. Be clear about what this proves — it pins the exact
bytes the transcription came from, which catches silent drift when a checklist
is revised. It is not a signature, and the committed PDF is a rendering of the
circulated `.docx`, not that `.docx` itself.

**If the checklist is revised to v3.1,** add a new `checklist/v3.1.yaml` with its
own source file and hash rather than editing v3.0 in place. Past runs should
remain reproducible against the rules that produced them.

### The approved-names file — `--approved-names`

Checklist point 3 has two halves: an EOSC logo, and **the official
Tripartite-approved node name**. The repository ships no list of those names,
because there is no authoritative machine-readable source for them — they come
from the Tripartite governance process, not from a file you can fetch. So you
supply the list yourself, and until you do, the name half of point 3 is not
assessed at all.

The format is as plain as it looks: a text file, one name per line. Blank lines
are skipped and surrounding whitespace is stripped.

```text
EOSC Node - BBMRI-ERIC
EOSC Node EUDAT
EGI Node
```

Note the third line. Nodes do not share a naming convention on their own pages:
that one writes `EGI Node`, not `EOSC Node EGI`. Take each name from the
Tripartite-approved list and check it against how the page actually writes it,
rather than deriving all of them from one pattern.

**Only the body text is searched.** The match runs against `full_text`, which
excludes the HTML `<title>`. That page's title is `EGI Node - EGI`, and that
string appears nowhere in the body, so a name taken from the browser tab will
not match. Take the name from the visible page.

```bash
uv run basic-check assess --approved-names approved-names.txt
uv run basic-check run --approved-names approved-names.txt
```

The file is not committed, and should not be: the list is an input you are
accountable for, not a project artefact.

**What matters about it, all verified against the committed evidence:**

| Behaviour | Consequence |
|---|---|
| Comment lines are **not** supported | A leading `#` line is read as a node name. Do not annotate the file. |
| Matching is an unanchored, case-insensitive **substring** of the page text | Not a whole-word or whole-phrase match. See the warning below. |
| The list is matched as a **whole**, not per node | Any name matching anywhere on any node's page satisfies that node's evidence line. The tool does not know which name belongs to which node. |
| The name never changes the verdict | Point 3 stays `MANUAL_REVIEW` either way. The list adds an evidence line for the reviewer; it cannot produce a `PASS`. |
| Only the first match is reported | If several names hit, the evidence names one of them. |

**⚠️ Short names match inside longer words.** With `EGI` in the list, the
BBMRI-ERIC page reports `approved name matched: EGI` — the hit is inside
"strat**egi**c". The Data Terra page matches the same way, inside
"Norw**egi**an". Neither page contains the EGI node name at all.

This is a defect in the check, not a finding about those nodes. Two practical
consequences:

- **Write names in full**, as they appear on the page: `EOSC Node EGI` rather
  than `EGI`. Longer strings do not collide by accident.
- **Read the matched name, never just the fact of a match.** The evidence line
  names which string hit, precisely so the reviewer can catch a match like the
  one above. A report that only said "matched" would be worse than no list.

Write the name exactly as it appears in the page text, punctuation included:
`EOSC Node - BBMRI-ERIC` matches that page, while `EOSC Node BBMRI-ERIC`
without the dash does not. If a name you expect does not match, read
`full_text` in that node's evidence file before assuming the page is at fault.

Whether you supplied a list is recorded in `results.json` as
`approved_names_supplied`, so a report cannot quietly imply the name was
checked when it was not. Note that this flag is in the JSON only — the HTML and
Markdown reports do not currently display it.

---

## 4. Running it

```bash
uv run basic-check run
```

That is the whole thing: fetch all nine nodes, apply the checklist, write the
reports. It takes a few minutes, most of it spent deliberately waiting between
requests.

### The commands

```bash
uv run basic-check points            # the checklist, and what is decidable
uv run basic-check collect           # fetch -> results/evidence/
uv run basic-check assess            # evidence -> results/
uv run basic-check run               # collect, then assess
uv run basic-check show eudat        # one node's results in the terminal
```

### Useful options

Not every option is accepted by every command, and passing one to the wrong
command is an error rather than a no-op. Each table below names the commands that
accept the option.

**Fetching** — `collect` and `run` only, because only these two touch the network:

| Option | Effect |
|---|---|
| `--depth N` | How far to follow links. See section 5. |
| `--delay S` | Seconds between hosts (default 2.0). Raise it to be gentler. |
| `--fetch-budget N` | Depth 2 only: hard ceiling on second-hop requests for the **whole run** (default 60). |
| `--max-children N` | Cap on followed pages per node at depth 1 (default 8). **`collect` only — `run` rejects it**, so use `collect` then `assess` if you need it. |

**Choosing what to check** — accepted by `collect`, `assess` and `run`:

| Option | Effect |
|---|---|
| `--only a,b` | Restrict to some nodes. **Read the warning below.** |
| `--url https://…` | Check any page without editing `nodes.yaml`. Repeatable. |
| `--eosc-page URL` | With a single `--url`: that node's own `eosc.eu` page, so a point 4 failure can name the exact URL that is missing. |
| `--nodes path` | Use a different node list. |

**Assessment and output:**

| Option | Where | Effect |
|---|---|---|
| `--approved-names path` | `assess`, `run` | Text file, one Tripartite-approved node name per line. **Without it, point 3's name requirement cannot be checked at all.** See section 3 for the format and its pitfalls. |
| `--checklist path` | `assess`, `run`, `points` | Use a different checklist version. |
| `--run LABEL` | `assess`, `run` | Label stored with the run, for telling one report from another. |
| `--results path` | all but `points` | Write somewhere other than `results/`. |
| `--one-off` | `show` only | Read `results/one-off/` instead of the federation run. |

### ⚠️ `--only` rewrites the shared report

This is a real defect, reproduced on a clean clone while writing this guide, and
it will mislead you if you do not know about it:

```bash
uv run basic-check assess --only data-terra
# results/results.json now contains ONE node, not nine.
```

`--only` scopes the **report**, not just the fetching. The nine-node matrix in
`results/` is replaced by a single row, and if you then look at `index.html` you
will see what appears to be a federation report covering one node.

Your evidence is not lost, so recovery is immediate and cheap:

```bash
uv run basic-check assess      # no --only: rebuilds all nine rows from disk
```

Verified on a clean clone: nine nodes restored, tally unchanged at 28 PASS /
7 FAIL / 55 review. **Use `--only` for fetching a subset gently, then always
finish with a bare `assess` before circulating anything.** Do not commit a
report produced with `--only`.

### Checking a page not in `nodes.yaml`

```bash
uv run basic-check run --url https://example.org/our-node-page
```

Ad hoc checks write to `results/one-off/` so a published run is never
overwritten, and the report carries a banner saying it is not a federation run.
That banner matters: these reports circulate before a production decision, and a
stray single-page file that looks official is a genuine hazard.

---

## 5. How deep to go: `--depth`

| `--depth` | What is fetched | Requests, 9 nodes, 21 Sep 2026 |
|---|---|---|
| `0` | The landing page only. | 9 |
| `1` **(default)** | The landing page, plus links from it that could settle a checklist point — policy, contact, about. At most 8 per node, 2 per point. | 31 (9 + 22) |
| `2` | The above, plus one further hop: a policy *index* that links on to the actual policy, for instance. At most 2 per fetched page and 1 per point, under a run-wide budget. | 45 (9 + 22 + 14) |

Links are followed only where the target could settle a point, so a policy link
is verified rather than taken on the strength of its label.

```bash
uv run basic-check run --depth 2                    # bounded by the default budget
uv run basic-check run --depth 2 --fetch-budget 20  # stricter ceiling
```

**A depth-2 run reports both depths.** You get two summary tables — *Results at
depth 1* and *Results at depth 2* — two explanatory sections, a list of every
cell whose verdict differs, and a table of exactly which second-hop pages were
fetched and what each was followed for.

Both tables come from the **same capture**: the shallow view is the deep
evidence with the second-hop pages set aside, not a second run. Nothing is
fetched twice to produce the comparison, so any difference between the two
tables is the extra hop and not the page changing in between.

**Is depth 2 worth it?** On this federation, so far, no. Two depth-2 runs on
21 September (18 and 14 second-hop requests) each changed **zero** verdicts. That
is a finding, not a disappointment: the points still marked review turn on a
judgement ("clearly state") or quantify over things no crawl enumerates ("all
research resources offered by the Node"), and no amount of fetching settles
either kind. Run it yourself before assuming the same holds for another
federation or a later date.

### Be considerate with other people's servers

These are production sites that did not ask to be tested. The defaults are
deliberately restrained: one request per node every two seconds, a per-node cap
on followed links, and a single run-wide budget for second-hop requests rather
than a per-node one.

This is not theoretical. `geant.org` served `HTTP 200` at 12:43 UTC on
21 September and `HTTP 403` at 13:07 the same afternoon, after several runs,
redirecting to a Cloudflare bot-protection challenge. **Repeated automated runs
are visible to the sites you are checking.** Run the full suite when you need a
result, not in a loop, and use `assess` — which needs neither browser nor
network — when you are iterating on the report itself.

---

## 6. Reading the output

`results/` after a run:

| File | What it is |
|---|---|
| `index.html` | **The deliverable.** The matrix, per-node detail, and the full checklist text. Open it in a browser. |
| `results.md` | The same content as Markdown, for reading on GitHub or pasting into a document. |
| `results.csv` | One row per node-point, for a spreadsheet or pivot table. |
| `results.json` | The full structured run, including every piece of evidence. Use this for any further analysis. |
| `checklist-v3.0.html` | The checklist points in full, with the reasoning behind each verdict. |
| `evidence/<id>.json` | The raw capture for one node: links, images, controls, text, headers. |
| `evidence/screenshots/<id>.png` | What the page looked like when it was fetched. |

### The four verdicts

| | Meaning |
|---|---|
| 🟢 **PASS** | Satisfied, and the tool can show why. |
| 🔴 **FAIL** | Violated, and the tool can show why. |
| 🟠 **review** | A human must decide. The tool has gathered the evidence and refuses to guess. |
| 🟣 **ERROR** | Could not be assessed at all. |

**A FAIL is an accusation, so the tool is careful about making one.** Absence is
never concluded from a page that did not render: if a capture yields no links at
all, or fewer than ten DOM elements, or under 500 characters of text, the tool
returns review rather than FAIL. The point is that "we found no contact link" and
"the page did not load for us" must not produce the same verdict.

The same restraint applies to being blocked. GÉANT's `HTTP 403` moved four cells
from decided verdicts to review — the tool does not convert bot protection into
a compliance failure.

### Reproducing a verdict by hand

Every verdict is traceable to evidence on disk:

```bash
uv run basic-check show geant                      # verdicts and evidence in the terminal
python3 -m json.tool results/evidence/geant.json | less   # the raw capture
```

`results.json` carries the same evidence strings the report displays, so you can
check any claim without re-fetching anything.

To work out *why* a particular cell came out the way it did, the decision
procedure for every point — every branch, in evaluation order, with the verdict
it yields — is tabulated in section 5 of the
**[analysis workflow](ANALYSIS-WORKFLOW.md)**. Section 6 of that document lists the
cases where the tool is known to be wrong, which is the first place to look when
a verdict surprises you.

---

## 7. The test suite

```bash
uv run pytest -q                    # 111 tests, offline, well under a second
uv run pytest -v                    # names of every test
uv run pytest tests/test_checks.py  # one file
uv run pytest -k depth              # anything about depth
uv run ruff check src tests         # lint
```

| File | Tests | Covers |
|---|---|---|
| `test_checklist.py` | 8 | The transcription matches the source document, including its SHA-256. |
| `test_checks.py` | 34 | The verdict logic, point by point, including the render gate. |
| `test_cli.py` | 22 | Command wiring, options, ad hoc `--url` isolation. |
| `test_crawl.py` | 34 | Link selection, host containment, depth-2 budget, the depth-1 view. |
| `test_report.py` | 13 | Matrix rendering, the dual-depth tables, table-breaking input. |

The suite makes no network requests and needs no browser, which is why CI runs
it without downloading Chromium.

**Test names are sentences**, because a failing test should tell you what broke
without opening the file:

```
test_a_consent_banner_does_not_excuse_a_missing_link
test_the_two_tables_show_their_own_verdicts
test_a_pipe_in_a_url_cannot_break_the_table
```

### A note on what a passing suite means

Green means nothing objected. It does not mean everything was verified.

When adding a check, make the test fail first, then implement — and when
changing a guard, mutate it deliberately to confirm the test actually bites. A
test that cannot fail is worse than no test, because it produces confidence
without evidence. Both dual-depth guards in `test_report.py` were confirmed this
way: rendering the deep results in the shallow table, and forcing the stray
heading back, each fail exactly one test.

---

## 8. Continuous integration

`.github/workflows/tests.yml` runs on every push and pull request:
`uv sync --locked`, `ruff check`, then `pytest` with a JUnit report published to
the run summary and uploaded as an artifact. No browser is installed, because
the suite does not need one.

Both workflows use `--locked` rather than a plain `uv sync`. The difference
matters: plain `uv sync` quietly updates the lockfile when it disagrees with
`pyproject.toml` and carries on, so a dependency change could go green in CI
while the versions tested were not the versions committed. `--locked` installs
exactly what `uv.lock` pins and fails otherwise. If CI ever stops at the install
step saying the lockfile needs updating, that is the guard working — run
`uv lock` and commit the result.

`.github/workflows/compliance.yml` is **manual dispatch only** — deliberately.
A scheduled compliance run would mean fetching nine production websites on a
timer, which is exactly the behaviour that got GÉANT's bot protection to start
refusing requests.

---

## 9. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Executable doesn't exist … playwright install` | Chromium is not installed. Run `uv run playwright install chromium --with-deps`. Not needed for `assess`, `show`, `points` or `pytest`. |
| `results.json` has one node after using `--only` | Known defect, section 4. Run a bare `uv run basic-check assess` to rebuild all rows from evidence on disk. |
| A node shows `HTTP 403` and everything moved to review | Bot protection, not an access policy. Check `final_url` in the evidence for a `__cf_chl_rt_tk` parameter. Wait, run less often, or verify that node by hand in a browser. |
| Everything is review for one node | The capture probably did not render. Look at `evidence/screenshots/<id>.png` — that is exactly what the render gate is protecting you from. |
| `test_checklist.py` fails on a hash | The checklist PDF changed. That is the test doing its job: transcribe the new version into a new YAML file rather than adjusting the hash. |
| A run takes far longer than expected | `--delay` defaults to 2.0s between hosts and slow nodes are waited on. This is intentional. |
| Point 3 reports `NONE of the supplied approved names appear` for a node you know is named correctly | The match is a literal substring of the body text and the `<title>` is not searched. Read `full_text` in that node's evidence file and copy the name as the page writes it, punctuation included. Section 3. |
| Point 3 reports a matched name that belongs to a different node | A short name matched inside an ordinary word. Write names in full. Section 3. |

---

## 10. Extending it

- **Add a node:** append to `nodes.yaml` with its `eosc.eu` slug from the live index.
- **Add a checklist version:** new YAML beside `v3.0.yaml`, with `source_file` and `source_sha256`; do not edit an existing version in place.
- **Add a check:** implement in `src/basic_check/checks.py`, write the failing test first, and prefer returning `MANUAL_REVIEW` with good evidence over a confident guess. Document its branches in [`ANALYSIS-WORKFLOW.md`](ANALYSIS-WORKFLOW.md) — a check whose decision procedure is not written down cannot be reviewed.
- **Change the report:** `src/basic_check/report.py` renders HTML, Markdown and CSV from one run dict. `tests/test_report.py` covers the matrix; add to it, because a rendering bug is silent.

Two known latent defects in `report.py`, both unfixed at the time of writing: a
`|` in a **node name** yields a misaligned Markdown row, and a newline inside an
evidence string breaks the Markdown list. Neither is triggered by the current
node list. A pipe in a second-hop *URL* is already handled and tested.

---

## Sources

- Checklist: `checklist/20260910_Node_Landing_Page_Verification_Checklist_v3.0.pdf`, transcribed to `checklist/v3.0.yaml` with its SHA-256 pinned
- EOSC Federation node index: https://eosc.eu/building-the-eosc-federation/
- Repository: https://github.com/marioreale/eosc-basic-compliance
- `uv` documentation: https://docs.astral.sh/uv/
- Playwright for Python: https://playwright.dev/python/
