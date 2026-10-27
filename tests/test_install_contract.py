"""Offline install resolver regressions against public upstream contracts.

Snapshots bind public commit identities, not live-host behavior. The source
checker can additionally inspect supplied real clones without installing them.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess

import pytest
import yaml

from scripts import check_marketplace_consistency as consistency
from scripts import check_manifest_observations as observations

ROOT = Path(__file__).resolve().parents[1]


def _bash_executable():
    """Select a shell whose path conventions match the test arguments."""
    if os.name == "nt":
        roots = []
        git = shutil.which("git")
        if git:
            roots.extend((Path(git).resolve().parent, *Path(git).resolve().parents))
        for variable in ("ProgramFiles", "ProgramFiles(x86)"):
            if os.environ.get(variable):
                roots.append(Path(os.environ[variable]) / "Git")
        for root in roots:
            candidate = root / "usr" / "bin" / "bash.exe"
            if candidate.is_file():
                return str(candidate)
        raise RuntimeError(
            "Windows Bash contract tests require Git for Windows Bash "
            "(usr/bin/bash.exe); WSL's bash launcher uses different path conventions."
        )
    return shutil.which("bash") or "bash"


def _bash_script_arg(path: Path) -> str:
    """Pass a MSYS-friendly absolute path when Python runs on Windows."""
    if os.name == "nt":
        drive, tail = os.path.splitdrive(str(path))
        if drive:
            return f"/{drive[0].lower()}{tail.replace(os.sep, '/')}"
    return str(path)


_BASH = _bash_executable()


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
    observed = json.loads(observations.OBSERVATIONS.read_text(encoding="utf-8"))
    assert observations.validate(marketplace, snapshot, observed) == []


def test_future_native_reader_fixture_does_not_advance_install_or_accepted_pins():
    future = json.loads((ROOT / "test-corpus/integration/native-reader-future-contract.json").read_text(encoding="utf-8"))
    accepted = json.loads((ROOT / "test-corpus/integration/upstream-contracts.json").read_text(encoding="utf-8"))
    _, marketplace = consistency._load()
    hub = next(row for row in accepted["repositories"] if row["repo_url"].endswith("/research-hub"))
    install = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "research-workspace")
    assert future["status"] == "future-candidate-contract-only" and future["updates_accepted_source"] is False
    assert accepted["checked_on"] == "2026-10-19"
    assert hub["commit"] == "7e046383368d85acb8dfbf0d734ecaaae335cf0a" and hub["plugin"]["version"] == "0.5.4"
    assert len(hub["skills"]) == 12 and len(hub["shared_references"]) == 8
    assert set(future["candidate_dependencies"]).isdisjoint(hub["shared_references"])
    assert install["version"] == "0.5.10" and install["source"]["ref"] == "master"


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
    command = [_BASH, _bash_script_arg(ROOT / "scripts/install-all.sh"), "--dry-run", "--scope", "project"]
    first = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    second = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True, text=True)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    assert first.stdout.count("claude plugin install") == 5
    assert "--scope project" in first.stdout
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("args", [["--scope"], ["--scope", "invalid"], ["--unknown"], ["--dry-run", "trailing"]])
def test_bash_rejects_invalid_arguments_before_cli(args, tmp_path):
    result = subprocess.run([_BASH, _bash_script_arg(ROOT / "scripts/install-all.sh"), *args], cwd=tmp_path, capture_output=True, text=True)
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
    env = dict(os.environ, HOME=str(tmp_path), PATH=os.pathsep.join((str(tmp_path), os.environ["PATH"])))
    result = subprocess.run([_BASH, _bash_script_arg(ROOT / "scripts/install-all.sh")], env=env, cwd=tmp_path, capture_output=True, text=True)
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


def _assert_powershell_scope_rejected(result):
    # PowerShell diagnostics are localized and need not use Python's encoding.
    # Windows PowerShell exposes the error ID; newer pwsh concise diagnostics
    # can omit it. Keep the observed English concise fallback scope-specific.
    assert result.returncode != 0
    stderr = result.stderr
    if b"FullyQualifiedErrorId" in stderr:
        assert b"ParameterArgumentValidationError" in stderr
    else:
        assert all(token in stderr for token in (
            b"Cannot validate argument on parameter 'Scope'",
            b'"invalid"', b"ValidateSet", b'"user,project,local"',
        ))


@pytest.mark.parametrize("encoding", ["cp950", "utf-8"])
def test_powershell_scope_diagnostic_encoding_contract(encoding):
    """Synthetic diagnostics only: neither runs nor emulates PowerShell."""
    stderr = (
        "無法驗證 'Scope' 參數上的引數。\r\n"
        "    + FullyQualifiedErrorId : ParameterArgumentValidationError,install-all.ps1\r\n"
    ).encode(encoding)
    result = subprocess.CompletedProcess([], 1, b"", stderr)
    _assert_powershell_scope_rejected(result)
    with pytest.raises(AssertionError):
        _assert_powershell_scope_rejected(subprocess.CompletedProcess([], 0, b"", stderr))
    with pytest.raises(AssertionError):
        _assert_powershell_scope_rejected(subprocess.CompletedProcess(
            [], 1, b"", stderr.replace(b"ParameterArgumentValidationError", b"CommandNotFoundException")
        ))


_CONCISE_SCOPE_DIAGNOSTIC = (
    b"\x1b[31;1minstall-all.ps1: Cannot validate argument on parameter 'Scope'. "
    b'The argument "invalid" does not belong to the set "user,project,local" '
    b"specified by the ValidateSet attribute.\x1b[0m\n"
)


def test_powershell_concise_scope_diagnostic_contract():
    """Synthetic known concise shape, not a captured/untruncated CI payload."""
    _assert_powershell_scope_rejected(subprocess.CompletedProcess(
        [], 1, b"", _CONCISE_SCOPE_DIAGNOSTIC
    ))


@pytest.mark.parametrize("stderr,returncode", [
    (_CONCISE_SCOPE_DIAGNOSTIC, 0),
    (_CONCISE_SCOPE_DIAGNOSTIC.replace(b"'Scope'", b"'Other'"), 1),
    (_CONCISE_SCOPE_DIAGNOSTIC.replace(b'"invalid"', b'"other"'), 1),
    (_CONCISE_SCOPE_DIAGNOSTIC.replace(b"ValidateSet", b"ValidatePattern"), 1),
    (_CONCISE_SCOPE_DIAGNOSTIC.replace(b'"user,project,local"', b'"other"'), 1),
    (_CONCISE_SCOPE_DIAGNOSTIC.replace(b"Cannot validate argument", b"Unrelated error"), 1),
    (b"CommandNotFoundException: install-all.ps1", 1),
    (_CONCISE_SCOPE_DIAGNOSTIC + b"FullyQualifiedErrorId : CommandNotFoundException", 1),
    (b"", 1),
])
def test_powershell_unrelated_diagnostics_are_not_scope_rejection(stderr, returncode):
    with pytest.raises(AssertionError):
        _assert_powershell_scope_rejected(subprocess.CompletedProcess([], returncode, b"", stderr))


@pytest.mark.skipif(_POWERSHELL is None, reason="PowerShell runtime not available")
def test_powershell_plan_is_repeatable_and_invalid_scope_rejected(tmp_path):
    env = dict(os.environ, HOME=str(tmp_path), XDG_CACHE_HOME=str(tmp_path / "cache"))
    command = [_POWERSHELL, "-NoLogo", "-NoProfile", "-File", str(ROOT / "scripts/install-all.ps1"), "-DryRun", "-Scope", "project"]
    first = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True)
    second = subprocess.run(command, env=env, cwd=tmp_path, capture_output=True)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    assert first.stdout.count(b"claude plugin install") == 5
    rejected = subprocess.run(command[:-1] + ["invalid"], env=env, cwd=tmp_path, capture_output=True)
    _assert_powershell_scope_rejected(rejected)


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


def test_accepted_source_matrix_matches_commit_bound_snapshot():
    snapshot = json.loads((ROOT / "test-corpus/integration/upstream-contracts.json").read_text(encoding="utf-8"))
    for suffix in ("", ".zh-TW"):
        text = (ROOT / f"docs/system-assessment{suffix}.md").read_text(encoding="utf-8")
        for source in snapshot["repositories"]:
            slug = source["repo_url"].rsplit("/", 1)[1]
            row = next(line for line in text.splitlines() if line.startswith(f"| {slug} |"))
            assert f"{source['repo_url']}/tree/{source['commit']}" in row
            assert source["plugin"]["version"] in row


def test_accepted_direction_review_source_identity_and_install_ref():
    _, marketplace = consistency._load()
    snapshot = json.loads((ROOT / "test-corpus/integration/upstream-contracts.json").read_text(encoding="utf-8"))
    source = next(item for item in snapshot["repositories"] if item["repo_url"].endswith("/research-hub"))
    assert source["commit"] == "7e046383368d85acb8dfbf0d734ecaaae335cf0a"
    assert source["plugin"] == {"name": "research-workspace", "version": "0.5.4"}
    plugin = next(item for item in marketplace["plugins"] if item["name"] == "research-workspace")
    # Current cache metadata is separately checked by the manifest-only guard;
    # historical commit, version and linked content remain bound above/below.
    assert plugin["name"] == source["plugin"]["name"]
    assert plugin["source"]["ref"] == source["default_branch"] == "master"
    contract_url = f"{source['repo_url']}/blob/{source['commit']}/docs/direction-review-contract.md"
    for suffix in ("", ".zh-TW"):
        text = (ROOT / f"docs/system-assessment{suffix}.md").read_text(encoding="utf-8")
        for term in (contract_url, "paper direction-check", "candidate_version", "candidate_sha256",
                     "data/tool/model/license/cost/premise/validation-path", "sharing_basis",
                     "human_selection: outside-checker", "execution_authorized: false",
                     "semantic_assessment: not-performed", "runtime_budget_verification: not-performed"):
            assert term in text


def test_source_audit_and_native_comparison_rollout_limits_remain_explicit():
    for suffix in ("", ".zh-TW"):
        text = (ROOT / f"docs/system-assessment{suffix}.md").read_text(encoding="utf-8")
        for term in ("source_audit", "artifact_root", "research-source-audit-1.0.json",
                     "codex-plugin-cc", "commandExecution", "fileChange"):
            assert term in text


def test_accepted_harness_source_docs_do_not_imply_a_runtime_engine():
    catalog, _ = consistency._load()
    evidence = catalog["extensions"][0]["verification"]["evidence"]
    assert "4aa56e47011b15a416f128b5a1c395baae8d0581" in evidence
    assert "declarative" in evidence and "mtime" in evidence
    assert "not a runtime preset engine" in evidence


def test_accepted_source_doc_reads_ignore_locale_default_encoding(monkeypatch):
    original = Path.read_text

    def require_utf8(path, *args, **kwargs):
        assert kwargs.get("encoding") == "utf-8"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", require_utf8)
    test_accepted_source_matrix_matches_commit_bound_snapshot()
    test_source_audit_and_native_comparison_rollout_limits_remain_explicit()
    test_accepted_harness_source_docs_do_not_imply_a_runtime_engine()


@pytest.mark.parametrize("skill,owner", [
    ("literature-triage-matrix", "research-hub"),
    ("gap-to-topic", "research-hub"),
    ("research-design-helper", "research-hub"),
    ("paper-memory-builder", "research-hub"),
    ("paper-summarize", "research-hub"),
    ("research-hub", "research-hub"),
    ("academic-writing-skills", "academic-writing-skills"),
    ("paper-review", "academic-writing-skills"),
    ("zotero-skills", "zotero-skills"),
    ("codex-delegate", "codex-delegate"),
    ("antigravity-delegate", "antigravity-delegate"),
])
def test_task_entry_links_resolve_to_catalog_source_owner(skill, owner):
    """Static route examples: link ownership, not model routing/host invocation."""
    import re
    catalog, _ = consistency._load()
    entries = {s["name"]: s for f in catalog["families"] for s in f["skills"]}
    text = (ROOT / "docs/install.md").read_text(encoding="utf-8")
    route_table = text.split("## Choose your task first", 1)[1].split("## Choose an install path", 1)[0]
    references = dict(re.findall(r"^\[([^]]+)\]: (\S+)$", route_table, re.MULTILINE))
    assert entries[skill]["repo_url"] == f"https://github.com/WenyuChiou/{owner}"
    assert references[skill] == entries[skill]["skill_url"]
    assert any(f"[{skill}]" in line for line in route_table.splitlines() if line.startswith("|"))


@pytest.mark.parametrize("relative", ["docs/install.md", "docs/runtime-contract.md"])
def test_runtime_route_local_links_and_examples_resolve(relative):
    """Catch broken local handoffs without fetching sources or invoking tools."""
    import re
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if target.startswith(("https://", "http://", "#")):
            continue
        file, _, fragment = target.partition("#")
        linked = path.parent / file
        assert linked.is_file(), target
        if fragment:
            linked_text = linked.read_text(encoding="utf-8")
            headings = re.findall(r"^#+ (.+)$", linked_text, re.MULTILINE)
            anchors = {re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings}
            assert fragment in anchors or f'id="{fragment}"' in linked_text, target
