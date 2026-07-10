---
name: capture-decisions
description: 'Record the decisions behind a change as first-class documentation material: the decision, its context, options considered, what was chosen and why, trade-offs, rejected options, and impact. Keeps decided, proposed, rejected, and open items clearly separate. Use when a change involves design choices, trade-offs, or unresolved decisions.'
---

# Capture decisions

The reasoning behind a change is worth as much as the change itself, and it's the
first thing lost once the work moves on. Capture decisions as they surface so the
"why" survives — without deciding anything on the human's behalf.

## What to capture

For each decision, record what's known and leave the rest open:

- **The decision** — what is being decided.
- **Context / problem** — what prompted it.
- **Options considered** — the alternatives on the table.
- **Chosen option** — if one has been chosen.
- **Rationale** — why, in terms the reader can follow.
- **Trade-offs** — what the choice costs or gives up.
- **Rejected options** — what was ruled out, and why.
- **User-facing impact** — what changes for the reader or user, if anything.
- **Documentation impact** — which docs this decision should land in.
- **Owner / follow-up** — who owns it or what happens next, if known.
- **Open questions** — what's still undecided.

## Keep the states distinct

- Separate **decided**, **proposed**, **rejected**, and **open** items. Don't let
  a proposal read as a settled decision.
- If a decision is only **implied** — visible in the work but never stated —
  label it as implied and ask the human to confirm.
- Don't turn a guess into a decision. Record uncertainty plainly.

## Guardrails

- Do not decide for the human. Surface the decision and its shape; they choose.
- Point to the source for a recorded decision where you can, so it can be trusted
  later (see separate-fact-from-inference).

A captured decision is something a future reader — or the same team in six
months — can understand without re-litigating it.
