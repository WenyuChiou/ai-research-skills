from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import subprocess

import pytest

from scripts import plan_branch_cleanup as cleanup


NOW = datetime(2026, 11, 7, 12, tzinfo=timezone.utc)
REPO = "WenyuChiou/ai-research-skills"


@pytest.fixture
def metadata():
    config = json.loads(cleanup.CONFIG.read_text(encoding="utf-8"))
    branch = {"name": "codex/done", "protected": False, "commit": {"sha": "a" * 40}}
    pr = {"number": 1, "state": "closed", "merged_at": "2026-10-20T12:00:00Z",
          "head": {"ref": branch["name"], "sha": branch["commit"]["sha"], "repo": {"full_name": REPO}},
          "base": {"ref": "main", "repo": {"full_name": REPO}}, "user": {"login": "WenyuChiou"}}
    return config, {"repository": {"full_name": REPO, "default_branch": "main"},
                    "complete": True, "captured_at": NOW.isoformat(),
                    "branches": [{"name": "main", "protected": True, "commit": {"sha": "b" * 40}}, branch],
                    "pulls": [pr]}


def run(metadata):
    return cleanup.plan(*metadata, now=NOW)


def reason(metadata):
    report = run(metadata)
    assert report["candidates"] == []
    return next(row["reason"] for row in report["retained"] if row["branch"] != "main")


def test_merged_exact_head_is_only_a_report(metadata):
    before = deepcopy(metadata)
    result = run(metadata)
    assert result["mode"] == "report-only"
    assert result["deletion_authorized"] is False
    assert result["candidates"][0]["head_sha"] == "a" * 40
    assert result["candidates"][0]["pr_number"] == 1
    assert result["retained"][0]["reason"] == "default_branch"
    assert "dependent PRs and local worktrees" in result["remaining_checks"]
    assert metadata == before


@pytest.mark.parametrize("protected", [True, None, "false"])
def test_protected_or_unknown_is_retained(metadata, protected):
    metadata[1]["branches"][1]["protected"] = protected
    assert reason(metadata) == "protected_or_unknown"


def test_missing_protection_is_retained(metadata):
    del metadata[1]["branches"][1]["protected"]
    assert reason(metadata) == "protected_or_unknown"


def test_keep_pattern_wins(metadata):
    metadata[0]["keep_patterns"].append("codex/*")
    assert reason(metadata) == "keep_pattern"


def test_custom_prefixes_and_authors_can_disable_candidates(metadata):
    metadata[0]["allowed_prefixes"] = []
    assert reason(metadata) == "prefix_not_allowed"
    metadata[0]["allowed_prefixes"] = ["codex/"]
    metadata[0]["allowed_pr_authors"] = []
    assert reason(metadata) == "pr_author_not_allowed"


def test_open_pr_retained_even_with_older_merged_evidence(metadata):
    newer = deepcopy(metadata[1]["pulls"][0])
    newer.update(number=2, state="open", merged_at=None)
    metadata[1]["pulls"].append(newer)
    assert reason(metadata) == "open_pr_or_unknown_source"


def test_dependent_open_pr_retains_base_branch(metadata):
    newer = deepcopy(metadata[1]["pulls"][0])
    newer.update(number=2, state="open", merged_at=None)
    newer["base"]["ref"] = "codex/done"
    newer["head"]["ref"] = "codex/depends"
    metadata[1]["pulls"].append(newer)
    assert reason(metadata) == "dependent_open_pr"


@pytest.mark.parametrize("change", ["null_repo", "missing_repo", "empty_repo", "missing_ref", "null_ref", "empty_ref"])
def test_unknown_dependent_base_identity_fails_closed(metadata, change):
    newer = deepcopy(metadata[1]["pulls"][0])
    newer.update(number=2, state="open", merged_at=None)
    newer["base"]["ref"] = "codex/done"
    newer["head"]["ref"] = "codex/depends"
    if change == "null_repo":
        newer["base"]["repo"] = None
    elif change == "missing_repo":
        del newer["base"]["repo"]
    elif change == "empty_repo":
        newer["base"]["repo"] = {}
    elif change == "missing_ref":
        del newer["base"]["ref"]
    elif change == "null_ref":
        newer["base"]["ref"] = None
    else:
        newer["base"]["ref"] = ""
    metadata[1]["pulls"].append(newer)
    with pytest.raises(ValueError):
        run(metadata)


def test_closed_unmerged_pr_is_not_cleanup_permission(metadata):
    newer = deepcopy(metadata[1]["pulls"][0])
    newer.update(number=2, merged_at=None)
    metadata[1]["pulls"].append(newer)
    assert reason(metadata) == "closed_unmerged_pr"


@pytest.mark.parametrize("change", ["head", "fork", "wrong_base", "base_repo", "orphan"])
def test_missing_exact_merge_evidence_is_retained(metadata, change):
    pr = metadata[1]["pulls"][0]
    if change == "head":
        metadata[1]["branches"][1]["commit"]["sha"] = "c" * 40
    elif change == "fork":
        pr["head"]["repo"]["full_name"] = "other/ai-research-skills"
    elif change == "wrong_base":
        pr["base"]["ref"] = "development"
    elif change == "base_repo":
        pr["base"]["repo"]["full_name"] = "other/ai-research-skills"
    else:
        metadata[1]["pulls"] = []
    assert reason(metadata) == "no_merged_pr_at_current_head"


def test_missing_source_repo_is_ambiguous(metadata):
    metadata[1]["pulls"][0]["head"]["repo"] = None
    assert reason(metadata) == "open_pr_or_unknown_source"


def test_other_author_is_retained(metadata):
    metadata[1]["pulls"][0]["user"]["login"] = "contributor"
    assert reason(metadata) == "pr_author_not_allowed"


def test_retention_is_configurable_and_enforced(metadata):
    metadata[1]["pulls"][0]["merged_at"] = "2026-11-06T12:00:00Z"
    assert reason(metadata) == "retention_period"
    metadata[0]["minimum_age_days"] = 1
    assert len(run(metadata)["candidates"]) == 1


@pytest.mark.parametrize("change", ["incomplete", "stale", "future", "naive", "repo", "sha", "default", "duplicate", "pr_repo"])
def test_invalid_snapshots_fail_closed(metadata, change):
    snapshot = metadata[1]
    if change == "incomplete":
        snapshot["complete"] = False
    elif change in {"stale", "future", "naive"}:
        snapshot["captured_at"] = {"stale": "2026-11-01T12:00:00Z", "future": "2026-11-08T12:00:00Z",
                                   "naive": "2026-11-07T12:00:00"}[change]
    elif change == "repo":
        snapshot["repository"]["full_name"] = "other/repo"
    elif change == "sha":
        snapshot["branches"][1]["commit"]["sha"] = "short"
    elif change == "default":
        snapshot["branches"] = snapshot["branches"][1:]
    elif change == "pr_repo":
        snapshot["pulls"][0]["head"]["repo"] = {"name": "missing identity"}
    else:
        snapshot["branches"].append(snapshot["branches"][1])
    with pytest.raises(ValueError):
        run(metadata)


@pytest.mark.parametrize("field,value", [("minimum_age_days", -1), ("minimum_age_days", True),
    ("allowed_prefixes", [""]), ("allowed_prefixes", ["codex"]), ("repository", "owner/repo?bad"),
    ("unexpected", True), ("keep_patterns", [None])])
def test_invalid_config_fails_closed(metadata, field, value):
    metadata[0][field] = value
    with pytest.raises(ValueError):
        run(metadata)


def test_collection_paginates_both_lists_with_get_only(monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        assert command[:7] == ["gh", "api", "--hostname", "github.com", "--method", "GET", command[6]]
        assert kwargs["check"] is True
        assert "shell" not in kwargs
        value = [[{"page": 1}], [{"page": 2}]] if "--paginate" in command else {"full_name": REPO}
        return subprocess.CompletedProcess(command, 0, json.dumps(value))

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = cleanup.collect(REPO)
    assert result["branches"] == result["pulls"] == [{"page": 1}, {"page": 2}]
    assert result["complete"] is True
    assert len(calls) == 3
    assert all("--slurp" in command for command in calls[1:])
    assert "state=all" in calls[2][6]


def test_live_failure_prints_no_plan_or_credentials(monkeypatch, capsys):
    def fail(_repository):
        raise subprocess.CalledProcessError(1, "gh", stderr="credential detail")
    monkeypatch.setattr(cleanup, "collect", fail)
    assert cleanup.main([]) == 2
    output = capsys.readouterr()
    assert output.out == ""
    assert "credential detail" not in output.err


def test_apply_flag_does_not_exist():
    with pytest.raises(SystemExit) as exc:
        cleanup.main(["--apply"])
    assert exc.value.code == 2


def test_governance_preserves_merge_consent_and_distinct_review():
    agents = (cleanup.ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Every PR merge needs separate explicit user consent" in agents
    assert "passing independent subagent review" in agents
    assert "must not be the authoring agent" in agents
    assert "Keep\n  actual GitHub protections in force" in agents
    guide = (cleanup.ROOT / "docs/review-governance.md").read_text(encoding="utf-8")
    assert "published head has the identical tree" in guide
    assert "There is no `--apply`" in guide
