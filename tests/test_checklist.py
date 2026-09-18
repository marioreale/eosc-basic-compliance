"""Tests that tie the checklist YAML to the source document and to the rules.

These exist because of a specific failure mode. The YAML drives every label,
quoted requirement and version string in the reports, but `checks.run_all` never
reads it -- the rules are ten hardcoded functions. So a revised checklist that
keeps the same point ids and merely *rewords* a requirement would sail through:
ids still match, reports would quote the new wording, and the functions would
quietly keep applying the old semantics. Reports saying v3.1 while testing v3.0
is worse than no reports, because they are trusted.

Nothing here checks that a rule is *correct* -- that is what test_checks.py is
for. These check that the paperwork and the code cannot drift apart unnoticed.
"""

import hashlib
import inspect
import re
from pathlib import Path

import pytest
import yaml
from test_checks import ev  # the evidence builder these tests reuse

from basic_check import checks

ROOT = Path(__file__).parents[1]
CHECKLIST_DIR = ROOT / "checklist"
CHECKLIST_PATH = CHECKLIST_DIR / "v3.0.yaml"


@pytest.fixture(scope="module")
def checklist() -> dict:
    return yaml.safe_load(CHECKLIST_PATH.read_text())


# --- 1. the source document is present, and is the one we transcribed ---------


def test_the_source_document_is_committed_next_to_the_transcription(checklist):
    """A transcription you cannot audit against its source is a rumour."""
    name = checklist.get("source_file")
    assert name, "the checklist must name the source file committed beside it"
    assert (CHECKLIST_DIR / name).is_file(), (
        f"{name} is declared in source_file but not committed to checklist/. "
        "Either commit the document or stop claiming it is the source."
    )


def test_the_source_document_still_has_the_bytes_we_transcribed_from(checklist):
    """The drift guard.

    If someone drops a revised checklist in under the same filename, this fails
    and forces a deliberate decision: re-read the document, re-check the ten
    rules against it, then update the hash. It cannot be satisfied by accident.
    """
    declared = checklist.get("source_sha256")
    assert declared, "the checklist must declare source_sha256"
    path = CHECKLIST_DIR / checklist["source_file"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == declared, (
        f"{path.name} has changed.\n"
        f"  declared: {declared}\n"
        f"  actual:   {actual}\n"
        "If the checklist was revised, the ten functions in checks.py may now "
        "implement the previous version. Re-read the document, confirm each "
        "rule, and only then update source_sha256."
    )


# --- 2. every point maps to a rule, and every rule is claimed -----------------


def _check_functions() -> dict:
    """Public `check_*` functions in basic_check.checks, by name."""
    return {
        name: fn
        for name, fn in inspect.getmembers(checks, inspect.isfunction)
        if name.startswith("check_") and fn.__module__ == checks.__name__
    }


def test_every_point_declares_the_function_that_decides_it(checklist):
    for point in checklist["points"]:
        assert point.get("implemented_by"), (
            f"point {point['id']} does not declare implemented_by, so nothing "
            "connects its wording to the code that applies it"
        )


def test_every_declared_function_exists_and_is_callable(checklist):
    available = _check_functions()
    for point in checklist["points"]:
        name = point["implemented_by"]
        assert name in available, (
            f"point {point['id']} declares {name}, which does not exist in "
            f"basic_check.checks. Available: {sorted(available)}"
        )


def test_every_check_function_is_claimed_by_exactly_one_point(checklist):
    """The mapping must be total in both directions.

    A check function no point claims is either dead code or a rule being applied
    that the reports never explain -- both worth knowing about.
    """
    claimed = [p["implemented_by"] for p in checklist["points"]]
    assert len(claimed) == len(set(claimed)), "two points claim the same function"
    assert set(claimed) == set(_check_functions()), (
        "the checklist and checks.py disagree about which rules exist.\n"
        f"  claimed by no point: {sorted(set(_check_functions()) - set(claimed))}\n"
        f"  claimed but absent:  {sorted(set(claimed) - set(_check_functions()))}"
    )


def test_the_declared_function_order_is_the_order_results_come_back_in(checklist):
    """Guards the report column order against a silent reshuffle."""
    declared = [p["implemented_by"] for p in checklist["points"]]
    actual = [f"check_{r.point_id}" for r in checks.run_all(ev())]
    assert actual == declared


# --- 3. revisions become new files, so past runs stay reproducible ------------


def test_the_filename_matches_the_version_it_declares(checklist):
    """Enforces the convention that a revision is a new file, not an edit.

    Editing v3.0.yaml in place and bumping checklist_version to 3.1 would make
    every previously generated report unreproducible: the reports name the file
    they came from. This fails until the revision is saved as v3.1.yaml.
    """
    version = checklist["checklist_version"]
    assert CHECKLIST_PATH.name == f"v{version}.yaml", (
        f"{CHECKLIST_PATH.name} declares version {version}. A revised checklist "
        f"belongs in checklist/v{version}.yaml, leaving the old file intact so "
        "earlier runs remain reproducible."
    )


def test_every_checklist_in_the_directory_follows_the_naming_convention():
    for path in sorted(CHECKLIST_DIR.glob("*.yaml")):
        assert re.fullmatch(r"v\d+\.\d+\.yaml", path.name), (
            f"{path.name} does not follow the vMAJOR.MINOR.yaml convention"
        )
        declared = yaml.safe_load(path.read_text())["checklist_version"]
        assert path.name == f"v{declared}.yaml", (
            f"{path.name} declares checklist_version {declared}"
        )
