# Runtime Contract

This catalog is the skill layer. The executable research workflow lives in
the source repos, especially `research-hub`.

For end-to-end AI-for-science inputs, outputs, quality evidence, and researcher
decisions at each existing stage, see [scientific lifecycle and quality gates](scientific-lifecycle.md).

## What Each Layer Does

| Layer | Provides | Does not provide |
|---|---|---|
| `ai-research-skills` catalog | Marketplace registry, install docs, links to canonical `SKILL.md` files | Python CLI, Zotero API access, NotebookLM browser session, MCP server |
| `SKILL.md` files | Portable workflow instructions and output contracts for AI hosts | Guaranteed host auto-triggering or external tool access |
| `research-hub-pipeline` | `research-hub` CLI, MCP/REST server, Zotero/Obsidian/NotebookLM automation, dashboard | Claude Code marketplace install for the whole catalog |

Installing this catalog or copying a `SKILL.md` file does not prove that the
Python runtime is installed. `claude plugin list` only verifies Claude Code
marketplace state.

## Skill Types

| Type | Examples | Runtime expectation |
|---|---|---|
| Prompt-only workflow skills | `gap-to-topic`, `research-design-helper`, `literature-triage-matrix`, `academic-writing-skills` | Any host that can read the needed files and follow the output contract |
| Workspace-file skills | `research-context-compressor`, `research-project-orienter`, `paper-memory-builder` | File-system access to the project or manually supplied context |
| Native literature discovery | Discovery guidance in `research-hub` and its shared research protocol | The search/reading tools actually exposed by Codex or Claude Code; no Hub CLI or storage account required for this route |
| Runtime-backed research automation | Configured `research-hub` automation, `paper-summarize`, parts of `notebooklm-brief-verifier`, Zotero-backed curation flows | `pip install research-hub-pipeline` plus any required Zotero, Obsidian, NotebookLM, LLM CLI, MCP, or REST setup |
| Deep Zotero CRUD | `zotero-skills` | Zotero local/Web API credentials and a host that can call the API |
| Delegation skills | `codex-delegate`, `antigravity-delegate`, `research-hub-multi-ai` | Target CLI installed and available on `PATH`, or a manual handoff prompt |

## What has actually been verified?

These are separate evidence levels, not interchangeable green checks:

| Evidence | Establishes | Does not establish |
|---|---|---|
| Registry declaration | Catalog/marketplace names, links, and intended install refs | Source files exist or any host loaded them |
| Source layout | Supplied source has the expected paths, manifests, and skill identities | It is the reviewed revision |
| Accepted snapshot | Exact commit/tree and the checker's bounded relevant file set match the reviewed snapshot | Full resource closure, adapter compatibility, or runtime availability |
| Installed discovery | The named host reports the installed skill/plugin | The requested operation was invoked successfully |
| Actual invocation | The observed operation's result for specific inputs, host, and version | Other operations/hosts, scientific validity, or human acceptance |

See [accepted-source verification](accepted-source-verification.md) for the
checker's limits. A newer source with a matching plugin/adapter version can still
fail snapshot identity; do not advance accepted pins, dates, or marketplace refs
to hide that drift. Missing host or runtime evidence remains unknown/unavailable.

## Local workspace and writing adapter

For project/artifact/task management, use Hub's existing
[workspace guide](https://github.com/WenyuChiou/research-hub/blob/master/docs/workspace-guide.md),
not the literature-ingestion smoke test below. Check the actual installed
workspace command help; source documentation and package version text alone do
not prove the installed wheel contains that capability. No Zotero or NotebookLM
account is needed for the account-free demo. Demo creation writes local teaching
fixtures; it does not run a model or establish scientific results.

Workspace writing audits additionally require an explicitly configured trusted
bundle; installing the writing skill in an AI host does not configure it in Hub.
Use the producer's [adapter contract](https://github.com/WenyuChiou/academic-writing-skills/blob/main/docs/workspace-adapter.md)
and Hub's [tested-source record](https://github.com/WenyuChiou/research-hub/blob/master/docs/workspace-writing-source.json).
Bundle hashes check integrity, not publisher trust. If the adapter or compatible
CLI is missing, keep the portable handoff and explicitly load the public skill in
the receiving host; do not describe the handoff as completed execution.

Concrete compatibility examples (source observations, not new acceptance):

- Hub at `6381dfa7d474dd27cd4adb33f0f59ea8ec395150` records tested Writing producer
  `bc15e29e976cd6ade3484aeaa4f1230444697f8a`. The catalog's accepted Writing source
  `aff90bc8b07f4f38d4ecacb8cd9c138fd9ce753c` is a different identity. Its snapshot
  check does not certify Hub adapter compatibility or the full writing-reference
  closure. Do not substitute one producer for the other without separate review.
- In that Hub implementation, `adapter_version` is a string, not an enforced
  producer allowlist. An unknown producer is **not assessed**, not necessarily
  rejected. Identical version labels or operation names are insufficient proof
  of semantic compatibility. Hub has six audit handlers: `state`, `consistency`,
  `prose`, `candidate`, `docx`, and `regression`; a bundled script alone does not
  register another handler.
- For an own-manuscript handoff, preserve [claims](example-paper-memory-claims.yml)
  and [figures](example-paper-memory-figures.yml) under their Hub-owned `.paper`
  contract. In that contract, `rejected` means editorial retirement, not scientific
  refutation; `gap` remains unresolved even when evidence pointers exist. Do not
  translate these into Writing evidence-confidence statuses, renumber historical
  claims, or invent missing support. Writing owns manuscript semantic decisions;
  Hub owns workspace registration/receipts, not scientific acceptance.
- A `paper-review` report is not permission to edit. An audit exit code or a valid
  artifact hash is mechanical evidence, not acceptance of a manuscript. Existing
  state must not be reinitialized to remove alignment findings; review the exact
  changed inputs and preserve unresolved issues.

## Agent Preflight For Literature Search

For native discovery, follow [Stage 1](pipeline.md#1-discover-literature): inspect
the host's available search/reading capabilities and retain evidence at its
actual level. The CLI checks below apply only to a requested Hub automation
route; they are not prerequisites for native research or a manual handoff.

This is a **live** literature workflow, not a catalog or local-workspace test.
`--no-nlm` disables NotebookLM only; it does not disable other network calls,
models, or writes. Complete the [live-run preflight](live-run-preflight.md) and
obtain the applicable data/cost/write authorization before the `auto` command.
Then verify the executable layer for the selected host:

```bash
research-hub describe --json
research-hub doctor
research-hub auto "agent-based modeling" --max-papers 3 --no-nlm
```

If `research-hub` is not found, only the CLI route is unavailable here. Inspect
any exposed MCP/REST/native Hub interfaces separately; a route not invoked
remains untested, not proof that Hub automation is unavailable. Keep the
native/manual route. Only if Hub automation is requested and setup is
authorized, use the existing installation route:

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher   # or: analyst | humanities | internal
```

If the smoke test stops because no relevance judge is configured, either
install/configure a supported LLM CLI (`claude`, `codex`, `gemini`,
`opencode`, `aichat`, `cursor`, or a custom adapter) or run the smoke test
with `--no-fit-check` and record that relevance filtering was skipped.

Add NotebookLM only after Zotero/Obsidian ingestion works:

```bash
research-hub notebooklm login --auto-detect
research-hub notebooklm bundle --cluster <slug>
research-hub notebooklm upload --cluster <slug>
research-hub notebooklm generate --cluster <slug> --type brief
research-hub notebooklm download --cluster <slug>
```

## Host Compatibility

- Claude Code has the packaged marketplace path and `claude plugin list`.
- Codex, Cursor, Gemini, Windsurf, Hermes, OpenClaw, and generic API clients
  can consume the same `SKILL.md` instructions, but each host needs its own
  discovery or prompt smoke test.
- MCP/REST-capable hosts should prefer `research-hub serve` when they need
  real tool execution instead of a prompt-only workflow.
- OpenClaw is a structurally compatible target through MCP/manual
  `SKILL.md` loading, but this catalog does not claim release-grade
  OpenClaw verification yet.
