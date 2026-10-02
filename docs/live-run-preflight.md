# First-live-run preflight

This is a supervisor review contract, not a catalog runtime hook. The catalog,
wrapper sidecars and specification fixtures do not enforce it automatically.
Apply it before the first **live model-backed test or delegation**, including
an official plugin task or direct CLI/API call. Read-only help/status inspection
and offline doubles are not live model tests.

繁中: [live-run-preflight.zh-TW.md](live-run-preflight.zh-TW.md)

## Resolve and show the effective settings

Use existing authorized, value-free host status and the final invocation.
CLI arguments, wrapper defaults and provider routing can override configuration;
a configured model label is not proof of the model actually selected.

| Field | What the supervisor must surface |
|---|---|
| Host/runtime | The actual host and execution route; native plugin, adapter or direct CLI/API |
| Provider/model | The resolved service and exact effective model identifier, including overrides |
| Authentication mode | ChatGPT subscription, API, another documented mode, or unknown; report availability without credential values |
| Budget/cost policy | Previously approved quota/spend/token policy and fallback limits; do not infer API budget from a subscription login |
| Data destination/scope | Which provider/service receives which approved files or context, plus any tools/uploads/storage destinations |

Never paste keys, tokens, authentication files or credential-bearing URLs into
chat, repository notes or CI logs. Record sanitized mode/status only. If the
effective model, authentication route, budget or data scope is unknown, do not
start a model call to discover it.

## Reuse valid choices and ask only when needed

1. Reuse a previous explicit user choice or approved canonical policy when it
   covers the current task and effective settings. Repository defaults and
   worker proposals cannot authorize themselves. Show the effective values;
   do not ask the same unchanged choices again on every run.
2. Before first use, ask one bundled question for missing material choices:
   provider/model, subscription versus API route, approved budget, and data
   destination/scope. A prior model preference does not resolve unknown billing
   or data-sharing choices.
3. Reconfirm a material provider/model, authentication, cost/budget, permission
   or data-destination/scope change outside existing approval. Do not silently
   upgrade a model, change a provider or take an expensive fallback.
4. Missing authentication or an unsupported model remains blocked. Use a
   separately authorized secure setup/handoff where needed; never ask for a
   secret in chat or create credentials/change security settings from this
   preflight. A quota/error sentinel is not approval for a new route.
5. Retain the task/run, sanitized effective settings, applicable prior
   choice/policy, unresolved choices and decision. Do not put private user
   preferences or project context into a public source repository.

## Verification and architecture boundary

The fixtures test these declared decisions with synthetic settings. They do
not probe a real account, prove billing/sandbox enforcement, start inference or
install an enforcement hook. A supervising host must actually carry out the
preflight; a direct wrapper call can bypass prose.

This check is an instance of the existing human authorization/policy boundary,
before a live action. It adds no component, store or research stage, so the
existing architecture and images remain unchanged.
