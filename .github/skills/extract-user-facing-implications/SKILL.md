---
name: extract-user-facing-implications
description: 'Identify how a technical change affects the people who use or operate a system: tasks, terminology, UI/API behavior, errors, setup, migration, support, and docs. Use when clarifying a change, defining user experience, or planning documentation.'
---

# Extract user-facing implications

Given a technical change, work out how it affects the people who use or operate
the system. Walk through each dimension and note where the change lands:

- **Tasks** — what users can now do, must do differently, or can no longer do.
- **Terminology** — new or changed names, labels, and words users encounter.
- **UI / API behavior** — visible changes to screens, commands, or endpoints.
- **Errors** — new failure messages, changed conditions, removed errors.
- **Setup / configuration** — new options, defaults, or required steps.
- **Migration** — what existing users must do to adopt the change.
- **Support** — new questions, tickets, or troubleshooting this may cause.
- **Documentation** — which docs must change and which new docs are needed.

For each impact:

- Note the affected audience (end users, operators, developers, support, etc.).
- Distinguish confirmed impacts from suspected ones.
- List anything you cannot determine as an open question.

The point is to make the human consequences of a technical change visible before
they surprise someone.
