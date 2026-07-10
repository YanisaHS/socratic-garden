---
name: assess-quality-attributes
description: 'Weigh a design against the non-functional and enterprise concerns that apply to it — security, privacy, compliance, API and interface contracts, performance, scalability, reliability, operability, usability and accessibility, and specialized environments — as lenses to judge which matter here, not a checklist to cover. Use when creating or reviewing a design so the ones that matter are decided on purpose, not discovered in production.'
---

# Assess quality attributes

Make sure a design accounts for the concerns that decide whether software holds
up in production, not just whether the happy path works. These are easy to skip
while framing a feature and expensive to retrofit once it ships.

Use the dimensions below as **lenses to think through, not a checklist to walk**.
For a given change, judge which ones actually matter, and spend attention there.
A small internal tool or a config-default tweak may touch almost none of them; a
new enterprise-facing service usually touches most. Don't ask about or document a
dimension that doesn't apply here — surfacing an irrelevant concern is its own
kind of noise. Apply this proportionally (see
[calibrate-scrutiny](../calibrate-scrutiny/SKILL.md)).

## Dimensions to consider

- **Security** — authentication and authorization, data protection in transit
  and at rest, secrets handling, input validation, the threat surface the change
  opens or widens, and who can now do what.
- **Privacy and data handling** — what personal or sensitive data is collected,
  where it lives, how long it's kept, and who can see it.
- **Compliance and regulation** — standards or obligations that apply (for
  example data residency, retention, auditability, accessibility law, sector
  rules), and what the design must do to meet them.
- **API and interface design** — the contract other people build against:
  request/response shapes, error semantics, versioning and backward
  compatibility, deprecation, rate limits, and stability guarantees.
- **Performance** — expected load, latency and throughput targets, hot paths,
  and what happens under peak or degraded conditions.
- **Scalability** — how the design behaves as data, users, or traffic grow, and
  where the ceilings are.
- **Reliability and resilience** — failure modes, recovery, retries, timeouts,
  data consistency, and the availability the design is expected to hold.
- **Operability and observability** — how it's deployed, configured, upgraded,
  monitored, and debugged; what logs, metrics, and alerts operators need.
- **Usability and accessibility** — whether the people using it can actually
  succeed, including accessibility for users with disabilities.
- **Specialized and constrained environments** — air-gapped or offline
  deployments, on-premises vs. cloud, specific platforms or architectures,
  resource-limited devices, and regional differences the design must work in.

## How to use it

- For each dimension that applies, ask **one focused question at a time** rather
  than dumping the whole list on the human.
- Don't invent requirements or thresholds. If a target (a latency budget, a
  compliance standard) isn't known, record it as an open question with an owner.
- Separate what's decided from what's assumed from what's still open.
- Where a dimension genuinely doesn't apply, it's fine to note that and move on —
  the goal is a deliberate decision, not a checkbox for its own sake.

The point is to surface these while they're still cheap questions, so a design
for real software has considered how it stays secure, compliant, performant, and
operable — not only how it behaves when everything goes right.
