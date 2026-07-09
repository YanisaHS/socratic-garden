"""Command-line interface for Socratic Garden.

Uses only the standard library (:mod:`argparse`). Commands generate Markdown
session files under the project's ``.socratic-garden/sessions/`` directory. No
network or AI calls are made.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from socratic_garden import __version__, paths
from socratic_garden.config import (
    DEFAULT_CONFIG_TEXT,
    Config,
    ConfigError,
    load_config,
)
from socratic_garden.sessions import GeneratedSession, SessionError, generate_session


def _add_config_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--config",
        default=paths.DEFAULT_CONFIG_NAME,
        metavar="PATH",
        help=f"Path to the project config (default: {paths.DEFAULT_CONFIG_NAME}).",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="socratic-garden",
        description=(
            "Socratic Garden: a docs-centered, human-driven AI environment. "
            "Generates Markdown session files to paste into an AI tool. It does "
            "not call AI providers or edit your repository."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"socratic-garden {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="command")

    p_init = sub.add_parser(
        "init", help="Create socratic-garden.yaml and the .socratic-garden/ work dir."
    )
    _add_config_arg(p_init)

    for name, help_text in (
        ("clarify", "Clarify a feature idea, behavior change, bug fix, or proposal."),
        ("ux", "Define the intended user experience for a feature or behavior."),
        ("design", "Create or review an engineering design document."),
        ("plan-docs", "Decide what documentation artifacts are needed."),
    ):
        p = sub.add_parser(name, help=help_text)
        p.add_argument(
            "--topic",
            required=True,
            metavar="TEXT",
            help="The feature, change, or question to work on.",
        )
        _add_config_arg(p)

    p_review = sub.add_parser(
        "review", help="Review an existing documentation artifact."
    )
    p_review.add_argument(
        "--file",
        required=True,
        metavar="PATH",
        help="Path to the documentation file to review.",
    )
    p_review.add_argument(
        "--topic",
        default="",
        metavar="TEXT",
        help="Optional description of what the review should focus on.",
    )
    _add_config_arg(p_review)

    p_draft = sub.add_parser(
        "draft",
        help="Draft a doc from goals/plans you already defined (boilerplate).",
    )
    p_draft.add_argument(
        "--topic",
        required=True,
        metavar="TEXT",
        help="The documentation artifact to draft.",
    )
    p_draft.add_argument(
        "--file",
        default=None,
        metavar="PATH",
        help="Optional brief, plan, or source file to draft from.",
    )
    _add_config_arg(p_draft)

    return parser


def _resolve_config_path(config_arg: str) -> Path:
    return Path(config_arg).expanduser()


def cmd_init(config_arg: str) -> int:
    config_path = _resolve_config_path(config_arg)
    base_dir = config_path.resolve().parent

    created: list[str] = []
    if config_path.exists():
        print(f"Config already exists: {config_path}")
        work_dir_name = _safe_work_dir(config_path)
    else:
        config_path.write_text(DEFAULT_CONFIG_TEXT, encoding="utf-8")
        created.append(str(config_path))
        work_dir_name = paths.DEFAULT_WORK_DIR

    work_root = paths.work_dir(base_dir, work_dir_name)
    for sub in paths.WORK_SUBDIRS:
        target = work_root / sub
        existed = target.exists()
        target.mkdir(parents=True, exist_ok=True)
        if not existed:
            created.append(str(target))

    print("Socratic Garden initialized.")
    if created:
        print("Created:")
        for item in created:
            print(f"  {item}")
    else:
        print("Nothing new to create; everything already existed.")
    print()
    print("Next steps:")
    print("  1. Edit socratic-garden.yaml to describe your project and sources.")
    print('  2. Run a session, e.g. socratic-garden clarify --topic "..."')
    return 0


def _safe_work_dir(config_path: Path) -> str:
    try:
        return load_config(config_path).work_dir
    except ConfigError:
        return paths.DEFAULT_WORK_DIR


def _run_session(command: str, config_arg: str, topic: str, input_file: str | None) -> int:
    config_path = _resolve_config_path(config_arg)
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    file_path = Path(input_file).expanduser() if input_file else None
    try:
        result = generate_session(command, config, topic=topic, input_file=file_path)
    except SessionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    _report(command, config, result)
    return 0


def _report(command: str, config: Config, result: GeneratedSession) -> None:
    for warning in result.warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    print(f"Generated session: {result.path}")
    print()
    print("What to do next:")
    print("  1. Open the session file and skim it.")
    print("  2. Paste its contents into your AI tool (ChatGPT, Claude, Cursor, etc.).")
    print("  3. Work through the questions and produce the artifact.")
    print("  4. Save any output you want to keep under your .socratic-garden/ folders.")
    print()
    print(
        "Reminder: this session is a working artifact. Review everything the AI "
        "produces. You remain the decision maker."
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "init":
        return cmd_init(args.config)

    if args.command == "review":
        topic = args.topic or f"Review the documentation file: {args.file}"
        return _run_session("review", args.config, topic, args.file)

    if args.command == "draft":
        return _run_session("draft", args.config, args.topic, args.file)

    topic = getattr(args, "topic", "")
    return _run_session(args.command, args.config, topic, None)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
