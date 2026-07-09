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

# Bundled, read-only resources.
AGENTS_DIR = REPO_ROOT / "agents"
SKILLS_DIR = REPO_ROOT / "skills"
TEMPLATES_DIR = REPO_ROOT / "templates"

# Default project config filename.
DEFAULT_CONFIG_NAME = "socratic-garden.yaml"

# Default project-local work directory (may be overridden by config).
DEFAULT_WORK_DIR = ".socratic-garden"

# Sub-directories created inside the work directory during ``init``.
# Only ``sessions`` is actively used in v0.1; the rest exist so that the
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
