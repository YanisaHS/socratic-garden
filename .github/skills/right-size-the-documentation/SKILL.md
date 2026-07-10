---
name: right-size-the-documentation
description: 'Match the amount of documentation to what the reader actually needs, rather than over- or under-documenting by default. When an interface already makes something clear, prefer lightweight docs; when the path is non-obvious, the stakes are high, or recovery is hard, invest more. Use when planning or drafting docs to decide how much to write.'
---

# Right-size the documentation

Decide how much documentation a feature needs based on the reader's actual need,
not a default habit. The goal is neither maximal coverage nor minimal effort — it
is the right amount for this feature and this reader.

## Two questions to ask first

- **Is the interface already telling the reader this?** A clear UI, a
  well-named command, or a self-describing API often carries its own explanation.
  Documenting what the interface already makes obvious adds noise and goes stale.
- **What goes wrong if this is not documented?** If the answer is "little", keep
  it light. If it is "the reader gets stuck, loses data, or makes an unsafe
  choice", invest more.

## Weigh it up

Lean toward **more** documentation when:

- the path is non-obvious or easy to get wrong,
- the consequences of a mistake are high or hard to reverse,
- the reader can't easily discover the answer by trying,
- setup, sequence, or preconditions matter.

Lean toward **less** when:

- the interface is self-evident and low-stakes,
- the reader learns as fast by doing as by reading,
- the detail would duplicate something already clear elsewhere.

## Notes

- This is a judgment per feature and per audience, not a rule to always or never
  document a given surface (such as a UI). Decide case by case.
- "Less" can still mean a short pointer or a single example rather than nothing.
- Prefer letting the product speak for itself where it genuinely can, and spend
  the documentation effort where the reader actually needs a guide.
