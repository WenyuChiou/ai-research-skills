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
        "researcher-facing",
        "graduate students",
        "research support staff",
        "Zotero",
        "Obsidian",
        "NotebookLM",
        "research-hub",
        "academic-writing-skills",
        "docs/install.md",
        "docs/verification.md",
    ]:
        assert phrase in readme


def test_readme_has_persona_starting_points():
    """The persona table is the redesigned README's primary entry point.
    Each of the 5 personas must be addressed by name."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for persona_phrase in [
        "First-year PhD",
        "Writing a paper",
        "Running experiments",
        "Cleaning a Zotero library",
        "Helping others adopt AI for research",
    ]:
        assert persona_phrase in readme, f"persona row missing: {persona_phrase}"


def test_zh_readme_mirrors_persona_table():
    """The zh-TW README must address all 5 personas with translated headings."""
    zh = (ROOT / "README.zh-TW.md").read_text(encoding="utf-8")
    for phrase in [
        "5 分鐘上手",
        "找到你的起點",
        "正在寫論文",
        "跑實驗 / 建模型",
        "整理 Zotero library",
        "Cross-cutting Tools",
    ]:
        assert phrase in zh, f"zh-TW phrase missing: {phrase}"


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
