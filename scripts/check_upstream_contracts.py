#!/usr/bin/env python3
"""Read-only producer/consumer contract check against explicitly supplied clones.

Usage: python scripts/check_upstream_contracts.py --source research-hub=/path/to/repo
Supply all five repositories. This never installs plugins or invokes an AI host.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

import yaml

try:
    from . import check_marketplace_consistency as consistency
    from .check_skill_health import _frontmatter_name
except ImportError:
    import check_marketplace_consistency as consistency
    from check_skill_health import _frontmatter_name


def check_sources(catalog: dict, marketplace: dict, sources: dict[str, Path]) -> dict:
    findings = consistency.check_skill_paths_and_refs(catalog, marketplace)
    checked = 0
    for plugin in marketplace["plugins"]:
        repo_url = consistency._normalize_repo(plugin["source"]["url"])
        slug = repo_url.rsplit("/", 1)[1]
        if slug not in sources:
            findings.append(f"{slug}: source clone was not supplied")
            continue
        root = sources[slug].resolve()
        manifest_path = root / ".claude-plugin/plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for key in ("name", "version"):
                if manifest.get(key) != plugin[key]:
                    findings.append(f"{slug}: manifest {key} {manifest.get(key)!r} differs from catalog {plugin[key]!r}")
        except (OSError, ValueError) as exc:
            findings.append(f"{slug}: manifest unreadable ({type(exc).__name__})")
            continue
        for family in catalog["families"]:
            for skill in family["skills"]:
                if consistency._normalize_repo(skill["repo_url"]) != repo_url:
                    continue
                path = (root / skill["directory"] / "SKILL.md").resolve()
                if not path.is_relative_to(root):
                    findings.append(f"{skill['name']}: skill path escapes source root")
                    continue
                try:
                    name = _frontmatter_name(path.read_text(encoding="utf-8"))
                    if name != skill["name"]:
                        findings.append(f"{skill['name']}: frontmatter identity is {name!r}")
                    checked += 1
                except OSError as exc:
                    findings.append(f"{skill['name']}: SKILL.md unreadable ({type(exc).__name__})")
    return {"status": "pass" if not findings else "fail", "skills_checked": checked,
            "verification_scope": "source-layout-and-manifest; host loading unverified", "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", default=[], metavar="REPO=PATH")
    args = parser.parse_args()
    sources = {}
    for entry in args.source:
        slug, sep, local = entry.partition("=")
        if not sep or not slug or not local or slug in sources:
            parser.error("each --source must be a unique REPO=PATH")
        sources[slug] = Path(local)
    catalog, marketplace = consistency._load()
    expected = {consistency._normalize_repo(p["source"]["url"]).rsplit("/", 1)[1] for p in marketplace["plugins"]}
    if sources.keys() - expected:
        parser.error("unknown source repositories: " + ", ".join(sorted(sources.keys() - expected)))
    report = check_sources(catalog, marketplace, sources)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
