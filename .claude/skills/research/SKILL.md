---
name: research
description: Deep multi-angle research with structured output
disable-model-invocation: true
---

# /research — Deep Research

## Usage
```
/research <topic>
/research <topic> --save       # Auto-save to plans/
```

## Process

### 1. Frame the Question
- Restate the research topic as 3-4 specific questions
- Identify what we need to learn: facts, comparisons, best practices, gotchas

### 2. Multi-Angle Search
Run **4+ WebSearch queries** from different angles:
- Direct query: the topic as-is
- Comparison query: "X vs Y" or "alternatives to X"
- Best practices: "X best practices 2026"
- Problems/gotchas: "X common issues" or "X pitfalls"

### 3. Deep Dive
- For the most promising results, use WebFetch to read full articles
- Cross-reference claims across multiple sources
- Note conflicting information — don't just pick the first answer

### 4. Synthesize
Structure findings as:

```markdown
# Research: [Topic]
**Date**: [today]
**Status**: Complete | Needs follow-up

## Summary
[2-3 sentence executive summary]

## Key Findings
1. [Finding with source]
2. [Finding with source]
3. [Finding with source]

## Comparison (if applicable)
| Criterion | Option A | Option B |
|-----------|----------|----------|

## Recommendation
[Opinionated recommendation with reasoning]

## Sources
- [Title](URL) — what we learned from it
```

### 5. Save
Save to `~/.claude/plans/research-<topic-slug>.md`
- Always save if `--save` flag is used
- Otherwise, ask if the user wants to save

## Guidelines
- Don't just summarize the first result — dig deeper
- Be opinionated in recommendations, not wishy-washy
- Flag when information is outdated or from unreliable sources
- If a topic needs hands-on testing (not just reading), say so
