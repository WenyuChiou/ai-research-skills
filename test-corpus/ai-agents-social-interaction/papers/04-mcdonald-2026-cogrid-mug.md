---
title: "CoGrid & the Multi-User Gymnasium: A Framework for Multi-Agent Experimentation"
authors:
  - Chase McDonald
  - Cleotilde Gonzalez
year: 2026
venue: arXiv
arxiv_id: "2604.15044"
url: http://arxiv.org/abs/2604.15044v1
citation_count: 0
source: arxiv
doc_type: preprint
paper_type: tooling-paper
method: tool / framework with case studies
domain: HCI / multi-agent experimentation infrastructure
---

# CoGrid & the Multi-User Gymnasium: A Framework for Multi-Agent Experimentation

## Abstract

The increasing integration of artificial intelligence (AI) in everyday
life brings with it new challenges and questions for regarding how humans
interact with autonomous agents. Multi-agent experiments, where humans and
AI act together, can offer important opportunities to study social
decision making, but there is a lack of accessible tooling available to
researchers to run such experiments. We introduce two tools designed to
reduce these barriers. The first, CoGrid, is a multi-agent grid-based
simulation library with dual NumPy and JAX backends. The second,
Multi-User Gymnasium (MUG), translates such simulation environments
directly into interactive web-based experiments. MUG supports interactions
with arbitrary numbers of humans and AI, utilizing either
server-authoritative or peer-to-peer networking with rollback netcode to
account for latency. Together, these tools can enable researchers to
deploy studies of human-AI interaction, facilitating inquiry into core
questions of psychology, cognition, and decision making and their
relationship to human-AI interaction. Both tools are open source and
available to the broader research community. Documentation and source
code is available at {cogrid, multi-user-gymnasium}.readthedocs.io. This
paper details the functionality of these tools and presents several case
studies to illustrate their utility in human-AI multi-agent
experimentation.

## Key extractable claims

- Two tools: CoGrid (NumPy + JAX backends) and Multi-User Gymnasium (MUG)
- MUG supports both server-authoritative and peer-to-peer networking with
  rollback netcode
- Both tools open source
- Paper provides case studies to illustrate utility
