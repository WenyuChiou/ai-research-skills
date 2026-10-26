"""Offline catalog clauses and worked-example consistency, not agent behavior.

The synthetic handoff is illustrative; it does not introduce a Hub schema or
validate a real PDF, search, model, research claim, or provider write.
"""
from collections import Counter
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = json.loads((ROOT / "test-corpus/integration/stage1-discovery-contract.json").read_text(encoding="utf-8"))


def _clause_tokens(text):
    # CJK characters need no space delimiters; keep Latin words, punctuation,
    # ordering and negations intact instead of deleting all whitespace blindly.
    return tuple(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]|[A-Za-z0-9_]+|[^\s]",
                            text.replace("**", "")))


def _require_clauses(text, clauses, label="guidance"):
    tokens = _clause_tokens(text)
    for clause in clauses:
        required = _clause_tokens(clause)
        assert required and any(tokens[start:start + len(required)] == required
                                for start in range(len(tokens) - len(required) + 1)), (
            f"{label}: missing required clause: {clause}")


@pytest.mark.parametrize("locale,document", [("en", "pipeline.md"), ("zh-TW", "pipeline.zh-TW.md")])
@pytest.mark.parametrize("contract", EXAMPLE["guidance"])
def test_stage1_exposes_each_guidance_contract(locale, document, contract):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    stage1 = text.split("## 1.", 1)[1].split("## 2.", 1)[0]
    _require_clauses(stage1, EXAMPLE["guidance"][contract][locale], f"{document}: {contract}")


@pytest.mark.parametrize("text,clause", [
    ("**已儲存不等於語義上\n已完成**", "已儲存不等於語義上已完成"),
    ("已儲存不等於語義上已完成", "已儲存不等於語義上 已完成"),
    ("Saved does\nnot mean\tsemantically completed.", "Saved does not mean semantically completed"),
])
def test_clause_checks_accept_harmless_reflow_in_text_or_requirement(text, clause):
    _require_clauses(text, [clause])


@pytest.mark.parametrize("text,clause", [
    ("已儲存等於語義上已完成", "已儲存不等於語義上已完成"),
    ("Saved does mean semantically completed.", "Saved does not mean semantically completed"),
    ("Saveddoes not mean semantically completed.", "Saved does not mean semantically completed"),
    ("Technical pending work is automatically a human-only decision.", "not automatically a human-only decision"),
    ("A file was saved.", "Saved does not mean semantically completed"),
])
def test_clause_checks_still_reject_missing_semantics_or_merged_words(text, clause):
    with pytest.raises(AssertionError, match="missing required clause"):
        _require_clauses(text, [clause])


@pytest.mark.parametrize("locale,document", [("en", "pipeline.md"), ("zh-TW", "pipeline.zh-TW.md")])
def test_actual_stage1_contracts_survive_harmless_document_reflow(locale, document):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    stage1 = text.split("## 1.", 1)[1].split("## 2.", 1)[0]
    reflowed = re.sub(r"(?<=[\u3400-\u9fff])\s*(?=[\u3400-\u9fff])", "\n", stage1)
    reflowed = re.sub(r"[ \t]+", "\n", reflowed)
    for contract in EXAMPLE["guidance"].values():
        _require_clauses(reflowed, contract[locale])


def test_supplied_preferences_example_needs_no_repeat_or_forced_storage():
    intake = EXAMPLE["intake"]
    assert str(intake["target_count"]) in intake["request"]
    assert intake["close_read_count"] == 2
    assert intake["repeat_supplied_questions"] == []
    assert intake["destinations"] == []
    assert "partial" in intake["round_status"]
    # Fewer relevant inclusions are reported, not padded to the user's target.
    assert EXAMPLE["counts"]["included"] < intake["target_count"]


def test_worked_handoff_counts_versions_depth_and_core_separately():
    works = EXAMPLE["works"]
    versions = EXAMPLE["versions"]
    counts = EXAMPLE["counts"]
    assert counts["raw_version_records"] == len(versions)
    work_ids = {work["id"] for work in works}
    assert work_ids == {version["work"] for version in versions}
    assert counts["discovered"] == len(work_ids) == len(works)
    assert counts["screened"] == sum(w["screened"] for w in works)
    included = [w for w in works if w["included"]]
    assert counts["included"] == len(included)
    assert counts["core"] == sum(w["core"] for w in included)
    assert counts["reading_depth_included"] == dict(Counter(w["reading_level"] for w in included))
    assert counts["raw_version_records"] > counts["discovered"]


def test_worked_handoff_binds_summary_to_read_version_and_scope():
    versions = {(v["work"], v["version"]) for v in EXAMPLE["versions"]}
    for work in EXAMPLE["works"]:
        if work["version_read"] is not None:
            assert (work["id"], work["version_read"]) in versions
        assert work["summary_version"] == work["version_read"]
        assert set(work["summary_sections"]) <= set(work["read_sections"])
        if work["reading_level"] == "abstract-only":
            assert work["read_sections"] == ["abstract"]
        if work["reading_level"] == "not-read":
            assert work["version_read"] is None and work["read_sections"] == []
        if work["included"]:
            assert work["screened"] and work["roles"] and work["reason"]
    assert {role for work in EXAMPLE["works"] for role in work["roles"]} == {
        "classic", "core", "nearest", "methodological", "contrary"}


@pytest.mark.parametrize("case", EXAMPLE["access_cases"], ids=lambda case: case["case"])
def test_worked_access_cases_require_public_validated_body(case):
    expected = (case["lawful_public"] and case["body_validated"]
                and case["body_kind"] in {"pdf-body", "html-body"})
    assert case["archive_nlm_eligible"] == expected


def test_saved_and_technical_pending_example_does_not_claim_completion():
    write = EXAMPLE["optional_write_example"]
    receipts = {receipt["destination"]: receipt for receipt in write["receipts"]}
    assert set(receipts) == set(write["separately_authorized_destinations"])
    assert receipts["Zotero"]["outcome"] == "success"
    assert receipts["Zotero"]["object_id"]
    assert receipts["NotebookLM"]["outcome"] == "failure"
    assert receipts["NotebookLM"]["reason"]
    assert write["overall_storage_outcome"] == "partial"
    assert not write["semantically_completed"]
    assert write["technical_pending"] and not write["human_decision_required"]
    work = next(w for w in EXAMPLE["works"] if w["id"] == write["work"])
    assert write["version"] == work["version_read"]
    assert not work["semantically_completed"]
    pending = next(w for w in EXAMPLE["works"] if w["id"] == "pending")
    assert pending["access_status"] == "pending/background"
    assert pending["included"] and pending["reading_level"] == "abstract-only"
