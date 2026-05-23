# Canonical Prompt — `pipeline-overview.png`

This is the working ChatGPT-image-gen prompt used to produce
`pipeline-overview.png` (EN) and `pipeline-overview.zh-TW.png` (繁中)
in 2026-05-12. Reuse when the skill count or stage mapping changes.

**Why save the prompt**: getting the chip placement right took
multiple iterations (paper-summarize missing, research-hub missing
from Stage 2, badge count off, etc.). Re-running this prompt verbatim
short-circuits all that.

## Pre-conditions before regenerating

1. Confirm canonical 15-skill list against
   [`docs/skill-directory.md`](../skill-directory.md) and
   [`docs/pipeline.md`](../pipeline.md). If the count has changed,
   update the prompt below before sending.
2. Confirm the badge counts:
   - Total skills = sum across all 5 plugins (currently 15).
   - "from research-hub" = `research-hub` plugin count
     (currently 11: research-hub, research-hub-multi-ai,
     research-design-helper, research-context-compressor,
     research-project-orienter, literature-triage-matrix,
     paper-memory-builder, paper-summarize,
     notebooklm-brief-verifier, zotero-library-curator,
     gap-to-topic).
   - "standalone repos" = the other 4 plugins
     (academic-writing-skills, zotero-skills, codex-delegate,
     gemini-delegate-skill).

## English prompt

```
Create a vertical infographic, 1024×1500 px, titled
"AI Research Skills" with subtitle
"15 AI skills catalog organized by research workflow stage".

Style: soft blue / white background, single teal accent #2DA89C,
no orange, no warning colors, every stage same color treatment.
Skill names rendered as monospace pill chips so they read as code
identifiers. No human silhouettes, no AI brain logos, no
gap/warning annotations.

Layout: 8 stages top to bottom, each row has the stage number, an
icon, a stage title, an italicized quote, and the relevant skill
chips.

Stages and their exact chip sets (must be present, no omissions):

1. Discover literature
   Quote: "What has been done? What should I read?"
   Chips: research-hub, paper-summarize, zotero-skills

2. Organise & compare, find the gap
   Quote: "Where is the gap? Which 5 papers actually matter?"
   Chips: literature-triage-matrix, gap-to-topic, research-hub,
          notebooklm-brief-verifier, zotero-library-curator

3a. Frame the problem
   Quote: "Is my research question sharp enough to be falsifiable?"
   Chips: research-design-helper

3b. Plan the project (capture artifacts)
   Quote: "What am I claiming, with what data, and what's my plan?"
   Chips: research-context-compressor, research-project-orienter

4. Design & build the model
   Quote: "What architecture, equations, agents do I need?"
   Chips: research-design-helper (re-read design_brief.md)

5. Run experiments, calibrate, validate (C&V)
   Quote: "Is the run reproducible? Can I save tokens?"
   Chips: research-context-compressor, research-project-orienter

6. Visualise & interpret results
   Quote: "What does the figure actually show?"
   Chips: codex-delegate, gemini-delegate

7. Draft & revise the manuscript
   Quote: "Does the prose match the figure? Sound human?"
   Chips: paper-memory-builder, academic-writing-skills

8. Submit, respond to reviewers, wrap up
   Quote: "Are claims defensible? Is project state preserved?"
   Chips: academic-writing-skills, research-context-compressor

Below the 8 stages, a separate "Cross-cutting Tools — Used at Every
Stage" band with three pill chips and one-line descriptions:
- codex-delegate — "token-heavy mechanical work"
- gemini-delegate — "long-context reading or 繁中 / CJK output"
- research-hub-multi-ai — "stage-agnostic routing across
  Claude / Codex / Gemini"

Dotted teal lines from this band back up to the stages each tool
supports (keep it readable, not all stages need a line).

Bottom legend (left to right):
- "15 skills total"
- "11 from research-hub"
- "4 standalone repos (academic-writing-skills, zotero-skills,
   codex-delegate, gemini-delegate-skill)"
- "Repo: github.com/WenyuChiou/ai-research-skills"
```

## 繁中 prompt

Same as English, except:

- Title: "AI Research Skills"
- Subtitle: "15 個 AI skills 的目錄，依研究 workflow 階段組織"
- Stage names + quotes in 繁中:
  1. 找文獻 — "別人做過什麼？我該讀什麼？"
  2. 整理比較、找 gap — "gap 在哪？哪 5 篇真的關鍵？"
  3a. 框問題 — "我的研究問題夠 sharp 嗎？可不可以證偽？"
  3b. 寫計畫 — "我的 claim 是什麼？用什麼資料？計畫是什麼？"
  4. 設計與建模 — "我需要什麼架構、什麼方程式、什麼 agents？"
  5. 執行、校正、驗證 (C&V) — "可重現嗎？可省 token 嗎？"
  6. 視覺化與結果解讀 — "這張圖到底在說什麼？"
  7. 論文撰寫與修改 — "文字描述跟圖一致嗎？讀起來像人寫的嗎？"
  8. 投稿、回覆審查、收尾 — "claim 站得住嗎？專案狀態保留好了嗎？"
- Cross-cutting band: "Cross-cutting Tools — 每個階段都會用到"
  - codex-delegate — "token 重的機械性工作"
  - gemini-delegate — "long-context reading or 繁中 / CJK 輸出"
  - research-hub-multi-ai — "stage-agnostic 在 Claude / Codex /
    Gemini 之間 routing"
- Skill chip names stay in English (skill names don't translate).

## Known iteration pitfalls (from 2026-05-12 regen)

- ChatGPT will sometimes drop `research-hub` from Stage 2 — it has
  to be re-listed explicitly. Stage 2 needs **five** chips
  (literature-triage-matrix, gap-to-topic, research-hub,
  notebooklm-brief-verifier, zotero-library-curator).
- ChatGPT will sometimes write the "from research-hub" badge as 8
  or 9. It must be **11**. Re-emphasize in follow-up if needed.
- ChatGPT may add a "(you do this)" annotation to a stage title.
  Strip in follow-up.
- ChatGPT may leak an English quote into a Chinese stage in the
  zh-TW version. Re-translate in follow-up.
- For incremental fixes after a draft, write them as a numbered
  diff against the previous image, not as a fresh prompt. Otherwise
  ChatGPT re-imagines the layout and loses chip placements that
  were already correct.
