"""Tests for Socratic Garden.

These tests exercise the fallback session generator and the dynamic discovery of
agent modes and skills from the ``.github/`` resources. They make no network or
AI calls.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from socratic_garden import cli, frontmatter, paths
from socratic_garden.config import DEFAULT_CONFIG_TEXT, SCHEMA_VERSION, load_config
from socratic_garden.sessions import (
    COMMAND_ALIASES,
    SessionError,
    discover_modes,
    discover_skills,
    generate_session,
    resolve_mode,
)


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A minimal initialized project rooted at a temp dir."""
    config_path = tmp_path / "socratic-garden.yaml"
    config_path.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8")
    return config_path


# --- Discovery ------------------------------------------------------------


def test_discover_modes_finds_all_agents() -> None:
    modes = discover_modes()
    # Every short verb alias must resolve to a discovered mode.
    for stem in COMMAND_ALIASES.values():
        assert stem in modes
    clarify = modes["clarify-change"]
    assert clarify.title == "Clarify Change"
    assert clarify.description
    assert clarify.template_path is not None
    assert clarify.template_path.name.endswith(".md")
    # Skills are resolved from the agent body links.
    skill_dirs = {p.parent.name for p in clarify.skill_paths}
    assert "grilling" in skill_dirs


def test_choose_a_mode_is_a_router() -> None:
    router = discover_modes().get("choose-a-mode")
    assert router is not None, "expected a choose-a-mode router mode"
    skill_dirs = {p.parent.name for p in router.skill_paths}
    assert {"choose-a-mode", "grilling"} <= skill_dirs
    # The router points to other modes; it produces no artifact of its own.
    assert router.template_path is None


def test_every_mode_composes_at_least_one_skill() -> None:
    for mode in discover_modes().values():
        assert mode.skill_paths, f"{mode.key} references no skills"


def test_thinking_modes_close_with_a_recap() -> None:
    modes = discover_modes()
    for key in (
        "clarify-change",
        "define-user-experience",
        "design-doc-assistant",
        "documentation-planner",
    ):
        skill_dirs = {p.parent.name for p in modes[key].skill_paths}
        assert "recap-the-session" in skill_dirs, f"{key} should reference recap-the-session"


def test_resolve_mode_accepts_alias_and_stem() -> None:
    assert resolve_mode("clarify").key == "clarify-change"
    assert resolve_mode("clarify-change").key == "clarify-change"


def test_resolve_mode_rejects_unknown() -> None:
    with pytest.raises(SessionError):
        resolve_mode("does-not-exist")


def test_discover_skills_have_frontmatter() -> None:
    skills = discover_skills()
    assert skills, "expected at least one skill"
    names = {doc.get_str("name") for doc in skills}
    assert "grilling" in names
    for doc in skills:
        assert doc.get_str("name")
        assert doc.get_str("description")


def test_all_referenced_skill_files_exist() -> None:
    for mode in discover_modes().values():
        for skill_path in mode.skill_paths:
            assert skill_path.exists(), f"{mode.key} links missing {skill_path}"
        if mode.template_path is not None:
            assert mode.template_path.exists()


# --- Skill format and reachability ----------------------------------------

# Portable Agent Skills naming rule: lowercase letters, digits, and hyphens.
_SKILL_NAME_RE = re.compile(r"[a-z0-9-]+")

# Length ceilings from the Agent Skills format.
_MAX_SKILL_NAME = 64
_MAX_SKILL_DESCRIPTION = 1024

# Skills that no agent links by a SKILL.md reference, but that are still reached
# another way. documentation-templates is loaded through its template assets,
# which agents link directly, rather than through its SKILL.md.
_STANDALONE_SKILLS = {"documentation-templates"}


def _skill_dirs() -> list[Path]:
    return sorted(paths.SKILLS_DIR.glob("*/SKILL.md"))


def test_every_skill_conforms_to_agent_skills_format() -> None:
    skill_paths = _skill_dirs()
    assert skill_paths, "expected at least one skill on disk"
    for skill_path in skill_paths:
        doc = frontmatter.load(skill_path)
        dir_name = skill_path.parent.name
        name = doc.get_str("name")
        description = doc.get_str("description")
        # name and description are both required by the format.
        assert name, f"{dir_name} is missing a 'name'"
        assert description, f"{dir_name} is missing a 'description'"
        # The name must match its directory so hosts load it by folder.
        assert name == dir_name, f"{skill_path}: name '{name}' != directory '{dir_name}'"
        assert _SKILL_NAME_RE.fullmatch(name), (
            f"skill name '{name}' must be lowercase letters, numbers, and hyphens"
        )
        assert len(name) <= _MAX_SKILL_NAME, f"skill name '{name}' exceeds {_MAX_SKILL_NAME} chars"
        assert len(description) <= _MAX_SKILL_DESCRIPTION, (
            f"{dir_name} description exceeds {_MAX_SKILL_DESCRIPTION} chars"
        )


def test_every_skill_is_reachable_from_an_agent() -> None:
    referenced = {
        skill_path.parent.name
        for mode in discover_modes().values()
        for skill_path in mode.skill_paths
    }
    on_disk = {p.parent.name for p in _skill_dirs()}

    unreferenced = on_disk - referenced - _STANDALONE_SKILLS
    assert not unreferenced, (
        "skills not linked by any agent (link them from a mode, or add to "
        f"_STANDALONE_SKILLS if reached another way): {sorted(unreferenced)}"
    )

    # Keep the allow-list honest: every standalone skill must exist and be
    # reachable through a template asset an agent points at.
    template_skills = {
        mode.template_path.parent.parent.name
        for mode in discover_modes().values()
        if mode.template_path is not None
    }
    for name in _STANDALONE_SKILLS:
        assert name in on_disk, f"_STANDALONE_SKILLS lists '{name}', which is not on disk"
        assert name in template_skills, (
            f"'{name}' is allow-listed as standalone but no agent template points into it"
        )


# --- Session generation ---------------------------------------------------


def test_generate_clarify_session(project: Path) -> None:
    config = load_config(project)
    result = generate_session("clarify", config, topic="new config option")
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    # The reordered layout puts guidance and authority before context.
    how_to = text.index("## How to use this session")
    authority = text.index("## Human authority reminder")
    goal = text.index("## User goal / topic")
    context = text.index("## Selected project context")
    template = text.index("## Output template")
    assert how_to < authority < goal < context < template
    assert "new config option" in text


def test_generate_session_is_unique(project: Path) -> None:
    config = load_config(project)
    first = generate_session("clarify", config, topic="same topic")
    second = generate_session("clarify", config, topic="same topic")
    assert first.path != second.path


def test_review_requires_file(project: Path) -> None:
    config = load_config(project)
    with pytest.raises(SessionError):
        generate_session("review", config, topic="", input_file=None)


def test_review_includes_file_content(project: Path, tmp_path: Path) -> None:
    doc = tmp_path / "example.md"
    doc.write_text("# Example\n\nUNIQUE_MARKER_TEXT\n", encoding="utf-8")
    config = load_config(project)
    result = generate_session("review", config, topic="", input_file=doc)
    text = result.path.read_text(encoding="utf-8")
    assert "UNIQUE_MARKER_TEXT" in text


def test_thinking_command_carries_prior_artifact(project: Path, tmp_path: Path) -> None:
    # A prior artifact passed with --file is carried into the next stage's session,
    # not just for review/draft but for the thinking commands too.
    prior = tmp_path / "brief.md"
    prior.write_text("# Brief\n\nCARRIED_ARTIFACT_MARKER\n", encoding="utf-8")
    config = load_config(project)
    result = generate_session("clarify", config, topic="next stage", input_file=prior)
    text = result.path.read_text(encoding="utf-8")
    assert "CARRIED_ARTIFACT_MARKER" in text


def test_missing_source_path_warns_not_fails(project: Path) -> None:
    # The default config points at directories that don't exist in tmp_path.
    config = load_config(project)
    result = generate_session("clarify", config, topic="anything")
    assert result.path.exists()
    # Missing sources should surface as warnings, not exceptions.
    assert isinstance(result.warnings, list)


def test_custom_work_dir_respected(tmp_path: Path) -> None:
    config_path = tmp_path / "socratic-garden.yaml"
    config_path.write_text(
        "project:\n  name: Custom\noutputs:\n  work_dir: .custom-work\n",
        encoding="utf-8",
    )
    config = load_config(config_path)
    result = generate_session("clarify", config, topic="topic")
    assert ".custom-work" in str(result.path)
    assert (tmp_path / ".custom-work" / "sessions").exists()


# --- Project config -------------------------------------------------------


def test_default_config_declares_current_schema_version(project: Path) -> None:
    # DEFAULT_CONFIG_TEXT (written by the fixture) declares a schema_version.
    assert load_config(project).schema_version == SCHEMA_VERSION


def test_config_without_schema_version_defaults(tmp_path: Path) -> None:
    # An older config with no schema_version still loads at the assumed version.
    config_path = tmp_path / "socratic-garden.yaml"
    config_path.write_text("project:\n  name: X\n", encoding="utf-8")
    assert load_config(config_path).schema_version == SCHEMA_VERSION


def test_config_reads_explicit_schema_version(tmp_path: Path) -> None:
    # A declared version is read as-is, so future tooling can branch on it.
    config_path = tmp_path / "socratic-garden.yaml"
    config_path.write_text(
        "schema_version: 2\nproject:\n  name: X\n", encoding="utf-8"
    )
    assert load_config(config_path).schema_version == 2


# --- Frontmatter parser ---------------------------------------------------


def test_frontmatter_parse_splits_metadata() -> None:
    doc = frontmatter.parse("---\nname: Thing\ndescription: A thing.\n---\nBody here.\n")
    assert doc.get_str("name") == "Thing"
    assert doc.get_str("description") == "A thing."
    assert doc.body.strip() == "Body here."


def test_frontmatter_without_metadata_is_all_body() -> None:
    doc = frontmatter.parse("Just body, no frontmatter.\n")
    assert doc.get_str("name") == ""
    assert "Just body" in doc.body


# --- CLI ------------------------------------------------------------------


def test_cli_init_creates_config_and_dirs(tmp_path: Path, capsys) -> None:
    config_path = tmp_path / "socratic-garden.yaml"
    rc = cli.cmd_init(str(config_path))
    assert rc == 0
    assert config_path.exists()
    work_root = paths.work_dir(tmp_path)
    for sub in paths.WORK_SUBDIRS:
        assert (work_root / sub).exists()


def test_cli_modes_lists_agents(capsys) -> None:
    rc = cli.cmd_modes()
    assert rc == 0
    out = capsys.readouterr().out
    assert "Clarify Change" in out


def test_cli_skills_lists_skills(capsys) -> None:
    rc = cli.cmd_skills()
    assert rc == 0
    out = capsys.readouterr().out
    assert "grilling" in out
