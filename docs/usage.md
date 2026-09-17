# Using Socratic Garden

This guide walks through both ways to use Socratic Garden: the agent modes in an
AI coding tool, and the fallback command-line tool for tools that can't load
agents directly. For the reasoning behind the design, see
[philosophy.md](philosophy.md).

## Before you start

Socratic Garden's agent modes live in `.github/agents/` and its skills in
`.github/skills/`. There are two ways to use them:

- **Try them out.** Clone this repository, run `copilot` from the checkout, and
  the modes act on Socratic Garden's own files. Good for a first look.
- **Use them on your own project.** Install the modes at the personal level so
  they show up in every project you open. Clone this repository once and symlink
  its agent and skill folders into your personal Copilot directories:

  ```bash
  git clone git@github.com:YanisaHS/socratic-garden.git ~/socratic-garden
  mkdir -p ~/.copilot
  ln -s ~/socratic-garden/.github/agents ~/.copilot/agents
  ln -s ~/socratic-garden/.github/skills ~/.copilot/skills
  ```

  Then run `copilot` from your own project and pick a mode with `/agent`. Because
  these are symlinks, a `git pull` in `~/socratic-garden` keeps the modes current
  without copying a snapshot that drifts, and picks up anything added upstream.
  If you already keep your own agents or skills in `~/.copilot/`, link the
  contents instead of the directories; see [installation.md](installation.md).

You need Python 3.11 or later only if you use the command-line tool, which runs
from a checkout of this repository. The agent modes need a tool that reads custom
agents, such as the Copilot CLI.

To install the skills in other tools — Zed, Claude Code, Codex, Cursor, and more —
see [installation.md](installation.md).

## Using the agent modes

The agent modes are the main way to use Socratic Garden. Use them in any tool that
reads custom agents.

With the Copilot CLI, run `copilot` and pick a mode with `/agent`. If you cloned
this repository, run it from the checkout to try the modes on Socratic Garden's
own files; if you installed the modes into `~/.copilot/` (see Before you start),
run it from your own project instead. Any other tool that reads custom agents
works the same way — open the repository in it and select a mode.

### Jump straight into a mode

Picking a mode from the `/agent` menu each time is fine, but you can skip it. The
Copilot CLI takes an `--agent` flag that boots straight into a mode by name:

```bash
copilot --agent "Design Doc Assistant"
```

Both the display name (`"Design Doc Assistant"`) and the file stem
(`design-doc-assistant`) are accepted. Wrap the one you use most in a shell alias:

```bash
alias design='copilot --agent design-doc-assistant'
```

This opens the interactive Copilot TUI already focused on the mode, which grills
you one question at a time. If you'd rather skip the TUI altogether, use the
harness described next.

### Run a mode without the TUI (the harness)

If you'd rather not use the Copilot terminal UI at all, there's a minimal
*harness* — [`bin/sg-chat`](../bin/sg-chat) — that owns the human↔agent loop
itself and renders each turn as plain text. It lets you pick a model, keeps the
conversation coherent, and drives the Copilot CLI headlessly in the background
(`copilot -p`), so you never enter the TUI.

```bash
bin/sg-chat                       # pick a model, then start talking
bin/sg-chat --model auto          # skip the model prompt
bin/sg-chat --draft braindump.md  # start the Design Doc Assistant from a draft
bin/sg-chat --agent "Clarify Change"   # run a different mode
```

What the harness owns, and what it delegates:

- **It owns** the turn loop, model selection, session continuity (one Copilot
  `--session-id` for the whole conversation), and rendering.
- **It delegates** to the Copilot CLI the agent's system prompt (`--agent` injects
  the mode plus its skills), the model call, and the read/search/edit tools.

Inside the loop, agent replies print to stdout and everything else (prompts, the
"thinking" spinner, errors) goes to stderr, so you can pipe a transcript. A few
slash-commands are available: `/model` (switch model, starts a fresh session),
`/new` (clear the conversation), `/session` (show the session id), `/paste`
(multi-line input, end with a lone `.`), and `/exit`.

Requirements and caveats:

- Needs the `copilot` binary on `PATH` and a logged-in Copilot session.
- Unlike the fallback command-line tool below (which never calls an AI provider),
  **the harness does drive an AI** through the Copilot CLI.
- It passes `--allow-all-tools` so the agent can read your draft and search the
  repo without a per-tool prompt; use `--no-tools` to withhold file access. The
  mode still only writes files when you approve it in the conversation.

### Working through a mode

Once a mode is running:

1. Describe what you are working on in a sentence or two.
2. Answer the questions the mode asks, one at a time.
3. When the mode has enough, it produces a structured artifact in the chat.
4. Keep what you want: copy it into your own docs, or ask the mode to write it to
   a file for you and approve the change.

The available modes are Choose a Mode (a guide to the rest), Clarify Change,
Define User Experience, Design Doc Assistant, Documentation Planner, Documentation
Reviewer, and Draft Documentation.

The modes read your code and docs — and your `socratic-garden.yaml` if you have
one — to ask better questions. They produce their artifacts in the chat, and they
can write a draft to a file or update an existing doc when you want to keep it —
but only after you approve the change. Nothing they produce is saved until you
decide it is.

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

| Mode | When you want to |
| --- | --- |
| **Choose a Mode** | Describe what you're working on and get pointed to the right mode. |
| **Clarify Change** | Pin down a fuzzy feature idea, behavior change, or bug fix. |
| **Define User Experience** | Design the experience itself: flow, terminology, failure behavior. |
| **Design Doc Assistant** | Write or pressure-test an engineering design doc, including who it's for. |
| **Documentation Planner** | Decide what docs a change needs and where they go. |
| **Documentation Reviewer** | Check an existing doc, including a design doc, against its purpose. |
| **Draft Documentation** | Turn decisions you have already made into a first draft. |

If you're not sure where to begin, run **Choose a Mode** and answer one question;
it points you to the right mode. A common path is Clarify Change, then Define User
Experience or Design Doc Assistant, then Documentation Planner, and finally Draft
Documentation. Use only the modes a given change needs.

You don't need Define User Experience to keep a design doc from ignoring users:
the Design Doc Assistant establishes who a change is for and what experience it
should enable as part of the design. Reach for Define User Experience when the
experience itself needs designing.

When you move from one mode to the next, treat it as a fresh start. Keep the
artifact the last mode produced — the brief, the design — and hand it to the next
one, rather than switching mid-conversation and expecting it to carry everything.
With the command-line tool, `--file` does this; in a chat tool, start a new
conversation for the next mode and paste or point at the artifact.

### Going round again

Moving forward isn't the only next step. Most artifacts worth having take more
than one pass, and a design doc almost always does: the first session gives you
an outline and a pile of questions, you go away and answer them, and the second
session can push on what you wrote instead of what was missing.

To iterate, start a fresh conversation in the same mode and give it your updated
draft:

```bash
socratic-garden design --topic "retry flag" --file design/retry-flag.md
```

In a chat tool, open the mode again and paste the draft in. Say what you changed
and what you want pushed on — the modes go deeper when they aren't rediscovering
the whole change each time.

Two modes are worth alternating for this. **Design Doc Assistant** asks you
questions and fills gaps; **Documentation Reviewer** reads what you wrote and
tells you what doesn't hold up. Drafting with one and checking with the other
tends to surface different things. Stop when the passes stop changing your mind.

## Using the command-line tool

Some AI tools can't load custom agents. For those, the command-line tool
assembles the same agent instructions, skills, and templates into one Markdown
session file you paste into a chat, such as ChatGPT or Claude. The tool doesn't
call an AI provider and doesn't edit your source files.

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
socratic-garden choose-a-mode
socratic-garden clarify   --topic "..." [--file path/to/prior.md]
socratic-garden ux        --topic "..." [--file path/to/prior.md]
socratic-garden design    --topic "..." [--file path/to/prior.md]
socratic-garden plan-docs --topic "..." [--file path/to/prior.md]
socratic-garden draft     --topic "..." [--file path/to/brief.md]
socratic-garden review    --file path/to/doc.md
```

The `review` command reads the file you pass and focuses the session on it. The
`clarify`, `ux`, `design`, `plan-docs`, and `draft` commands each take an optional
`--file` so you can carry a prior artifact — a brief, a design, or notes — into the
next stage. Every session-generating command accepts `--config path/to/config.yaml`;
the default is `socratic-garden.yaml` in the current directory.

The `Makefile` wraps these commands. Run `make help` to see the shortcuts.

## Where output goes

The `.socratic-garden/` work directory holds a `sessions/` folder for generated
session files. That's the only folder Socratic Garden creates, since it's the only
one it writes to. Keep anything you decide to save in folders of your own choosing
alongside it.

## Keeping authority

Every artifact Socratic Garden helps produce is a working draft, not a source of
truth. Read what the AI gives you, correct what is wrong, and keep only what you
agree with. You own the facts, the product behavior, and the final docs.
