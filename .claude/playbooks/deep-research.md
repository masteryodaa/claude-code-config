# Playbook: Deep Research Methodology

## When to Use
- Evaluating a new technology, library, or approach
- Making architectural decisions with long-term impact
- Investigating unfamiliar domains or APIs
- Comparing multiple solutions to a problem

## Process

### 1. Define Scope (2 min)
Before searching, write down:
- What specific questions need answers?
- What would a "good enough" answer look like?
- What's the deadline / urgency?

### 2. Multi-Angle Search (5-10 min)
Run **4+ searches** from different perspectives:

| Angle | Query Pattern | Example |
|-------|--------------|--------|
| Direct | "[topic]" | "FastAPI middleware" |
| Comparison | "[topic] vs [alternative]" | "FastAPI vs Django REST" |
| Best practices | "[topic] best practices [year]" | "FastAPI best practices 2026" |
| Problems | "[topic] issues OR pitfalls OR gotchas" | "FastAPI common pitfalls" |
| Implementation | "[topic] tutorial OR example" | "FastAPI middleware tutorial" |

### 3. Deep Dive (5-15 min)
- Use WebFetch on the 3-5 most promising URLs
- Read official docs first, then community content
- Cross-reference claims — if only one source says it, be skeptical

### 4. Synthesize
Use the research template: `~/.claude/plans/templates/research-template.md`

Key sections:
- **Summary**: 2-3 sentences a busy person can read
- **Key Findings**: Numbered, with sources
- **Recommendation**: Opinionated, not wishy-washy
- **Open Questions**: What we still don't know

### 5. Save & Share
- Save to `~/.claude/plans/research-<topic-slug>.md`
- Present the summary to the user
- Offer to dive deeper on any finding

## Quality Checklist
- [ ] Multiple sources consulted (not just the first result)
- [ ] Official docs checked
- [ ] Conflicting information noted
- [ ] Recommendation is actionable
- [ ] Sources are cited with URLs
- [ ] Date-sensitive info marked with year

## Parallel Research
For large topics, use parallel agents:
- Agent 1: Core topic research
- Agent 2: Alternatives/comparison research
- Agent 3: Community sentiment / real-world experience
