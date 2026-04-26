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
    """README must reference the core tools and audience the catalog
    actually addresses — Zotero, Obsidian, NotebookLM as the data
    surface; graduate students and research support staff as the
    audience; the two main upstream skills (research-hub,
    academic-writing-skills); and the two long-form docs
    (install.md, verification.md). Marketing language like
    "researcher-facing" is intentionally not asserted — it was trimmed
    in the UX pass for being overclaim-y."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for phrase in [
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
        "找到你的起點",
        "找文獻、比較文獻",
        "寫論文 / 改稿",
        "管理研究專案",
        "協助別人用 AI 做研究",
        # Pipeline + cross-cutting tools moved to docs/pipeline.zh-TW.md
        # to keep the README focused on install + how-to-use; the
        # README must still link out to the moved doc.
        "docs/pipeline.zh-TW.md",
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


def test_claude_plugin_marketplace_is_well_formed():
    """The .claude-plugin/marketplace.json file makes the catalog a Claude
    Code plugin marketplace. Guard its basic structure so future edits
    don't silently break `/plugin marketplace add`.

    Ships 5 plugins: research-workspace (9 skills auto-discovered from
    research-hub's skills/ subdir) + 4 standalone single-skill plugins
    (academic-writing-skills, zotero-skills, codex-delegate,
    gemini-delegate) whose source repos declare {"skills": ["./"]} in
    their .claude-plugin/plugin.json so the root SKILL.md is picked up.
    See .claude-plugin/README.md for the full story."""
    import json
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    assert marketplace_path.exists(), "missing .claude-plugin/marketplace.json"

    with marketplace_path.open(encoding="utf-8") as f:
        data = json.load(f)

    # Top-level required fields
    assert data.get("name") == "ai-research-skills"
    assert "owner" in data and data["owner"].get("name")
    assert "metadata" in data
    assert "plugins" in data and isinstance(data["plugins"], list)
    plugin_names = [plugin.get("name") for plugin in data["plugins"]]
    assert plugin_names == [
        "research-workspace",
        "academic-writing-skills",
        "zotero-skills",
        "codex-delegate",
        "gemini-delegate",
    ]

    # Per-plugin required fields
    for plugin in data["plugins"]:
        assert plugin.get("name"), f"plugin missing name: {plugin}"
        assert plugin.get("description"), f"plugin {plugin['name']} missing description"
        assert plugin.get("category"), f"plugin {plugin['name']} missing category"
        assert plugin.get("homepage"), f"plugin {plugin['name']} missing homepage"
        assert "source" in plugin, f"plugin {plugin['name']} missing source"

        src = plugin["source"]
        # source can be a string (local path) or an object (github / url / git-subdir)
        if isinstance(src, dict):
            assert src.get("source") in {"github", "url", "git-subdir"}, (
                f"plugin {plugin['name']} has unknown source type: {src.get('source')}"
            )
            if src["source"] == "github":
                assert src.get("repo"), f"plugin {plugin['name']} github source missing repo"
            elif src["source"] in {"url", "git-subdir"}:
                assert src.get("url"), f"plugin {plugin['name']} {src['source']} missing url"
        else:
            assert isinstance(src, str) and src, (
                f"plugin {plugin['name']} string source must be non-empty"
            )


def test_canonical_install_command_consistent_across_sources_of_truth():
    """The catalog standardized on `research-hub setup` (interactive
    onboarding) as the fresh-user command. README, install docs, and
    the machine-readable YAML must all lead with `setup`, not bare
    `install`. The README dropped `--persona <X>` because it was a
    CLI-internal flag the README shouldn't be teaching; the interactive
    setup asks the same questions without forcing the user to learn the
    persona names. Per-doc files (docs/install.md, catalog/skills.yml,
    etc.) may still reference `--persona` for completeness."""
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
        assert "research-hub setup" in text, (
            f"{doc.relative_to(ROOT)}: missing canonical `research-hub setup` command"
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

    # YAML-side verification counts: 12 pass + 1 caveat + 0 fail + 0 not_yet = 13
    assert pass_count == 12, f"expected 12 pass, got {pass_count}"
    assert caveat_count == 1, f"expected 1 caveat (codex-delegate gpt-5.5), got {caveat_count}"
    assert fail_count == 0, f"expected 0 fail, got {fail_count}"
    assert not_yet_count == 0, f"expected 0 not_yet, got {not_yet_count}"

    # README intentionally does NOT advertise verification counts in its
    # body (avoids self-aggrandizing tone). docs/verification.md carries
    # the per-skill detail; this test only guards the YAML-side counts.
