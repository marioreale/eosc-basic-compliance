"""Tests for personal-data masking.

Two ways this can go wrong. The first is publishing a person's address or
number, which cannot be taken back. The second is masking what a reviewer needs:
a helpdesk mailbox, or an ordinary word that happens to share its spelling with
a masked address. The cases below come from both sides, and several are
taken from pages the tool has actually collected, with the people replaced by
fictional ones.
"""

from __future__ import annotations

import pytest

from basic_check import report
from basic_check.fetch import Link, PageEvidence, load_evidence, write_evidence
from basic_check.privacy import country_code, is_role_address, mask_data, mask_text

# --- email addresses ---------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("jane.doe@example.org", "XXXXX@example.org"),
        ("mailto:jdoe@uni.example.cz", "mailto:XXXXX@uni.example.cz"),
        ("write to jane.doe [at] example.org", "write to XXXXX [at] example.org"),
        ("write to jane.doe(at)example.org", "write to XXXXX(at)example.org"),
    ],
)
def test_a_personal_address_keeps_only_its_domain(text, expected):
    assert mask_text(text) == expected


@pytest.mark.parametrize(
    "address",
    [
        "support@egi.eu",
        "info@eosc.cz",
        "events@eosc.cz",
        "contact@data-terra.org",
        "it@helpdesk.bbmri-eric.eu",  # every mailbox under a helpdesk host
        "rd@helpdesk.bbmri-eric.eu",
        "elsi-helpdesk@bbmri-eric.eu",
        "csirt@eudat.eu",
        "base-infra-resources@ebrains.eu",
        "report-vulnerability[at]egi.eu",
        "sit[at]egi.eu",
        "business[at]egi.eu",
        "geant@geant.org",  # the organisation's own mailbox
        "bbmri@bbmri-eric.eu",
    ],
)
def test_a_role_mailbox_is_kept(address):
    assert mask_text(address) == address


def test_role_detection_reads_the_host_as_well_as_the_local_part():
    assert is_role_address("it", "helpdesk.bbmri-eric.eu")
    assert is_role_address("eudat.support", "example.org")
    assert not is_role_address("jane.doe", "example.org")


def test_a_map_link_is_not_an_address():
    # A Google Maps URL has ",+Netherlands/@52.33,4.95": no address in it.
    url = "https://www.google.com/maps/place/Amsterdam-Zuidoost,+Netherlands/@52.3326,4.9478,17z"
    assert mask_text(url) == url


def test_masking_is_idempotent():
    once = mask_text("Jane Doe, jane.doe@example.org, +31 20 123 4567")
    assert mask_text(once) == once


# --- phone numbers -----------------------------------------------------------


@pytest.mark.parametrize(
    "text, expected",
    [
        ("+31 20 123 4567", "+31 XXXXXX"),
        ("+420 725 640 000", "+420 XXXXXX"),
        ("+33 (0)1 23 45 67 89", "+33 XXXXXX"),
        ("T:+31(0)20 5304488", "T:+31 XXXXXX"),
        ("+1 (555) 123-4567", "+1 XXXXXX"),
        ("+358 9 457 0000.", "+358 XXXXXX."),
        ("tel:+420725640000", "tel:+420 XXXXXX"),
        ("tel:0043316349900", "tel:+43 XXXXXX"),  # dialled with 00
        ("Tel.: 06 1234 5678", "Tel.: XXXXXX"),  # no prefix, but labelled
        ("phone: +44 20 7946 0000", "phone: +44 XXXXXX"),
    ],
)
def test_a_phone_number_keeps_only_its_international_prefix(text, expected):
    assert mask_text(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "+1000 users joined",
        "growth of +30% in 2025",
        "published 2026-09-24",
        "grant agreement 101057264",
        "open from 8.30 to 16:00",
        "https://eosc.eu/x?a=1&b=+2",
    ],
)
def test_numbers_that_are_not_phones_are_left_alone(text):
    assert mask_text(text) == text


@pytest.mark.parametrize(
    "digits, code",
    [
        ("31201234567", "31"),
        ("420725640000", "420"),
        ("15551234567", "1"),
        ("74951234567", "7"),
        ("35894570000", "358"),
    ],
)
def test_the_country_code_is_read_from_the_e164_plan(digits, code):
    assert country_code(digits) == code


# --- the name beside an address ----------------------------------------------


def test_the_name_beside_a_personal_address_is_masked_but_not_the_title():
    text = (
        "Contact for media Mgr. Bc. Jana Nováková correspondence Address: "
        "novakova@uni.example.cz phone: +420 725 640 000 General contacts: info@eosc.cz"
    )
    assert mask_text(text) == (
        "Contact for media Mgr. Bc. XXXXX XXXXX correspondence Address: "
        "XXXXX@uni.example.cz phone: +420 XXXXXX General contacts: info@eosc.cz"
    )


def test_a_masked_address_masks_its_name_only_nearby_and_never_in_a_url():
    far = " filler" * 40
    text = f"Anna Smith smith@x.example.org{far} Smith & Sons, https://x.example.org/smith/"
    assert mask_text(text) == (
        f"XXXXX XXXXX XXXXX@x.example.org{far} Smith & Sons, https://x.example.org/smith/"
    )


def test_an_acronym_is_never_taken_for_a_surname():
    assert mask_text("ebrains@example.org EBRAINS") == "XXXXX@example.org EBRAINS"


# --- where masking is applied ------------------------------------------------


PERSONAL = "Head of unit John Smith, j.smith@example.org, +32 2 123 45 67"


def _has_personal_data(text: str) -> bool:
    return any(s in text for s in ("j.smith@", "Smith", "123 45 67"))


def test_the_evidence_file_is_written_masked(tmp_path):
    ev = PageEvidence(
        node_id="t",
        node_name="Test Node",
        requested_url="https://node.example/",
        main_text=PERSONAL,
        full_text=PERSONAL,
        links=[
            Link("mailto:j.smith@example.org", "j.smith@example.org"),
            Link("mailto:support@node.example", "Helpdesk"),
        ],
    )
    path = write_evidence(tmp_path, ev)
    raw = path.read_text()
    assert not _has_personal_data(raw)
    assert "XXXXX@example.org" in raw and "+32 XXXXXX" in raw
    assert "mailto:support@node.example" in raw
    assert (
        load_evidence(tmp_path, "t").main_text
        == "Head of unit XXXXX XXXXX, XXXXX@example.org, +32 XXXXXX"
    )


def test_every_report_is_written_masked_even_from_unmasked_evidence(tmp_path):
    # Evidence collected before masking existed goes straight into the results
    # through the check messages. The reports must mask it on the way out.
    run = {
        "run_id": "t",
        "generated_at": "2026-09-25T00:00:00+00:00",
        "checklist": {
            "checklist_version": "3.0",
            "checklist_date": "2026-09-10",
            "points": [{"id": "6", "title": "Helpdesk", "requirement": "r", "decidable": True}],
        },
        "nodes": [
            {
                "id": "t",
                "name": "Test Node",
                "url": "https://node.example/",
                "fetch": {"crawl_depth": 1, "children": []},
                "results": [
                    {
                        "point_id": "6",
                        "title": "Helpdesk",
                        "verdict": "MANUAL_REVIEW",
                        "message": PERSONAL,
                        "evidence": [PERSONAL],
                    }
                ],
            }
        ],
    }
    paths = report.write_all(run, tmp_path)
    for kind in ("json", "html", "csv", "md"):
        assert not _has_personal_data(paths[kind].read_text(encoding="utf-8")), kind


def test_mask_data_leaves_keys_and_non_strings_alone():
    data = {"jane.doe@example.org": 1, "n": 3, "ok": True, "xs": ["+31 20 123 4567", None]}
    assert mask_data(data) == {
        "jane.doe@example.org": 1,
        "n": 3,
        "ok": True,
        "xs": ["+31 XXXXXX", None],
    }
