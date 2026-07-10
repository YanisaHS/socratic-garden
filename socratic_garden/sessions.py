"""Fallback session generation for Socratic Garden.

The primary way to use Socratic Garden is the agent-native layer under
``.github/`` (custom agents in ``.github/agents/`` and skills in
``.github/skills/``), which a tool such as the Copilot CLI loads directly.

For AI tools that do not support agent skills (for example the plain ChatGPT or
Claude web apps), this module generates a *fallback session*: a single
self-contained Markdown file that bundles one agent mode, the skills it
references, the project config, bounded context, and the output template, so it
can be pasted into any chat.

Modes and their skills are discovered by reading the ``.github/`` resource files
and the Markdown links inside each agent, so adding a skill or re-wiring a mode
is a Markdown edit and needs no code change here.

Nothing in this module calls an AI provider. The generated file is a working
artifact the human runs, reviews, and decides what to keep.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from socratic_garden import frontmatter, paths
from socratic_garden.config import Config
from socratic_garden.context import (
    ContextResult,
    build_source_context,
    read_file_content,
)


@dataclass(frozen=True)
class AgentMode:
    """A human-facing workflow, discovered from a ``*.agent.md`` file."""

    key: str  # filename stem, e.g. "clarify-change"
    title: str
    description: str
    agent_path: Path
    skill_paths: tuple[Path, ...]
    template_path: Path | None


# Short CLI verbs mapped to agent filename stems. The verbs are for ergonomics;
# the stem itself also works as a command. Everything else about a mode (its
# skills and template) is discovered from the agent file, so adding a skill
# needs no change here.
COMMAND_ALIASES: dict[str, str] = {
    "clarify": "clarify-change",
    "ux": "define-user-experience",
    "design": "design-doc-assistant",
    "plan-docs": "documentation-planner",
    "draft": "draft-documentation",
    "review": "documentation-reviewer",
}

_AGENT_SUFFIX = ".agent.md"
_LINK_RE = re.compile(r"\]\(([^)]+)\)")


class SessionError(Exception):
    """Raised when a session cannot be generated."""


def _parse_links(body: str, agent_path: Path) -> tuple[list[Path], Path | None]:
    """Extract skill and template paths from an agent body's Markdown links."""
    skill_paths: list[Path] = []
    template_path: Path | None = None
    seen: set[str] = set()
    for match in _LINK_RE.finditer(body):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "#")):
            continue
        resolved = (agent_path.parent / target).resolve()
        posix = resolved.as_posix()
        if resolved.name == "SKILL.md":
            if posix not in seen:
                seen.add(posix)
                skill_paths.append(resolved)
        elif template_path is None and "/assets/" in posix and resolved.suffix == ".md":
            template_path = resolved
    return skill_paths, template_path


def discover_modes() -> dict[str, AgentMode]:
    """Discover all agent modes under ``.github/agents/``."""
    modes: dict[str, AgentMode] = {}
    if not paths.AGENTS_DIR.exists():
        raise SessionError(
            f"Agents directory not found: {paths.AGENTS_DIR}. Run the CLI from a "
            f"checkout of the Socratic Garden repository."
        )
    for agent_path in sorted(paths.AGENTS_DIR.glob(f"*{_AGENT_SUFFIX}")):
        doc = frontmatter.load(agent_path)
        key = agent_path.name[: -len(_AGENT_SUFFIX)]
        title = doc.get_str("name", key)
        description = doc.get_str("description")
        skill_paths, template_path = _parse_links(doc.body, agent_path)
        modes[key] = AgentMode(
            key=key,
            title=title,
            description=description,
            agent_path=agent_path,
            skill_paths=tuple(skill_paths),
            template_path=template_path,
        )
    return modes


def resolve_mode(command: str, modes: dict[str, AgentMode] | None = None) -> AgentMode:
    """Resolve a CLI command (short verb or stem) to a discovered mode."""
    modes = modes if modes is not None else discover_modes()
    key = COMMAND_ALIASES.get(command, command)
    mode = modes.get(key)
    if mode is None:
        available = ", ".join(sorted(COMMAND_ALIASES)) or "(none)"
        raise SessionError(
            f"Unknown agent mode for command '{command}'. Available: {available}."
        )
    return mode


def discover_skills() -> list[frontmatter.Document]:
    """Discover all skills under ``.github/skills/`` (each ``<name>/SKILL.md``)."""
    skills: list[frontmatter.Document] = []
    if not paths.SKILLS_DIR.exists():
        return skills
    for skill_path in sorted(paths.SKILLS_DIR.glob("*/SKILL.md")):
        skills.append(frontmatter.load(skill_path))
    return skills


HOW_TO_USE_SESSION = """\
You are being run inside **Socratic Garden**, a docs-centered, human-driven AI
environment. A human generated this file and pasted it to you on purpose. This is
the fallback path for tools without native agent-skill support.

Behave as follows:

1. Take on the agent mode described below and follow its instructions.
2. When you need information, ask **one focused question at a time** — not a long
   questionnaire.
3. Do not invent product behavior, APIs, commands, file paths, or history. If
   something is unknown, say so and record it as an open question.
4. Keep facts, inferences, guesses, and open questions clearly separated.
5. Use the project config and included context as background; ask for more if you
   need it.
6. When you produce an artifact, follow the output template's structure.
7. Produce a reviewable draft, never final truth. The human decides what to keep.
"""


HUMAN_AUTHORITY_REMINDER = """\
The human owns the facts, the strategy, the product behavior, the user
experience, and every final documentation decision.

- You may ask questions, assemble context, summarize source material, identify
  missing decisions and edge cases, suggest structure, and produce drafts.
- You must **not** decide product behavior, state unsupported claims as fact,
  edit files or publish anything without the human's explicit approval, or treat
  your own inferences as truth.
- Everything you produce here is something the human may edit, accept, reject, or
  ignore.
"""


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "session"


def _read_body(path: Path) -> str:
    """Read a resource file and return its Markdown body without frontmatter."""
    if not path.exists():
        raise SessionError(
            f"Missing bundled resource: {path}. Your Socratic Garden checkout may "
            f"be incomplete."
        )
    return frontmatter.load(path).body.rstrip("\n")


def _config_summary(config: Config) -> str:
    lines = [
        f"- **Project name:** {config.project_name}",
        f"- **Description:** {config.project_description or '_(none provided)_'}",
    ]
    if config.audiences:
        audiences = ", ".join(config.audiences)
    else:
        audiences = "_(none configured)_"
    lines.append(f"- **Audiences:** {audiences}")

    if config.sources:
        lines.append("- **Source categories:**")
        for category, source_paths in config.sources.items():
            pretty = category.replace("_", " ")
            joined = ", ".join(f"`{p}`" for p in source_paths) or "_(none)_"
            lines.append(f"    - {pretty}: {joined}")
    else:
        lines.append("- **Source categories:** _(none configured)_")

    if config.rules:
        lines.append("- **Rules:**")
        for key, value in config.rules.items():
            lines.append(f"    - {key.replace('_', ' ')}: {value}")
    return "\n".join(lines)


def build_session_markdown(
    mode: AgentMode,
    config: Config,
    topic: str,
    context: ContextResult,
) -> str:
    """Assemble the full fallback-session Markdown for a given agent mode."""
    agent_body = _read_body(mode.agent_path)

    skill_sections = [_read_body(path) for path in mode.skill_paths]
    skills_block = "\n\n---\n\n".join(skill_sections) if skill_sections else (
        "_This mode references no separate skills._"
    )

    if mode.template_path is not None:
        template_body = _read_body(mode.template_path)
    else:
        template_body = "_This mode has no fixed output template._"
    config_summary = _config_summary(config)

    parts = [
        f"# Socratic Garden session: {mode.title}",
        "",
        f"- **Agent mode:** {mode.title}",
        f"- **Topic / goal:** {topic}",
        f"- **Project:** {config.project_name}",
        f"- **Generated:** {date.today().isoformat()}",
        "",
        "> Socratic Garden generated this file for you to paste into an AI tool "
        "(ChatGPT, Claude, etc.). It does not call AI providers or edit your "
        "repository. If your tool supports agent skills, use the agents under "
        "`.github/` instead.",
        "",
        "## How to use this session",
        "",
        HOW_TO_USE_SESSION.rstrip("\n"),
        "",
        "## Human authority reminder",
        "",
        HUMAN_AUTHORITY_REMINDER.rstrip("\n"),
        "",
        "## User goal / topic",
        "",
        topic,
        "",
        "## Agent mode instructions",
        "",
        agent_body,
        "",
        "## Relevant skills",
        "",
        skills_block,
        "",
        "## Project config summary",
        "",
        config_summary,
        "",
        "## Selected project context",
        "",
        context.markdown.rstrip("\n"),
        "",
        "_Context is intentionally bounded. Add more relevant files, code, or "
        "source material manually if the AI needs it._",
        "",
        "## Output template",
        "",
        "Produce your artifact using this structure. Adapt headings only if the "
        "human asks you to.",
        "",
        template_body,
        "",
    ]
    return "\n".join(parts)


@dataclass
class GeneratedSession:
    """Result of writing a session file to disk."""

    path: Path
    warnings: list[str] = field(default_factory=list)


def generate_session(
    command: str,
    config: Config,
    topic: str,
    input_file: Path | None = None,
) -> GeneratedSession:
    """Assemble a fallback session and write it under the project's sessions dir.

    ``input_file`` is the file to review (required for ``review``) or an optional
    brief/plan/source file to draft from (for ``draft``).
    """
    mode = resolve_mode(command)

    if command in ("review", "documentation-reviewer"):
        if input_file is None:
            raise SessionError("The review command requires a --file argument.")
        context = read_file_content(config.base_dir, input_file)
        # Reviews focus on one file; skip the broader source tree.
    elif command in ("draft", "draft-documentation") and input_file is not None:
        # Draft from an already-defined brief/plan/source file.
        context = read_file_content(config.base_dir, input_file)
    else:
        context = build_source_context(config)

    markdown = build_session_markdown(mode, config, topic, context)

    out_dir = paths.sessions_dir(config.base_dir, config.work_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug_source = input_file.name if input_file is not None else topic
    filename = f"{date.today().isoformat()}-{mode.key}-{_slugify(str(slug_source))}.md"
    out_path = _unique_path(out_dir / filename)
    out_path.write_text(markdown, encoding="utf-8")

    return GeneratedSession(path=out_path, warnings=context.warnings)


def _unique_path(path: Path) -> Path:
    """Avoid clobbering an existing session generated on the same day."""
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1
