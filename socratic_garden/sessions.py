"""Session generation for Socratic Garden.

A *session* is a self-contained Markdown file that a human pastes into an AI
tool. It combines, in a fixed and reviewable order:

1. Session title
2. User goal / topic
3. Agent mode instructions
4. Relevant reusable skills
5. Project config summary
6. Selected project context (if available)
7. Output template
8. Human authority reminder
9. Instructions to the AI tool

Nothing here calls an AI provider. The file is a working artifact that the
human runs, reviews, and decides what to keep.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from socratic_garden import paths
from socratic_garden.config import Config
from socratic_garden.context import (
    ContextResult,
    build_source_context,
    read_file_content,
)


@dataclass(frozen=True)
class AgentMode:
    """A human-facing workflow that maps to a bundled agent-mode file."""

    key: str
    title: str
    agent_file: str
    skills: tuple[str, ...]
    template_file: str


# Registry of agent modes. Each command in the CLI maps to one of these.
AGENT_MODES: dict[str, AgentMode] = {
    "clarify": AgentMode(
        key="clarify",
        title="Clarify Change",
        agent_file="clarify-change.md",
        skills=(
            "interview-one-question-at-a-time.md",
            "separate-fact-from-inference.md",
            "extract-user-facing-implications.md",
            "identify-edge-cases.md",
            "route-documentation-artifacts.md",
        ),
        template_file="change-brief.md",
    ),
    "ux": AgentMode(
        key="ux",
        title="Define User Experience",
        agent_file="define-user-experience.md",
        skills=(
            "interview-one-question-at-a-time.md",
            "separate-fact-from-inference.md",
            "extract-user-facing-implications.md",
            "identify-edge-cases.md",
        ),
        template_file="user-experience-brief.md",
    ),
    "design": AgentMode(
        key="design",
        title="Design Doc Assistant",
        agent_file="design-doc-assistant.md",
        skills=(
            "interview-one-question-at-a-time.md",
            "separate-fact-from-inference.md",
            "identify-edge-cases.md",
            "extract-user-facing-implications.md",
        ),
        template_file="design-doc-outline.md",
    ),
    "plan-docs": AgentMode(
        key="plan-docs",
        title="Documentation Planner",
        agent_file="documentation-planner.md",
        skills=(
            "route-documentation-artifacts.md",
            "extract-user-facing-implications.md",
            "separate-fact-from-inference.md",
        ),
        template_file="documentation-plan.md",
    ),
    "draft": AgentMode(
        key="draft",
        title="Draft Documentation",
        agent_file="draft-documentation.md",
        skills=(
            "separate-fact-from-inference.md",
            "extract-user-facing-implications.md",
            "route-documentation-artifacts.md",
        ),
        template_file="documentation-draft.md",
    ),
    "review": AgentMode(
        key="review",
        title="Documentation Reviewer",
        agent_file="documentation-reviewer.md",
        skills=(
            "separate-fact-from-inference.md",
            "extract-user-facing-implications.md",
            "identify-edge-cases.md",
        ),
        template_file="review-report.md",
    ),
}


HUMAN_AUTHORITY_REMINDER = """\
This session is a **working artifact**, not a source of truth.

- The human is the driver and the decision maker.
- You (the AI) may ask questions, assemble context, summarize source material,
  identify missing decisions and edge cases, suggest structure, and produce
  reviewable drafts.
- You must **not** decide product behavior, claim unsupported facts, treat
  inference as truth, or present drafts as final.
- Clearly separate facts from inferences, guesses, and open questions.
- Every output here is something the human may edit, accept, reject, or ignore.
"""


AI_TOOL_INSTRUCTIONS = """\
You are being run by a human using **Socratic Garden**, a docs-centered,
human-driven AI environment. The human has pasted this file into you on purpose.

Please:

1. Read the agent mode instructions and the referenced skills below.
2. Use the project config summary and any included context as background.
3. Follow the agent mode. When you need information, ask **one focused question
   at a time** rather than a long questionnaire.
4. When you produce an artifact, follow the output template's structure.
5. Keep facts, inferences, and open questions clearly separated.
6. Do not fabricate product behavior, APIs, file paths, or source material. If
   something is unknown, say so and list it as an open question.
7. Remember that the human reviews and owns every decision.
"""


class SessionError(Exception):
    """Raised when a session cannot be generated."""


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "session"


def _read_resource(directory: Path, name: str) -> str:
    path = directory / name
    if not path.exists():
        raise SessionError(
            f"Missing bundled resource: {path}. Your Socratic Garden checkout may "
            f"be incomplete."
        )
    return path.read_text(encoding="utf-8").rstrip("\n")


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
    """Assemble the full session Markdown for a given agent mode."""
    agent_body = _read_resource(paths.AGENTS_DIR, mode.agent_file)

    skill_sections = []
    for skill_name in mode.skills:
        skill_body = _read_resource(paths.SKILLS_DIR, skill_name)
        skill_sections.append(skill_body)
    skills_block = "\n\n---\n\n".join(skill_sections)

    template_body = _read_resource(paths.TEMPLATES_DIR, mode.template_file)
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
        "(ChatGPT, Claude, Cursor, etc.). It does not call AI providers or edit "
        "your repository.",
        "",
        "## 1. User goal / topic",
        "",
        topic,
        "",
        "## 2. Agent mode instructions",
        "",
        agent_body,
        "",
        "## 3. Relevant skills",
        "",
        skills_block,
        "",
        "## 4. Project config summary",
        "",
        config_summary,
        "",
        "## 5. Selected project context",
        "",
        context.markdown.rstrip("\n"),
        "",
        "_Context is intentionally bounded. Add more relevant files, code, or "
        "source material manually if the AI needs it._",
        "",
        "## 6. Output template",
        "",
        "Produce your artifact using this structure. Adapt headings only if the "
        "human asks you to.",
        "",
        template_body,
        "",
        "## 7. Human authority reminder",
        "",
        HUMAN_AUTHORITY_REMINDER.rstrip("\n"),
        "",
        "## 8. Instructions to the AI tool",
        "",
        AI_TOOL_INSTRUCTIONS.rstrip("\n"),
        "",
    ]
    return "\n".join(parts)


@dataclass
class GeneratedSession:
    """Result of writing a session file to disk."""

    path: Path
    warnings: list[str]


def generate_session(
    command: str,
    config: Config,
    topic: str,
    input_file: Path | None = None,
) -> GeneratedSession:
    """Assemble a session and write it under the project's ``sessions/`` dir.

    ``input_file`` is the file to review (required for ``review``) or an optional
    brief/plan/source file to draft from (for ``draft``).
    """
    mode = AGENT_MODES.get(command)
    if mode is None:
        raise SessionError(f"Unknown agent mode for command: {command}")

    if command == "review":
        if input_file is None:
            raise SessionError("The review command requires a --file argument.")
        context = read_file_content(config.base_dir, input_file)
        # Reviews focus on one file; skip the broader source tree.
    elif command == "draft" and input_file is not None:
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
