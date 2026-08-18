---
name: verification-gate
description: Determine how to actually verify a piece of work in this repo before it's declared done — detecting the test framework, build system, and any repo-specific verification quirks. Use when the standing verification rule isn't enough on its own, e.g. an unfamiliar repo, a non-standard test setup, or work that doesn't have an obvious automated check.
---

# Verification gate

Companion to the always-on verification-before-completion steering rule. That rule says "never claim done without verifying" — this skill is for the harder case of figuring out *how* to verify in a repo you don't already know cold.

## Process

1. **Find the existing verification path** before inventing one:
   - Look for `package.json` scripts, `Makefile` targets, CI config (`.github/workflows`, etc.) — these tell you the command the team actually trusts.
   - If a test suite exists, identify the framework from config/imports rather than assuming (Jest vs Vitest vs pytest vs go test, etc.).
   - If a linter/typechecker is configured, treat it as part of verification, not optional.
2. **If no automated check covers the change**, say so explicitly rather than declaring success on vibes. Propose the smallest manual check that would catch a wrong implementation (a repro script, a manual walkthrough, a curl against a running server).
3. **Run the verification and show the actual output** — not a paraphrase of what you expect it to say.
4. **If verification fails**, that's the end state to report, not something to quietly retry until it passes without surfacing what changed.

## Output

A one-line statement of what was run and its result, immediately before any "done"/"fixed"/"passing" claim. If nothing was run, say so instead of implying otherwise.
