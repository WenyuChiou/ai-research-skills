"""Offline install resolver regressions against public upstream contracts.

Snapshots bind public commit identities, not live-host behavior. The source
checker can additionally inspect supplied real clones without installing them.
"""
from pathlib import Path
import json
import os
import subprocess

import pytest
import yaml

from scripts import check_marketplace_consistency as consistency

ROOT = Path(__file__).resolve().parents[1]


def test_catalog_directories_and_marketplace_match_checked_upstreams():
    catalog, marketplace = consistency._load()
    snapshot = json.loads((ROOT / "test-corpus/integration/upstream-contracts.json").read_text())
    by_repo = {r["repo_url"]: r for r in snapshot["repositories"]}
    assert len(by_repo) == 5
    for family in catalog["families"]:
        for skill in family["skills"]:
            source = by_repo[skill["repo_url"]]
            expected = next(s["directory"] for s in source["skills"] if s["name"] == skill["name"])
            assert skill["directory"] == expected, skill["name"]
    for plugin in marketplace["plugins"]:
        source = by_repo[plugin["source"]["url"].removesuffix(".git")]
        assert plugin["source"]["ref"] == source["default_branch"]
        assert plugin["name"] == source["plugin"]["name"]
        assert plugin["version"] == source["plugin"]["version"]


def test_canonical_installs_do_not_clone_nested_repo_as_a_single_skill():
    catalog, _ = consistency._load()
    for family in catalog["families"]:
        for command in family["install"]["commands"]:
            assert "git clone" not in command or "~/.claude/skills/" not in command
    for relative in ("docs/install.md", "docs/skill-directory.md", "docs/researcher-workflow-checklist.md"):
        text = (ROOT / relative).read_text()
        assert not any("git clone" in line and "~/.claude/skills/" in line for line in text.splitlines()), relative


def test_bash_dry_run_is_repeatable_without_cli_or_mutation(tmp_path):
    env = dict(os.environ, HOME=str(tmp_path))
    command = ["bash", str(ROOT / "scripts/install-all.sh"), "--dry-run", "--scope", "project"]
    first = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    second = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    assert first.stdout.count("claude plugin install") == 5
    assert "--scope project" in first.stdout
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("args", [["--scope"], ["--scope", "invalid"], ["--unknown"], ["--dry-run", "trailing"]])
def test_bash_rejects_invalid_arguments_before_cli(args, tmp_path):
    result = subprocess.run(["bash", str(ROOT / "scripts/install-all.sh"), *args], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 2
    assert "argument" in result.stderr or "scope" in result.stderr


def test_resolver_rejects_directory_ref_and_traversal_mismatch():
    import copy
    catalog, marketplace = consistency._load()
    assert consistency.check_skill_paths_and_refs(catalog, marketplace) == []
    for value in (".", "../outside", "/absolute", "skills\\research-hub", "skills//research-hub"):
        broken = copy.deepcopy(catalog)
        broken["families"][0]["skills"][0]["directory"] = value
        assert consistency.check_skill_paths_and_refs(broken, marketplace)
    broken = copy.deepcopy(marketplace)
    broken["plugins"][0]["source"]["ref"] = "other-ref"
    assert consistency.check_skill_paths_and_refs(catalog, broken)


def test_real_source_checker_fails_closed_for_absent_or_wrong_producer(tmp_path):
    from scripts.check_upstream_contracts import check_sources
    catalog, marketplace = consistency._load()
    missing = check_sources(catalog, marketplace, {})
    assert missing["status"] == "fail" and missing["skills_checked"] == 0
    root = tmp_path / "producer"
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin/plugin.json").write_text(json.dumps({"name": "wrong-name", "version": "999.0.0"}))
    report = check_sources(catalog, marketplace, {"research-hub": root})
    assert report["status"] == "fail"
    assert any("manifest name" in finding for finding in report["findings"])
    assert any("SKILL.md unreadable" in finding for finding in report["findings"])


def test_installer_stops_on_first_failed_native_command(tmp_path):
    fake = tmp_path / "claude"
    fake.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOME/calls"\nexit 17\n')
    fake.chmod(0o755)
    env = dict(os.environ, HOME=str(tmp_path), PATH=f"{tmp_path}:{os.environ['PATH']}")
    result = subprocess.run(["bash", str(ROOT / "scripts/install-all.sh")], env=env, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 17
    assert (tmp_path / "calls").read_text().splitlines() == ["plugin marketplace add WenyuChiou/ai-research-skills"]


def test_scientific_lifecycle_docs_preserve_all_stages_gates_and_limits():
    import re
    required = ("topic_dossier.gaps.yml", "design_brief.md", "project_manifest.yml",
                "experiment_matrix.yml", "data_dictionary.yml", "provenance.from_gap",
                ".paper/claims.yml", ".paper/figures.yml", "preregistration", "429",
                "ResearchEvidencePacket", "work/version", "PowerShell")
    for stem in ("scientific-lifecycle", "system-assessment"):
        paths = [ROOT / f"docs/{stem}{suffix}.md" for suffix in ("", ".zh-TW")]
        texts = [path.read_text() for path in paths]
        assert texts[0].count("\n## ") == texts[1].count("\n## ")
        for path, text in zip(paths, texts):
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if not target.startswith(("https://", "http://", "#")):
                    assert (path.parent / target).resolve().exists(), target
        if stem == "scientific-lifecycle":
            for text in texts:
                for term in required[:-1]:
                    assert term in text
                for stage in ("1.", "2.", "3a.", "3b.", "4.", "5.", "6.", "7.", "8."):
                    assert f"| {stage}" in text
        else:
            for text in texts:
                assert "PowerShell" in text
                assert "unverified" in text or "未驗證" in text


_POWERSHELL = __import__("shutil").which("pwsh") or __import__("shutil").which("powershell")


@pytest.mark.skipif(_POWERSHELL is None, reason="PowerShell runtime not available")
def test_powershell_plan_is_repeatable_and_invalid_scope_rejected(tmp_path):
    env = dict(os.environ, HOME=str(tmp_path), XDG_CACHE_HOME=str(tmp_path / "cache"))
    command = [_POWERSHELL, "-NoLogo", "-NoProfile", "-File", str(ROOT / "scripts/install-all.ps1"), "-DryRun", "-Scope", "project"]
    first = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    second = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    assert first.stdout.count("claude plugin install") == 5
    rejected = subprocess.run(command[:-1] + ["invalid"], env=env, cwd=tmp_path, capture_output=True, text=True)
    assert rejected.returncode != 0
    assert "Cannot validate argument" in rejected.stderr


@pytest.mark.skipif(_POWERSHELL is None or os.name == "nt", reason="POSIX-native failure double requires PowerShell on POSIX")
def test_powershell_installer_propagates_first_native_failure(tmp_path):
    fake = tmp_path / "claude"
    fake.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOME/calls"\nexit 17\n')
    fake.chmod(0o755)
    env = dict(os.environ, HOME=str(tmp_path), XDG_CACHE_HOME=str(tmp_path / "cache"), PATH=f"{tmp_path}:{os.environ['PATH']}")
    result = subprocess.run([_POWERSHELL, "-NoLogo", "-NoProfile", "-File", str(ROOT / "scripts/install-all.ps1")], env=env, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode != 0
    assert "exit code 17" in result.stderr
    assert (tmp_path / "calls").read_text().splitlines() == ["plugin marketplace add WenyuChiou/ai-research-skills"]


def test_optional_harness_fallback_is_official_checksum_bound_and_keeps_registry():
    from urllib.parse import urlparse
    catalog, _ = consistency._load()
    extension = catalog["extensions"][0]
    assert "pip install agent-collab-harness==0.4.0" in extension["install"]
    fallback = next(command for command in extension["install"] if "#sha256=" in command)
    snapshot = json.loads((ROOT / "test-corpus/integration/harness-release-artifacts.json").read_text())
    legacy = next(item for item in snapshot["artifacts"] if item["tag"] == "v0.4.0")
    assert legacy["asset_url"] + "#sha256=" + legacy["sha256"] in fallback
    assert urlparse(legacy["asset_url"]).netloc == "github.com"
    assert len(legacy["sha256"]) == 64
    for suffix in ("", ".zh-TW"):
        text = (ROOT / f"docs/for-agent-harness-builders{suffix}.md").read_text()
        assert fallback in text
        assert "0.5.1" in text and "v2" in text
