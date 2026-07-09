# Socratic Garden

**A docs-centered, human-driven AI environment for engineering teams.**

Socratic Garden helps you use AI to ask better questions before you write the
docs. It doesn't try to automate documentation decisions — it tries to make those
decisions easier to see, discuss, and record.

## What Socratic Garden is

Socratic Garden is a command-line tool. You run a command, it writes a Markdown
**session file**, and you paste that file into whatever AI tool you already use —
ChatGPT, Claude, Cursor, or something else. The session file tells the AI what
you're working on, what role to play, and what to hand back.

It does not call any AI provider itself, and it does not touch your repository
beyond writing those session files. Nothing it produces is final until you say
so.

## What problem it solves

Documentation usually gets written last, once the real decisions are already
buried in code and old chat threads. Socratic Garden treats documentation as part
of the engineering process, not only as an output after implementation. Design
docs capture decisions. User-doc drafts help define the intended user experience.
Internal docs preserve reproduction, testing, and maintenance knowledge.

Writing about a change early tends to expose the parts you haven't actually
decided yet. That is the point: surface unclear assumptions, missing edge cases,
and design gaps while they are still cheap to fix.

## Human-driven AI principles

You stay in charge. Socratic Garden is built so the AI does the legwork and you
make the calls.

Within a session, the AI is meant to:

- ask clarifying questions,
- assemble context and summarize source material,
- point out missing decisions, user-facing implications, and edge cases,
- suggest structure and produce reviewable drafts,
- handle boilerplate.

By default, it should not:

- decide product behavior,
- state unsupported claims as fact,
- edit source files or publish anything,
- treat its own inferences as truth,
- make irreversible decisions for you.

See [docs/philosophy.md](docs/philosophy.md) for the longer version.

## How it relates to documentation-driven development

Socratic Garden reflects a documentation-driven development lifecycle:

1. **Design** — clarify the problem, goals, constraints, and proposed solution;
   create or review design docs; identify decisions and open questions.
2. **Document** — draft user-facing docs early to define the intended experience;
   capture internal notes; use docs to expose gaps.
3. **Develop** — implement once the design direction is clear; docs keep evolving.
4. **Feature finalization / testing** — compare implementation against the
   intended experience; prepare release-note input.
5. **Maintenance** — review and update docs when behavior changes.

Socratic Garden is most useful early — during design and documentation
planning — while the important questions are still open.

## Supported artifact types

Socratic Garden supports more than public user docs. It helps with:

- engineering design docs
- public user documentation drafts
- internal engineering notes
- reproduction / testing notes
- release-note input
- documentation plans
- review reports
- decision and edge-case analysis

## What v0.1 does

- Provides six **agent modes** (human-facing workflows).
- Provides reusable **skills** that agent modes reference.
- Provides **templates** for the expected output artifacts.
- Reads a project **config** file so the environment stays project-agnostic.
- Assembles bounded project **context**.
- Generates timestamped Markdown **session files** you paste into an AI tool.

## What it deliberately does not do

v0.1 does **not**:

- call any AI provider or make network requests,
- run autonomous file-editing agents,
- edit your repository (except `init`, which may create `socratic-garden.yaml`
  and the `.socratic-garden/` work directory),
- act as an MCP server, GitHub app, GitHub Action, or web app,
- propose diffs or open pull requests,
- publish documentation.

This is a personal, early-stage project. It is not production-ready and is not
autonomous.

## Installation / local usage

Requires Python 3.11+. No third-party dependencies are required.

Run directly from a checkout:

```bash
python -m socratic_garden --help
```

Or install it to get the `socratic-garden` console script:

```bash
pip install -e .
socratic-garden --help
```

A `Makefile` provides shortcuts:

```bash
make help
```

## Example workflow

```bash
# 1. Initialize config and the work directory.
python -m socratic_garden init

# 2. Clarify a change. This generates a session file.
python -m socratic_garden clarify --topic "new configuration option"

# 3. Open the generated file under .socratic-garden/sessions/ and paste it
#    into your AI tool. Work through the questions and produce the artifact.

# 4. Review an existing doc, using the example project's config:
python -m socratic_garden review \
  --file examples/minimal-project/docs/example-user-doc.md \
  --config examples/minimal-project/socratic-garden.yaml
```

Available commands:

```bash
socratic-garden init
socratic-garden clarify   --topic "..."
socratic-garden ux        --topic "..."
socratic-garden design    --topic "..."
socratic-garden plan-docs --topic "..."
socratic-garden draft     --topic "..." [--file path/to/brief.md]
socratic-garden review    --file path/to/doc.md
```

All commands accept `--config path/to/socratic-garden.yaml` (default:
`socratic-garden.yaml`).

## Project config example

A project supplies its own context and source locations through
`socratic-garden.yaml`:

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

The config is project-agnostic. Socratic Garden makes no product-specific
assumptions. YAML support uses a built-in minimal parser; installing PyYAML
(`pip install -e ".[yaml]"`) enables full YAML if you need it.

## Agent modes and skills

**Agent modes** are human-facing workflows. Each maps to instructions in
[agents/](agents/):

- **Clarify Change** — clarify a feature idea, behavior change, bug fix, or
  proposal before or during design.
- **Define User Experience** — define the intended user experience for a feature.
- **Design Doc Assistant** — create or review an engineering design document.
- **Documentation Planner** — decide what documentation artifacts are needed.
- **Draft Documentation** — turn goals and plans you have *already defined* into
  a first draft. This is deliberately a boilerplate/scaffolding step: use it
  after clarifying, defining UX, or planning, not as a way to skip that work.
  It will not invent product behavior, and it marks unconfirmed details with
  placeholders for you to resolve.
- **Documentation Reviewer** — review an existing doc against its purpose.

**Skills** are reusable capabilities that agent modes reference, in
[skills/](skills/):

- interview one question at a time
- separate fact from inference
- extract user-facing implications
- identify edge cases
- route documentation artifacts

**Templates** in [templates/](templates/) define the structure of each output
artifact (change brief, user experience brief, design doc outline, documentation
plan, documentation draft, review report).

## Generated artifacts

Each command writes a self-contained Markdown session file under
`.socratic-garden/sessions/` with a timestamped name, for example
`.socratic-garden/sessions/2026-07-09-clarify-new-configuration-option.md`.

A session combines the agent mode instructions, relevant skills, a project config
summary, bounded project context, the output template, a human authority
reminder, and instructions to the AI tool.

The `.socratic-garden/` work directory also contains `context-packs/`, `briefs/`,
`drafts/`, `reviews/`, and `decisions/` folders. In v0.1 only `sessions/` is
actively used; the others exist so the intended artifact model is clear.

**Every session is a working artifact, not a source of truth.** Review everything
the AI produces. You decide what to keep.

## Roadmap

Possible future directions (not implemented yet):

- optional AI provider integration
- a patch proposal mode that creates reviewable diffs
- Git diff / pull-request context mode
- design doc comparison mode
- context update proposals
- artifact validation
- project-specific adapters
- agent packaging for specific tools
- CI support for deterministic checks

## License

See [LICENSE](LICENSE).