# The checklist directory

This directory holds the reference checklist as data, plus the document it was
transcribed from. It is the single configuration point for which checklist the
test suite applies: `--checklist` / `-c` on `basic-check assess`, `run` and
`points`, defaulting to `checklist/v3.0.yaml` (`cli.py`, `DEFAULT_CHECKLIST`).

| File | Role |
| --- | --- |
| `v3.0.yaml` | The checklist transcribed as data: version, date, provenance, and one entry per point |
| `20260910_Node_Landing_Page_Verification_Checklist_v3.0.pdf` | The document the transcription was made from, so it can be audited |

## What the YAML governs, and what it does not

It governs the **reporting surface**: report titles, the matrix columns and their
order, the quoted requirement wording, and the decidable/review framing.

It does **not** govern the rules. `checks.run_all()` calls ten functions
`check_1 … check_7` and never reads this file. So the YAML declares the
checklist; the Python interprets it. `implemented_by` on each point records
which function does the interpreting, and `tests/test_checklist.py` asserts that
mapping is total in both directions — every point resolves to a real callable,
and every callable is claimed by exactly one point.

The failure mode this guards against: a revision that keeps the same ten point
ids and merely *rewords* a requirement would otherwise pass unnoticed, producing
reports that quote the new wording while the code applies the old rule.

## Adding a revision

Revisions become **new files**. Do not edit `v3.0.yaml` in place — the reports
name the file they were generated from, so editing it retroactively invalidates
every past run. `tests/test_checklist.py` enforces this: the declared
`checklist_version` must match the filename.

1. Commit the new source document to this directory.
2. `cp v3.0.yaml v3.1.yaml`, then update `checklist_version`, `checklist_date`,
   `source_document`, `source_file`, and `source_sha256`
   (`sha256sum <file>`).
3. **Re-read every point against the new document.** This is the step the
   tooling cannot do for you. Where wording changed, confirm the corresponding
   `check_*` function still implements it, and change the function if not.
4. Run `uv run pytest -q`. The hash and mapping tests will tell you if the
   paperwork and the code disagree; they will not tell you whether a rule is
   *correct*.
5. Run with `-c checklist/v3.1.yaml`.

## On the hash

`source_sha256` pins the exact bytes the transcription was made from, which is
what catches a document being silently swapped. Note what it does not do: the
committed file is a PDF rendering of the `.docx` named in `source_document`, not
that `.docx` itself, and the hash is not a signature over the authoritative
original. Replacing the PDF with the real `.docx` is a two-line change in the
YAML plus a re-hash.
