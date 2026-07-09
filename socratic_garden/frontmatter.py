"""Parse YAML frontmatter from Markdown resource files.

Agent modes (``*.agent.md``) and skills (``SKILL.md``) carry a small YAML
frontmatter block delimited by ``---`` lines, followed by a Markdown body. This
module extracts the two so the CLI can discover modes and skills by reading their
metadata instead of relying on a hard-coded registry.

The YAML is parsed with the same dependency-free loader used for the project
config (see :mod:`socratic_garden.config`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from socratic_garden.config import _load_yaml


@dataclass
class Document:
    """A Markdown file split into its frontmatter and body."""

    metadata: dict[str, Any] = field(default_factory=dict)
    body: str = ""

    def get_str(self, key: str, default: str = "") -> str:
        value = self.metadata.get(key, default)
        return str(value) if value is not None else default


def parse(text: str) -> Document:
    """Split ``text`` into frontmatter metadata and Markdown body.

    Files without a leading ``---`` frontmatter block are returned with empty
    metadata and the whole text as the body.
    """
    if not text.startswith("---"):
        return Document(metadata={}, body=text.strip("\n"))

    lines = text.splitlines()
    # lines[0] is the opening '---'. Find the closing '---'.
    closing = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing = i
            break
    if closing is None:
        # No closing marker; treat the whole file as body.
        return Document(metadata={}, body=text.strip("\n"))

    front = "\n".join(lines[1:closing])
    body = "\n".join(lines[closing + 1 :]).strip("\n")
    try:
        metadata = _load_yaml(front)
    except Exception:
        metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    return Document(metadata=metadata, body=body)


def load(path: Path) -> Document:
    """Read and parse a Markdown file at ``path``."""
    return parse(path.read_text(encoding="utf-8"))
