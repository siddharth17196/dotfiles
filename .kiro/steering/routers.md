---
inclusion: always
---

# Routers

Nudges toward specific skills on specific triggers — kept together since both are always-on, single-purpose, and share the same owner.

## Reach for `scope` on large or ambiguous work

Before writing code for a request that is large, spans multiple systems, or has more than one reasonable interpretation, invoke the `scope` skill rather than starting implementation directly. Signals that a request needs scoping first:

- The request could reasonably be built two different ways and picking wrong would waste real work.
- The request touches more than one component/service/repo.
- Constraints, edge cases, or the actual trigger for the request aren't stated.

Small, unambiguous changes (a typo fix, a one-line bugfix with an obvious cause, a well-specified task) don't need this — use judgment rather than routing everything through an interview.

## Capture corrections immediately

Whenever the user corrects an approach, rejects a suggestion, or points out something done wrong, invoke the `lessons` skill immediately to log it — don't wait until the session ends to reconstruct it from memory. Session-end summarization and correction-capture are different mechanisms; this rule exists because corrections lose specificity fast if capture is deferred.
