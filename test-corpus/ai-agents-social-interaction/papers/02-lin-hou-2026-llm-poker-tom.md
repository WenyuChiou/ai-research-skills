---
title: "Readable Minds: Emergent Theory-of-Mind-Like Behavior in LLM Poker Agents"
authors:
  - Hsieh-Ting Lin
  - Tsung-Yu Hou
year: 2026
venue: arXiv
arxiv_id: "2604.04157"
url: http://arxiv.org/abs/2604.04157v1
citation_count: 0
source: arxiv
doc_type: preprint
paper_type: empirical-study
method: experiment (2x2 factorial)
domain: LLM / theory of mind / poker
---

# Readable Minds: Emergent Theory-of-Mind-Like Behavior in LLM Poker Agents

## Abstract

Theory of Mind (ToM) — the ability to model others' mental states — is
fundamental to human social cognition. Whether large language models
(LLMs) can develop ToM has been tested exclusively through static
vignettes, leaving open whether ToM-like reasoning can emerge through
dynamic interaction. Here we report that autonomous LLM agents playing
extended sessions of Texas Hold'em poker progressively develop
sophisticated opponent models, but only when equipped with persistent
memory. In a 2x2 factorial design crossing memory (present/absent) with
domain knowledge (present/absent), each with five replications (N = 20
experiments, ~6,000 agent-hand observations), we find that memory is both
necessary and sufficient for ToM-like behavior emergence (Cliff's delta =
1.0, p = 0.008). Agents with memory reach ToM Level 3-5 (predictive to
recursive modeling), while agents without memory remain at Level 0 across
all replications. Strategic deception grounded in opponent models occurs
exclusively in memory-equipped conditions (Fisher's exact p < 0.001).
Domain expertise does not gate ToM-like behavior emergence but enhances
its application: agents without poker knowledge develop equivalent ToM
levels but less precise deception (p = 0.004). Agents with ToM deviate
from game-theoretically optimal play (67% vs. 79% TAG adherence, delta =
-1.0, p = 0.008) to exploit specific opponents, mirroring expert human
play. All mental models are expressed in natural language and directly
readable, providing a transparent window into AI social cognition.
Cross-model validation with GPT-4o yields weighted Cohen's kappa = 0.81
(almost perfect agreement). These findings demonstrate that functional
ToM-like behavior can emerge from interaction dynamics alone, without
explicit training or prompting, with implications for understanding
artificial social intelligence and biological social cognition.

## Key extractable numbers

- N = 20 experiments, ~6,000 agent-hand observations
- 2×2 factorial: memory × domain knowledge
- Cliff's delta = 1.0, p = 0.008 (memory effect on ToM emergence)
- ToM Level 3–5 with memory; Level 0 without
- Fisher's exact p < 0.001 (strategic deception)
- TAG adherence: 67% (with ToM) vs. 79% (without), delta = -1.0
- Cross-model validation: weighted Cohen's kappa = 0.81 (GPT-4o)
