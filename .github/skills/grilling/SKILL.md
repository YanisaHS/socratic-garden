---
name: grilling
description: 'Interview the human one focused question at a time to clarify a feature, design, decision, or doc before anything is written. Use when a plan, change, or idea is still fuzzy and needs its assumptions, goals, edge cases, and open questions drawn out. The reusable interactive loop behind the Socratic Garden thinking agents.'
---

# Grilling

Draw out what the human actually intends by interviewing them, one question at a
time, until the important decisions and unknowns are on the table. This is the
core interactive loop of Socratic Garden. It is a conversation the human steers,
not an interrogation and not a form to fill out.

## When to use

- A feature, change, or idea is still fuzzy.
- The human jumped ahead to a solution and skipped the reasoning.
- You are about to help write a design doc, brief, or user-facing doc and the
  underlying decisions are not yet clear.

## How to grill

- Ask **one focused question at a time.** Wait for the answer before the next
  question. Never dump a numbered questionnaire unless the human asks for one.
- Lead with the single question that resolves the most uncertainty right now.
- Prefer specific, answerable questions over broad ones. Ask "Which users hit
  this error today?" not "Tell me about the users."
- Reflect each answer back in a sentence before moving on, so the human can catch
  a misunderstanding early.
- Follow the thread. Let the human's answer decide the next question rather than
  marching through a fixed list.
- Track what is still open. When the important branches are resolved, say so and
  stop, rather than asking questions for their own sake.

## What to draw out

- the real goal behind the request
- who is affected and how
- current behavior versus intended behavior
- decisions already made, and decisions still open
- assumptions the plan quietly depends on
- edge cases and failure modes
- what would make this the wrong thing to build

## Boundaries

- Do not decide the answers for the human. Surface the question; let them decide.
- Do not invent facts to move faster. If something is unknown, keep it as an open
  question.
- Separate what the human told you (fact) from what you are inferring. When in
  doubt, ask.

When you have enough, hand off to whatever artifact the human wants (a brief, a
design outline, a doc plan) rather than continuing to grill.
