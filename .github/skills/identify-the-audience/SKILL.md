---
name: identify-the-audience
description: 'Decide who a document is actually for before writing it, because the reader changes everything else. Distinguishes end users, operators and deployers, developers and integrators, internal engineering, security and compliance auditors, and support. Use at the start of any documentation work to fix the primary and secondary reader.'
---

# Identify the audience

Before writing anything, work out who the document is for. The same change can
produce very different docs depending on the reader, and most doc problems trace
back to writing for the wrong one — or for several at once without deciding.

## Reader categories

These are common categories, not a fixed list. Name the ones that apply:

- **End users** — use the product to get their own work done.
- **Operators / deployers** — install, configure, and run the software in real
  environments (field engineers, SREs, administrators).
- **Developers / integrators** — build against an API, extend, or embed it.
- **Internal engineering** — the team itself; design docs, architecture, and
  rationale live here.
- **Security / compliance auditors** — need boundaries, guarantees, and evidence
  rather than task steps.
- **Support / success** — troubleshoot and answer questions on someone else's
  behalf.

## What to settle

- **Primary reader** — the one the document must serve. Pick one.
- **Secondary readers** — who else will read it, and what they need that differs.
- **Prior knowledge** — what the reader already knows, so the doc starts in the
  right place.
- **Their task or decision** — what they came to do or decide.
- **What they should not need to understand** — detail this reader can be spared.

## Why it matters

- An operator needs configuration and failure recovery; an end user needs the
  task; an auditor needs guarantees. The same feature, three different docs.
- Writing for "everyone" usually serves no one. If two readers need genuinely
  different things, that is often two documents, not one.

Settle the audience first. Every later choice — depth, terminology, structure,
and how much to write — follows from it.
