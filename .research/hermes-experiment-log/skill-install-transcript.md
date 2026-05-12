# Skill Install Transcript

**Skill under test**: `literature-triage-matrix` from `WenyuChiou/research-hub:skills/literature-triage-matrix/SKILL.md`

**Why this skill**: Phase 2 audit identified it as the lowest-cost first cross-platform skill. 127 lines, zero Claude-Code-only patterns, zero MCP dependencies. Pure prompt-engineering skill with only `name` + `description` in the frontmatter — the strict agentskills.io spec minimum.

## Install command

```bash
hermes skills install \
  --category research \
  --yes \
  https://raw.githubusercontent.com/WenyuChiou/research-hub/master/skills/literature-triage-matrix/SKILL.md
```

Note: default branch is `master`, not `main`. First attempt with `/main/` failed with HTTP 404 and Hermes' fetcher reported "Could not fetch ... from any source". Switching to `/master/` worked.

## Output

```
Fetching: https://raw.githubusercontent.com/WenyuChiou/research-hub/master/skills/literature-triage-matrix/SKILL.md
Quarantined to .hub/quarantine/literature-triage-matrix
Running security scan...
Scan: literature-triage-matrix (.../community)  Verdict: SAFE
Decision: ALLOWED — Allowed (community source, safe verdict)
Installed: research/literature-triage-matrix
Files: SKILL.md
```

Total time: ~3 seconds. No prompts.

## What Hermes did with our SKILL.md (in order)

1. **Fetched** from public GitHub raw URL.
2. **Quarantined** to `~/.hermes/skills/.hub/quarantine/literature-triage-matrix/` (pre-scan staging).
3. **Security-scanned** — content vs. a community reputation source. **Verdict: SAFE**.
4. **Decision: ALLOWED** — moved out of quarantine into `~/.hermes/skills/research/literature-triage-matrix/SKILL.md`.
5. **Registered** in the skills subsystem (`.hub/lock.json`, `.hub/audit.log`).

## Verification commands

### `hermes skills list`

Filtered output (full table truncated):

```
| Skill                    | Category | Source | Trust     | Status  |
|--------------------------|----------|--------|-----------|---------|
| literature-triage-matrix | research | url    | community | enabled |
```

The skill is **enabled** by default. No additional config needed.

### `hermes dump` (features section)

```
features:
  toolsets:           hermes-cli
  mcp_servers:        0
  memory_provider:    built-in
  gateway:            stopped (systemd (user))
  platforms:          none
  cron_jobs:          0
  skills:             1
```

`skills: 1` confirms Hermes counts our installed skill in its loaded set.

### `hermes skills audit`

Re-runs the security scanner on all installed hub skills:

```
Auditing 1 skill(s)...

Scan: literature-triage-matrix
(https://raw.githubusercontent.com/WenyuChiou/research-hub/master/skills/literature-triage-matrix/SKILL.md/community)
Verdict: SAFE
Decision: ALLOWED — Allowed (community source, safe verdict)
```

Same SAFE verdict on re-scan. Stable.

## Install location quirk

Hermes did **not** respect `HERMES_HOME` for the skill install. The skill landed at `~/.hermes/skills/research/literature-triage-matrix/SKILL.md`, not `~/hermes-compat-test/skills/research/literature-triage-matrix/SKILL.md`.

This is an inconsistency in Hermes itself, not a portability issue. Documented for the cleanup step (the cleanup needs to delete both `~/.hermes/` and `~/hermes-compat-test/`).

## Verdict at the loading layer

✅ **Hermes accepted a minimal agentskills.io-compliant SKILL.md** (only `name` + `description` in frontmatter) and integrated it into its skills subsystem without modification.

The frontmatter `description` field on this skill is 478 chars and includes trigger phrases for skill routing — those are exactly the structural cues Hermes' router will use to dispatch the skill at runtime. The skill body (markdown instructions) was not transformed; the SKILL.md installed is byte-equivalent to the source.
