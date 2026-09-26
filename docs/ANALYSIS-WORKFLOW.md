# Analysis workflow

What the test suite actually does, step by step, when it assesses a node against
the **Node Landing Page Verification Checklist v3.0**.

This document is written against the code in `src/basic_check/` as it stands, not
against the design intent. Where the implementation is weaker than the checklist
wording, that is stated rather than smoothed over — the point of this document is
that a reviewer can predict the verdict before running the tool, and can tell
which verdicts are worth trusting. It was last checked against commit `ada1b4a`
on 25 September 2026: every `file.py:line` reference below points at the current
source, and the figures quoted from runs say which run they come from.

Reading order: sections 1–4 describe the machinery shared by every point;
section 5 gives the decision procedure for each of the ten points individually;
section 6 lists the known ways the machinery can be wrong.

---

## 1. The three stages

The tool is deliberately split so that **no judgement is ever made against a live
website**. Evidence is captured once, written to disk, and every verdict is then
derived from that file.

| Stage | Command | Reads | Writes | Network |
|---|---|---|---|---|
| 1. Collect | `collect` | `nodes.yaml` | `results/evidence/<node>.json` (personal data masked), `results/evidence/screenshots/<node>.png` | yes |
| 2. Assess | `assess` | evidence JSON + `checklist/v3.0.yaml` | `results/results.json` | **no** |
| 3. Report | (part of `assess`) | the run dict in memory, masked again before rendering | `index.html`, `results.md`, `results.csv`, `checklist-v3.0.html` | no |

`run` is stages 1–3 in one invocation. `points` and `show` are inspection
commands and assess nothing.

Two consequences of the split matter in practice:

- **A verdict can be re-derived without touching the node's server.** After a
  checklist reinterpretation or a bug fix, re-running `assess` against the stored
  evidence regenerates every verdict offline, and the new report can be diffed
  against the old one.
- **The checks cannot see anything the collector did not record.** If a fact is
  not in `PageEvidence`, no check can use it — see section 3.

---

## 2. Stage 1 — collection

Per node, in order:

1. **`robots.txt` for the landing page host** (`_robots`, `fetch.py:194`).
   Fetched with a plain HTTP client (`httpx`, not the browser), with the tool's
   own User-Agent string. Three outcomes:
   - disallowed → `error = "not fetched: robots.txt disallows it"`, evidence
     record returned immediately, **every point becomes `ERROR`**. This is not
     hypothetical: on a trial run on 25 September 2026, BBMRI-ERIC's new
     `dev3.` address served `User-agent: *` / `Disallow: /`, and all ten of its
     points were `ERROR`;
   - HTTP ≠ 200 → treated as "nothing disallowed", proceed;
   - unreachable → proceed with one request, and the reason is recorded in
     `robots_note`. A network failure is not read as permission, but it is also
     not read as a prohibition.
2. **Render in a real browser.** Chromium via Playwright, viewport 1440×1000,
   locale `en-GB`, `Accept-Language: en-GB,en;q=0.9`. Navigation waits for
   `domcontentloaded` (45 s cap), then gives `networkidle` a bounded 2.5 s chance,
   then a fixed 1.2 s settle. Institutional sites run analytics that never let the
   network go idle, so the wait is bounded and whatever has rendered is taken.
   Rendering rather than plain HTTP matters: several of these landing pages are
   client-side rendered, and an HTML fetch would see an empty shell and report the
   node as having no content — a false accusation produced by the tool.
3. **Record status, final URL and redirect chain.** Redirects are captured from
   response events (first 10 kept).
4. **Extract the evidence** from the rendered DOM (`_extract`, `fetch.py:211`).
   `script`, `style`, `noscript` and `template` are removed first. Then:
   - `full_text` — all body text, whitespace-collapsed;
   - `main_text` — text of the first of `main`, `[role=main]`, `article`,
     `#content`, `.content`, falling back to `body`. Kept separate so a cookie
     banner or a language switcher cannot sway language detection;
   - `links` — every `a[href]` except `javascript:` and bare `#`, resolved to
     absolute URLs; if the anchor has no text, a nested `img`'s `alt` is used as
     its label;
   - `images` — every `img` (`src`, `alt`, `aria-label`, `title`, `class`) plus
     every `svg` (its text content as the label);
   - `controls` — every `button`, `a[href]`, `input[type=submit]` and
     `[role=button]` that has a label, taken from its text, its `aria-label` or
     its `value`;
   - `title`, `lang_attr` (the `html` element's `lang`), `meta_description`.
5. **Screenshot** the viewport (not the full page) to
   `results/evidence/screenshots/<node>.png`. Nothing in the assess stage reads
   the screenshot; it exists for the human reviewer. It captures the visible
   viewport, not the full page, so it cannot be used to confirm the absence of
   anything — a footer link is real but off-image.
6. **Depth 1, if requested.** `select_children` (`fetch.py:414`) picks which links
   to follow. A link qualifies only if it is `http(s)`, is not a binary by
   extension, is on the node's own host or a related host, and its combined link
   text and URL path matches the vocabulary of a point that a second page can
   settle. The vocabulary is defined once in `patterns.py` and consumed by both
   the crawler and the checks, so the crawler cannot fail to fetch something a
   check would have accepted.

   The purposes, in the order they consume budget:

   | Order | Point | Vocabulary |
   |---|---|---|
   | 1 | 5b | Acceptable Use Policy, AUP, terms of use/service, conditions of use, user agreement |
   | 2 | 5c | user access policy, UAP, access policy, conditions of access, access conditions |
   | 3 | 6 | helpdesk, help desk, service desk, support, ticket, contact, get in touch |
   | 4 | 2 | about, who we are, our mission, mission |

   Caps: `MAX_PER_PURPOSE = 2`, `MAX_CHILDREN = 8` per node (overridable with
   `--max-children`), 1.2 s between child requests. Each child page carries
   `selected_for`, the list of points it was fetched for, and every link that was
   matched but dropped is recorded in `children_skipped` **with the reason**. That
   list is the difference between "checked and absent" and "never looked".

   Child pages are fetched more cheaply than the landing page: 25 s timeout,
   600 ms settle, no `networkidle` wait, no screenshot.

7. **Depth 2, if requested.** Only from children that rendered — a child that
   failed has no trustworthy links. Meaner caps: `MAX_PER_PURPOSE_D2 = 1`,
   at most 2 grandchildren per child, a run-wide fetch budget of 60, 1.5 s
   between requests. A URL already fetched for this node is never fetched twice.
   `robots.txt` is consulted per host at this level too, cached one fetch per host
   per run, because following links reaches hosts the landing page never named.

   When depth 2 was used, the assess stage runs **both** the full assessment and
   an assessment of the same evidence with the second hop stripped
   (`without_depth_2`), storing the latter as `results_depth_1`. The report can
   then show what the extra requests actually changed instead of asserting they
   were worth making.

8. **Write** the whole record as JSON.

---

## 3. What the evidence contains — and what it does not

`PageEvidence` (`fetch.py:126`) holds: `node_id`, `node_name`, `requested_url`,
`fetched_at`, `final_url`, `http_status`, `redirect_chain`, `robots_allowed`,
`robots_note`, `title`, `lang_attr`, `main_text`, `full_text`, `links`, `images`,
`controls`, `meta_description`, `error`, `screenshot`, `crawl_depth`, `children`,
`children_skipped`, `crawl_note`.

`Image` holds only `src`, `alt`, `aria_label`, `title`, `css_class`, `inline_svg`.
`Link` holds `href`, `text`, `visible`. `Control` holds `text`, `href`, `tag`.

**No geometry, visibility or computed style is captured anywhere.**
`getBoundingClientRect`, `offsetWidth` and `getComputedStyle` do not appear in
`src/`. This is the single most consequential gap in the design, and it is why
point 3 can never be closed automatically: the checklist asks whether a logo is
*visibly displayed*, and the tool has recorded nothing about visibility. It knows
an element exists in the markup. It does not know whether a human would see it.

Likewise, a logo delivered as a CSS `background-image`, as an SVG sprite
reference, or from a file whose name does not contain `eosc`, is invisible to the
tool. Its absence from the evidence is not evidence of absence.

Every string in the evidence is saved with personal data masked (`privacy.py`,
through `write_evidence` in `fetch.py`). Personal addresses become
`XXXXX@domain`, phone numbers become `+CC XXXXXX`, and a name next to a masked
address becomes `XXXXX`. Role mailboxes are kept. The checks therefore run on
masked text, which costs nothing: point 6 needs a helpdesk, and no check uses a
person's address or number. Re-assessing the 24 September evidence after masking
gave the same verdict in all 120 cells, and the published run has been masked
this way since commit `ada1b4a`. The reports are masked a second time as they
are written (`write_all` in `report.py`), so a report rebuilt from evidence
captured before masking existed is masked too. Screenshots are not masked.

---

## 4. Stage 2 — the assessment machinery

`checks.run_all(ev, approved_names, expected_eosc_page)` calls exactly ten
functions in checklist order and returns exactly ten `Result` records. The
mapping between checklist point ids and check functions is asserted to be total
in both directions by the test suite, so a point cannot be silently unassessed
and a function cannot assess a point that no longer exists.

A `Result` carries `point_id`, `title`, `verdict`, `message`, `evidence` (a list
of strings), and `reviewer_action`.

### The verdict vocabulary

| Verdict | Meaning |
|---|---|
| `PASS` | Satisfied, and the tool can show why |
| `FAIL` | Violated, and the tool can show why |
| `MANUAL_REVIEW` | A human must decide; evidence is attached to make that fast |
| `ERROR` | The tool could not assess at all (page unreachable, robots disallowed) |

`MANUAL_REVIEW` is the load-bearing one. Several checklist points turn on phrases
like "clearly state", or quantify over "all research resources offered by the
Node". Neither is settleable by inspecting one page, and emitting `PASS` or
`FAIL` on them would be a guess dressed as a verdict. A wrong `FAIL` against a
named organisation is expensive to retract, so where the tool cannot know, it
says so and hands over the evidence.

### The first step of every check

Every one of the ten functions begins the same way:

```
if ev.error:  ->  ERROR
```

So a node whose landing page could not be fetched at all returns ten `ERROR`
cells, never a mix of passes and a failure.

### Shared helpers

| Helper | Line | What it does |
|---|---|---|
| `_match(text, patterns)` | 58 | Returns the matched substring for each pattern that hits |
| `_link_hits(ev, patterns)` | 67 | Links whose `"{text} {href}"` matches any pattern |
| `_fmt(link)` | 76 | Renders a link as `"label" -> href` for the evidence list |
| `_is_host(netloc, domain)` | 164 | Exact host **or true subdomain**. Rejects `myeosc.eu` and `not-eosc.eu`, which a naive `endswith` would accept |
| `_verify_child(ev, point, …)` | 571 | The child page that was followed for this point, or `None` |
| `_policy_check(...)` | 578 | The whole decision procedure shared by points 5b and 5c |
| `render_warning(ev)` | — | Reason to distrust *absence of text* on this page |
| `link_collection_warning(ev)` | — | Reason to distrust *absence of a link* |

### The two absence gates — and why there are two

Concluding "absent" from an incomplete capture is the most damaging mistake this
kind of tool can make, because the output is an accusation against a named
organisation. So absence-based `FAIL`s are gated. But the two kinds of absence
need different gates.

**`render_warning`** asks *did the page render enough to read?* It fires when a
cookie-consent overlay dominates the captured text (consent markers present and
`main_text` under 1200 chars), when fewer than 25 links were captured, or when
`main_text` is under 600 chars. This is the right question for a judgement about
prose and the **wrong** question for a link.

**`link_collection_warning`** asks only *did the DOM arrive?* It fires when no
links at all were captured, when `len(links) + len(images) + len(controls) < 10`
(`DOM_ELEMENT_FLOOR`), or when `full_text` is under 500 chars
(`EMPTY_DOCUMENT_CHARS`). Text length is not evidence about DOM delivery — a small
page is not a truncated one.

The distinction came from a real case. One node in this set serves 530 characters
of main text behind a cookie banner but 20 anchors — exactly the 20 in the
server's HTML, and 21 in the rendered DOM both before and after accepting
consent. Gating a link-absence `FAIL` on text length let a genuinely verified
absence escape as "cannot conclude". The absence of an `eosc.eu` link there is a
fact about the node, not an artefact of collection.

Where a `FAIL` stands despite a render warning, `_render_note` appends the caveat
to the evidence: the verdict is not suppressed, but the reviewer is told a
consent banner was in the way so the finding can be spot-checked.

---

## 5. Per-point decision procedures

Ten points, ten functions. For each: the steps taken, the branch conditions in
evaluation order, and the verdict each branch yields.

---

### Point 1 — NLP publicly accessible, or reachable via EOSC AAI

`check_1`. Decided almost entirely on HTTP status.

**Steps:** read `http_status`; measure `len(full_text)`; on a 401/403, search
`full_text` for login vocabulary and `final_url` for AAI markers, then search
`full_text + title` for bot-wall wording.

| # | Condition | Verdict |
|---|---|---|
| 1 | `error` set | `ERROR` |
| 2 | 2xx **and** `full_text` > 200 chars | `PASS` — branch (a) satisfied |
| 3 | 401/403 **and** a login affordance found | `MANUAL_REVIEW` — branch (b) may apply, but whether that login is EOSC AAI cannot be read off the page |
| 4 | 401/403, no login affordance | `MANUAL_REVIEW` |
| 5 | 404 or 410 | `FAIL` — the registered URL does not resolve to a page |
| 6 | ≥ 500 | `MANUAL_REVIEW` — often transient, not recorded as a failure without a retry |
| 7 | any other ≥ 400 | `MANUAL_REVIEW` |
| 8 | 2xx but ≤ 200 chars | `MANUAL_REVIEW` — may need JavaScript the tool did not run, or be a shell |

Branch 4 deserves its own note, because it looks like it should be a failure and
is not. A bare 403 to an automated client is far more often bot mitigation than
an access policy — genuine access control almost always redirects to a login.
This was not hypothetical: a node in this set served HTTP 200 to the tool and
then 403 once the crawl made a handful more requests. Reporting that as "not
publicly accessible" would have been the tool blaming a node for its own request
rate. The same node returned 200 again hours later to a run from an address that
had made no requests that day, settling all four of its review cells — so the
abstention was not merely cautious, it was correct, and a `FAIL` would have
stood as a wrong verdict about a named organisation. The evidence records any bot-protection wording found (`cloudflare`,
`just a moment`, `ray id`, `captcha`, …) and the reviewer action is to open the
URL in an ordinary browser.

---

### Point 1R — resources behind the landing page are public or behind EOSC AAI

`check_1R`. **Returns `MANUAL_REVIEW` unconditionally** (unless `error`).

**Steps:**

1. Take the landing page host from `final_url`.
2. Collect every link whose host differs from it and is not `eosc.eu` or a
   subdomain (via `_is_host`).
3. Group those by host, listing up to 12 hosts with up to 3 distinct link labels
   each, so the reviewer sees distinct destinations rather than 90 URLs.
4. Search `full_text` and all `href`s for AAI markers (`eosc-aai`, `aai.eosc`,
   `myaccessid`, `egi check-in`, `aai.egi.eu`, …) and list any found.
5. If depth ≥ 1, report how many followed child pages were served anonymously,
   and name up to 5 that were not.

The point quantifies over every resource reachable through the landing page,
including through intermediate pages, and whether a given login is genuinely
EOSC AAI compliant is settled during EEN enrolment rather than by reading HTML.
One level of crawling narrows this; it cannot close it. The output is a worklist,
not a verdict.

---

### Point 2 — scope, intended users and responsible organisation stated

`check_2`. **Returns `MANUAL_REVIEW` unconditionally** (unless `error`).

**Steps:**

1. Take the first 600 characters of `main_text`, falling back to `full_text`.
2. Add the `meta` description if present (first 200 chars).
3. Find organisation-like names by regex: up to four capitalised words followed
   by a legal-entity or institutional suffix — `ERIC`, `e.V.`, `GmbH`, `Ltd`,
   `Foundation`, `Institute`, `Institut`, `University`, `Universit[eéà]`,
   `Consortium`, `Association`, `Council`, `Agency`, `Centre`, `Center`, `CNRS`,
   `CNR`, `CSC`. Up to six are listed; if none match, that is stated explicitly.
4. If an About page was followed at depth 1 and rendered, quote its opening 260
   characters — **clearly marked as one level down**, because the checklist asks
   the *landing page* to state these things and an About page cannot satisfy it
   on the page's behalf.

Whether the prose conveys scope, intended users and the responsible organisation
to a researcher is a reading judgement. The check's job is to make that reading
take thirty seconds instead of five minutes.

---

### Point 3 — EOSC logo and official node name visible

`check_3`. **Returns `MANUAL_REVIEW` on both branches** (unless `error`).

**Steps:**

1. For every captured image and inline SVG, build the haystack
   `"{src} {alt} {aria_label} {title} {css_class}"` — but with the **host part of
   `src` removed**, so a node served from a host containing "eosc" does not match
   on every locally-hosted image. The path and query survive, so
   `eosc-node-final.webp` still counts. "eosc" must then appear as a token, not
   inside a longer word: `geoscience` and `neoscope` do not match, while the
   official lockups `EOSCNode_Finland.jpg` and `EOSCNodeBBMRIERIC_ColourPos.png`
   do, because CamelCase is treated as a word break. Separately, an asset genuinely
   served from `eosc.eu` counts via a host check, so a cross-host node logo —
   correct behaviour — is still found, while `myeosc.eu` is not.
2. For each hit, record the kind (`img` or `inline SVG`) and a label, preferring
   `alt`, then `aria_label`, then `title`, then the filename.
3. Take the names that apply to *this* node — those written as `node-id: Name`,
   then any unscoped ones — and test each against `full_text` in file order. The
   list is `checklist/approved-names.txt` unless `--approved-names` replaces it
   or `--no-approved-names` suppresses it. Each word of a name is matched
   literally and case-insensitively, and never inside a longer word or
   hyphenated token; the separator *between* words is flexible, so whitespace
   and the glyphs `|`, `-`, `–`, `—`, `:`, `/`, `·` are interchangeable — unless
   `--strict-separators` is passed, which restores literal glyph matching (and is
   recorded in the output, so a reader knows which rule was in force). Record
   the first match, what the page actually wrote, and whether the name was
   scoped to this node. If the body is empty (a 403, say), record that the name
   was not looked for rather than that it is absent. If nothing matched, also
   record how many times the longest leading phrase shared by all the candidate
   names — `EOSC Node`, for the official list — occurs in the body, so the
   reviewer knows whether there is anything to look at.

| # | Condition | Verdict |
|---|---|---|
| 1 | At least one EOSC-referencing image asset | `MANUAL_REVIEW` — the logo requirement is *likely* met |
| 2 | None | `MANUAL_REVIEW` — explicitly **not** proof of absence |

Neither branch can be closed, for two separate reasons that are worth keeping
apart:

- **A missing capability.** "Clearly and visibly shown" is a question about
  rendered geometry, and section 3 explains that no geometry was captured. This
  is not a judgement call the tool declines to make; it is data the tool does not
  have.
- **A name the tool can check, against a list it cannot validate.** The official
  Tripartite list is now committed at `checklist/approved-names.txt` and used by
  default, so the name half *is* assessed — but the tool cannot tell whether that
  file is current, and a non-match may mean the page is wrong, the name is in an
  image, or the list is stale. `results.json` records which list was in force
  under `approved_names`, including whether it was the committed default, and
  both reports state it in prose, so a `REVIEW` here cannot be misread as a
  checked-and-clean name. `--no-approved-names` skips the half entirely, and the
  reports say that too.
- **A weaker claim from an unscoped list.** A name given without a `node-id:`
  prefix applies to every node, so a match shows the string is on the page but
  not that it is that node's own name. The evidence line says which of the two
  claims it is making. Scoping each name to its node is what makes the stronger
  claim available, and `checklist/approved-names-scoped.txt` does exactly that.
  It is deliberately not the default: the names in it are official, but the
  mapping from each name to a node id in `nodes.yaml` was derived here and is not
  part of the Tripartite file, so that mapping is what a reviewer should
  challenge first.

Branch 1 used to over-match badly; the history is in section 6.

---

### Point 4 — link to the node's own page on `eosc.eu`

`check_4`. The point that produces most of the `FAIL`s in practice: all 6 in the
published run of 24 September 2026, and 6 of the 7 in the run of 21 September,
the seventh being point 6 for a node with no contact route of any kind on its
landing page.

**Steps:** for every link, parse the URL; keep only those whose host is `eosc.eu`
or a true subdomain (`_is_host`, so `myeosc.eu` does not qualify); strip the
trailing slash from the path; sort into three buckets —

- **`node_pages`** — path contains `building-the-eosc-federation` *and* has a
  non-empty tail after it;
- **`index_only`** — path contains `building-the-eosc-federation` with nothing
  after it;
- **`other_eosc`** — any other `eosc.eu` link.

| # | Condition | Verdict |
|---|---|---|
| 1 | `node_pages` non-empty | `PASS` (up to 3 links quoted) |
| 2 | `index_only` non-empty | `FAIL` — the index is explicitly excluded by the checklist |
| 3 | `other_eosc` non-empty | `FAIL` — links to `eosc.eu` but not to the dedicated page; the homepage is excluded |
| 4 | none, and `link_collection_warning` fires | `MANUAL_REVIEW` — too little captured to conclude absence |
| 5 | none, DOM complete | `FAIL` — no link to `eosc.eu` found, with any render caveat appended |

When `nodes.yaml` records the node's `eosc_page`, that URL is passed in as
`expected_page` and appended to the evidence of branches 2, 3, 4 and 5 as
"the node's dedicated page exists at … but is not linked from here". Naming the
exact page turns "something is absent" into a one-line fix the node operator can
action.

**What a `PASS` here does not establish.** Three things, all of which a reviewer
should know before quoting one:

- **The target is never requested.** The check matches the URL's *shape* — host,
  path prefix, non-empty tail. A link to a node page that has since been deleted
  would `PASS` identically. Confirming the destination is a manual step.
- **Placement is not recorded.** A link in the footer and a link in the body are
  indistinguishable in the evidence. The checklist requires a link and says
  nothing about prominence, so footer placement is compliant — but the evidence
  cannot tell you which you are looking at. EUDAT's link, for instance, is the
  fourth item in a "Navigation & Legal" footer column, 89% of the way down the
  page.
- **The screenshot cannot corroborate it.** Captures are viewport-only
  (`full_page=False` in `fetch.py`), so anything below the fold — which includes
  every footer link — is absent from the saved image. A reviewer checking a
  `PASS` against the screenshot may conclude the tool invented the link. This has
  happened.

---

### Point 5a — purpose description for research resources

`check_5a`. **Returns `MANUAL_REVIEW` unconditionally** (unless `error`).

The evidence is two numbers: the count of outbound links, and the length of
`main_text`. The point quantifies over "all research resources offered by the
Node", which cannot be enumerated from the landing page, and the checklist
separately allows the description to live in the resource's EOSC Catalogue entry
rather than on this page. There is no branch on which the tool could honestly
resolve it, so it does not pretend to.

---

### Points 5b and 5c — AUP and UAP accessible

`check_5b` and `check_5c` both delegate to `_policy_check` with different
vocabularies. Identical procedure, so it is described once.

**Steps:**

1. `_link_hits` — links whose label or address matches the policy vocabulary.
   The address is read twice, raw and with its separators turned into spaces
   (`patterns.link_haystack`), so `/geant-node-acceptable-use-policy/` matches
   `acceptable\s+use\s+polic`. The crawler selects links with the same function.
2. `_match` on `full_text` — mentions of the vocabulary in the prose.
3. If links were found, look for the child page fetched for this point.

| # | Condition | Verdict |
|---|---|---|
| 1 | Link found, **no child fetched** | `PASS`, stated as "a pointer, not a verified document", with the reason: depth 0, a PDF or other document, a cap reached, another site, or not selected at collection |
| 2 | Link found, child returned 404/410 | `FAIL` — the policy is not accessible |
| 3 | Link found, child not `ok` for another reason | `MANUAL_REVIEW` — may be a bot restriction rather than a real problem |
| 4 | Child fetched, but `main_text` < 400 chars **or** no policy wording | `MANUAL_REVIEW` — reads like a navigation stub, not a policy |
| 5 | Child fetched, substantial, policy wording present | `PASS` |
| 6 | No link, but the vocabulary appears in the page text | `MANUAL_REVIEW` — mentioned but not followable |
| 7 | Nothing at all | `MANUAL_REVIEW` — **deliberately not a `FAIL`** |

Branch 1 is weaker than it looks, and the message says so: a link labelled
"Acceptable Use Policy" pointing at a 404 satisfies "there is a link" while
failing the actual requirement, which is that the policy be *accessible*. Running
at `--depth 1` converts branch 1 into one of branches 2–5 for ordinary pages on
the node's own site. It cannot do so for a PDF or a page on another site, and
the reviewer action says so rather than suggesting a re-run that would not help.

Branch 4's "policy wording" test is `POLICY_BODY_PATTERNS`: `must not`,
`you may/must/shall/agree`, `permitted`, `prohibit`, `terms`, `policy`,
`conditions`, `responsib`, `comply`, `authorised`, `authorized`. It exists to
tell a real policy document apart from a navigation page that merely has the word
"policy" in its link text.

Branch 7 is not a `FAIL` because the checklist permits the policy to be reached
via each resource's entry in the EOSC Catalogue, which this tool does not follow.
Failing a node for an absence the checklist does not require to be on this page
would be the tool enforcing a stricter rule than the one it is checking.

---

### Point 6 — means of contacting the node helpdesk

`check_6`. Two tiers: wording that identifies a helpdesk, then general contact
vocabulary. The word "support" on its own is only a reason to follow a link. On
24 September 2026 it labelled a funding programme (Czechia), a EuroHPC proposal
service (EBRAINS) and a service overview (BBMRI-ERIC), and all three had passed.

**Steps:**

1. Collect `mailto:` links.
2. `_link_hits` with the full contact vocabulary.
3. From those two sets, keep the ones that **identify a helpdesk**. That means
   the label or address matches `HELPDESK_STRONG` (helpdesk, service desk,
   ticket, a support team, request or portal, user/technical support,
   contact/ask/get support, a `support@` or `support[at]` address, ServiceNow).
   A host whose first label is `hd`, `support` or `helpdesk` also counts, and so
   does a mailbox such as `support@`, `helpdesk@`, `x-helpdesk@` or
   `x@helpdesk.…`.
4. Otherwise read **every** page followed for point 6, not only the first. A
   page counts if it matches `HELPDESK_ON_PAGE` (helpdesk, service desk, ticket,
   a support address, ServiceNow) or gives a helpdesk mailbox. Qualified
   "support" phrases are strong in a link label, but not in page prose: they
   describe services there.

| # | Condition | Verdict |
|---|---|---|
| 1 | Landing-page link or mailto that identifies a helpdesk | `PASS` |
| 2 | Contact or bare "support" link, a followed page names a helpdesk or gives a helpdesk mailbox | `PASS` — quoting the wording and the addresses |
| 3 | Contact or bare "support" link, followed pages `ok`, none identifies a helpdesk | `MANUAL_REVIEW` — says when a "support" label was the only lead, and lists addresses and links not followed |
| 4 | Every followed page returned 404/410 | `FAIL` — the route offered does not work |
| 5 | Generic contact link, nothing further established | `MANUAL_REVIEW` |
| 6 | No contact route, `link_collection_warning` fires | `MANUAL_REVIEW` |
| 7 | No contact route, DOM complete | `FAIL` — no `mailto:`, no link labelled or addressed as contact, support or helpdesk |

Branches 2 and 3 are why depth 1 is worth the requests here. A "Contact" link is
ambiguous on its own; the page behind it usually is not — it either names a
helpdesk and offers a form or an address, or it does not. One request settles
what keyword matching cannot.

---

### Point 7 — the page is in English

`check_7`. The only point using statistical detection rather than pattern
matching.

**Steps:**

1. Take `main_text`, falling back to `full_text`. Read the declared `lang`
   attribute.
2. If under 120 characters → `MANUAL_REVIEW`, too little to detect a language.
3. Build a `lingua` detector over all Latin-script languages, take the first
   4000 characters, and record the top language and its confidence.

| # | Detected | Declared | Verdict |
|---|---|---|---|
| 1 | en | `en*` | `PASS` |
| 2 | en | anything else | `PASS` — the mismatch is a metadata inconsistency worth fixing, but it does not breach point 7 |
| 3 | not en | `en*` | `MANUAL_REVIEW` — mixed-language pages and navigation-heavy text both cause this |
| 4 | not en | not `en*` | `FAIL` |

If `lingua` is not installed, the check degrades rather than crashing: a declared
`en` gives `PASS` noting that detection was unavailable, anything else gives
`MANUAL_REVIEW`.

Separating `main_text` from `full_text` matters most here. A cookie banner or a
language switcher listing eight languages in the page chrome is exactly the kind
of text that misleads a detector, and it is excluded by construction.

---

## 6. Where this workflow is known to be wrong

Listed because a checker whose limitations are undocumented invites more trust
than it has earned.

**Point 3 over-matched on the page's own hostname — fixed, and the first
diagnosis of it was wrong.** The haystack included `img.src` in full, so for a
node served from a host containing "eosc" the regex matched the *hostname of
every locally-hosted image*. The run of 21 September 2026 reported 8
"EOSC-referencing image assets" for that node; probing the captured evidence
showed **7 of the 8 matched on the hostname alone** — a favicon counted three
times, a parallax background, a gateway logo, a partner logo, and an EU funding
badge named `FundedbytheEU.png`. None is an EOSC logo. Exactly one was real.

This document previously recorded the cause as cross-host loading and proposed
restricting the host. That was the wrong fix, and probing the evidence before
applying it is what showed why: several nodes legitimately serve their EOSC
lockup from a CDN or their own domain (`i0.wp.com`, `research.csc.fi`,
`portal.eudat.eu`, `www.panosc.eu`), so a host restriction would have discarded
genuine logos. The defect was never cross-host loading; it was the node's *own*
host being part of the text being searched.

The fix strips the host from `src` and requires "eosc" to be a token rather than
a substring, with an explicit allowance for `eosc.eu`-hosted assets. Re-running
against the same evidence moved that node from 8 assets to 1 and left all eight
other nodes untouched. **No verdict changed** — the branch returns
`MANUAL_REVIEW` either way — and the tally is still 28 PASS / 7 FAIL / 55 review;
what changed is that the evidence line no longer pushes a reviewer towards the
wrong conclusion.

The boundary rule then had a defect of its own, found by regenerating the report
rather than by reasoning about it: requiring a non-word character *after* "eosc"
rejected `EOSCNode_Finland-1-1-scaled.jpg`, which is the official lockup, and
cost the Finnish node its only EOSC asset — flipping its point 3 evidence from
"asset present" to "none found". An uppercase letter is now accepted as a word
break. The leading guard is still strict, which is what keeps `geoscience` and
`GEOSCIENCE` out.

**The approved-name match over-matched, then under-matched.** Both are recorded
because both shipped. First, the name was matched as a bare substring of the
page body, so a short name matched inside ordinary words: `EGI` in the list
reported a match on the BBMRI-ERIC page (inside "strat**egi**c") and on Data
Terra (inside "Norw**egi**an"), neither of which names the EGI node. The list
was also matched as a whole, so any name matching any page satisfied that page's
evidence line. Matching was made boundary-aware and scopable with a `node-id:`
prefix.

That fix was then too strict. Run against the official Tripartite list, which
writes every name as `EOSC Node | X`, it matched **none of the nine pages**: the
pages disagree about the separator glyph, not the name — BBMRI-ERIC writes a
hyphen and an en dash, European DTO the pipe, EUDAT nothing at all. Publishing
that would have been a finding against every node for a typographic difference.
Separator glyphs are now interchangeable, and the evidence quotes what the page
wrote so the variant is visible. This is a deliberate loosening, so it is
reversible rather than baked in: `--strict-separators` restores the literal rule
and reproduces the 0-of-9 result, and the report states which rule was in force
either way. The place to challenge the default is the table in the guide.

**The match is still not proof of the right name.** The committed list is
unscoped, so a match says the string is on the page, not that it is that page's
own name; and with 9 names applying to all 9 nodes, a page carrying a *different*
node's approved name would satisfy its own evidence line. The line says which
claim it is making. Scoping the list is what makes the stronger claim available,
and `checklist/approved-names-scoped.txt` now does. Run against the same
evidence it returns the same two nodes, BBMRI-ERIC and EUDAT, which retires the
concern for this dataset: the 2-of-9 headline does not depend on names leaking
between pages. The published run of 24 September confirms it on twelve nodes:
both lists match the same five (BBMRI-ERIC, Czechia, EUDAT, GÉANT, Slovakia), and
`--strict-separators` matches none. The residual weakness is no longer the matching but the mapping —
name to node id — which was derived in this repository rather than taken from
the Tripartite file.

No verdict changed at any point, because the name never decides point 3 — but
the evidence line did, twice, and both times it was wrong.

**Nothing about visibility is captured**, as set out in section 3. Point 3 cannot
be closed automatically under the current evidence model, regardless of how the
matching is fixed.

**The vocabularies are English-only.** A node serving a Dutch or Finnish contact
page will be missed by points 5b, 5c and 6. Point 7 requires the landing page to
be in English, so the bias is tolerable for this checklist — but it is a bias,
not a neutral default.

**A legitimate cross-host logo is indistinguishable from an unrelated one.** At
least one node in this set loads its node logo from `eosc.eu` while being served
from its own domain, which is correct behaviour. A host check alone would need
care not to reject it.

**Binary policy documents are never read.** `select_children` skips URLs ending in
a binary extension, so an AUP published as a PDF is recorded as a pointer
(branch 1 of `_policy_check`) and never verified. The checklist's requirement is
accessibility, and the tool cannot confirm it for these.

**`--only` used to narrow the run in place — fixed, with a cost.** Assessing a
subset rewrote the shared report, so a one-node table replaced the full one
and looked complete. `--only` now narrows only which sites are fetched; the
report written to the default results directory still covers every node, and the
requested subset is recorded in a top-level `selection` list. An explicit
`--results DIR` keeps the old narrowing, where nothing shared is at risk.

The cost is that such a report is no longer uniformly fresh: unselected rows come
from evidence already on disk, under a header stating a single run timestamp.
That is a freshness claim the report cannot make, so it no longer makes it — a
**Mixed freshness** banner in both the Markdown and HTML output names what was
re-fetched, counts what was not, and gives the capture date of the reused
evidence. Nodes with no evidence at all are still listed under
`missing_evidence`, printed in red, with exit code 2.

**The row heading comes from `nodes.yaml`, not from the evidence.** `assess`
labels each node with the `url` configured now, while every verdict comes from
the evidence captured then. After BBMRI-ERIC's URL changed on 25 September, a
bare `assess` headed its row with the new `dev3.` address above verdicts taken
from the old `www.` page. The address really fetched is kept only as
`final_url`, in the evidence and in the `fetch` summary of `results.json`.
Until the tool compares the two, rebuild an old run with the node list it was
collected with (`--nodes`); the run guide gives the exact command.

**A public CI summary is not the place for per-node verdicts.** The workflow
used to copy the whole of `results.md` into `$GITHUB_STEP_SUMMARY`, which on a
public repository is world-readable. The verdicts are already public — the report
is committed — so nothing leaked that was not already published; but that page
is produced automatically from an unreviewed run and carries the repository's
name, which makes a table of FAILs against named organisations read as a
finding rather than a draft. The summary now publishes counts only, labelled as
unreviewed, and points at the artifact for the per-node detail. It also refuses
to summarise at all unless the check step succeeded, because `results.json` is
committed and would otherwise have been read out of a fresh checkout as though it
were this run's result.

---

## 7. Reading the output

`results.json` carries `run_id`, `generated_at`, the full `checklist` as loaded,
`approved_names` (whether a list was used, whether it was the committed default
(`default_used`), whether it was scoped, how many names, its path, the `sha256`
of the bytes actually read, and `strict_separators` — plus the older
`approved_names_supplied` flag, kept for readers of earlier result files),
`selection` (the node ids `--only` restricted the fetch to, empty on a full run),
`skipped` (the node ids `--skip` left out, empty when nothing was skipped),
`url_mismatch` (present only when some node's evidence was collected from a URL
other than the one now configured: `id`, `configured_url`, `evidence_url`,
`fetched_at`; the reports then carry an "Evidence from a different URL"
banner), and `nodes`. Each node carries `id`, `name`, `url`,
`ad_hoc`, a `fetch` summary (status, final URL, robots note, screenshot, crawl
depth, every child with its `selected_for` and outcome, and `children_skipped`),
`results`, and `results_depth_1` when depth 2 was used.

The same run is rendered to `index.html` (the matrix, with evidence expandable
per cell), `results.md`, `results.csv`, and `checklist-v3.0.html` (named after the
revision applied, so `checklist-v3.1.html` after a switch; the checklist
itself, so a reader can see the rule a verdict was derived from without opening
the source document).

The honest summary of the whole workflow: of the ten points, **two** (1 and 4) are
routinely settled by inspection, **three** (5b, 5c, 6) are settled when depth 1
gives the tool a second page to read, and **five** (1R, 2, 3, 5a, and 7 in its
mixed-language branch) end in a human's hands by design. A tool that returned
PASS or FAIL on every line would look more useful and be worth considerably less.

---

*Source checklist: Node Landing Page Verification Checklist v3.0, 15 September
2026, transcribed to `checklist/v3.0.yaml` alongside the source document.
Implementation: `src/basic_check/{fetch,patterns,checks,names,privacy,report,cli}.py`.
Repository: <https://github.com/marioreale/eosc-basic-compliance>.*
