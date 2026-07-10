---
name: map-user-journey
description: 'Trace the ordered path a user takes through a feature or a doc: entry point, happy path, decision points, recovery, and success state. Complements the audience and edge-case skills by focusing on sequence rather than depth. Use when the task needs the user path laid out end to end.'
---

# Map the user journey

Lay out the path a user actually takes, in order, from where they start to where
they succeed. This skill is about **sequence** — the other skills cover who the
user is and what can go wrong; this one puts the steps in order and finds where
the path breaks.

## The path, in order

- **Entry point** — where and how the user arrives at this.
- **Prerequisites / assumptions** — what must already be true to start.
- **Happy path** — the ordered steps to the goal when nothing goes wrong.
- **Decision points** — where the user must choose, and what guides the choice.
- **Errors and failure modes** — where the path can break.
- **Recovery paths** — how the user gets back on track after a failure.
- **Success state** — how the user knows they're done.

## Keep it user-centered

- Describe what the user does and sees, in their order — not the internal call
  flow (see write-for-the-reader).
- Note the terminology the user meets along the way, and what they should *not*
  need to understand to get through it.
- End with the documentation implications: which steps need a doc, and where the
  path is confusing enough to warrant more explanation.

## Defer, don't duplicate

- For **who** the journey is for, use identify-the-audience.
- For a thorough sweep of **what can go wrong**, use identify-edge-cases.
- Don't invent UI, commands, API, or product behavior. Where a step is unknown,
  mark it as an open question rather than filling it in.

The output is an ordered walk through the experience the human can check step by
step, not a guess at behavior that hasn't been decided.
