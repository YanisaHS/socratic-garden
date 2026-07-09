# Socratic Garden

**A docs-centered, human-driven AI environment for engineering teams.**

> *This project is a work in progress.*

Socratic Garden is a set of AI agent modes and skills that help you produce
better documentation by thinking a change through before you write it up. The
skills are reusable disciplines aimed at documentation quality: drawing out
unstated decisions, separating fact from inference, finding edge cases, and
routing each piece of knowledge to the right kind of doc. An agent mode composes
several of these skills and ends with a reviewable artifact.

The main purpose is thinking that leads to good documentation, not churning out
text. A design doc that comes out of Socratic Garden should reflect a feature
that has actually been thought through: its goals, alternatives, edge cases, and
open questions made explicit. A mode can produce a first draft when you ask, but
its more valuable job is to make sure what you document is worth documenting.

Socratic Garden is meant for engineers and technical writers. Both need a shared,
honest picture of what a change actually does.

## How it works

Socratic Garden lives in a `.github/` folder you can drop into any repository.

- `.github/agents/` holds six custom agent modes you invoke in VS Code Copilot,
  or any tool that reads custom agents.
- `.github/skills/` holds the reusable skills those modes draw on, each a
  discipline for producing better documentation: interviewing, separating fact
  from inference, finding edge cases, routing knowledge to the right doc, and
  more. The set is meant to grow.

Open the repository in VS Code with Copilot and pick an agent mode from the agent
selector, for example **Clarify Change** or **Design Doc Assistant**. The mode
composes the skills it needs, works through the change with you, and produces a
structured artifact from a template.

The agent modes are restricted to read and search tools. They cannot edit your
source files, so the environment helps you think without changing your code
behind your back.

For a full walkthrough of both the agent modes and the command-line tool, see
[docs/usage.md](docs/usage.md).

## Why documentation comes first

Documentation is often written last, after the real decisions are already buried
in code and old chat threads. Socratic Garden treats documentation as part of the
engineering process rather than an output after implementation.

- Design docs record decisions: the problem, the alternatives, and the direction
  chosen.
- User-doc drafts help define the intended user experience.
- Internal docs preserve reproduction, testing, and maintenance knowledge.

Writing about a change early exposes the parts you have not actually decided yet.
That is the point. Unclear assumptions, missing edge cases, and design gaps are
cheapest to fix while they are still questions.

## The agent modes

Each mode is a custom agent under [.github/agents/](.github/agents). A mode
composes the skills it needs and ends with a reviewable artifact.

- **Clarify Change** clarifies a feature idea, behavior change, bug fix, or
  proposal before or during design.
- **Define User Experience** defines the intended user experience for a feature.
- **Design Doc Assistant** creates or reviews an engineering design document.
- **Documentation Planner** decides what documentation artifacts a change needs.
- **Documentation Reviewer** reviews an existing doc against its purpose.
- **Draft Documentation** turns goals and plans you have already defined into a
  first draft. Use it after clarifying, defining UX, or planning, not as a way to
  skip that work. It does not invent product behavior, and it marks unconfirmed
  details with placeholders for you to resolve.

## The skills

Skills are reusable disciplines the modes share, under
[.github/skills/](.github/skills). Each one is a habit of good documentation
work, and the library is meant to grow as new disciplines prove useful.

- **grilling** draws out unstated goals and decisions by interviewing you one
  question at a time.
- **separate-fact-from-inference** labels what is known versus assumed.
- **extract-user-facing-implications** turns changes into user-visible effects.
- **identify-edge-cases** surfaces boundaries, failure modes, and gaps.
- **route-documentation-artifacts** decides which docs a change needs.
- **documentation-templates** holds the output structures every mode produces.
  The templates live under
  [.github/skills/documentation-templates/assets/](.github/skills/documentation-templates/assets).

Grilling is one skill among these, not the whole point. A mode leans on it when a
change is still fuzzy, and on the others when the work is to sort evidence, find
gaps, or route and structure a doc.

To add a skill, create a `SKILL.md`, link it from an agent mode, and it is picked
up automatically. No code changes are required.

## Human-driven AI principles

You stay in charge. Socratic Garden does the legwork so you can make the calls.

Within a session, the AI can:

- ask clarifying questions, one at a time,
- assemble context and summarize source material,
- point out missing decisions, user-facing implications, and edge cases,
- suggest structure and produce reviewable drafts,
- handle boilerplate.

By default, it does not:

- decide product behavior,
- state unsupported claims as fact,
- edit source files or publish anything,
- treat its own inferences as truth,
- make irreversible decisions for you.

See [docs/philosophy.md](docs/philosophy.md) for the longer version.

## Fallback: the CLI

Some tools do not read custom agents. For those, Socratic Garden includes a small
standard-library CLI that assembles the same agent instructions, skills, and
templates into one Markdown session file you paste into ChatGPT, Claude, or a
similar tool. The CLI does not call an AI provider and does not edit your source
files.

The CLI needs Python 3.11+ and no third-party dependencies. The agents, skills,
and templates live at the repository root under `.github/`, so run the CLI from a
checkout of this repository.

```bash
# List what's available.
python -m socratic_garden modes
python -m socratic_garden skills

# Create a config and work directory in your project.
python -m socratic_garden init

# Generate a fallback session to paste into an AI tool.
python -m socratic_garden clarify --topic "new configuration option"

# Review an existing doc, using the example project's config.
python -m socratic_garden review \
  --file examples/minimal-project/docs/example-user-doc.md \
  --config examples/minimal-project/socratic-garden.yaml
```

Commands:

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

All session-generating commands accept `--config path/to/socratic-garden.yaml`.
The default is `socratic-garden.yaml`. A `Makefile` provides shortcuts; run
`make help`.

## Project config

A project supplies its own context and source locations through
`socratic-garden.yaml`, so the environment stays project-agnostic.

```yaml
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
```

YAML support uses a built-in minimal parser. Installing PyYAML
(`pip install -e ".[yaml]"`) enables full YAML if you need it.

## Generated fallback sessions

Each fallback command writes a self-contained Markdown session under
`.socratic-garden/sessions/` with a timestamped name, for example
`.socratic-garden/sessions/2026-07-09-clarify-change-new-configuration-option.md`.

A session leads with how to use it and a human-authority reminder, then combines
your goal, the agent mode instructions, the relevant skills, a project config
summary, bounded project context, and the output template.

Every session is a working artifact, not a source of truth. Review what the AI
produces and decide what to keep.

## What it does not do

Socratic Garden does not:

- call any AI provider or make network requests,
- run autonomous file-editing agents,
- edit your repository, apart from `init`, which may create `socratic-garden.yaml`
  and the `.socratic-garden/` work directory,
- act as an MCP server, GitHub app, GitHub Action, or web app,
- propose diffs or open pull requests,
- publish documentation on your behalf.


## Roadmap

The following are possible future directions and are not implemented yet.

- Adapters that install the agents and skills for other tools, such as Cursor and
  Claude Code.
- A router skill that picks the right mode for you.
- Optional AI provider integration for the fallback path.
- A patch proposal mode that creates reviewable diffs.
- A Git diff or pull-request context mode.
- A design doc comparison mode.
- Artifact validation and CI support for deterministic checks.

## License

See [LICENSE](LICENSE).
