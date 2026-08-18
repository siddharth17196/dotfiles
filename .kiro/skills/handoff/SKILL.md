---
name: handoff
description: Compact the current conversation into a structured handoff document for another session or engineer to pick up with full context. Use only when explicitly asked for a handoff, summary-to-continue, or context dump for someone else.
disable-model-invocation: true
argument-hint: "What will the next session be used for?"
---

# Handoff

Writes a plain markdown file, not a steering file — a handoff is a one-time snapshot for a specific continuation, not standing project context.

## Process

1. **Ask what the next session needs to do**, if not already stated — a handoff written for "someone continuing this exact task" looks different from one written for "someone auditing what happened."
2. **Compact the conversation into**:
   - Context: what this work is and why it exists.
   - Decisions already made, and the reasoning behind each (not just the conclusion — the next session needs to know what's settled vs. still open).
   - Current state: what's done, what's in progress, what's explicitly not started.
   - Immediate next action: the concrete next step, not a vague direction.
   - Anything parked or explicitly out of scope, so it isn't accidentally redone or reopened.
3. **Write it to a file** (not a steering file, not memory) at a location the user confirms or a sensible default (e.g. `docs/handoffs/` or the repo root if no convention exists).
4. Keep it dense — the goal is a session that reads this once and has full context, not a transcript replay.

## Anti-patterns to avoid

- Padding with narration of the process ("first I explored X, then I tried Y") instead of the outcome that matters.
- Omitting the *why* behind decisions — a decision without its reasoning gets silently re-litigated or reversed by the next session.
