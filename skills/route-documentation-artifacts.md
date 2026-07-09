# Skill: Route documentation artifacts

Help decide where a piece of knowledge belongs. Not everything needs public docs,
and not everything needs docs right now. Route each item to one or more of:

- **Design docs** — decisions, rationale, trade-offs, and constraints.
- **Public user docs** — tasks, concepts, and reference users need.
- **Internal engineering docs** — how the system is built, reproduced, and
  maintained.
- **Release notes** — user-visible changes to announce at release time.
- **Troubleshooting docs** — known issues, errors, and their resolutions.
- **No docs yet** — nothing to write at this stage (note why).

Guidance:

- Prefer the smallest set of artifacts that captures the knowledge well.
- If routing depends on an unknown, mark it as needing SME clarification.
- Distinguish "needed now" from "needed later", and note the trigger for later.
- Point to the likely source of truth for each item so it does not get
  duplicated inconsistently.

The output is a routing decision the human can review, not a mandate to write
everything.
