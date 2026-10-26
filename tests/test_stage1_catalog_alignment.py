"""Catalog routing/claim regressions, not execution or scientific-quality tests."""
from pathlib import Path
import re

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def _skill(name):
    catalog = yaml.safe_load((ROOT / "catalog/skills.yml").read_text(encoding="utf-8"))
    return next(skill for family in catalog["families"] for skill in family["skills"]
                if skill["name"] == name)


def test_discovery_catalog_has_evidence_handoff_without_mandatory_storage():
    skill = _skill("research-hub")
    assert any("source versions" in output and "reading levels" in output
               for output in skill["outputs"])
    storage = [output for output in skill["outputs"]
               if any(tool in output for tool in ("Zotero", "Obsidian", "NotebookLM"))]
    assert storage and all("optional" in output.lower() for output in storage)
    assert "host-native" in skill["purpose"]


def test_summary_does_not_upgrade_abstracts_or_unknown_write_outcomes():
    skill = _skill("paper-summarize")
    assert "abstract-only" in skill["purpose"]
    assert "full-text" in skill["purpose"]
    outputs = " ".join(skill["outputs"])
    assert "unknown" in outputs
    assert "atomically" not in outputs
    assert "Historical" in skill["verification_notes"]
    assert "not a distributed transaction" in skill["verification_notes"]


@pytest.mark.parametrize("document", ["pipeline.md", "pipeline.zh-TW.md"])
def test_stage1_routes_to_canonical_shared_contracts(document):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    stage1 = text.split("## 1.", 1)[1].split("## 2.", 1)[0]
    targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", stage1)
    base = "https://github.com/WenyuChiou/research-hub/blob/master/skills/"
    for relative in ("research-hub/SKILL.md",
                     "research-hub/references/research-protocol.md",
                     "research-hub/references/source-claim-audit.md"):
        assert base + relative in targets
    # A summary/metadata path must not silently stand in for actual source reading.
    assert "abstract-only" in stage1
    assert "not-read" in stage1 and "unknown" in stage1
    assert "Codex" in stage1 and "Claude Code" in stage1


@pytest.mark.parametrize("document,target", [
    ("README.md", "docs/pipeline.md#1-discover-literature"),
    ("README.zh-TW.md", "docs/pipeline.zh-TW.md#1-找文獻"),
    ("docs/skill-directory.md", "pipeline.md#1-discover-literature"),
    ("docs/researcher-workflow-checklist.md", "pipeline.md#1-discover-literature"),
])
def test_discovery_entrypoints_link_to_stage1_not_a_new_parallel_skill(document, target):
    text = (ROOT / document).read_text(encoding="utf-8")
    assert target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
    assert (ROOT / document).parent.joinpath(target.split("#")[0]).is_file()


@pytest.mark.parametrize("document,conditional,scope", [
    ("runtime-contract.md", "If `research-hub` is not found", "only the CLI route"),
    ("runtime-contract.zh-TW.md", "如果找不到 `research-hub`", "只代表此環境的 CLI 路徑"),
])
def test_missing_path_cli_does_not_hide_other_hub_interfaces(document, conditional, scope):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    missing_cli_guidance = text.split(conditional, 1)[1].split("```", 1)[0]
    assert scope in missing_cli_guidance
    assert "MCP/REST/native Hub" in missing_cli_guidance
