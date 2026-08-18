---
name: code-review
description: Review the changes since a fixed point (a commit, branch, tag, or merge-base) along two independent axes — Standards (does the code follow this repo's documented conventions and avoid smells?) and Spec (does the diff actually deliver what the originating request/ADR asked for?). Dispatches both checks as parallel subagents so neither contaminates the other's judgment, then reports them side by side. Use when the user wants to review a branch, a PR, or work-in-progress changes.
---

# Code review (two-axis)

Standards review and spec review ask different questions and are easy to blur together — a reviewer holding both in mind at once tends to let "well-written" stand in for "correct," or vice versa. This skill keeps them separate by running them as two independent subagents.

## Process

1. **Establish the diff boundary** — ask or infer the fixed point to diff against (usually `main`/`master`, or the branch's merge-base).
2. **Dispatch two subagents in parallel**, each blind to the other's output:
   - **Standards agent**: reviews the diff against this repo's documented conventions (steering files, linter config, existing patterns in touched files) and flags smells — duplication, unclear naming, missed error handling at real boundaries, inconsistent style with surrounding code.
   - **Spec agent**: reviews the diff against the originating request — the ADR from `scope`, the linked issue, or the conversation that scoped the work — and flags gaps: something asked for but not delivered, or scope creep beyond what was asked.
3. **Report both sets of findings side by side**, labeled by axis, not merged into one undifferentiated list. Don't let one axis's findings soften or amplify the other's.
4. If there's no discoverable spec to check against (no ADR, no issue, no prior scoping conversation), say so explicitly and skip the Spec axis rather than inventing one.

## Output format

Two labeled sections, each a short list of concrete findings with file:line references where applicable. No finding without a specific location or a stated reason it can't have one.
