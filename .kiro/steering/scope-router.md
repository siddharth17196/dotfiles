---
inclusion: always
---

# Reach for `scope` on large or ambiguous work

Before writing code for a request that is large, spans multiple systems, or has more than one reasonable interpretation, invoke the `scope` skill rather than starting implementation directly. Signals that a request needs scoping first:

- The request could reasonably be built two different ways and picking wrong would waste real work.
- The request touches more than one component/service/repo.
- Constraints, edge cases, or the actual trigger for the request aren't stated.

Small, unambiguous changes (a typo fix, a one-line bugfix with an obvious cause, a well-specified task) don't need this — use judgment rather than routing everything through an interview.
