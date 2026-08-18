---
name: scope
description: Interview the user before code gets written on work that's large, ambiguous, or touches multiple systems. Explores intent, constraints, and edge cases; presents the design in short sections for the user to validate one at a time; records the agreed decisions as an ADR. Use when a request is underspecified, spans multiple systems/repos, or when the user asks to scope, align, or plan before building.
---

# Scope

A relentless-but-focused interview that turns an ambiguous request into a validated design before any code is written. Optimizes for catching wrong assumptions early, when they cost a sentence to fix, not after they cost a PR.

## When to use

- The request is large enough that a wrong assumption would waste real implementation time.
- The request is ambiguous — multiple valid interpretations exist and picking wrong is expensive.
- The user explicitly asks to scope, align, or plan before building.

Skip this for small, unambiguous changes — a one-line fix doesn't need an interview.

## Process

1. **Restate the request** in your own words and name what's actually being asked, distinct from how it was phrased.
2. **Interview**, one question at a time, not a questionnaire dump. Prioritize questions whose answer would change the design, not ones that just confirm what's already obvious. Cover:
   - What's the actual trigger/pain this solves, and for whom?
   - What's explicitly out of scope?
   - What existing systems/conventions does this need to respect?
   - What's the failure mode if this is built wrong — cheap to fix later, or costly?
3. **Present the design in short sections**, one at a time, not as a single wall of text. After each section, stop and let the user validate or correct it before moving to the next. Typical sections: problem statement → approach → key tradeoffs → what's explicitly out of scope.
4. **Capture the outcome as an ADR** — a short markdown file recording the decision, the alternatives considered, and why this one won. Save it wherever this repo already keeps decision records; don't invent a new location silently if one exists.
5. Hand off to implementation only after the user has validated the full design.

## Anti-patterns to avoid

- Don't ask questions you could answer yourself by reading the code.
- Don't present the whole design at once and ask "does this look right?" — that invites rubber-stamping, not real validation.
- Don't skip the ADR because the conversation already covered it — the point is a durable record, not just alignment in the moment.
