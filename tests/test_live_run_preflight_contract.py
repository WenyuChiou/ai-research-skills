"""Supervisor-contract fixtures, not a production preflight/enforcement hook.

All settings and approvals below are synthetic. No host/account/model request,
credential setup, pricing verification or security enforcement is exercised.
"""
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("host", "provider", "model", "auth_mode", "budget", "cost_policy",
            "data_destination", "data_scope")
MATERIAL = tuple(field for field in REQUIRED if field != "host")


def _effective():
    return dict(host="configured-host", provider="configured-provider",
                model="configured-model", auth_mode="chatgpt_subscription",
                budget="approved-budget-ref", cost_policy="approved-cost-policy",
                data_destination="approved-service", data_scope="approved-files",
                auth_ready=True, model_supported=True)


def _choice(effective):
    return {**deepcopy(effective), "decision": "approved", "valid": True}


def _decision_fixture(effective, explicit=None):
    """Illustrate declared review decisions; supplied records are not authenticated."""
    if any(effective.get(field) is None or effective.get(field) == ""
           or effective.get(field) == "unknown" for field in REQUIRED):
        return "ask_missing"
    if effective["model"] in {"auto", "default"}:
        return "ask_missing"
    if not effective.get("auth_ready") or not effective.get("model_supported"):
        return "blocked_setup"
    if explicit is None:
        return "ask_first_choice"
    if explicit.get("decision") == "declined":
        return "blocked_approval"
    if not explicit.get("valid") or explicit.get("decision") != "approved":
        return "ask_first_choice"
    if any(field not in explicit for field in MATERIAL):
        return "ask_missing"
    if any(effective[field] != explicit[field] for field in MATERIAL):
        return "ask_change"
    return "reuse_valid_choice"


def test_bilingual_preflight_surfaces_material_choices_and_has_no_runtime_claim():
    paths = [ROOT / f"docs/live-run-preflight{suffix}.md" for suffix in ("", ".zh-TW")]
    texts = [path.read_text(encoding="utf-8") for path in paths]
    assert texts[0].count("\n## ") == texts[1].count("\n## ") == 3
    for text in texts:
        for term in ("Host/runtime", "Provider/model", "Authentication mode",
                     "ChatGPT subscription", "API", "Budget/cost policy",
                     "Data destination/scope", "fallback", "secret", "hook"):
            assert term in text
    for suffix in ("", ".zh-TW"):
        for stem in ("install", "system-assessment", "setup-guide"):
            text = (ROOT / f"docs/{stem}{suffix}.md").read_text(encoding="utf-8")
            assert f"live-run-preflight{suffix}.md" in text


@pytest.mark.parametrize("suffix,clauses", [
    ("", [
        "Native-only users skip this step",
        "before running `auto`",
        "`--no-nlm` disables only NotebookLM",
        "does not disable other network requests, model calls or local/external writes",
        "not a read-only or offline test",
    ]),
    (".zh-TW", [
        "只走原生路線的使用者跳過此步驟",
        "執行 `auto` 前",
        "`--no-nlm` 只停用 NotebookLM",
        "不會停用其他網路請求、模型呼叫或本機／外部寫入",
        "不是唯讀或離線測試",
    ]),
])
def test_setup_auto_smoke_test_surfaces_live_boundary_before_invocation(suffix, clauses):
    text = (ROOT / f"docs/setup-guide{suffix}.md").read_text(encoding="utf-8")
    smoke = text.split("### D4. Runtime smoke test", 1)[1].split("### Phase D checkpoint", 1)[0]
    before_auto = smoke.split('research-hub auto "agent-based flood modeling"', 1)[0]
    assert f"live-run-preflight{suffix}.md" in before_auto
    for clause in clauses:
        assert clause in " ".join(before_auto.split())


def test_first_use_requires_choices_even_when_observed_defaults_are_available():
    assert _decision_fixture(_effective()) == "ask_first_choice"


@pytest.mark.parametrize("field", REQUIRED)
def test_missing_material_settings_are_not_discovered_with_a_model_call(field):
    effective = _effective()
    effective.pop(field)
    assert _decision_fixture(effective) == "ask_missing"


def test_prior_model_choice_does_not_approve_unknown_auth_budget_or_data():
    assert _decision_fixture(_effective(), {"model": "configured-model"}) != "reuse_valid_choice"


def test_unchanged_valid_explicit_choices_are_reused_without_repeated_questions():
    effective = _effective()
    assert _decision_fixture(effective, _choice(effective)) == "reuse_valid_choice"


def test_structured_budget_refs_and_data_scope_are_not_missing_choices():
    effective = _effective()
    effective.update(budget={"policy_ref": "approved-budget-ref"},
                     data_scope=["approved-file"])
    assert _decision_fixture(effective, _choice(effective)) == "reuse_valid_choice"


def test_prior_choices_are_snapshots_not_mutable_aliases():
    effective = _effective()
    effective["budget"] = {"policy_ref": "approved-budget-ref"}
    prior = _choice(effective)
    effective["budget"]["policy_ref"] = "different-budget-ref"
    assert _decision_fixture(effective, prior) == "ask_change"


@pytest.mark.parametrize("field", MATERIAL)
def test_unapproved_material_changes_require_reconfirmation(field):
    effective = _effective()
    prior = _choice(effective)
    effective[field] = "different-material-choice"
    assert _decision_fixture(effective, prior) == "ask_change"


@pytest.mark.parametrize("unavailable", ["auth_ready", "model_supported"])
def test_unavailable_setup_does_not_trigger_secret_collection_or_fallback(unavailable):
    effective = _effective()
    effective[unavailable] = False
    assert _decision_fixture(effective, _choice(effective)) == "blocked_setup"


def test_declined_or_expired_choices_are_not_normalized_to_success():
    effective = _effective()
    declined = _choice(effective)
    declined["decision"] = "declined"
    assert _decision_fixture(effective, declined) == "blocked_approval"
    expired = deepcopy(declined)
    expired.update(decision="approved", valid=False)
    assert _decision_fixture(effective, expired) == "ask_first_choice"
