---
name: trace-documentation-ripple
description: 'Find the existing docs a change touches, not just the obvious new one. A change often ripples into upgrade guides, install and configuration docs, networking or port references, security notes, compatibility and requirements, and troubleshooting. Use when planning docs so downstream docs do not silently go out of date.'
---

# Trace documentation ripple

Engineers usually spot the obvious new document a change needs — a new how-to for
a new feature. What's harder is seeing where the same change quietly invalidates
or extends **existing** docs elsewhere. Trace those ripples so nothing goes stale.

## How to trace

Start from what the change actually does, then follow it outward:

- **What did it add, change, or remove?** A service, a port, a dependency, a
  default, a permission, a step, a limit, a name.
- **Which existing docs state something that is now different?** Search the doc
  set for the old value, the surrounding topic, and adjacent features.
- **Who else's task now includes a new step?** Installers, upgraders, operators,
  integrators.

## Common ripple paths

Use these as prompts, not a checklist to force. Ask which apply:

- **New service or component** → install guide, architecture overview, upgrade
  guide (existing users must add it too), resource/requirements docs.
- **New or changed port, endpoint, or protocol** → networking guide, firewall or
  port reference, security guidance, deployment/reference architecture.
- **New dependency, version, or platform requirement** → requirements and
  compatibility docs, install prerequisites, upgrade notes.
- **Changed default, flag, or config option** → configuration reference, tutorials
  that showed the old default, examples, troubleshooting.
- **New permission, credential, or role** → security docs, setup, operator guide.
- **Renamed or removed thing** → every doc using the old name (see
  define-terminology), redirects, release notes.
- **New failure mode** → troubleshooting and support docs.

## What to produce

For each affected existing doc: name it (or note it needs locating), what
specifically must change, and whether it's blocking for this change or a
follow-up. Where the doc set can't be searched, mark it as a place to check
rather than assuming it's fine.

The goal is that a change updates the whole doc set it touches, not only the one
doc the author first thought of.
