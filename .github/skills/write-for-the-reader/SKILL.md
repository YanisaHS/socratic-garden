---
name: write-for-the-reader
description: 'Turn builder language into reader language. Catch docs that describe how the software was built instead of what the user does and sees: internal component names, implementation detail, feature-flag talk, and architecture the reader never touches. Use when drafting or reviewing user-facing documentation.'
---

# Write for the reader, not the builder

Engineers often write docs the way they built the software, not the way someone
uses it. The result reads like an internal tour of the system instead of a guide
for the person trying to get something done. Catch that and steer it back to the
reader.

## What to look for

- **Internal component names** — modules, services, classes, or subsystems the
  reader never interacts with. Name what the user acts on, not what's behind it.
- **Implementation detail** — how it works under the hood, when the reader only
  needs to know what to do and what happens.
- **Development-state language** — "feature flagged", "behind a rollout", "new in
  the refactor", "temporary until". This is builder context, not user guidance.
- **Architecture framing** — describing the doc around how the system is
  structured rather than around the task the reader wants to finish.
- **Builder's vantage point** — "we added", "the system now supports", instead of
  "you can now".

## How to steer it back

- Lead with the reader's task and goal, not the feature or the code.
- Describe what the user does and what they see or get back.
- Keep internal names and mechanics only where the reader genuinely needs them
  (and then name the concept, not the class).
- Cut development state unless the reader must act on it; if it matters, say what
  they need to do, not how it's wired.
- Prefer "you" and the task over "we" and the implementation.

The test: could a reader who has never seen the codebase follow this and succeed?
If a sentence only makes sense to someone who built it, rewrite it for the reader.
