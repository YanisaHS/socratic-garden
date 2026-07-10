---
name: compare-design-to-docs
description: 'Check whether a documentation artifact accurately reflects the source material it should describe (a design doc, change brief, decision record, issue, or plan). Reports matches, gaps, unsupported claims, and conflicts as an alignment report. Needs both a source artifact and a doc artifact. Use when both are available; it is an alignment check, not a general review or a truth oracle.'
---

# Compare design to docs

Check that a documentation artifact lines up with the source material it's meant
to describe. This is an **alignment check between two artifacts**, not a review of
one doc on its own, and not a judgment of whether the design itself is right.

## When it applies

You need two things:

1. **A source artifact** — describes intended behavior: a design doc, change
   brief, decision record, issue, or implementation plan.
2. **A documentation artifact** — a user-docs draft, internal note, release-note
   input, or an existing public page.

If only one is supplied, say the comparison isn't possible and ask for the
missing artifact. Don't review a single artifact as if it were a comparison.

## What to check

Read both, then report where they align and where they don't:

- **Matches** — what the docs get right against the source.
- **Gaps** — behavior in the source that the docs don't cover.
- **Unsupported claims** — statements in the docs the source doesn't back.
- **Design ambiguities** — places the source is unclear enough that the docs
  can't be written confidently.
- **User-experience mismatches** — the docs describe a different experience than
  the source intends.
- **Missing edge cases or limitations** — covered in the source, absent in docs.
- **Terminology mismatches** — the two use different names for the same thing.
- **Leaking internals** — implementation detail from the source that shouldn't be
  in user docs (see write-for-the-reader).
- **Needs confirmation** — claims only a human or SME can verify.

## Guardrails

- Don't judge whether the design is correct unless the material directly supports
  that conclusion.
- Don't invent missing behavior, and don't treat inference as fact.
- If the docs and source **conflict**, report the conflict — don't silently pick
  one.
- The output is an alignment report the human acts on, not a rewritten doc.

## Output

Produce an alignment report with these sections:

```
# Design-to-docs alignment report

## Summary
## Source artifacts reviewed
## Documentation artifacts reviewed
## Matches
## Gaps in the documentation
## Unsupported documentation claims
## Design ambiguities affecting docs
## User experience mismatches
## Missing edge cases or limitations
## Terminology mismatches
## Recommended human decisions
## Questions for confirmation
```
