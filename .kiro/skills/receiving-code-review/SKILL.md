---
name: receiving-code-review
description: Triage incoming code review feedback (PR comments, reviewer notes) into blocking vs. non-blocking, verify feedback that seems unclear or technically questionable rather than agreeing by default, and turn what survives into concrete edits. Use when the user pastes in review comments or asks to address PR feedback.
---

# Receiving code review

Incoming feedback deserves the same rigor outgoing feedback gets — agreeing with everything reflexively doesn't actually respect the reviewer, and neither does dismissing anything inconvenient.

## Process

1. **Enumerate each comment as a discrete item** — don't address a batch of feedback as one undifferentiated pass.
2. **Classify each as blocking or non-blocking**:
   - Blocking: correctness, security, or a real violation of stated requirements.
   - Non-blocking: style preference, a suggestion beyond the original scope, or genuinely optional.
3. **For anything unclear or that seems technically questionable, verify before implementing** — read the code the comment refers to, check whether the premise holds. If a comment is factually wrong (references code that no longer exists, misunderstands the actual behavior), say so directly rather than implementing a fix for a problem that isn't real.
4. **Turn confirmed blocking items into concrete edits.** For non-blocking items, either apply them if cheap and clearly net-positive, or note them as deferred with a one-line reason — don't silently drop them.
5. **Report back** which comments were addressed, which were deferred and why, and which were pushed back on and why.

## Anti-patterns to avoid

- Performative agreement — "Good catch!" followed by a change that doesn't actually address the concern.
- Implementing a suggestion that contradicts the original spec without flagging the conflict.
