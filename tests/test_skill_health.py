from __future__ import annotations

import json
import urllib.error
from pathlib import Path

import yaml

from scripts import check_skill_health as health


def _write_fixture(tmp_path: Path, *, marketplace_version: str = "1.0.0") -> tuple[Path, Path]:
    catalog = {
        "version": 3,
        "families": [{
            "skills": [{
                "name": "demo-skill",
                "repo_url": "https://github.com/WenyuChiou/demo-plugin",
                "skill_url": "https://github.com/WenyuChiou/demo-plugin/blob/main/skills/demo-skill/SKILL.md",
                "lifecycle_status": "active",
                "mutation_class": "local-reversible",
                "human_gates": [],
            }],
        }],
    }
    marketplace = {
        "metadata": {"version": "9.9.9"},
        "plugins": [{
            "name": "demo-plugin",
            "version": marketplace_version,
            "source": {
                "source": "url",
                "url": "https://github.com/WenyuChiou/demo-plugin.git",
                "ref": "main",
            },
        }],
    }
    catalog_path = tmp_path / "skills.yml"
    marketplace_path = tmp_path / "marketplace.json"
    catalog_path.write_text(yaml.safe_dump(catalog), encoding="utf-8")
    marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")
    return catalog_path, marketplace_path


def _install_fixture(monkeypatch, tmp_path: Path, *, source_version: str = "1.0.0") -> None:
    catalog_path, marketplace_path = _write_fixture(tmp_path)
    monkeypatch.setattr(health, "CATALOG", catalog_path)
    monkeypatch.setattr(health, "MARKETPLACE", marketplace_path)
    monkeypatch.setattr(
        health,
        "_request_json",
        lambda _url: {"archived": False, "default_branch": "main"},
    )

    def request_text(url: str) -> str:
        if ".claude-plugin/plugin.json" in url:
            return json.dumps({"name": "demo-plugin", "version": source_version})
        return "---\nname: demo-skill\n---\n# Demo\n"

    monkeypatch.setattr(health, "_request_text", request_text)


def test_frontmatter_name_never_uses_body_name_field():
    text = "---\ndescription: missing identity\n---\nBody fixture:\nname: demo-skill\n"
    assert health._frontmatter_name(text) is None


def test_remote_manifest_version_drift_requires_human_review(monkeypatch, tmp_path):
    _install_fixture(monkeypatch, tmp_path, source_version="1.1.0")
    report = health.run_checks()
    assert report["status"] == "needs_human_review"
    assert any(item["check"] == "plugin_version_drift" for item in report["findings"])


def test_missing_remote_plugin_manifest_is_an_error(monkeypatch, tmp_path):
    _install_fixture(monkeypatch, tmp_path)

    def missing_manifest(url: str) -> str:
        if ".claude-plugin/plugin.json" in url:
            raise urllib.error.HTTPError(url, 404, "missing", {}, None)
        return "---\nname: demo-skill\n---\n"

    monkeypatch.setattr(health, "_request_text", missing_manifest)
    report = health.run_checks()
    finding = next(item for item in report["findings"] if item["check"] == "plugin_manifest_fetch")
    assert finding["severity"] == "error"


def test_healthy_remote_fixture_passes(monkeypatch, tmp_path):
    _install_fixture(monkeypatch, tmp_path)
    assert health.run_checks()["status"] == "pass"


def test_monthly_workflow_preserves_human_loop_on_checker_failure():
    workflow = (health.ROOT / ".github" / "workflows" / "monthly-skill-health.yml").read_text(encoding="utf-8")
    assert workflow.count("if: always()") >= 3
    assert "continue-on-error: true" in workflow
    assert "checker_crash" in workflow
    assert 'issue["title"] == title' in workflow
    assert '"gh", "issue", "close"' in workflow
    assert "skill-health" in workflow
    assert "github.run_id" in workflow
