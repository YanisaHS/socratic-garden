---
name: calibrate-scrutiny
description: 'Match the depth of review, questioning, and output to what a change actually warrants. Keep feedback concise by default and escalate to a full, structured treatment only when the stakes, complexity, or blast radius call for it. Use when reviewing, comparing, or grilling, so a small thing gets a small response and a risky thing gets real scrutiny.'
---

# Calibrate scrutiny

Match how hard you push, and how much you write, to what the change deserves. A
one-paragraph edit does not need a full report. A design that others will build
on, or a doc a mistake in which is expensive to reverse, does. The goal is
proportion: enough scrutiny to catch what matters, not so much that a small thing
drowns in process.

## Default to concise

Unless the change clearly warrants more, keep it light:

- Lead with a short verdict and the few things that actually matter.
- Raise the handful of issues worth acting on, not every possible observation.
- Skip empty sections and structured headings the change doesn't need.
- If nothing is wrong, say so plainly instead of manufacturing findings.

Concise is the default because most changes are small, and a wall of feedback on
a small change buries the one thing the reader should notice.

## Escalate when the stakes are real

Push harder, and produce the fuller structured output, when:

- the change is an engineering **design** others will build on,
- a mistake is **expensive or hard to reverse** (data loss, security, migrations,
  public API or contract, published user docs),
- the change is **large, novel, or complex**, or touches many parts,
- **edge cases, failure modes, or tests** are central to whether it's correct,
- the **audience is broad** or the doc is externally published,
- the human **asks for a deep review**.

When several of these are true, do the full treatment: work through the issues
systematically, name the missing decisions and edge cases, and use the structured
report.

## How to decide

Ask two quick questions before choosing depth:

- **What breaks if this is wrong, and how hard is it to undo?** Low and easy →
  keep it brief. High or irreversible → scrutinize.
- **Is this a decision others will rely on?** A throwaway note can be light; a
  load-bearing design or a published doc earns the deeper pass.

## Notes

- Calibrate the *depth*, not the *honesty*. A brief response still flags a real
  blocker; it just doesn't pad it with process.
- State the level you chose if it isn't obvious ("quick pass — this is a small,
  low-stakes edit"), so the human can ask for more.
- When in doubt on something genuinely high-stakes, err toward more scrutiny.
