# The checklist directory

This directory holds the reference checklist as data, plus the document it was
transcribed from. It is the single configuration point for which checklist the
test suite applies: `--checklist` / `-c` on `basic-check assess`, `run` and
`points`, defaulting to `checklist/v3.2.yaml` (`cli.py`, `DEFAULT_CHECKLIST`).

| File | Role |
| --- | --- |
| `v3.2.yaml` | **The default.** Checklist v3.2 (28 September 2026) transcribed as data: version, date, provenance, the item 5 rule (`item5_on_nlp: true`), one entry per point, and a header listing what changed from v3.1 |
| `20260928_Node_Landing_Page_Verification_Checklist_v3.2.pdf` | The document v3.2 was transcribed from, so it can be audited |
| `v3.1.yaml` | Checklist v3.1 (24 September 2026), kept unchanged so runs made from 26 to 28 September 2026 can be rebuilt with `-c checklist/v3.1.yaml` |
| `20260910_Node_Landing_Page_Verification_Checklist_v3.1.pdf` | The document v3.1 was transcribed from |
| `v3.0.yaml` | Checklist v3.0 (15 September 2026), kept unchanged so runs made before 26 September 2026 can be rebuilt with `-c checklist/v3.0.yaml` |
| `20260910_Node_Landing_Page_Verification_Checklist_v3.0.pdf` | The document v3.0 was transcribed from |

## What the YAML governs, and what it does not

It governs the **reporting surface**: report titles, the matrix columns and their
order, the quoted requirement wording, and the decidable/review framing.

It does **not** govern the rules, with one exception. `checks.run_all()` calls
ten functions `check_1 … check_7`; the only value it takes from this file is
`item5_on_nlp`, which v3.2 declares `true`. It selects the item 5 rule: under
v3.2 the purpose, AUP and UAP must be on the NLP *and* in the Catalogue, so a
landing page with no AUP or UAP link fails 5b or 5c; under v3.0 and v3.1, which
do not declare the key, they could be on the NLP *or* in the Catalogue, so that
absence was review. Keeping the switch in the file is what lets older runs be
rebuilt with the rule they were made under. So the YAML declares the
checklist; the Python interprets it. `implemented_by` on each point records
which function does the interpreting, and `tests/test_checklist.py` asserts that
mapping is total in both directions — every point resolves to a real callable,
and every callable is claimed by exactly one point.

The failure mode this guards against: a revision that keeps the same ten point
ids and merely *rewords* a requirement would otherwise pass unnoticed, producing
reports that quote the new wording while the code applies the old rule.

## Adding a revision

Revisions become **new files**. Do not edit `v3.2.yaml` (or `v3.1.yaml`, `v3.0.yaml`) in place — the reports
name the file they were generated from, so editing it retroactively invalidates
every past run. `tests/test_checklist.py` enforces this: the declared
`checklist_version` must match the filename.

1. Commit the new source document to this directory.
2. `cp v3.2.yaml v3.3.yaml`, then update `checklist_version`, `checklist_date`,
   `source_document`, `source_file`, and `source_sha256`
   (`sha256sum <file>`).
3. **Re-read every point against the new document.** This is the step the
   tooling cannot do for you. Where wording changed, confirm the corresponding
   `check_*` function still implements it, and change the function if not.
4. Run `uv run pytest -q`. The hash and mapping tests will tell you if the
   paperwork and the code disagree; they will not tell you whether a rule is
   *correct*.
5. Try it on the saved evidence first, which contacts no one:
   `uv run basic-check assess -c checklist/v3.3.yaml --results /tmp/v33`, after
   copying `results/evidence` into `/tmp/v33`.
6. Make it the default. This is one line in `src/basic_check/cli.py`:
   `DEFAULT_CHECKLIST = ROOT / "checklist" / "v3.3.yaml"`. The help texts, the
   generated `checklist-v3.3.html` and the tests follow it. Run
   `uv run pytest -q` again.
7. Produce a new run, review it, and publish it. Remove the stale
   `results/checklist-v3.2.html` and update the links to it in the top-level
   `README.md`.

There is no URL to change: the tool never downloads the checklist, it reads the
committed copy. Every command for steps 1–7 is in "Worked examples", example 3,
in [`docs/GUIDE.md`](../docs/GUIDE.md) and [`docs/TEST-SUITE.md`](../docs/TEST-SUITE.md).
The move from v3.0 to v3.1 on 26 September 2026 followed exactly these steps.
The move to v3.2 on 29 September 2026 did too, and also changed a rule: item 5
became stricter, so `check_5a`–`check_5c` gained the `on_nlp` switch described
above, and `item5_on_nlp` was added to `v3.2.yaml` only.

## On the hash

`source_sha256` pins the exact bytes the transcription was made from, which is
what catches a document being silently swapped. Note what it does not do: the
committed file is a PDF rendering of the `.docx` named in `source_document`, not
that `.docx` itself, and the hash is not a signature over the authoritative
original. Replacing the PDF with the real `.docx` is a two-line change in the
YAML plus a re-hash.
