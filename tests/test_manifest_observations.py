"""Synthetic observation fixtures are not evidence for real upstream commits."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from scripts import check_manifest_observations as checker

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def example():
    repo = "https://github.com/WenyuChiou/zotero-skills"
    old = {"name": "zotero-skills", "version": "0.3.1"}
    new = {"name": "zotero-skills", "version": "0.4.0"}
    marketplace = {"plugins": [{**new, "source": {"url": repo + ".git", "ref": "master"}}]}
    snapshot = {"repositories": [{"repo_url": repo, "plugin": old, "default_branch": "master"}]}
    raw = json.dumps(new).encode()
    record = {"repo_url": repo, "plugin": new, "ref": "master", "commit": "a" * 40,
              "tree": "b" * 40, "manifest_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(),
              "manifest_text": raw.decode(), "scope": checker.SCOPE}
    return marketplace, snapshot, {"schema_version": 1, "observations": [record]}


def test_changed_version_matching_observation_passes(example):
    assert checker.validate(*example) == []


def test_accepted_version_needs_no_observation(example):
    market, snapshot, observed = example
    market["plugins"][0]["version"] = "0.3.1"
    observed["observations"] = []
    assert checker.validate(*example) == []


def test_changed_version_missing_observation_fails(example):
    example[2]["observations"] = []
    assert "exactly one observation" in " ".join(checker.validate(*example))


@pytest.mark.parametrize("field,value", [
    ("repo_url", "https://github.com/other/zotero-skills"),
    ("plugin", {"name": "other", "version": "0.4.0"}),
    ("plugin", {"name": "zotero-skills", "version": "0.3.1"}),
    ("ref", "main"), ("commit", "short"), ("tree", "not-a-tree"),
    ("manifest_blob", "not-a-blob"), ("manifest_blob", "a" * 40),
    ("commit", "0" * 40), ("tree", None), ("manifest_text", "not-json"),
    ("manifest_text", None), ("scope", "accepted-source"),
])
def test_wrong_or_malformed_record_fails(example, field, value):
    example[2]["observations"][0][field] = value
    assert checker.validate(*example)


def test_duplicate_observations_fail(example):
    example[2]["observations"] *= 2
    assert "found 2" in " ".join(checker.validate(*example))


def test_missing_record_field_fails(example):
    del example[2]["observations"][0]["tree"]
    assert checker.validate(*example)


def test_stale_observation_for_accepted_version_fails(example):
    example[0]["plugins"][0]["version"] = "0.3.1"
    assert checker.validate(*example)


def test_manifest_bytes_cannot_claim_another_version(example):
    record = example[2]["observations"][0]
    raw = b'{"name":"zotero-skills","version":"0.9.9"}'
    record["manifest_text"] = raw.decode()
    record["manifest_blob"] = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert "manifest name/version mismatch" in " ".join(checker.validate(*example))


def test_processing_does_not_modify_accepted_evidence(example):
    paths = [checker.SNAPSHOT, ROOT / "docs/system-assessment.md",
             ROOT / "docs/system-assessment.zh-TW.md", ROOT / "catalog/skills.yml"]
    before = {p: p.read_bytes() for p in paths}
    original = copy.deepcopy(example)
    assert checker.validate(*example) == []
    assert example == original
    assert before == {p: p.read_bytes() for p in paths}


def test_absent_sibling_clones_cannot_disable_observation_check(example, monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda _: False)
    example[2]["observations"] = []
    assert checker.validate(*example)


@pytest.mark.parametrize("document", [None, [], {}, {"schema_version": True, "observations": []},
                                       {"schema_version": 1, "observations": [None]}])
def test_malformed_document_or_record_fails_cleanly(example, document):
    assert checker.validate(example[0], example[1], document)
