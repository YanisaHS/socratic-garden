"""Bounded project-context assembly for Socratic Garden.

Context assembly in v0.1 is intentionally small and predictable:

* For each configured source directory, include a short file-tree snippet.
* Include the full content of a file only when it is explicitly supplied
  (for example, the ``--file`` passed to ``review``).
* Skip binary files and avoid reading very large files.
* Handle missing paths gracefully by warning instead of crashing.

The goal is a reviewable, bounded context block, not an exhaustive dump of the
repository. The generated session always reminds the human that they can add
more context manually.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from socratic_garden.config import Config

# Bounds to keep generated sessions reviewable.
MAX_TREE_ENTRIES_PER_SOURCE = 40
MAX_FILE_BYTES = 60_000
BINARY_SNIFF_BYTES = 1024


@dataclass
class ContextResult:
    """Assembled context plus any non-fatal warnings."""

    markdown: str
    warnings: list[str] = field(default_factory=list)


def _looks_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:BINARY_SNIFF_BYTES]
    except OSError:
        return True
    if b"\x00" in chunk:
        return True
    return False


def _iter_files(root: Path, limit: int) -> tuple[list[Path], bool]:
    """Return up to ``limit`` files under ``root`` and whether it was truncated."""
    found: list[Path] = []
    truncated = False
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        # Skip Socratic Garden's own work directory and VCS noise.
        parts = set(path.parts)
        if ".git" in parts or ".socratic-garden" in parts:
            continue
        found.append(path)
        if len(found) >= limit:
            truncated = True
            break
    return found, truncated


def _source_tree(base_dir: Path, rel_path: str, warnings: list[str]) -> str:
    target = (base_dir / rel_path).resolve()
    if not target.exists():
        warnings.append(f"Source path not found (skipped): {rel_path}")
        return f"- `{rel_path}` — not found (skipped)\n"

    if target.is_file():
        return f"- `{rel_path}` (file)\n"

    files, truncated = _iter_files(target, MAX_TREE_ENTRIES_PER_SOURCE)
    if not files:
        return f"- `{rel_path}` — (empty)\n"

    lines = [f"- `{rel_path}`"]
    for path in files:
        try:
            rel = path.relative_to(base_dir)
        except ValueError:
            rel = path
        lines.append(f"    - `{rel.as_posix()}`")
    if truncated:
        lines.append(
            f"    - _...listing truncated at {MAX_TREE_ENTRIES_PER_SOURCE} entries..._"
        )
    return "\n".join(lines) + "\n"


def build_source_context(config: Config) -> ContextResult:
    """Build file-tree snippets for all configured source directories."""
    warnings: list[str] = []
    if not config.sources:
        return ContextResult(
            markdown="_No sources configured. Add paths under `sources:` in your "
            "config to include file listings._\n",
            warnings=warnings,
        )

    blocks: list[str] = []
    for category, paths in config.sources.items():
        pretty = category.replace("_", " ")
        block_lines = [f"**{pretty}:**"]
        if not paths:
            block_lines.append("- _(none configured)_")
        else:
            for rel_path in paths:
                block_lines.append(_source_tree(config.base_dir, rel_path, warnings))
        blocks.append("\n".join(block_lines))

    return ContextResult(markdown="\n".join(blocks).strip() + "\n", warnings=warnings)


def read_file_content(base_dir: Path, file_path: Path) -> ContextResult:
    """Read a specific file's content for inclusion in a review session.

    A relative ``file_path`` is resolved first against the current working
    directory (how the user typed it) and, failing that, against the project's
    ``base_dir``.
    """
    warnings: list[str] = []
    if file_path.is_absolute():
        resolved = file_path.resolve()
    else:
        cwd_candidate = (Path.cwd() / file_path).resolve()
        base_candidate = (base_dir / file_path).resolve()
        resolved = cwd_candidate if cwd_candidate.exists() else base_candidate

    if not resolved.exists():
        return ContextResult(
            markdown=f"_File not found: `{file_path}`_\n",
            warnings=[f"File to review not found: {file_path}"],
        )
    if resolved.is_dir():
        return ContextResult(
            markdown=f"_Path is a directory, not a file: `{file_path}`_\n",
            warnings=[f"Path to review is a directory: {file_path}"],
        )
    if _looks_binary(resolved):
        return ContextResult(
            markdown=f"_Skipped binary file: `{file_path}`_\n",
            warnings=[f"File to review appears to be binary: {file_path}"],
        )

    data = resolved.read_bytes()
    truncated = False
    if len(data) > MAX_FILE_BYTES:
        data = data[:MAX_FILE_BYTES]
        truncated = True
    text = data.decode("utf-8", errors="replace")

    fence = "```"
    body = [
        f"**File:** `{file_path}`",
        "",
        f"{fence}",
        text.rstrip("\n"),
        f"{fence}",
    ]
    if truncated:
        warnings.append(
            f"File truncated to {MAX_FILE_BYTES} bytes for review: {file_path}"
        )
        body.append(
            f"\n_...file truncated at {MAX_FILE_BYTES} bytes. Provide the rest "
            f"manually if needed._"
        )
    return ContextResult(markdown="\n".join(body) + "\n", warnings=warnings)
