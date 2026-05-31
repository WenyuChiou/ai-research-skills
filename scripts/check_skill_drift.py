#!/usr/bin/env python3
"""Monthly drift sweep for the ai-research-skills catalog — REPORT-ONLY.

This is the slow-moving counterpart to the per-PR CI checks
(`pytest tests/` + `check_marketplace_consistency.py` +
`check_catalog_schema.py`). Those are deterministic and gate every PR.
This script covers the things a per-PR gate *shouldn't* own — network
reachability (flaky), install-cache staleness (machine-local), and
date-based staleness — and reports them rather than failing a build.

Run it monthly (cron / Task Scheduler) or on demand:

    python scripts/check_skill_drift.py            # report, always exit 0
    python scripts/check_skill_drift.py --strict   # exit 1 if any drift found

It checks, in report mode:
  1. skill_url / repo_url reachability (HEAD request, best-effort).
  2. Installed plugin-cache top version vs the marketplace pin (local
     ~/.claude/plugins/cache; skipped if absent). Surfaces the
     0.2.0-vs-0.3.16 install-cache staleness class.
  3. verified_on staleness in skills.yml (older than --max-age-days).
  4. CHANGELOG heading <-> footer parity, in diff form (the hard gate is
     test_release_hygiene.py; this prints WHICH versions drifted).

Pure standard library + PyYAML.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "skills.yml"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CHANGELOG = ROOT / "CHANGELOG.md"
CACHE_ROOT = Path.home() / ".claude" / "plugins" / "cache" / "ai-research-skills"

_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
_FOOTER = re.compile(r"^\[(\d+\.\d+\.\d+)\]:", re.MULTILINE)


def _load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_skills(catalog):
    for family in catalog["families"]:
        for skill in family["skills"]:
            yield family, skill


def check_links(report):
    catalog = _load_yaml(CATALOG)
    urls = set()
    for _, skill in _iter_skills(catalog):
        for key in ("skill_url", "repo_url"):
            if skill.get(key):
                urls.add(skill[key])
    bad = []
    for url in sorted(urls):
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=15) as resp:
                # urlopen raises HTTPError for 4xx/5xx (handled below); this
                # branch only fires if a server returns a >=400 status without
                # raising — defensive, rarely reached.
                if resp.status >= 400:
                    bad.append(f"{resp.status} {url}")
        except urllib.error.HTTPError as e:
            # 429 / 405 are GitHub throttling/method quirks, not dead links —
            # flag for manual review rather than asserting dead.
            bad.append(f"HTTP {e.code} {url}")
        except Exception as e:  # noqa: BLE001 - report-only, never crash the sweep
            bad.append(f"ERR {type(e).__name__} {url}")
    if bad:
        report.append(f"[links] {len(bad)}/{len(urls)} URLs need manual review:")
        report.extend(f"          {b}" for b in bad)
        return len(bad)
    report.append(f"[links] OK — all {len(urls)} skill_url/repo_url reachable.")
    return 0


def check_cache_versions(report):
    if not CACHE_ROOT.exists():
        report.append("[cache] skipped — no local plugin cache at ~/.claude/plugins/cache.")
        return 0
    pins = {p["name"]: p["version"] for p in _load_json(MARKETPLACE)["plugins"]}
    drift = 0
    for name, pin in pins.items():
        plugin_dir = CACHE_ROOT / name
        if not plugin_dir.exists():
            report.append(f"[cache] {name}: pin {pin} but not installed in cache.")
            continue
        versions = sorted(
            (d.name for d in plugin_dir.iterdir()
             if d.is_dir() and re.fullmatch(r"\d+\.\d+\.\d+", d.name)),
            key=lambda v: tuple(int(x) for x in v.split(".")),
        )
        top = versions[-1] if versions else "(none)"
        if top != pin:
            report.append(f"[cache] {name}: marketplace pins {pin}, cache top is {top} (stale install).")
            drift += 1
    if not drift:
        report.append("[cache] OK — installed cache top versions match marketplace pins.")
    return drift


def check_verified_on(report, max_age_days):
    catalog = _load_yaml(CATALOG)
    today = _dt.date.today()
    stale = []
    for _, skill in _iter_skills(catalog):
        vo = skill.get("verified_on")
        if not vo:
            continue
        try:
            d = _dt.date.fromisoformat(str(vo).strip().strip('"'))
        except ValueError:
            stale.append(f"{skill.get('name')}: unparseable verified_on {vo!r}")
            continue
        age = (today - d).days
        if age > max_age_days:
            stale.append(f"{skill.get('name')}: verified_on {vo} ({age}d ago)")
    if stale:
        report.append(f"[verified_on] {len(stale)} skill(s) older than {max_age_days}d:")
        report.extend(f"          {s}" for s in stale)
        return len(stale)
    report.append(f"[verified_on] OK — all within {max_age_days} days.")
    return 0


def check_changelog(report):
    text = CHANGELOG.read_text(encoding="utf-8")
    headings = set(_HEADING.findall(text))
    footers = set(_FOOTER.findall(text))
    missing = sorted(headings - footers)
    orphan = sorted(footers - headings)
    if missing or orphan:
        if missing:
            report.append(f"[changelog] {len(missing)} headings missing footer links: {missing}")
        if orphan:
            report.append(f"[changelog] {len(orphan)} orphan footer links: {orphan}")
        return len(missing) + len(orphan)
    report.append(f"[changelog] OK — {len(headings)} versions, all with footer links.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Monthly drift sweep for ai-research-skills (report-only).")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any drift is found")
    ap.add_argument("--max-age-days", type=int, default=120, help="verified_on staleness threshold")
    args = ap.parse_args()

    report = []
    drift = 0
    drift += check_links(report)
    drift += check_cache_versions(report)
    drift += check_verified_on(report, args.max_age_days)
    drift += check_changelog(report)

    print("=== ai-research-skills drift sweep ===")
    for line in report:
        print(line)
    print("=" * 38)
    print("RESULT: PASS — no drift." if drift == 0 else f"RESULT: {drift} drift item(s) found.")

    sys.exit(1 if (args.strict and drift) else 0)


if __name__ == "__main__":
    main()
