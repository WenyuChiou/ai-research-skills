# Open questions

Surfaced by `research-context-compressor` on 2026-04-25.

1. **Is `.research/` itself in scope for the umbrella repo, or should it
   stay only in downstream research projects?** Writing it here is useful
   as a verification artifact, but readers of the catalog might assume
   the catalog repo *is* a research project. The README does not currently
   mention this distinction.

2. **How should `catalog/skills.yml` versioning evolve?** The YAML now has
   `verified_on` / `verification_status` / `verification_tier` fields,
   but no top-level `schema_version` was bumped. Future re-runs should
   either bump `version: 2 → 3` or keep schema versioning informal.

3. **Should `README.bilingual.md` track the new pipeline structure?** It
   was flagged out of scope in the original restructure plan but will
   drift from the English/Chinese single-language READMEs over time.

4. **No CONTRIBUTING.md yet.** External contributors don't have guidance
   on how to add a skill (which `families:` family, which `verified_on`
   conventions, whether new skills must include verification before
   merging).
