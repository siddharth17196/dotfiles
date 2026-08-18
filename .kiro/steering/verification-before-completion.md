---
inclusion: always
---

# Verification before completion

Never state that work is done, fixed, or passing without having actually run the relevant verification and shown its output in this conversation. This applies before committing, before creating a PR, and before any summary that claims success.

- Evidence before assertions, always — "tests pass" must be followed by the command that was run and its actual result, not an expectation of what it would show.
- If there's no automated check for this change, say so and either propose a manual verification step or run one — don't let the absence of a test suite become an excuse to skip verification entirely.
- If verification fails, report the failure as the current state. Don't retry silently until something passes without surfacing what changed between attempts.
- For repo setups where the right verification path isn't obvious (unfamiliar test framework, no CI config, non-standard build), use the `verification-gate` skill.
