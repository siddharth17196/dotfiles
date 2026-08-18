---
name: tdd-and-debugging
description: Write new code test-first (red-green-refactor) and diagnose bugs through a systematic root-cause process rather than guess-and-check. Use whenever writing new functionality, fixing a bug, or investigating a test failure or unexpected behavior.
---

# TDD and systematic debugging

Two related disciplines: build new things test-first, and fix broken things by understanding them first.

## Test-driven development (new code)

1. **Detect the repo's existing test framework and conventions** before writing a test — check existing test files for the runner, assertion style, and fixture patterns. Don't introduce a second framework into a repo that already has one.
2. **Write a failing test first** that encodes the requirement, not the implementation.
3. **Confirm it actually fails** for the expected reason — a test that passes immediately, or fails with an unrelated error, isn't validating anything.
4. **Write the minimum code to pass it.**
5. **Refactor** with the test as a safety net, then re-run to confirm it's still green.

If the repo has no test infrastructure at all, say so and ask whether to set one up rather than silently skipping tests or inventing a throwaway harness.

## Systematic debugging (bugs / unexpected behavior)

Gated process — don't skip to a fix before completing the phase you're in:

1. **Reproduce.** Get a reliable trigger for the bug before touching code. If you can't reproduce it, that's the actual blocker — say so.
2. **Localize.** Narrow the failure to the smallest unit that exhibits it (a function, a query, a component) using logging, bisection, or a debugger — not by reading code and guessing.
3. **Explain the root cause** in one or two sentences, in terms of what's actually happening, before writing a fix. If you can't explain it, you don't understand it yet — keep localizing.
4. **Fix and verify** the fix against the original reproduction, plus a regression test that would have caught it.

## Anti-patterns to avoid

- Don't patch symptoms ("add a null check") without the root-cause sentence from phase 3 — that's a guess, not a fix.
- Don't write tests that mock away the exact thing you're supposed to be testing.
