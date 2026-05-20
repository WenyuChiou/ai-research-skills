#!/usr/bin/env python3
"""Catalog <-> marketplace consistency check.

Run from the repo root:

    python scripts/check_marketplace_consistency.py

Exits non-zero on any mismatch with a specific reason. Designed to be
called from CI (and from the install-all script if you want a pre-flight
check before publishing).

Checks:

1. The five marketplace plugins line up with the canonical_repo URLs
   in catalog/skills.yml. Order matters because the README and install
   docs reference plugins in this order.
2. The research-workspace plugin description's "<N> research-hub skills"
   count matches the actual number of skills under the research-workspace
   family in skills.yml.
3. Every catalog skill's repo_url maps to one of the marketplace
   plugins' source URLs (modulo a .git suffix).
4. Every catalog skill's skill_url is a /blob/<branch>/ URL pointing
   into a real-looking SKILL.md path.

Pure standard library + PyYAML (already a dev dependency for the
existing test_catalog.py suite).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.yml"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"

EXPECTED_PLUGIN_NAMES = [
    "research-workspace",
    "academic-writing-skills",
    "zotero-skills",
    "codex-delegate",
    "gemini-delegate",
]


def _load() -> tuple[dict, dict]:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        catalog = yaml.safe_load(f)
    with MARKETPLACE_PATH.open(encoding="utf-8") as f:
        marketplace = json.load(f)
    return catalog, marketplace


def _normalize_repo(url: str) -> str:
    """Strip trailing .git and trailing slashes so catalog (no .git) and
    marketplace (with .git) URLs compare equal."""
    return re.sub(r"\.git/?$", "", url.rstrip("/"))


def check_plugin_order(marketplace: dict) -> list[str]:
    actual = [p.get("name") for p in marketplace["plugins"]]
    if actual != EXPECTED_PLUGIN_NAMES:
        return [
            "marketplace plugin order drifted from canonical sequence:\n"
            f"  expected: {EXPECTED_PLUGIN_NAMES}\n"
            f"  actual:   {actual}"
        ]
    return []


def check_research_workspace_skill_count(catalog: dict, marketplace: dict) -> list[str]:
    rw_family = next(
        (f for f in catalog["families"] if f["id"] == "research-workspace"), None
    )
    rw_plugin = next(
        (p for p in marketplace["plugins"] if p["name"] == "research-workspace"), None
    )
    if rw_family is None:
        return ["catalog has no research-workspace family"]
    if rw_plugin is None:
        return ["marketplace has no research-workspace plugin"]

    actual_count = len(rw_family["skills"])
    desc = rw_plugin.get("description", "")
    match = re.search(r"(\d+)\s+research-hub\s+skills", desc)
    if match is None:
        return [
            "research-workspace plugin description does not mention "
            '"<N> research-hub skills" — cannot verify count drift'
        ]
    claimed_count = int(match.group(1))
    if claimed_count != actual_count:
        return [
            f"research-workspace skill count drift: catalog has {actual_count} "
            f"skills, marketplace description claims {claimed_count}.\n"
            "  Fix .claude-plugin/marketplace.json description to match."
        ]
    return []


def check_skill_repo_urls_match_marketplace(catalog: dict, marketplace: dict) -> list[str]:
    plugin_sources = set()
    for plugin in marketplace["plugins"]:
        src = plugin.get("source", {})
        if isinstance(src, dict) and src.get("url"):
            plugin_sources.add(_normalize_repo(src["url"]))
        if plugin.get("homepage"):
            plugin_sources.add(_normalize_repo(plugin["homepage"]))

    errors: list[str] = []
    for family in catalog["families"]:
        for skill in family["skills"]:
            normalized = _normalize_repo(skill["repo_url"])
            if normalized not in plugin_sources:
                errors.append(
                    f"skill {skill['name']!r} repo_url ({skill['repo_url']}) "
                    "does not match any marketplace plugin source/homepage"
                )
    return errors


def check_skill_url_shape(catalog: dict) -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"^https://github\.com/[^/]+/[^/]+/blob/[^/]+/.*SKILL\.md$")
    for family in catalog["families"]:
        for skill in family["skills"]:
            if not pattern.match(skill["skill_url"]):
                errors.append(
                    f"skill {skill['name']!r} skill_url has unexpected shape: "
                    f"{skill['skill_url']}"
                )
    return errors


def main() -> int:
    catalog, marketplace = _load()
    all_errors: list[str] = []
    all_errors += check_plugin_order(marketplace)
    all_errors += check_research_workspace_skill_count(catalog, marketplace)
    all_errors += check_skill_repo_urls_match_marketplace(catalog, marketplace)
    all_errors += check_skill_url_shape(catalog)

    if all_errors:
        print("catalog <-> marketplace consistency check FAILED:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("catalog <-> marketplace consistency check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
