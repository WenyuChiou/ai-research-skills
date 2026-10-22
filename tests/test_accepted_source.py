"""Real local Git fixtures; no cloning, installation, models or network."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts import check_upstream_contracts as checker


def git(root, *args):
    return subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgSign=false", "-C", str(root), *args], check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout.strip()


@pytest.fixture
def source(tmp_path):
    root = tmp_path / "local producer"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Offline fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "core.autocrlf", "false")
    relative = "skills/research-hub/SKILL.md"
    reference = "skills/research-hub/references/research-protocol.md"
    for name, text in {
        ".claude-plugin/plugin.json": json.dumps({"name": "research-workspace", "version": "0.5.4"}),
        relative: "---\nname: research-hub\n---\nRead references/research-protocol.md.\n",
        reference: "# Bounded source evidence\n",
    }.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    git(root, "add", ".")
    git(root, "commit", "-qm", "Reviewed fixture")
    repo = "https://github.com/WenyuChiou/research-hub"
    skill = {"name": "research-hub", "directory": "skills/research-hub",
             "repo_url": repo, "skill_url": repo + "/blob/master/" + relative}
    plugin = {"name": "research-workspace", "version": "0.5.4",
              "source": {"url": repo + ".git", "ref": "master"}}
    snapshot = {"checked_on": "2026-10-03", "verification_scope": "historical source-layout-and-manifest",
                "repositories": [{"repo_url": repo, "commit": git(root, "rev-parse", "HEAD"),
                                  "tree": git(root, "rev-parse", "HEAD^{tree}"), "default_branch": "master",
                                  "plugin": {"name": "research-workspace", "version": "0.5.4"},
                                  "skills": [{"name": "research-hub", "directory": "skills/research-hub"}],
                                  "shared_references": [reference]}]}
    return root, {"families": [{"skills": [skill]}]}, {"plugins": [plugin]}, snapshot


def report(source, *, accepted=True, root=None):
    path, catalog, marketplace, snapshot = source
    return checker.check_sources(catalog, marketplace, {"research-hub": root or path},
                                 accepted_snapshot=snapshot if accepted else None)


def test_detached_exact_commit_passes_without_writing_or_network(source, monkeypatch):
    root, _, _, snapshot = source
    git(root, "checkout", "--detach", snapshot["repositories"][0]["commit"])
    before = copy.deepcopy(snapshot)
    calls = []
    original = subprocess.run

    def recorded(command, **kwargs):
        calls.append(command)
        assert command[0] == "git" and not kwargs.get("shell")
        assert "--no-lazy-fetch" in command
        assert not any(word in command for word in ("clone", "fetch", "checkout", "install"))
        return original(command, **kwargs)

    monkeypatch.setattr(checker.subprocess, "run", recorded)
    result = report(source)
    assert result["status"] == "pass"
    assert result["accepted_sources"][0]["head_tree"] == snapshot["repositories"][0]["tree"]
    assert result["accepted_sources"][0]["files_checked"] == 3
    assert result["snapshot_checked_on"] == "2026-10-03" and snapshot == before
    assert calls


@pytest.mark.parametrize("relative,staged", [
    ("skills/research-hub/SKILL.md", False),
    ("skills/research-hub/references/research-protocol.md", False),
    (".claude-plugin/plugin.json", True),
])
def test_dirty_relevant_paths_cannot_pass_with_the_same_version(source, relative, staged):
    root = source[0]
    path = root / relative
    path.write_bytes(path.read_bytes() + b"\nchanged" if relative.endswith(".md") else path.read_bytes() + b"\n")
    if staged:
        git(root, "add", relative)
    assert report(source, accepted=False)["status"] == "pass"
    result = report(source)
    assert result["status"] == "fail"
    assert any("dirty" in reason for reason in result["accepted_sources"][0]["findings"])


def test_same_version_new_commit_rejects_stale_snapshot_and_preserves_dates(source):
    root, _, marketplace, snapshot = source
    original = copy.deepcopy(snapshot)
    path = root / "skills/research-hub/SKILL.md"
    path.write_bytes(path.read_bytes() + b"new behavior\n")
    git(root, "add", "skills/research-hub/SKILL.md")
    git(root, "commit", "-qm", "Same plugin version, changed bytes")
    assert report(source, accepted=False)["status"] == "pass"
    result = report(source)
    assert result["status"] == "fail" and snapshot == original
    assert result["snapshot_checked_on"] == original["checked_on"]
    assert result["accepted_sources"][0]["head_commit"] != original["repositories"][0]["commit"]
    assert marketplace["plugins"][0]["source"]["ref"] == "master"


def test_missing_shared_reference_is_a_failure_not_layout_success(source):
    (source[0] / source[3]["repositories"][0]["shared_references"][0]).unlink()
    assert report(source, accepted=False)["status"] == "pass"
    result = report(source)
    assert result["status"] == "fail"
    assert any("required file missing" in reason for reason in result["accepted_sources"][0]["findings"])


@pytest.mark.parametrize("flag", ["--assume-unchanged", "--skip-worktree"])
def test_content_read_detects_edits_hidden_from_git_status(source, flag):
    root = source[0]
    relative = source[3]["repositories"][0]["shared_references"][0]
    git(root, "update-index", flag, relative)
    (root / relative).write_text("hidden changed behavior\n", encoding="utf-8")
    assert git(root, "status", "--porcelain", "--", relative) == ""
    result = report(source)
    assert result["status"] == "fail"
    assert any("content differs" in reason for reason in result["accepted_sources"][0]["findings"])


def test_unrelated_dirty_files_are_outside_the_bounded_claim(source):
    (source[0] / "unrelated-notes.txt").write_text("not covered", encoding="utf-8")
    assert report(source)["status"] == "pass"


@pytest.mark.parametrize("driver", ["clean", "process"])
def test_configured_content_filters_are_never_executed(source, driver):
    root, _, _, snapshot = source
    relative = "skills/research-hub/SKILL.md"
    (root / ".gitattributes").write_text(f"{relative} filter=probe\n", encoding="utf-8")
    git(root, "add", ".gitattributes")
    git(root, "commit", "-qm", "Review attributes without executing filters")
    snapshot["repositories"][0].update(commit=git(root, "rev-parse", "HEAD"),
                                        tree=git(root, "rev-parse", "HEAD^{tree}"))
    git(root, "config", f"filter.probe.{driver}", "echo FILTER_RAN > filter-ran.txt")
    (root / relative).write_bytes((root / relative).read_bytes() + b"changed\n")
    assert report(source)["status"] == "fail"
    assert not (root / "filter-ran.txt").exists()


def test_staged_change_fails_even_when_worktree_matches_reviewed_blob(source):
    root = source[0]
    relative = "skills/research-hub/SKILL.md"
    path = root / relative
    reviewed = path.read_bytes()
    path.write_bytes(reviewed + b"staged behavior\n")
    git(root, "add", relative)
    path.write_bytes(reviewed)
    result = report(source)
    assert result["status"] == "fail"
    assert "relevant index paths are dirty or unmerged" in result["accepted_sources"][0]["findings"]


def test_missing_git_metadata_is_unavailable_and_layout_mode_is_compatible(source, tmp_path):
    archive = tmp_path / "archive"
    shutil.copytree(source[0], archive, ignore=shutil.ignore_patterns(".git"))
    assert report(source, accepted=False, root=archive)["verification_scope"] == "source-layout-and-manifest; host loading unverified"
    assert report(source, accepted=False, root=archive)["status"] == "pass"
    result = report(source, root=archive)
    assert result["status"] == "unavailable"
    assert result["accepted_sources"][0]["head_commit"] is None


def test_git_failure_remains_unavailable(source, monkeypatch):
    def unavailable(*args):
        raise checker.GitUnavailable("Git executable unavailable")
    monkeypatch.setattr(checker, "_git", unavailable)
    assert report(source)["status"] == "unavailable"


def test_archive_inside_another_git_repo_does_not_borrow_parent_identity(source):
    nested = source[0] / "nested archive"
    shutil.copytree(source[0], nested, ignore=shutil.ignore_patterns(".git", "nested archive"))
    assert report(source, accepted=False, root=nested)["status"] == "pass"
    assert report(source, root=nested)["status"] == "unavailable"


def test_cli_opt_in_preserves_snapshot_file_and_historical_date(source, tmp_path, monkeypatch, capsys):
    root, catalog, marketplace, snapshot = source
    path = tmp_path / "snapshot.json"
    path.write_text(json.dumps(snapshot), encoding="utf-8")
    original = path.read_bytes()
    monkeypatch.setattr(checker, "SNAPSHOT", path)
    monkeypatch.setattr(checker.consistency, "_load", lambda: (catalog, marketplace))
    monkeypatch.setattr(sys, "argv", ["checker", "--accepted-source", "--source", f"research-hub={root}"])
    assert checker.main() == 0
    result = json.loads(capsys.readouterr().out)
    assert result["snapshot_checked_on"] == "2026-10-03"
    assert path.read_bytes() == original


def test_tree_identity_is_required_even_if_version_and_commit_match(source):
    source[3]["repositories"][0]["tree"] = "f" * 40
    assert report(source)["status"] == "fail"


@pytest.mark.parametrize("path", ["../outside.md", "/absolute.md", "skills\\outside.md", "./file.md"])
def test_shared_reference_paths_cannot_escape_or_expand_scope(source, path):
    source[3]["repositories"][0]["shared_references"] = [path]
    assert report(source)["status"] == "fail"


def test_success_explicitly_does_not_claim_live_or_scientific_acceptance(source):
    scope = report(source)["verification_scope"]
    for term in ("bounded relevant text", "live models", "host loading", "runtime capability", "scientific quality unverified"):
        assert term in scope


def test_recorded_hub_dependency_coverage_does_not_change_snapshot_or_install_ref():
    root = Path(__file__).resolve().parents[1]
    snapshot = json.loads(checker.SNAPSHOT.read_text(encoding="utf-8"))
    hub = snapshot["repositories"][0]
    assert hub["commit"] == "7e046383368d85acb8dfbf0d734ecaaae335cf0a"
    assert snapshot["checked_on"] == "2026-10-19"
    assert hub["tree"] == "cb437e52f23f2448bb9b5a259ed683c2e7788a18"
    expected = {
        "skills/research-hub/references/research-protocol.md",
        "skills/research-hub/references/source-claim-audit.md",
        "skills/gap-to-topic/references/dossier-template.md",
        "skills/gap-to-topic/references/dead-end-history.md",
        "skills/gap-to-topic/references/contribution-typing.md",
        "skills/research-design-helper/references/socratic-segments.md",
        "skills/research-design-helper/references/design_brief_template.md",
        "docs/direction-review-contract.md",
    }
    assert set(hub["shared_references"]) == expected
    marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["plugins"][0]["source"]["ref"] == "master"


def test_matching_newer_manifest_is_not_accepted_source(source):
    """A valid observation/default check cannot upgrade historical acceptance."""
    import hashlib
    from scripts import check_manifest_observations as observations

    root, catalog, marketplace, snapshot = source
    manifest = root / ".claude-plugin/plugin.json"
    raw = json.dumps({"name": "research-workspace", "version": "0.5.6"}).encode()
    manifest.write_bytes(raw)
    git(root, "add", ".claude-plugin/plugin.json")
    git(root, "commit", "-qm", "Synthetic newer manifest")
    marketplace["plugins"][0]["version"] = "0.5.6"
    record = {"repo_url": snapshot["repositories"][0]["repo_url"],
              "plugin": {"name": "research-workspace", "version": "0.5.6"}, "ref": "master",
              "commit": git(root, "rev-parse", "HEAD"), "tree": git(root, "rev-parse", "HEAD^{tree}"),
              "manifest_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
              "manifest_text": raw.decode(), "scope": observations.SCOPE}
    before = copy.deepcopy(snapshot)
    assert observations.validate(marketplace, snapshot, {"schema_version": 1, "observations": [record]}) == []
    assert report(source, accepted=False)["status"] == "pass"
    result = report(source)
    assert result["status"] == "fail"
    assert any("reviewed manifest identity differs" in finding for finding in result["accepted_sources"][0]["findings"])
    assert snapshot == before


def test_historical_checkout_cannot_pass_accepted_check_with_current_version_drift(source):
    """Current-marketplace equality is checked before historical Git identity."""
    source[2]["plugins"][0]["version"] = "0.5.6"
    result = report(source)
    assert result["status"] == "fail"
    assert any("reviewed manifest identity differs" in finding for finding in result["accepted_sources"][0]["findings"])
