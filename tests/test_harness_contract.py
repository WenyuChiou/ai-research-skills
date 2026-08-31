from pathlib import Path
import hashlib
import json
import re

import yaml

from scripts.run_harness_replay import run_replay


ROOT = Path(__file__).resolve().parents[1]


def _mermaid_edges(text: str) -> list[tuple[str, str]]:
    edges = []
    for raw in text.splitlines():
        if "-->" not in raw and "-." not in raw:
            continue
        line = re.sub(r"-\..*?\.->", "-->", raw)
        line = re.sub(r"\|[^|]*\|", "", line)
        parts = [part.strip() for part in line.split("-->")]
        ids = []
        for part in parts:
            match = re.search(r"\b([A-Z][A-Z0-9]*)\s*(?:\[|\{|\()", part)
            if not match:
                match = re.search(r"\b([A-Z][A-Z0-9]*)\b", part)
            ids.append(match.group(1) if match else None)
        edges.extend((left, right) for left, right in zip(ids, ids[1:]) if left and right)
    return edges


def test_behavior_corpus_covers_required_failure_modes():
    data = yaml.safe_load((ROOT / "test-corpus/harness-behavior/cases.yml").read_text(encoding="utf-8"))
    ids = {case["id"] for case in data["cases"]}
    assert ids == {
        "doi-metadata-conflict", "unsupported-citation", "contradictory-papers",
        "paywall-api-unavailable", "prompt-injection-paper", "human-decline",
        "human-revise", "cancel-resume", "crash-after-external-write",
        "duplicate-retry", "policy-budget-exhaustion", "notebooklm-unsupported-claim",
    }
    assert all(case["kind"] and case["input"] and case["expected"] for case in data["cases"])
    results = run_replay(ROOT / "test-corpus/harness-behavior/cases.yml")
    assert len(results) == 12
    assert all(result["passed"] for result in results)
    cancelled = next(result for result in results if result["id"] == "cancel-resume")
    assert cancelled["actual"] == {"status": "terminal", "reason": "cancelled"}


def test_builder_docs_and_diagrams_have_bilingual_parity():
    pairs = [
        ("docs/for-agent-harness-builders.md", "docs/for-agent-harness-builders.zh-TW.md"),
        ("docs/skill-lifecycle.md", "docs/skill-lifecycle.zh-TW.md"),
    ]
    required = ["research-hub", "agent-collab-harness", "ResearchEvidencePacket", "Zotero", "Obsidian", "NotebookLM"]
    for en_path, zh_path in pairs:
        en = (ROOT / en_path).read_text(encoding="utf-8")
        zh = (ROOT / zh_path).read_text(encoding="utf-8")
        for term in required if "for-agent" in en_path else ["gemini-delegate", "codex-delegate", "antigravity-delegate"]:
            assert term in en and term in zh, term
        assert en.count("\n## ") == zh.count("\n## ")
        assert en.count("\n|---") == zh.count("\n|---")
        assert not any(term in zh for term in ("软件", "网络", "数据"))
    en_builder = (ROOT / "docs/for-agent-harness-builders.md").read_text(encoding="utf-8")
    zh_builder = (ROOT / "docs/for-agent-harness-builders.zh-TW.md").read_text(encoding="utf-8")
    for term in ("continue", "checkpoint", "stop"):
        assert term in en_builder and term in zh_builder


def test_builder_docs_resolve_relative_markdown_links():
    for name in ("for-agent-harness-builders.md", "for-agent-harness-builders.zh-TW.md"):
        path = ROOT / "docs" / name
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (path.parent / target).resolve().exists(), f"broken local link: {name} -> {target}"


def test_optional_harness_does_not_change_core_skill_count():
    data = yaml.safe_load((ROOT / "catalog/skills.yml").read_text(encoding="utf-8"))
    assert data["version"] == 4
    assert len(data["extensions"]) == 1
    assert data["extensions"][0]["required"] is False
    assert sum(len(family["skills"]) for family in data["families"]) == 17


def test_release_version_matches_bilingual_glossaries():
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    version = marketplace["metadata"]["version"]
    assert f"catalog {version} mix" in (ROOT / "docs/glossary.md").read_text(encoding="utf-8")
    assert f"catalog {version} 比例" in (ROOT / "docs/glossary.zh-TW.md").read_text(encoding="utf-8")


def test_bilingual_mermaid_topology_and_exports_match():
    for stem in ("harness-architecture", "hitl-state-machine"):
        en = (ROOT / f"docs/img/{stem}.mmd").read_text(encoding="utf-8")
        zh = (ROOT / f"docs/img/{stem}.zh-TW.mmd").read_text(encoding="utf-8")
        assert _mermaid_edges(en) == _mermaid_edges(zh)
        for suffix in ("svg", "png"):
            for locale in ("", ".zh-TW"):
                export = ROOT / f"docs/img/{stem}{locale}.{suffix}"
                assert export.exists() and export.stat().st_size > 1000


def test_mermaid_sources_match_reviewed_export_hash_manifest():
    for line in (ROOT / "docs/img/diagram-sources.sha256").read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        canonical = (ROOT / relative).read_text(encoding="utf-8").encode("utf-8")
        actual = hashlib.sha256(canonical).hexdigest()
        assert actual == expected, f"regenerate and visually review exports for {relative}"
