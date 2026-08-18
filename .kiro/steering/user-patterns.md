---
inclusion: auto
name: user-patterns
description: The user's architectural preferences, design-review habits, stated opinions, recurring cross-session themes, and environment/tooling facts. Load when making a design or architectural decision, reviewing code for coupling or scope issues, or when environment-specific tooling choices (shell, CLI) are relevant.
---

# User patterns

Promoted, reinforced patterns only — not a running log. Every entry here should already pass two tests: would knowing this change a future decision (the master test), and is it concrete enough to actually apply (the specificity test). New entries arrive via the `patterns-consolidation` skill, not by direct append — see `lessons.md` for the raw, unpromoted log this is sourced from.

## Design patterns

Patterns about the *shape of systems* — coupling, scope, deliberate pattern use. Interaction/delivery preferences belong in `working-style.md`, not here, even if they surfaced during a design conversation.

- Pushes back on accidental coupling (e.g. questions why an entire catalogue needs to be cloned when only part of it is needed).
- Always questions the implied scope of an operation before accepting it.

## Architectural preferences

## Opinions expressed

Check for overlap with Design Patterns and Architectural Preferences before adding — keep an opinion under its most specific heading, not duplicated across several.

## Recurring themes

Only entries observed across multiple sessions — not a restatement of one session's topic.

## Environment & tooling

Durable, actionable facts about the working environment — not vague fragments. "Uses a custom script" isn't enough to act on; what does it do, how is it invoked?

- Works on WSL.
- Uses GitLab CLI (`glab`).

## Team & environment context

A current snapshot, not a history — this section gets overwritten as things change, not appended to. Reference data (URLs, keys, workspace identifiers) doesn't belong here at all; it goes stale fast and isn't a behavioral pattern.
