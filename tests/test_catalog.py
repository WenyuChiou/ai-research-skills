import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_has_required_families():
    data = yaml.safe_load((ROOT / "catalog" / "skills.yml").read_text(encoding="utf-8"))
    family_ids = {family["id"] for family in data["families"]}
    assert {
        "research-workspace",
        "academic-writing",
        "zotero-operations",
        "ai-delegation",
    }.issubset(family_ids)


def test_every_family_has_canonical_repo_and_skills():
    data = yaml.safe_load((ROOT / "catalog" / "skills.yml").read_text(encoding="utf-8"))
    for family in data["families"]:
        assert family["canonical_repo"].startswith("https://github.com/WenyuChiou/")
        assert family["default_branch"]
        assert family["install"]["commands"], family["id"]
        assert family["skills"], family["id"]
        for skill in family["skills"]:
            assert skill["name"]
            assert skill["purpose"]
            assert skill["repo_url"].startswith("https://github.com/WenyuChiou/")
            assert "/blob/" in skill["skill_url"]
            assert skill["use_when"], skill["name"]
            assert skill["outputs"], skill["name"]


def test_readme_mentions_core_tool_combinations():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in [
        "Zotero + Obsidian",
        "Obsidian + NotebookLM",
        "Zotero + NotebookLM",
        "research-hub",
        "academic-writing-skills",
        "docs/skill-directory.md",
        "docs/researcher-workflow-checklist.md",
    ]:
        assert phrase in readme


def test_researcher_workflow_checklist_lists_core_research_combinations():
    checklist = (ROOT / "docs" / "researcher-workflow-checklist.md").read_text(encoding="utf-8")
    for phrase in [
        "Zotero + Obsidian",
        "Obsidian + NotebookLM",
        "Zotero + NotebookLM",
        "Zotero + Obsidian + NotebookLM",
        "notebooklm-brief-verifier",
        "literature-triage-matrix",
        "paper-memory-builder",
        "academic-writing-skills",
        "zotero-skills",
    ]:
        assert phrase in checklist


def test_skill_directory_has_every_catalog_skill():
    data = yaml.safe_load((ROOT / "catalog" / "skills.yml").read_text(encoding="utf-8"))
    directory = (ROOT / "docs" / "skill-directory.md").read_text(encoding="utf-8")
    for family in data["families"]:
        assert family["canonical_repo"] in directory
        for skill in family["skills"]:
            assert skill["name"] in directory
            assert skill["skill_url"] in directory


def test_no_model_project_specific_positioning():
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [ROOT / "README.md", ROOT / "README.zh-TW.md", ROOT / "catalog" / "skills.yml"]
    )
    project = "".join(["W", "A", "G", "F"])
    lower_project = "".join(["w", "a", "g", "f"])
    forbidden = r"\b" + project + r"\b|" + lower_project + "-skills|" + "domain" + "-pack"
    assert not re.search(forbidden, text)
