"""Release-hygiene invariants for the catalog: CHANGELOG completeness, version
freshness, and plugin-version sync.

Until 1.5.30 nothing referenced the CHANGELOG, which is how 20 versions
(1.5.7-1.5.26) accumulated headings with no footer comparison-link (rendering
as dead text on GitHub). Under the catalog's `ref:<branch>` plugin pinning,
the marketplace version string is the only cache-busting signal, so its
freshness is load-bearing.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = ROOT / "CHANGELOG.md"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
_FOOTER = re.compile(r"^\[(\d+\.\d+\.\d+)\]:", re.MULTILINE)

EXPECTED_PLUGINS = [
    "research-workspace",
    "academic-writing-skills",
    "zotero-skills",
    "codex-delegate",
    "gemini-delegate",
]

# Best-effort cross-source check: only fires where the sibling source repo is
# cloned (operator's machine, pre-push); skips cleanly on CI where it is absent.
SIBLING_PLUGIN_JSON = {
    "research-workspace": ROOT.parent / "research-hub" / ".claude-plugin" / "plugin.json",
    "academic-writing-skills": ROOT.parent / "academic-writing-skills" / ".claude-plugin" / "plugin.json",
}


def _changelog():
    return CHANGELOG.read_text(encoding="utf-8")


def _headings():
    return _HEADING.findall(_changelog())


def _marketplace():
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


def test_changelog_heading_footer_parity():
    """Every `## [x.y.z]` heading must have a matching `[x.y.z]:` footer
    compare-link and vice versa — otherwise the version header renders as dead
    text on GitHub. Guards the 20-version footer gap backfilled in 1.5.30."""
    headings = set(_headings())
    footers = set(_FOOTER.findall(_changelog()))
    missing = sorted(headings - footers)
    orphan = sorted(footers - headings)
    assert not missing, f"CHANGELOG headings with no footer link: {missing}"
    assert not orphan, f"CHANGELOG footer links with no heading: {orphan}"


def test_changelog_versions_strictly_decreasing():
    """Version headings must descend strictly (newest first), no dupes."""
    def key(v):
        return tuple(int(x) for x in v.split("."))

    headings = _headings()
    for a, b in zip(headings, headings[1:]):
        assert key(a) > key(b), f"CHANGELOG order/dup violation: {a} not > {b}"


def test_marketplace_version_matches_newest_changelog():
    """metadata.version must equal the newest (top) CHANGELOG version heading."""
    newest = _headings()[0]
    mv = _marketplace()["metadata"]["version"]
    assert mv == newest, (
        f"marketplace metadata.version {mv} != newest CHANGELOG heading {newest}"
    )


def test_plugin_set_and_versions_well_formed():
    plugins = _marketplace()["plugins"]
    assert [p["name"] for p in plugins] == EXPECTED_PLUGINS, "plugin set drifted"
    for p in plugins:
        assert _VERSION.match(p["version"]), (
            f"{p['name']} version {p['version']!r} is not semver"
        )


def test_marketplace_version_matches_source_when_present():
    """If a sibling source repo is cloned, its plugin.json version must match the
    marketplace pin (every plugin uses ref:<branch>, so this string is the only
    cache-buster). Skips cleanly on CI where the sibling is absent — no assertion
    on how many were checked."""
    pins = {p["name"]: p["version"] for p in _marketplace()["plugins"]}
    checked = []
    for name, path in SIBLING_PLUGIN_JSON.items():
        if not path.exists():
            continue
        src = json.loads(path.read_text(encoding="utf-8"))
        assert pins[name] == src["version"], (
            f"marketplace {name} {pins[name]} != source plugin.json {src['version']} "
            f"(at {path})"
        )
        checked.append(name)
    if not checked:
        pytest.skip("no sibling source repos cloned; cross-source version check skipped (expected on CI)")
