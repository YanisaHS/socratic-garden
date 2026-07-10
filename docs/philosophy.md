# Philosophy

Socratic Garden is a docs-centered, human-driven AI environment. It helps you use
AI to ask better questions before you write the docs. The main purpose is the
thinking a change requires, not the documents it produces. Socratic Garden can
draft a doc when you ask it to, but its more valuable job is to make the
decisions behind a change easy to see, discuss, and record.

## Documentation is a window into the engineering process

Socratic Garden treats documentation as part of the engineering process, not only
as an output after implementation.

- **Design docs capture decisions.** They record the problem, the alternatives,
  the trade-offs, and the direction chosen.
- **User docs drafts help define the intended user experience.** Writing them
  early exposes unclear assumptions and missing decisions.
- **Internal docs preserve reproduction, testing, and maintenance knowledge.**
  They record how engineers reason about and operate the system.

Writing about a change is one of the fastest ways to discover what is still
unclear about it.

## Human-driven by default

The human remains the driver and the decision maker. Socratic Garden supports the
human's skills; it doesn't replace them.

AI can:

- ask clarifying questions,
- assemble context,
- summarize source material,
- identify missing decisions,
- identify user-facing implications,
- identify edge cases,
- suggest documentation structure,
- produce reviewable drafts,
- handle boilerplate,
- write or update files once the human approves the change,
- produce artifacts that humans can edit, accept, reject, or ignore.

AI must not, by default:

- decide product behavior,
- claim unsupported facts,
- silently edit source files,
- publish documentation,
- treat inference as truth,
- make irreversible documentation or design decisions,
- replace human strategy or judgment.

## Documentation-driven development

Socratic Garden reflects a documentation-driven development approach. The rough
lifecycle is:

1. **Design.** Clarify the problem, goals, user needs, constraints, trade-offs,
   and proposed solution. Create or review engineering design documentation.
   Identify decisions and open questions.
2. **Document.** Draft user-facing docs early enough to help define the intended
   user experience. Capture internal docs or engineering notes where needed. Use
   documentation to expose unclear assumptions, missing edge cases, and design
   gaps.
3. **Develop.** Implementation starts after the design direction is sufficiently
   clear. User docs, internal docs, and code-related docs may continue to evolve.
   Design docs generally represent the finalized direction and shouldn't be
   casually rewritten during implementation.
4. **Feature finalization / testing.** Compare implementation against the intended
   user experience and documentation. Identify discrepancies between design,
   implementation, and docs. Prepare release-note input or final public docs.
5. **Maintenance.** Review existing docs when behavior changes. Update public
   docs, internal docs, troubleshooting notes, or design records as needed.

Socratic Garden focuses especially on the early design and documentation-planning
stages, where good questions have the most leverage.

## The artifact model

Every Socratic Garden session produces a **working artifact**, not a source of
truth. You reach it one of two ways.

The primary path is agent-native. You open the repository in a tool that reads
custom agents (such as the Copilot CLI), pick an agent mode, and it works through
the change with you using its skills:

```
Human goal
  → agent mode (.github/agents)
    → reusable skills (.github/skills)
      → project + repository context
        → the mode applies its skills with you (interviewing, sorting evidence,
          finding gaps, structuring the doc)
          → reviewable artifact
            → human decides what to keep
```

The fallback path serves tools without agent-skill support. The CLI assembles the
same instructions, skills, and templates into a session file you paste in:

```
Human goal
  → CLI assembles agent mode + skills + template + bounded context
    → generated session file
      → human runs session in an AI tool
        → reviewable artifact
          → human decides what to keep
```

Either way, the human owns truth, strategy, user experience, and final
documentation. AI handles questioning, synthesis, structure, and boilerplate. The
agent modes can write files and update existing docs, but only with your
approval: they propose a change and you confirm it before anything is saved, so
the human-driven promise is enforced by that approval step rather than left to
good intentions.
