"""Filesystem paths and layout for Socratic Garden.

This module centralizes where things live:

* The bundled resources (agent modes, skills, templates) that ship with the
  Socratic Garden package.
* The project-local ``.socratic-garden/`` work directory that Socratic Garden
  creates and writes generated artifacts into.

Keeping these in one place makes the intended artifact model explicit and keeps
the rest of the code free of hard-coded strings.
"""

from __future__ import annotations

from pathlib import Path

# Root of the installed/checked-out project (the parent of this package).
PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent

# Bundled, agent-native resources. These live under .github/ so that opening the
# repository in VS Code exposes the agents and skills directly, and so the whole
# set can be copied into another project's .github/ folder.
#
# NOTE: because these resources live at the repo root rather than inside the
# Python package, the CLI is designed to be run from a checkout of the repo. It
# is a fallback generator for AI tools that do not support agent skills, not the
# primary way to use Socratic Garden.
GITHUB_DIR = REPO_ROOT / ".github"
AGENTS_DIR = GITHUB_DIR / "agents"
SKILLS_DIR = GITHUB_DIR / "skills"
TEMPLATES_DIR = SKILLS_DIR / "documentation-templates" / "assets"

# Default project config filename.
DEFAULT_CONFIG_NAME = "socratic-garden.yaml"

# Default project-local work directory (may be overridden by config).
DEFAULT_WORK_DIR = ".socratic-garden"

# Sub-directories created inside the work directory during ``init``.
# Only ``sessions`` is actively used so far; the rest exist so that the
# intended artifact model is clear.
WORK_SUBDIRS = (
    "sessions",
    "context-packs",
    "briefs",
    "drafts",
    "reviews",
    "decisions",
)


def work_dir(base: Path, configured: str = DEFAULT_WORK_DIR) -> Path:
    """Return the absolute work directory for a project rooted at ``base``."""
    return (base / configured).resolve()


def sessions_dir(base: Path, configured: str = DEFAULT_WORK_DIR) -> Path:
    """Return the directory where generated session files are written."""
    return work_dir(base, configured) / "sessions"
