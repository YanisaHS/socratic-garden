# Using Socratic Garden

This guide walks through both ways to use Socratic Garden: the agent modes in an
AI coding tool, and the fallback command-line tool for tools that cannot load
agents directly. For the reasoning behind the design, see
[philosophy.md](philosophy.md).

## Before you start

Socratic Garden lives in a `.github/` folder inside a repository. To use it in
your own project, copy the `.github/agents/` and `.github/skills/` folders from
this repository into your project's `.github/` folder. The command-line tool
also expects the `socratic_garden/` package, so the simplest setup is to work
from a checkout of this repository, or to copy both `.github/` and
`socratic_garden/` into your project.

You need Python 3.11 or later only if you use the command-line tool. The agent
modes need an AI coding tool that reads custom agents, such as VS Code with
GitHub Copilot.

## Using the agent modes

The agent modes are the main way to use Socratic Garden.

1. Open the repository in VS Code with GitHub Copilot.
2. Open the Copilot chat view.
3. Select an agent mode from the mode selector. The available modes are Clarify
   Change, Define User Experience, Design Doc Assistant, Documentation Planner,
   Documentation Reviewer, and Draft Documentation.
4. Describe what you are working on in a sentence or two.
5. Answer the questions the mode asks, one at a time.
6. When the mode has enough, it produces a structured artifact in the chat.
7. Copy the parts you want to keep into your own docs or notes.

The modes use read and search tools only. They read your code and docs to ask
better questions, but they do not edit your files. Nothing they produce is final
until you decide it is.

### What a session looks like

Here is a short example with the Clarify Change mode.

> **You:** I want to add a `--retry` flag to our upload command.
>
> **Clarify Change:** What problem does the retry flag solve for the person
> running the upload today?
>
> **You:** Uploads fail on flaky networks and people have to rerun the whole
> command by hand.
>
> **Clarify Change:** Got it: retries are about surviving transient network
> failures without a full manual rerun. When an upload fails today, does the
> command exit with an error, or does it leave a partial upload behind?

The mode keeps going one question at a time, reflecting each answer back so you
can correct it early. It draws out the goal, who is affected, current versus
intended behavior, the decisions you have made, and the questions still open.
When the picture is clear, it hands you a change brief you can review.

### Choosing a mode

| Start here | When you want to |
| --- | --- |
| **Clarify Change** | Pin down a fuzzy feature idea, behavior change, or bug fix. |
| **Define User Experience** | Decide how a feature should feel to use. |
| **Design Doc Assistant** | Write or pressure-test an engineering design doc. |
| **Documentation Planner** | Decide what docs a change needs and where they go. |
| **Documentation Reviewer** | Check an existing doc against its purpose. |
| **Draft Documentation** | Turn decisions you have already made into a first draft. |

A common path is Clarify Change, then Define User Experience or Design Doc
Assistant, then Documentation Planner, and finally Draft Documentation. Use only
the modes a given change needs.

## Using the command-line tool

Some AI tools cannot load custom agents. For those, the command-line tool
assembles the same agent instructions, skills, and templates into one Markdown
session file you paste into a chat, such as ChatGPT or Claude. The tool does not
call an AI provider and does not edit your source files.

Run it from a checkout of this repository.

### Set up a project

```bash
python -m socratic_garden init
```

This creates `socratic-garden.yaml` and a `.socratic-garden/` work directory.
Edit `socratic-garden.yaml` to describe your project and point at your source
locations. See [the config section in the README](../README.md#project-config)
for the full format.

### See what is available

```bash
python -m socratic_garden modes
python -m socratic_garden skills
```

### Generate a session

```bash
python -m socratic_garden clarify --topic "add a retry flag"
```

This writes a session file under `.socratic-garden/sessions/` with a timestamped
name. Open it, read it, and paste its contents into your AI tool. Work through
the questions the same way you would with an agent mode, then save what you want
to keep.

The session leads with instructions for the AI tool and a reminder that you hold
final authority, then includes your goal, the agent mode instructions, the
relevant skills, a summary of your config, bounded context from your project,
and the output template.

### The commands

```bash
socratic-garden init
socratic-garden modes
socratic-garden skills
socratic-garden clarify   --topic "..."
socratic-garden ux        --topic "..."
socratic-garden design    --topic "..."
socratic-garden plan-docs --topic "..."
socratic-garden draft     --topic "..." [--file path/to/brief.md]
socratic-garden review    --file path/to/doc.md
```

The `review` command reads the file you pass and focuses the session on it. The
`draft` command can take an optional `--file` holding a brief or plan to draft
from. Every session-generating command accepts `--config path/to/config.yaml`;
the default is `socratic-garden.yaml` in the current directory.

The `Makefile` wraps these commands. Run `make help` to see the shortcuts.

## Where output goes

The `.socratic-garden/` work directory holds a `sessions/` folder for generated
session files, plus `context-packs/`, `briefs/`, `drafts/`, `reviews/`, and
`decisions/` folders. Only `sessions/` is written automatically. The others are
there so you have an obvious place to save the artifacts you decide to keep.

## Keeping authority

Every artifact Socratic Garden helps produce is a working draft, not a source of
truth. Read what the AI gives you, correct what is wrong, and keep only what you
agree with. You own the facts, the product behavior, and the final docs.
