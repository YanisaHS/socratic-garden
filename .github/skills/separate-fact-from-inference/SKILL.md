---
name: separate-fact-from-inference
description: 'Keep facts, inferences, guesses, and open questions clearly distinct so the human can trust and review the output. Use whenever summarizing source material, drafting docs, or answering from a codebase, to avoid presenting assumptions as truth.'
---

# Separate fact from inference

Keep these categories clearly distinct in everything you produce:

- **Facts** — statements supported by supplied source material. Point to the
  source when you can.
- **Reasonable inferences** — conclusions drawn from the facts. Label them as
  inferences and state what they rest on.
- **Guesses** — plausible but unsupported ideas. Mark them clearly as guesses.
- **Open questions** — things you do not know and cannot infer.
- **Needs human/SME confirmation** — statements that must be verified by a person
  before they are treated as true.

## Rules

- Never present an inference or a guess as a fact.
- When source material is missing, say so instead of filling the gap with
  invention.
- When you state a fact drawn from source material, note where it came from — a
  file path or line, a doc name, or "confirmed by <person>" — so the reader can
  check it.
- If you are unsure which category something belongs in, treat it as an open
  question.

This separation is what makes the output safe for a human to review and act on.
