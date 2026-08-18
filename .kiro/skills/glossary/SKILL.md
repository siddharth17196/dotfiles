---
name: glossary
description: Propose additions to the team's domain glossary (.kiro/steering/glossary.md) when new domain terms, jargon, or ambiguous vocabulary come up in conversation or code. Use when a term is used that isn't already in the glossary and would benefit someone new to the codebase.
---

# Glossary maintenance

Keeps `.kiro/steering/glossary.md` current as a living, always-on reference — not a one-time onboarding artifact.

## Process

1. **Notice candidate terms** as they come up: domain-specific nouns, internal abbreviations, or a common word used with a specific meaning in this codebase that differs from its everyday meaning.
2. **Check whether it's already in the glossary** before proposing an addition — don't duplicate entries.
3. **Propose the addition inline**, in context, rather than batching it silently: a short note that this term seems worth capturing, with a one-line definition drawn from how it's actually used in the code/conversation (not a generic dictionary definition).
4. **On confirmation, add it to `.kiro/steering/glossary.md`** as a single-line entry: `**term** — definition`, keeping the file alphabetized within its sections.
5. Don't add a term unilaterally without flagging it first — the glossary is a team asset and entries should reflect team-agreed meaning, not one session's guess.

## What counts as glossary-worthy

- Internal system/service names that aren't self-explanatory.
- Business/domain terms specific to this team's problem space.
- Words that are overloaded — used differently here than their common meaning.

Not glossary-worthy: standard language/framework terminology, one-off variable names, anything already well-documented elsewhere.
