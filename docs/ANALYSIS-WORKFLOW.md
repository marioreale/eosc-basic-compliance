# Analysis workflow

What the test suite actually does, step by step, when it assesses a node against
the **Node Landing Page Verification Checklist v3.0**.

This document is written against the code in `src/basic_check/` as it stands, not
against the design intent. Where the implementation is weaker than the checklist
wording, that is stated rather than smoothed over — the point of this document is
that a reviewer can predict the verdict before running the tool, and can tell
which verdicts are worth trusting.

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
| 1. Collect | `collect` | `nodes.yaml` | `results/evidence/<node>.json`, `results/evidence/screenshots/<node>.png` | yes |
| 2. Assess | `assess` | evidence JSON + `checklist/v3.0.yaml` | `results/results.json` | **no** |
| 3. Report | (part of `assess`) | the run dict in memory | `index.html`, `results.md`, `results.csv`, `checklist-v3.0.html` | no |

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

1. **`robots.txt` for the landing page host** (`_robots`, `fetch.py:193`).
   Fetched over plain HTTP with the tool's own User-Agent string. Three outcomes:
   - disallowed → `error = "not fetched: robots.txt disallows it"`, evidence
     record returned immediately, **every point becomes `ERROR`**;
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
4. **Extract the evidence** from the rendered DOM (`_extract`, `fetch.py:210`).
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
   the screenshot; it exists for the human reviewer.
6. **Depth 1, if requested.** `select_children` (`fetch.py:413`) picks which links
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

`PageEvidence` (`fetch.py:125`) holds: `node_id`, `node_name`, `requested_url`,
`fetched_at`, `final_url`, `http_status`, `redirect_chain`, `robots_allowed`,
`robots_note`, `title`, `lang_attr`, `main_text`, `full_text`, `links`, `images`,
`controls`, `meta_description`, `error`, `screenshot`, `crawl_depth`, `children`,
`children_skipped`.

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
cells, never nine passes and a failure.

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
rate. The evidence records any bot-protection wording found (`cloudflare`,
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
   `"{src} {alt} {aria_label} {title} {css_class}"` and test it against the
   case-insensitive regex `eosc`.
2. For each hit, record the kind (`img` or `inline SVG`) and a label, preferring
   `alt`, then `aria_label`, then `title`, then the filename.
3. If `--approved-names` supplied a list, test each name against `full_text` and
   record either the first match or "NONE of the supplied approved names appear".

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
- **A missing input.** The tool has no authoritative list of Tripartite-approved
  node names. Without `--approved-names`, the name half of the point is not
  assessed at all, and `results.json` records `approved_names_supplied: false` so
  the report cannot quietly imply otherwise.

Branch 1 also over-matches badly — see section 6.

---

### Point 4 — link to the node's own page on `eosc.eu`

`check_4`. The one point that produces `FAIL`s in practice.

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

1. `_link_hits` — links whose `"{text} {href}"` matches the policy vocabulary.
2. `_match` on `full_text` — mentions of the vocabulary in the prose.
3. If links were found, look for the child page fetched for this point.

| # | Condition | Verdict |
|---|---|---|
| 1 | Link found, **no child fetched** (depth 0) | `PASS`, stated as "a pointer, not a verified document" |
| 2 | Link found, child returned 404/410 | `FAIL` — the policy is not accessible |
| 3 | Link found, child not `ok` for another reason | `MANUAL_REVIEW` — may be a bot restriction rather than a real problem |
| 4 | Child fetched, but `main_text` < 400 chars **or** no policy wording | `MANUAL_REVIEW` — reads like a navigation stub, not a policy |
| 5 | Child fetched, substantial, policy wording present | `PASS` |
| 6 | No link, but the vocabulary appears in the page text | `MANUAL_REVIEW` — mentioned but not followable |
| 7 | Nothing at all | `MANUAL_REVIEW` — **deliberately not a `FAIL`** |

Branch 1 is weaker than it looks, and the message says so: a link labelled
"Acceptable Use Policy" pointing at a 404 satisfies "there is a link" while
failing the actual requirement, which is that the policy be *accessible*. Running
at `--depth 1` converts branch 1 into one of branches 2–5.

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

`check_6`. Two tiers: helpdesk-specific vocabulary, then general contact
vocabulary.

**Steps:**

1. Collect `mailto:` links.
2. `_link_hits` with the full contact vocabulary.
3. From those two sets, keep the ones that also match the **helpdesk-specific**
   subset (`helpdesk`, `help desk`, `service desk`, `support`, `ticket`).

| # | Condition | Verdict |
|---|---|---|
| 1 | Helpdesk-specific link or mailto found | `PASS` |
| 2 | Generic contact link, child fetched and `ok`, helpdesk wording on that page | `PASS` — with the mailto addresses found there quoted |
| 3 | Generic contact link, child `ok`, no helpdesk wording, but a mailto or a contact form is present | `MANUAL_REVIEW` — a route exists, but general enquiries may not be the helpdesk |
| 4 | Contact link whose target returned 404/410 | `FAIL` — the route offered does not work |
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

**Point 3 over-matches on hostname.** The haystack includes `img.src`, so when a
node is served from a host that itself contains "eosc" — which is true of at
least one node in this set — the regex matches the *hostname of every
locally-hosted image*. In the run of 21 September 2026 that produced 8
"EOSC-referencing image assets" for that node, of which 7 were a favicon counted
three times, a parallax background, a gateway logo, a partner logo and an EU
funding badge. None is an EOSC logo. The evidence line "EOSC-referencing image
asset(s): 8" is therefore misleading, and the reviewer sees the labels only for
the first five.

This is a defect in the checker, not a finding against the node concerned:
the page is entitled to host its own images, and the tool is the thing counting
them wrongly. Because the branch returns `MANUAL_REVIEW` either way, no verdict
is wrong — but the evidence pushes the reviewer towards the wrong conclusion,
which is nearly as bad.

The same regex has no host-awareness at all, so `not-eosc.eu` and `myeosc.eu`
also match. Point 4 uses `_is_host` and does not have this problem; point 3 does
not use it.

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

**`--only` narrows the run in place.** Assessing a subset writes a report that
looks complete. The code partly guards this — nodes with no evidence are listed
under `missing_evidence`, printed in red, and the process exits with code 2 — but
the HTML report itself does not shout about it.

---

## 7. Reading the output

`results.json` carries `run_id`, `generated_at`, the full `checklist` as loaded,
`approved_names_supplied`, and `nodes`. Each node carries `id`, `name`, `url`,
`ad_hoc`, a `fetch` summary (status, final URL, robots note, screenshot, crawl
depth, every child with its `selected_for` and outcome, and `children_skipped`),
`results`, and `results_depth_1` when depth 2 was used.

The same run is rendered to `index.html` (the matrix, with evidence expandable
per cell), `results.md`, `results.csv`, and `checklist-v3.0.html` (the checklist
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
Implementation: `src/basic_check/{fetch,patterns,checks,report,cli}.py`.
Repository: <https://github.com/marioreale/eosc-basic-compliance>.*
