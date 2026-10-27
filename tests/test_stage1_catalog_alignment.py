"""Catalog routing/claim regressions, not execution or scientific-quality tests."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from html.parser import HTMLParser
import json
import re

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
FUTURE_READER = json.loads((ROOT / "test-corpus/integration/native-reader-future-contract.json").read_text(encoding="utf-8"))


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
    ("docs/setup-guide.md", "pipeline.md#1-discover-literature"),
    ("docs/setup-guide.zh-TW.md", "pipeline.zh-TW.md#1-找文獻"),
])
def test_discovery_entrypoints_link_to_stage1_not_a_new_parallel_skill(document, target):
    text = (ROOT / document).read_text(encoding="utf-8")
    assert target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
    assert (ROOT / document).parent.joinpath(target.split("#")[0]).is_file()


@pytest.mark.parametrize("document,clauses,foundation,checkpoint", [
    ("setup-guide.md", [
        "Research Hub itself is optional",
        "no Claude Code, Python or Git installation is required for this native route",
        "stop without Zotero or any storage destination",
        "Native-route users skip Phases A–F below",
    ], "For the optional Claude Code/plugin and Hub CLI route",
     "Native Stage 1 discovery does not require Phase C / D / E"),
    ("setup-guide.zh-TW.md", [
        "Research Hub 本身是可選的",
        "這條原生路線不要求安裝 Claude Code、Python 或 Git",
        "可以不使用 Zotero 或任何儲存目的地，直接停在此處",
        "原生路線使用者跳過下方 Phase A–F",
    ], "只有選用 Claude Code/plugin 與 Hub CLI 路線時",
     "原生 Stage 1 發現文獻不需要 Phase C / D / E"),
])
def test_setup_guides_offer_native_route_before_optional_installation(
        document, clauses, foundation, checkpoint):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    before_install, installation = text.split("## Phase A", 1)
    for clause in clauses:
        assert clause in " ".join(before_install.split())
    assert foundation in " ".join(installation.split("### A1.", 1)[0].split())
    phase_b = text.split("### Phase B checkpoint", 1)[1].split("### B-extra.", 1)[0]
    assert checkpoint in " ".join(phase_b.split())


@pytest.mark.parametrize("document,target,heading", [
    ("setup-guide.md", "../README.md#7-compatibility", "## 7. Compatibility"),
    ("setup-guide.zh-TW.md", "../README.zh-TW.md#7-相容性-compatibility", "## 7. 相容性 (Compatibility)"),
])
def test_setup_cross_host_help_links_to_current_compatibility_section(document, target, heading):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    help_section = text.split("### F7.", 1)[1]
    assert target in re.findall(r"\[[^]]+\]\(([^)]+)\)", help_section)
    assert heading in (ROOT / "docs" / target.split("#")[0]).read_text(encoding="utf-8")


@pytest.mark.parametrize("document,conditional,scope", [
    ("runtime-contract.md", "If `research-hub` is not found", "only the CLI route"),
    ("runtime-contract.zh-TW.md", "如果找不到 `research-hub`", "只代表此環境的 CLI 路徑"),
])
def test_missing_path_cli_does_not_hide_other_hub_interfaces(document, conditional, scope):
    text = (ROOT / "docs" / document).read_text(encoding="utf-8")
    missing_cli_guidance = text.split(conditional, 1)[1].split("```", 1)[0]
    assert scope in missing_cli_guidance
    assert "MCP/REST/native Hub" in missing_cli_guidance


class _ReaderEntry(HTMLParser):
    """Inspect authored fixture text/links only; this is not a browser or renderer."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.count_text, self.count_blocks, self.in_counts = [], [], 0, False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "pre" and attrs.get("id") == "recorded-counts":
            self.count_blocks += 1
            self.in_counts = True

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_counts = False

    def handle_data(self, text):
        if self.in_counts:
            self.count_text.append(text)


def _assert_future_reader_handoff(delivery):
    """Check preservation of supplied synthetic decisions, never decide eligibility."""
    files = delivery["files"]
    for name in delivery["required_attachments"]:
        assert name in files, "missing required attachment"
    sidecar = json.loads(files["assessment-status.sidecar.json"])
    assert sidecar["counts"] == delivery["counts"], "recorded counts changed"
    assert sidecar["assessment_statuses"] == delivery["assessment_statuses"], "assessment identity/status changed"
    for language in delivery["languages_supplied"]:
        name = delivery["entrypoints"][language]
        assert name in files, "missing supplied-language entrypoint"
        entry = _ReaderEntry()
        entry.feed(files[name])
        entry.close()
        assert set(delivery["required_attachments"]) <= set(entry.links), "required attachment not discoverable"
        assert all(target in files for target in entry.links), "unresolved local fixture link"
        assert entry.count_blocks == 1, "recorded counts not visible exactly once"
        assert json.loads("".join(entry.count_text)) == delivery["counts"], "visible recorded counts changed"


def test_future_reader_fixture_preserves_unknown_counts_versions_and_recorded_decisions():
    delivery = FUTURE_READER["delivery"]
    _assert_future_reader_handoff(delivery)
    works, counts = delivery["works"], delivery["counts"]
    assert counts["raw_hits"] is counts["discovered"] is None
    assert counts["raw_version_records"] == len(delivery["versions"]) == 3
    assert counts["cohort_distinct_works"] == len({work["work_id"] for work in works}) == 2
    assert counts["screened"] == sum(work["screened"] for work in works)
    included = [work for work in works if work["included"]]
    assert counts["included"] == len(included)
    assert counts["core"] == sum(work["core"] for work in included)
    assert counts["reading_depth_included"] == dict(Counter(work["reading_level"] for work in included))
    assert included[0]["roles"] == ["core", "nearest"] and included[0]["access"] == "restricted"
    assert delivery["round_scope"] == "general-discovery" and all(work["summary"] is None for work in works)
    assert {(row["work_id"], row["version"]) for row in delivery["assessment_statuses"]} == {
        (work["work_id"], work["version_read"]) for work in works}


@pytest.mark.parametrize("language", ["en", "zh-TW"])
@pytest.mark.parametrize("attachment", ["assessment-status.sidecar.json", "README.md"])
def test_future_reader_requires_attachment_discoverability_not_just_valid_links(language, attachment):
    delivery = deepcopy(FUTURE_READER["delivery"])
    name = delivery["entrypoints"][language]
    delivery["files"][name] = delivery["files"][name].replace('href="' + attachment + '"', 'href="reader.en.html"')
    entry = _ReaderEntry()
    entry.feed(delivery["files"][name])
    assert all(target in delivery["files"] for target in entry.links)
    with pytest.raises(AssertionError, match="not discoverable"):
        _assert_future_reader_handoff(delivery)


@pytest.mark.parametrize("language", ["en", "zh-TW"])
@pytest.mark.parametrize("before,after", [('"discovered":null', '"discovered":0'), ('"included":1', '"included":2'), ('"raw_version_records":3', '"raw_version_records":2')])
def test_future_reader_rejects_changed_visible_counts(language, before, after):
    delivery = deepcopy(FUTURE_READER["delivery"])
    name = delivery["entrypoints"][language]
    delivery["files"][name] = delivery["files"][name].replace(before, after)
    with pytest.raises(AssertionError, match="visible recorded counts changed"):
        _assert_future_reader_handoff(delivery)


@pytest.mark.parametrize("field,value", [("status", "silently-upgraded"), ("version", "wrong-version")])
def test_future_reader_rejects_assessment_status_or_identity_loss(field, value):
    delivery = deepcopy(FUTURE_READER["delivery"])
    sidecar = json.loads(delivery["files"]["assessment-status.sidecar.json"])
    sidecar["assessment_statuses"][0][field] = value
    delivery["files"]["assessment-status.sidecar.json"] = json.dumps(sidecar)
    with pytest.raises(AssertionError, match="assessment identity/status changed"):
        _assert_future_reader_handoff(delivery)


@pytest.mark.parametrize("missing", ["README.md", "assessment-status.sidecar.json", "reader.zh-TW.html"])
def test_future_reader_missing_declared_delivery_files_are_errors(missing):
    delivery = deepcopy(FUTURE_READER["delivery"])
    del delivery["files"][missing]
    with pytest.raises(AssertionError, match="missing"):
        _assert_future_reader_handoff(delivery)


def test_future_reader_acceptance_guidance_keeps_catalog_counts_and_statuses_discoverable():
    text = (ROOT / "docs/accepted-source-verification.md").read_text(encoding="utf-8")
    section = " ".join(text.split("## Future native-reader source and handoff coverage", 1)[1].split("## ", 1)[0].split())
    for relative in FUTURE_READER["candidate_dependencies"]:
        assert relative in section
    for term in ("23", "24", "raw hits", "discovered", "screened", "included", "reading-depth counts", "core count", "each supplied language", "assessment-status.sidecar.json", "README.md", "not current accepted-source verification"):
        assert term in section
