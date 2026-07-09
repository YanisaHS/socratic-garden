"""Socratic Garden: a docs-centered, human-driven AI environment.

Socratic Garden is a set of AI agent modes and skills (under ``.github/``) that
interview you one question at a time to think through a change before you
document it. This package is the fallback command-line tool: it lists the agent
modes and skills, and assembles them into Markdown session files for AI tools
that cannot load agents directly. It does not call AI providers, edit your
repository, or publish documentation. The human remains the driver and decision
maker.
"""

__version__ = "0.1.0"
