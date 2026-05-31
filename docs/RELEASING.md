# Releasing the ai-research-skills catalog

This catalog is a **registry + docs** repo, not a packaged artifact: it
ships `marketplace.json`, `catalog/skills.yml`, the README/docs, the
`docs/example-*` worked artifacts, and the test suite. A "release" is a
`metadata.version` bump plus a CHANGELOG entry. There is no PyPI/npm
publish and no tag-based gate — the quality gate is **CI green on the
release commit**, which the tests below enforce mechanically.

## Release flow

1. **Land the change.** Bump `.claude-plugin/marketplace.json`
   `metadata.version` (semver). Add a `## [x.y.z] - YYYY-MM-DD` entry to
   `CHANGELOG.md` **and its `[x.y.z]:` compare-link in the footer** — the
   footer link is not optional (see the gate below).
2. **Run the gate locally:**
   ```bash
   python -m pytest tests/ -q
   python scripts/check_marketplace_consistency.py
   python scripts/check_catalog_schema.py
   ```
   On Windows, prefix with `PYTHONUTF8=1` (the marketplace JSON contains
   an em-dash that the cp950 default codec rejects).
3. **PR → CI green → squash-merge.** The same three commands run on every
   PR via `.github/workflows/test.yml`.

## The gate (what keeps a release honest)

`tests/test_release_hygiene.py` asserts, on every PR:

- **CHANGELOG completeness** — every `## [x.y.z]` heading has a matching
  `[x.y.z]:` footer compare-link (and vice versa). A release that adds a
  heading without a footer link **fails CI**. This is why step 1 says the
  footer link is mandatory; it also backfilled the 1.5.7–1.5.26 gap that
  had accumulated silently before the test existed.
- **Version freshness** — `marketplace.json` `metadata.version` equals
  the newest CHANGELOG heading. Bumping one without the other fails CI.
- **Plugin set + semver shape** — the five plugins and their version
  strings are well-formed.
- **Cross-source version sync (best-effort)** — when a sibling source
  repo is cloned, its `.claude-plugin/plugin.json` version must match the
  marketplace pin (the only cache-buster under `ref:<branch>` pinning).
  Skips cleanly on CI where siblings are absent.

`tests/test_example_artifacts.py` asserts the shipped `docs/example-*`
artifacts parse and have no dangling cross-references (the regression net
for the 1.5.29 dangling `linked_claim`).

## Plugin version bumps

The five plugins are pinned by `ref:<branch>` (no tag), so the
`marketplace.json` plugin `version` string is the **only** signal that
busts a stale install cache. When a source plugin releases a new version,
bump its `version` in `marketplace.json` in the same release. The
cross-source test above catches a forgotten bump locally; the monthly
drift sweep catches it across machines.

## Monthly drift sweep (report-only)

`scripts/check_skill_drift.py` is the slow-moving counterpart to the
per-PR gate — it owns the checks a build shouldn't (network reachability,
install-cache staleness, date-based staleness):

```bash
python scripts/check_skill_drift.py              # report, exit 0
python scripts/check_skill_drift.py --strict     # exit 1 on any drift
```

It reports: `skill_url`/`repo_url` reachability, installed plugin-cache
top version vs the marketplace pin (surfaces the 0.2.0-vs-0.3.16
install-cache staleness class), `verified_on` staleness, and a
CHANGELOG heading↔footer diff. Run it via cron / Task Scheduler monthly,
or whenever a release feels overdue. It never fails a build by default.

## Files

- `.claude-plugin/marketplace.json` — the registry (plugin pins + `metadata.version`).
- `catalog/skills.yml` — machine-readable skill registry (consumed by the consistency scripts).
- `tests/test_release_hygiene.py` — the release gate (CHANGELOG + version sync).
- `tests/test_example_artifacts.py` — the shipped-artifact integrity net.
- `scripts/check_marketplace_consistency.py` — catalog↔marketplace structural consistency (per-PR).
- `scripts/check_catalog_schema.py` — `skills.yml` schema validation (per-PR).
- `scripts/check_skill_drift.py` — monthly report-only drift sweep (network + cache + staleness).
