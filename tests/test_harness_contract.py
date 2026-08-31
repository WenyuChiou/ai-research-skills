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
        ("docs/round2-dogfood-benchmark.md", "docs/round2-dogfood-benchmark.zh-TW.md"),
    ]
    required = ["research-hub", "agent-collab-harness", "ResearchEvidencePacket", "Zotero", "Obsidian", "NotebookLM"]
    for en_path, zh_path in pairs:
        en = (ROOT / en_path).read_text(encoding="utf-8")
        zh = (ROOT / zh_path).read_text(encoding="utf-8")
        if "for-agent" in en_path:
            pair_required = required
        elif "skill-lifecycle" in en_path:
            pair_required = ["gemini-delegate", "codex-delegate", "antigravity-delegate"]
        else:
            pair_required = ["research-hub", "NotebookLM", "reconcile_required"]
        for term in pair_required:
            assert term in en and term in zh, term
        assert en.count("\n## ") == zh.count("\n## ")
        assert en.count("\n|---") == zh.count("\n|---")
        assert not any(term in zh for term in ("软件", "网络", "数据"))
    en_builder = (ROOT / "docs/for-agent-harness-builders.md").read_text(encoding="utf-8")
    zh_builder = (ROOT / "docs/for-agent-harness-builders.zh-TW.md").read_text(encoding="utf-8")
    for term in ("continue", "checkpoint", "stop"):
        assert term in en_builder and term in zh_builder


def test_round2_report_preserves_failure_evidence_and_measured_counts():
    paths = (
        ROOT / "docs/round2-dogfood-benchmark.md",
        ROOT / "docs/round2-dogfood-benchmark.zh-TW.md",
    )
    required = (
        "3,348", "12/12 PASS", "3/3", "0/3", "1/1",
        "HTTP 429", "degraded/SKIP", "reconcile_required",
        "USD 0", "research-hub/pull/130",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for term in required:
            assert term in text, f"{path.name}: missing {term}"
        assert "not a general ranking" in text or "不是通用排名" in text
        assert "no-write action" in text
        assert "Duplicate no-write retries rejected" in text or "duplicate no-write retry" in text
        assert "Duplicate external actions prevented" not in text
        assert "避免的 duplicate external action" not in text


def test_readme_first_screen_routes_why_what_and_how_in_both_locales():
    pairs = (
        ROOT / "README.md",
        ROOT / "README.zh-TW.md",
    )
    required = (
        "Why", "What", "How", "pipeline-overview", "harness-architecture",
        "hitl-state-machine", "17", "8", "Zotero", "Obsidian", "NotebookLM",
        "claude plugin install research-workspace@ai-research-skills",
    )
    for path in pairs:
        text = path.read_text(encoding="utf-8")
        first_screen = text[:7000]
        for term in required:
            assert term in first_screen, f"{path.name}: first-screen route missing {term}"
        assert first_screen.index("pipeline-overview") < first_screen.index("## Contents") if path.name == "README.md" else first_screen.index("pipeline-overview") < first_screen.index("## 目錄")


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


def test_image2_assets_match_reviewed_hash_manifest():
    manifest = ROOT / "docs/img/image-2-assets.sha256"
    entries = manifest.read_text(encoding="utf-8").splitlines()
    assert len(entries) == 6
    expected_paths = {
        "docs/img/pipeline-overview.png",
        "docs/img/pipeline-overview.zh-TW.png",
        "docs/img/harness-architecture.png",
        "docs/img/harness-architecture.zh-TW.png",
        "docs/img/hitl-state-machine.png",
        "docs/img/hitl-state-machine.zh-TW.png",
    }
    manifest_paths = [line.split(maxsplit=1)[1] for line in entries]
    assert len(set(manifest_paths)) == 6
    assert set(manifest_paths) == expected_paths
    for line in entries:
        expected, relative = line.split(maxsplit=1)
        asset = (ROOT / relative).resolve()
        assert asset.is_relative_to(ROOT.resolve())
        assert asset.exists() and asset.suffix == ".png"
        actual = hashlib.sha256(asset.read_bytes()).hexdigest()
        assert actual == expected, f"visually review Image 2.0 asset before accepting {relative}"
