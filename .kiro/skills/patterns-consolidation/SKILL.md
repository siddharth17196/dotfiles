---
name: patterns-consolidation
description: Periodically review the raw lessons log and the existing user-patterns/working-style files, promote reinforced entries into standing rules, de-duplicate, and prune anything stale or vague. Use on a recurring cadence (e.g. monthly) or when the lessons log has grown noticeably, not after every session.
---

# Patterns consolidation

The batch step that keeps `user-patterns.md` and `working-style.md` curated instead of letting them grow by pure append. This does not need to run every session — promotion criteria (recurrence, reinforcement) usually can't be judged from a single session anyway.

Migrating a pre-existing, ungoverned patterns file into this structure for the first time? See `references/migrating-existing-file.md` for heading-by-heading guidance before running the regular process below.

## Process

1. **Review `.kiro/lessons.md`.** For each entry, check whether it's recurred (the same or a closely related lesson appears more than once) or has otherwise been confirmed as a standing rule. Promote only those into `user-patterns.md` (or `working-style.md` if it's a universal interaction preference) — leave one-off instances in the log rather than promoting on a single occurrence.
2. **Remove promoted entries from `lessons.md`** once they've been folded in, so the log doesn't accumulate things that have already graduated.
3. **Apply the master test to every existing entry** in `user-patterns.md`/`working-style.md`: would knowing this change a future decision? Cut anything that's drifted into logging what happened rather than stating a rule for what to do.
4. **Apply the specificity test**: cut or sharpen anything too vague to act on.
5. **De-duplicate across headings** — the same fact shouldn't appear under Design Patterns and Opinions Expressed and Architectural Preferences simultaneously. Keep it under the most specific heading and remove the rest.
6. **Check for staleness and contradiction** — if two entries conflict (an old preference superseded by a newer one), keep the current one and remove the outdated one rather than leaving both.
7. **Update the `<!-- last-consolidated: -->` marker at the top of `lessons.md` to today's date.** The `lessons-consolidation-check` hook uses this to decide when to run consolidation again — leaving it stale causes the hook to keep re-triggering every session.
