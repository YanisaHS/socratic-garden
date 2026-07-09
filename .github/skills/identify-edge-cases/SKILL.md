---
name: identify-edge-cases
description: 'Find what the happy path misses: boundary conditions, failure modes, ambiguous states, hidden assumptions, and uncovered user paths. Use when defining behavior, reviewing a design, or checking a doc for gaps.'
---

# Identify edge cases

Help the human find what the happy path misses. For the behavior in question,
probe for:

- **Edge cases** — boundary values, empty inputs, maximums, unusual but valid
  combinations.
- **Failure modes** — what happens when a dependency, input, or precondition
  fails.
- **Ambiguous states** — partial completion, retries, concurrency, timeouts,
  interrupted operations.
- **Assumptions** — conditions the design silently relies on that may not hold.
- **Uncovered user paths** — valid ways to reach the feature that the happy path
  does not describe.

For each item:

- Describe the trigger and the expected (or undefined) behavior.
- Note whether the behavior is confirmed, assumed, or unknown.
- Flag unknowns as open questions for the human or an SME.

Do not invent behavior for undefined cases. Surface the gap and let the human
decide what should happen.
