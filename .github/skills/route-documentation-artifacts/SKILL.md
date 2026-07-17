---
name: route-documentation-artifacts
description: 'Decide where a piece of knowledge belongs: design docs, public user docs, internal docs, release notes, troubleshooting docs, or no docs yet. Use when planning documentation so work is not written in the wrong place or written before it is needed.'
---

# Route documentation artifacts

Help decide where a piece of knowledge belongs. Not everything needs public docs,
and not everything needs docs right now. Route each item to one or more of:

- **Design docs** — decisions, rationale, trade-offs, and constraints.
- **Public user docs** — tasks, concepts, and reference users need. For one
  feature, that is usually a task-focused **how-to**, not a tutorial.
- **Internal engineering docs** — how the system is built, reproduced, and
  maintained.
- **Release notes** — user-visible changes to announce at release time.
- **Troubleshooting docs** — known issues, errors, and their resolutions.
- **No docs yet** — nothing to write at this stage (note why).

## Guidance

- Prefer the smallest set of artifacts that captures the knowledge well.
- Favor a **how-to** for a feature; reserve tutorials for whole-product
  onboarding. When the reader is new to the idea, add a short concept or
  explanation piece so the steps land.
- Prefer updating an existing doc when that is the natural home — don't default to
  a new page when an edit, rewrite, or redirect is the right move.
- If routing depends on an unknown, mark it as needing SME clarification.
- Distinguish "needed now" from "needed later", and note the trigger for later.
- Point to the likely source of truth for each item so it does not get
  duplicated inconsistently.

The output is a routing decision the human can review, not a mandate to write
everything.
