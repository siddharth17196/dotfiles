---
name: merge-conflict-resolution
description: Resolve an in-progress git merge or rebase conflict hunk by hunk, tracing each side's intent rather than mechanically picking one side or the other. Use when there's an active, unresolved merge/rebase conflict in the working tree.
---

# Merge conflict resolution by intent

Conflicts are resolved by understanding what each side was trying to accomplish, not by pattern-matching on diff markers.

## Process

1. **Confirm there's an active conflict** (`git status` shows unmerged paths) before doing anything — don't run this speculatively.
2. **For each conflicted hunk**:
   - Read the commit(s) on each side that touched this hunk to understand *why* each change was made, not just what changed.
   - Determine whether the two sides are actually incompatible, or whether both intents can be preserved (e.g. one side added a parameter, the other added a validation check — both belong in the result).
   - Write the resolution that satisfies both intents where possible; where truly incompatible, pick the one that matches the more recent/authoritative context (the branch being merged into, an explicit user instruction) and say which you picked and why.
3. **Never use `--abort` as a way to avoid resolving** — if a conflict is genuinely too ambiguous to resolve safely, stop and ask the user rather than aborting silently or guessing.
4. **After resolving all hunks**, show the user a summary of what was resolved and why, before staging/committing — this is exactly the kind of change that's hard to review after the fact.
5. **Verify** — run the test suite or build if one exists, since a syntactically clean resolution can still be semantically wrong.

## Anti-patterns to avoid

- Taking "ours" or "theirs" wholesale without reading what the hunk actually contains.
- Resolving conflicts silently across an entire file without pausing to explain non-obvious calls.
