"""Project configuration loading for Socratic Garden.

The project config is a small YAML file (``socratic-garden.yaml``). To keep
Socratic Garden dependency-free, this module ships a minimal YAML *subset*
parser that supports exactly what the documented config format needs:

* nested mappings expressed through indentation,
* block sequences (``- item``),
* scalar values including booleans, integers, and quoted/unquoted strings,
* ``#`` comments and blank lines.

If the optional :mod:`yaml` package (PyYAML) happens to be installed, it is
used instead, since it is a superset of what we support. Either way, no
dependency is required.

The parser deliberately does not implement flow collections, anchors, multi-line
scalars, or other advanced YAML features. If a project needs those, it can
install PyYAML.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    """Raised when a config file is missing or cannot be parsed."""


# ---------------------------------------------------------------------------
# Minimal YAML subset parser
# ---------------------------------------------------------------------------


def _strip_comment(line: str) -> str:
    """Remove a trailing ``#`` comment that is not inside quotes."""
    in_single = in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            # Only treat as a comment if preceded by whitespace or at start.
            if i == 0 or line[i - 1].isspace():
                return line[:i]
    return line


def _parse_scalar(raw: str) -> Any:
    """Convert a scalar token into a Python value."""
    text = raw.strip()
    if not text:
        return ""
    if (text[0] == '"' and text[-1] == '"') or (text[0] == "'" and text[-1] == "'"):
        return text[1:-1]
    lowered = text.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    if lowered in ("null", "~", "none"):
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


@dataclass
class _Line:
    indent: int
    content: str
    number: int


def _tokenize(text: str) -> list[_Line]:
    lines: list[_Line] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = _strip_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append(_Line(indent=indent, content=stripped.strip(), number=number))
    return lines


def _parse_block(lines: list[_Line], start: int, indent: int) -> tuple[Any, int]:
    """Parse a block starting at ``lines[start]`` with the given indent level.

    Returns the parsed value and the index of the next unconsumed line.
    """
    if start >= len(lines):
        return None, start

    first = lines[start]
    if first.content.startswith("- "):
        return _parse_sequence(lines, start, indent)
    if first.content == "-":
        return _parse_sequence(lines, start, indent)
    return _parse_mapping(lines, start, indent)


def _parse_sequence(lines: list[_Line], start: int, indent: int) -> tuple[list[Any], int]:
    items: list[Any] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if line.indent != indent or not (
            line.content == "-" or line.content.startswith("- ")
        ):
            break
        value_part = line.content[1:].strip()
        if value_part:
            items.append(_parse_scalar(value_part))
            i += 1
        else:
            # Nested block belongs to this list item.
            child, i = _parse_block(lines, i + 1, _next_indent(lines, i + 1, indent))
            items.append(child)
    return items, i


def _parse_mapping(lines: list[_Line], start: int, indent: int) -> tuple[dict[str, Any], int]:
    mapping: dict[str, Any] = {}
    i = start
    while i < len(lines):
        line = lines[i]
        if line.indent != indent:
            break
        if line.content.startswith("- "):
            break
        if ":" not in line.content:
            raise ConfigError(f"Line {line.number}: expected 'key: value' mapping")
        key, _, value = line.content.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            mapping[key] = _parse_scalar(value)
            i += 1
        else:
            child_indent = _next_indent(lines, i + 1, indent)
            if child_indent is None or child_indent <= indent:
                mapping[key] = None
                i += 1
            else:
                child, i = _parse_block(lines, i + 1, child_indent)
                mapping[key] = child
    return mapping, i


def _next_indent(lines: list[_Line], index: int, parent_indent: int) -> int | None:
    if index >= len(lines):
        return None
    return lines[index].indent


def _minimal_yaml_load(text: str) -> dict[str, Any]:
    lines = _tokenize(text)
    if not lines:
        return {}
    value, _ = _parse_block(lines, 0, lines[0].indent)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError("Top-level config must be a mapping")
    return value


def _load_yaml(text: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        return _minimal_yaml_load(text)
    loaded = yaml.safe_load(text)
    return loaded or {}


# ---------------------------------------------------------------------------
# Config model
# ---------------------------------------------------------------------------


@dataclass
class Config:
    """Parsed project configuration."""

    project_name: str = "Unnamed project"
    project_description: str = ""
    sources: dict[str, list[str]] = field(default_factory=dict)
    audiences: list[str] = field(default_factory=list)
    rules: dict[str, Any] = field(default_factory=dict)
    work_dir: str = ".socratic-garden"
    # Directory the config file lives in; used as the project root.
    base_dir: Path = field(default_factory=Path)
    config_path: Path | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any], config_path: Path) -> "Config":
        project = data.get("project") or {}
        sources_raw = data.get("sources") or {}
        sources: dict[str, list[str]] = {}
        for key, value in sources_raw.items():
            if value is None:
                sources[key] = []
            elif isinstance(value, list):
                sources[key] = [str(v) for v in value]
            else:
                sources[key] = [str(value)]
        outputs = data.get("outputs") or {}
        return cls(
            project_name=str(project.get("name", "Unnamed project")),
            project_description=str(project.get("description", "")),
            sources=sources,
            audiences=[str(a) for a in (data.get("audiences") or [])],
            rules=dict(data.get("rules") or {}),
            work_dir=str(outputs.get("work_dir", ".socratic-garden")),
            base_dir=config_path.resolve().parent,
            config_path=config_path.resolve(),
            raw=data,
        )


def load_config(config_path: Path) -> Config:
    """Load and parse a project config file.

    Raises :class:`ConfigError` with a helpful message when the file is missing
    or cannot be parsed.
    """
    if not config_path.exists():
        raise ConfigError(
            f"Config file not found: {config_path}\n"
            f"Run 'socratic-garden init' to create one, or pass "
            f"--config path/to/socratic-garden.yaml."
        )
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - unusual IO failure
        raise ConfigError(f"Could not read config file {config_path}: {exc}") from exc
    try:
        data = _load_yaml(text)
    except ConfigError:
        raise
    except Exception as exc:  # pragma: no cover - parser edge cases
        raise ConfigError(f"Could not parse config file {config_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError(f"Config file {config_path} must contain a mapping at the top level")
    return Config.from_dict(data, config_path)


DEFAULT_CONFIG_TEXT = """\
project:
  name: Example Project
  description: A short description of the product, system, or codebase.

sources:
  public_docs:
    - docs/
  design_docs:
    - design/
  internal_docs:
    - internal-docs/
  code:
    - src/

audiences:
  - end users
  - operators
  - developers
  - support engineers

rules:
  human_decides: true
  direct_file_edits: false
  require_source_evidence: true
  public_claims_require_confirmation: true

outputs:
  work_dir: .socratic-garden
"""
