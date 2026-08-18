# Migrating an existing user-patterns file

One-time guidance for folding a pre-existing, ungoverned patterns file (e.g. one that grew by pure append, with no lessons/promotion split) into this repo's `working-style.md` / `user-patterns.md` structure. Run this once per legacy file, then rely on the regular `patterns-consolidation` process going forward.

Go heading by heading. For each entry, apply the master test (would knowing this change a future decision?) and the specificity test (is it concrete enough to act on?) before deciding where — or whether — it lands.

- **Code style** — keep. Standing conventions only; if an entry is really a one-off note about a single file/PR, cut it.
- **Design patterns** — keep only entries about the *shape of systems*: coupling, scope creep, deliberate pattern use, review habits like questioning implied scope. Move any entry that's actually about *how output should be delivered* (e.g. "prefers save-as-file over inline code," "wants runnable scripts") to `working-style.md` — those are interaction preferences, not design patterns, even though they surfaced in a design conversation.
- **Architectural preferences** — keep as-is; this is usually the clearest principle-level content in the file.
- **Working style** — keep, and merge in the delivery-preference entries pulled out of Design Patterns above. This becomes the file's compact, always-on core.
- **Opinions expressed** — keep, but de-duplicate against Architectural Preferences and Design Patterns first. If the same opinion appears under more than one heading, keep it in the most specific one and delete the rest.
- **Repository conventions** — delete this heading entirely. Conventions are repo-specific; storing them in a cross-repo personal file makes them noise everywhere except the one repo they're about, and wrong if misapplied elsewhere. If anything here is worth keeping, it belongs in that repo's own steering, not here.
- **Team and environment context** — collapse to a short *current snapshot* (who/what you're currently embedded in), not a running list. Delete anything that's timestamped history rather than present state — that history belongs in session archives, if those exist.
- **[X] documentation patterns** (e.g. change-documentation writing conventions) — keep as a standing output-format preference, same family as Working Style. Fold it under Working Style unless it's substantial enough to justify staying separate.
- **Recurring themes** — keep only entries that describe something observed across *multiple* sessions. Delete anything that's really just restating a single session's topic.
- **Topics and work types** (or any heading logging "what was worked on") — delete entirely. It's a log of what happened, not a pattern that changes future behavior — that detail belongs in per-session archives, not a patterns file.
- **General / catch-all headings** — rename to something specific (e.g. "Environment & Tooling"). Keep durable, actionable entries (e.g. "works on WSL," "uses GitLab CLI" — these genuinely change decisions like path/shell conventions and which CLI to suggest). Cut or sharpen anything too vague to act on (e.g. "uses a custom script" with no further detail on what it does or how it's invoked).
- **Random context / environment state** (URLs, keys, workspace identifiers) — delete entirely. This is reference data, not a behavioral pattern — a different kind of thing from the rest of the file. It goes stale fast and knowing it doesn't change a future decision. If genuinely worth keeping, it belongs in a separate reference doc, not a patterns file.

After sorting, run the regular `patterns-consolidation` steps (dedup, staleness check) over the result before treating it as the new baseline.
