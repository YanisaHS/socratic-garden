<p align="center">
  <img src="docs/assets/logo.svg" alt="Socratic Garden logo" width="140" height="140">
</p>

<h1 align="center">Socratic Garden</h1>

<p align="center"><strong>A docs-centered, human-driven AI environment for engineering teams.</strong></p>

> *This project is a work in progress.*

Socratic Garden helps engineering teams produce better documentation and better products.

It does this by helping you think a change through: what the change really does, who it
affects, which decisions are still open, and where the reasoning needs improvements.
Working this out gives you clearer design docs, user docs, and internal notes —
and, because the gaps surface early, a better thought-out product at the end.

It's built around agent modes and reusable skills. A mode guides a task, such
as clarifying a change, defining user experience, planning docs, drafting, or
reviewing. Skills provide the reusable habits behind that work: drawing out
unstated assumptions, separating fact from inference, identifying edge cases,
and routing information to the right kind of doc.

The point is to make the thinking behind the documentation clearer, so the
artifacts you keep are easier to trust, revise, and maintain.

Humans remain responsible for product decisions, user experience, technical accuracy, and final documentation.

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

The agent modes are read-only by design: they have read and search tools only, so
they can read your code and docs to ask sharper questions but can't change
anything. You place whatever you decide to keep. That's what keeps the work
human-driven — the environment helps you think without editing your repository on
its own.

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

Writing about a change early exposes the parts you haven't actually decided yet.
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
  skip that work. It doesn't invent product behavior, and it marks unconfirmed
  details with placeholders for you to resolve.

## The skills

Skills are reusable disciplines the modes share, under
[.github/skills/](.github/skills). Each one is a habit of good documentation
work, and the library is meant to grow as new disciplines prove useful.

- **grilling** draws out unstated goals and decisions by interviewing you one
  question at a time.
- **identify-the-audience** fixes who the doc is for before anything is written.
- **separate-fact-from-inference** labels what is known versus assumed.
- **extract-user-facing-implications** turns changes into user-visible effects.
- **identify-edge-cases** surfaces boundaries, failure modes, and gaps.
- **write-for-the-reader** keeps docs about what the user does, not how the
  software was built.
- **define-terminology** keeps names consistent across a doc and the doc set.
- **right-size-the-documentation** matches how much to write to what the reader
  needs.
- **route-documentation-artifacts** decides which docs a change needs.
- **trace-documentation-ripple** finds existing docs a change also affects.
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

By default, it doesn't:

- decide product behavior,
- state unsupported claims as fact,
- edit source files or publish anything,
- treat its own inferences as truth,
- make irreversible decisions for you.

See [docs/philosophy.md](docs/philosophy.md) for the longer version.

## Fallback: the CLI

Some tools don't read custom agents. For those, Socratic Garden includes a small
standard-library CLI that assembles the same agent instructions, skills, and
templates into one Markdown session file you paste into ChatGPT, Claude, or a
similar tool. The CLI doesn't call an AI provider and doesn't edit your source
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

## What it doesn't do

Socratic Garden doesn't:

- edit your repository, by design — the agent modes are read-only, and the CLI
  only ever writes session files (plus `socratic-garden.yaml` and the
  `.socratic-garden/` work directory on `init`),
- run autonomous file-editing agents,
- call any AI provider or make network requests,
- act as an MCP server, GitHub app, GitHub Action, or web app,
- propose diffs or open pull requests,
- publish documentation on your behalf.


## Roadmap

The following are possible future directions and aren't implemented yet.

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
