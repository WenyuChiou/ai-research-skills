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
    """The persona table is the README's primary entry point. After the UX
    trim it has 3 goal-based rows + a librarian/RA/advisor callout."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for persona_phrase in [
        "Find & compare literature",
        "Write or revise a paper",
        "Manage a research project",
        "Helping others adopt AI for research",
    ]:
        assert persona_phrase in readme, f"persona row missing: {persona_phrase}"


def test_zh_readme_mirrors_persona_table():
    """The zh-TW README must mirror the 3 goal-based persona rows + librarian callout."""
    zh = (ROOT / "README.zh-TW.md").read_text(encoding="utf-8")
    for phrase in [
        "10 分鐘上手",
        "找到你的起點",
        "找文獻、比較文獻",
        "寫論文 / 改稿",
        "管理研究專案",
        "協助別人用 AI 做研究",
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


def test_canonical_install_command_consistent_across_sources_of_truth():
    """The catalog standardized on `research-hub setup --persona <X>` as the
    fresh-user onboarding command. README, install docs, and the
    machine-readable YAML must all lead with `setup`, not bare `install`."""
    docs_with_install = [
        ROOT / "README.md",
        ROOT / "README.zh-TW.md",
        ROOT / "docs" / "install.md",
        ROOT / "docs" / "skill-directory.md",
        ROOT / "docs" / "researcher-workflow-checklist.md",
        ROOT / "catalog" / "skills.yml",
    ]
    for doc in docs_with_install:
        text = doc.read_text(encoding="utf-8")
        assert "research-hub setup --persona" in text, (
            f"{doc.relative_to(ROOT)}: missing canonical `research-hub setup --persona` command"
        )


def test_verification_counts_match_catalog():
    """The README + verification.md claim 13 skills with a specific T1/T2
    split. The machine-readable YAML must agree on the count."""
    data = yaml.safe_load((ROOT / "catalog" / "skills.yml").read_text(encoding="utf-8"))
    total_skills = sum(len(family["skills"]) for family in data["families"])
    assert total_skills == 13, f"catalog has {total_skills} skills; README claims 13"

    statuses = [s.get("verification_status") for f in data["families"] for s in f["skills"]]
    pass_count = statuses.count("pass")
    caveat_count = statuses.count("caveat")
    fail_count = statuses.count("fail")
    not_yet_count = statuses.count("not_yet")

    # README hero claims: 11 T1 + 2 T2 = 13 total; 0 fail; 0 not_yet
    assert pass_count == 12, f"expected 12 pass, got {pass_count}"
    assert caveat_count == 1, f"expected 1 caveat (codex-delegate gpt-5.5), got {caveat_count}"
    assert fail_count == 0, f"expected 0 fail, got {fail_count}"
    assert not_yet_count == 0, f"expected 0 not_yet, got {not_yet_count}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for claim in ["13 verified", "11 of 13", "T1", "T2"]:
        assert claim in readme, f"README missing verification claim: {claim}"
