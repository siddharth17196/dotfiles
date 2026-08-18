---
inclusion: always
---

# Development Guidelines

## Core Principles

- **Simplicity First** — minimum code that solves the problem. No speculative abstraction, no "flexibility" or "configurability" that wasn't asked for. If it could be a third of the size, rewrite it.
- **Surgical Changes** — touch only what the request requires. Don't refactor or reformat adjacent code; match existing style even if you'd do it differently. Remove only the imports/variables/functions your own change orphaned — leave pre-existing dead code alone, just mention it.
- **No Laziness** — find the root cause. No temporary patch standing in for a real fix. Same standard `tdd-and-debugging`'s debugging phase already enforces — don't undercut it with a quick fix elsewhere.

## Before Coding

State assumptions explicitly. If multiple interpretations exist, present them rather than picking one silently.

The fork that decides whether to ask first: is there more than one reasonable interpretation, or one right answer waiting to be found?

- **Ambiguous or generative work** (a new feature, a design decision, an underspecified request) — ask, or see `scope-router` for when to hand off to the `scope` skill.
- **Well-defined diagnostic work** (a bug with a clear reproduction, a stack trace, a failing test) — just fix it via `tdd-and-debugging`. One right answer doesn't need hand-holding.

## Execution

- **Subagents** — dispatch when facing 2+ independent tasks with no shared state or sequential dependency between them (research, parallel exploration). One focused task per subagent.
- **Elegance is simplicity done correctly, not cleverness.** For non-trivial changes: is this the simple solution done well, or a shortcut deferring its cost? A hack is rarely actually simpler — it's just faster to type.
