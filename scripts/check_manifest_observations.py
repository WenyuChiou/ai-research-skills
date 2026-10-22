#!/usr/bin/env python3
"""Offline cache-version evidence, deliberately NOT accepted-source verification.

Recorded object identities are observation provenance, not a live remote check.
The manifest bytes are bound to their Git blob ID; this does not certify skill
content, commit ancestry, host loading, or a published release.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "test-corpus/integration/manifest-observations.json"
SNAPSHOT = ROOT / "test-corpus/integration/upstream-contracts.json"
MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
FIELDS = {"repo_url", "plugin", "ref", "commit", "tree", "manifest_blob", "manifest_text", "scope"}
SCOPE = "manifest-only; not accepted-source or published-release verification"


def validate(marketplace: dict, snapshot: dict, observations: dict) -> list[str]:
    """Require exactly one well-formed observation for each changed version.

    No filesystem, sibling-clone, network or subprocess operations are used.
    Unchanged accepted versions need no observation. Extra/stale observations
    fail rather than becoming an unbounded allowlist.
    """
    errors = []
    if not isinstance(observations, dict) or set(observations) != {"schema_version", "observations"}:
        return ["manifest observations: invalid document fields"]
    if type(observations["schema_version"]) is not int or observations["schema_version"] != 1 or not isinstance(observations["observations"], list):
        return ["manifest observations: invalid schema version or record list"]
    records = observations["observations"]
    accepted = {r["repo_url"]: r for r in snapshot["repositories"]}
    expected = {}
    for plugin in marketplace["plugins"]:
        repo = plugin["source"]["url"].removesuffix(".git")
        baseline = accepted.get(repo)
        if baseline is None:
            errors.append(f"{repo}: missing accepted repository identity")
            continue
        if plugin["name"] != baseline["plugin"]["name"] or plugin["source"]["ref"] != baseline["default_branch"]:
            errors.append(f"{repo}: source name/ref differs from accepted identity")
        if plugin["version"] != baseline["plugin"]["version"]:
            expected[repo] = plugin
    counts = {}
    for index, record in enumerate(records):
        label = f"observation[{index}]"
        if not isinstance(record, dict) or set(record) != FIELDS:
            errors.append(f"{label}: missing or unexpected fields")
            continue
        repo = record["repo_url"]
        if not isinstance(repo, str) or repo not in expected:
            errors.append(f"{label}: unexpected repository or unchanged accepted version")
            continue
        counts[repo] = counts.get(repo, 0) + 1
        plugin = expected[repo]
        if record["plugin"] != {k: plugin[k] for k in ("name", "version")}:
            errors.append(f"{label}: plugin name/version mismatch")
        if record["ref"] != plugin["source"]["ref"]:
            errors.append(f"{label}: source ref mismatch")
        if record["scope"] != SCOPE:
            errors.append(f"{label}: invalid observation scope")
        for key in ("commit", "tree", "manifest_blob"):
            if not isinstance(record[key], str) or not re.fullmatch(r"[0-9a-f]{40}", record[key]) or record[key] == "0" * 40:
                errors.append(f"{label}: invalid {key} object identity")
        try:
            raw = record["manifest_text"].encode("utf-8")
            manifest = json.loads(raw)
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
            if blob != record["manifest_blob"]:
                errors.append(f"{label}: manifest bytes do not match Git blob")
            if not isinstance(manifest, dict) or {k: manifest.get(k) for k in ("name", "version")} != record["plugin"]:
                errors.append(f"{label}: recorded manifest name/version mismatch")
        except (AttributeError, UnicodeError, ValueError, TypeError):
            errors.append(f"{label}: invalid manifest text/JSON")
    for repo in expected:
        if counts.get(repo, 0) != 1:
            errors.append(f"{repo}: changed version requires exactly one observation (found {counts.get(repo, 0)})")
    return errors


def main() -> int:
    try:
        errors = validate(*[json.loads(path.read_text(encoding="utf-8")) for path in (MARKETPLACE, SNAPSHOT, OBSERVATIONS)])
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"manifest observation check FAILED: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("manifest observation check FAILED:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("manifest observation check OK (manifest-only; accepted-source unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
