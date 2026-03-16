---
title: Maintainer Guide
---

# Maintainer Guide

______________________________________________________________________

## Introduction

This guide is for **ILS Team members** who maintain the specification
framework, review pull requests, and manage the repository. It covers
the tooling, CI pipeline, deployment process, and operational workflows
that keep the project running.

**Prerequisite:** Read the [Contributing Guide](./contributing-guide.md)
first — it covers the contributor workflow that this guide builds on.
Everything in the contributing guide applies to maintainers too; this
document adds the operational layer on top.

______________________________________________________________________

## Repository Overview

```
ils-specs/
├── specs/                  # All specification documents
│   ├── FRAMEWORK.md        # Common conventions (front matter, versioning, style)
│   ├── schema.yaml         # Machine-readable schema
│   ├── glossary.md         # Controlled vocabulary
│   ├── guides/             # Category-specific writing guides
│   ├── contributing/       # Contributor and maintainer guides (this guide)
│   ├── reports/            # Report specifications
│   ├── code-tables/        # Code table specifications
│   ├── loan-rules/         # Loan rule specifications (planned)
│   ├── workflows/          # Workflow specifications (planned)
│   └── policies/           # Policy specifications (planned)
├── scripts/                # Validation and formatting tools
├── .github/workflows/      # CI and deployment automation
├── .githooks/              # Git hooks (formatting check)
├── overrides/              # MkDocs theme customization
└── mkdocs.yml              # Site configuration
```

______________________________________________________________________

## Local Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cincinnatilibrary/ils-specs.git
   cd ils-specs
   ```

2. **Install uv** (Python package manager):
   Follow the instructions at
   <https://docs.astral.sh/uv/getting-started/installation/>.

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Enable the pre-commit hook:**

   ```bash
   git config core.hooksPath .githooks
   ```

   This project uses a custom hook in `.githooks/pre-commit`, not the
   `pre-commit` framework. The hook runs `mdformat --check` on staged
   Markdown files before each commit. If formatting is off, the commit
   is blocked and the hook tells you to run the formatter.

5. **Preview the site locally:**

   ```bash
   uv run mkdocs serve
   ```

   Opens at <http://127.0.0.1:8000>. The site reloads automatically
   when you save changes to files under `specs/`.

______________________________________________________________________

## Scripts & Tooling

### validate-specs.py

**Location:** `scripts/validate-specs.py`

**What it checks:**

- Required front matter fields are present (per `schema.yaml`)
- `category` and `status` values are valid (per `schema.yaml`)
- `version` follows semver format (MAJOR.MINOR.PATCH)
- `depends_on` and `related_specs` paths resolve to existing files
- `schema.yaml` `framework_version` matches `FRAMEWORK.md` `version`

**How to run:**

```bash
uv run python scripts/validate-specs.py
```

**Reading output:**

- `PASS` — no issues found for that file.
- `FAIL` — errors that must be fixed. Blocks CI.
- `WARN` — advisory warnings. Does not block CI, but should be
  investigated.

The script skips non-spec directories (`guides/`, `contributing/`) and
root-level files (`README.md`, `FRAMEWORK.md`, `glossary.md`,
`schema.yaml`).

### format-specs.sh

**Location:** `scripts/format-specs.sh`

**What it does:** Runs `mdformat` on all Markdown files in `specs/`,
plus `README.md` and `AGENTS.md` at the repository root.

**How to run:**

```bash
./scripts/format-specs.sh
```

**When to run:** Before committing, or after the pre-commit hook blocks
a commit due to formatting drift.

### mdformat (manual usage)

**Check formatting without changing files:**

```bash
uv run mdformat --check specs/ AGENTS.md
```

**Format a single file:**

```bash
uv run mdformat specs/path/to/file.md
```

**Configuration:** `.mdformat.toml` controls wrap mode and number list
formatting, aligned with `.editorconfig` and `.markdownlint.json`.

______________________________________________________________________

## CI Pipeline

The following checks run on every pull request to `main`
(`.github/workflows/ci.yml`):

| Step             | Command                                    | What it catches                                                           |
| ---------------- | ------------------------------------------ | ------------------------------------------------------------------------- |
| Validate specs   | `uv run python scripts/validate-specs.py`  | Missing fields, invalid values, broken cross-references                   |
| Check formatting | `uv run mdformat --check specs/ AGENTS.md` | Formatting inconsistencies in all Markdown under `specs/` and `AGENTS.md` |
| Build site       | `uv run mkdocs build --strict`             | Broken links, invalid nav references, MkDocs config errors                |

All three steps must pass for a PR to be mergeable. If a step fails, the
PR page shows which step failed and the error output.

______________________________________________________________________

## Deployment

The published site is updated automatically
(`.github/workflows/deploy-pages.yml`):

- **Trigger:** Every push to `main` (including PR merges).
- **Build:** Runs `mkdocs build --strict`.
- **Deploy:** Publishes to GitHub Pages.
- **No manual steps required** — merge a PR and the site updates within
  minutes.

**Note on the edit pencil:** The `edit_uri: edit/main/specs/` setting
in `mkdocs.yml` powers the edit icon on every page of the published
site. It constructs a link to the GitHub editor for that file on the
`main` branch. If the branch name or `specs/` directory ever changes,
this setting must be updated to match.

______________________________________________________________________

## Reviewing & Merging PRs

### 1. Check CI status

All three checks must pass before merging. If the formatting check fails
and the content is correct, you can either:

- Fix formatting locally and push to the contributor's branch, or
- Ask the contributor to run `./scripts/format-specs.sh` and push again.

### 2. Review the diff

Verify:

- **Version was bumped appropriately** — PATCH for typos, MINOR for
  clarifications, MAJOR for business logic changes.
- **`last_updated` is set** to today's date (or a recent date).
- **A changelog entry was added** at the bottom of the spec.
- **The content change is correct** — the rule statement, flag
  condition, or code table entry accurately reflects reality.

### 3. Squash and merge

Use the **"Squash and merge"** button. Write the squash commit message
in conventional commit format:

- `docs(reports): confirm F01 status in slitemdata`
- `docs(code-tables): fix typo in item-types ITYPE-70 description`
- `docs(framework): add new schedule convention example`

______________________________________________________________________

## Framework Maintenance

### FRAMEWORK.md and schema.yaml

These two files must stay in sync. The `framework_version` in
`schema.yaml` must match the `version` in FRAMEWORK.md front matter.
The validation script warns if they drift.

**When updating:** Edit both files, bump the version, and commit them
together.

### Adding a new spec category

1. Add the category to `schema.yaml` under `categories` and
   `category_folders`.
2. Add any category-specific required fields to `required_fields`.
3. Add a rule prefix to `rule_prefixes`.
4. Update the FRAMEWORK.md Document Categories table.
5. Create the folder under `specs/` (with a `.gitkeep` if empty).
6. Add a guide stub in `specs/guides/`.
7. Add nav entries in `mkdocs.yml`.

### Adding a new spec

1. Create the file in the appropriate category folder.

2. Add it to `specs/README.md` under the right category table.

3. Add it to the `nav` section in `mkdocs.yml`.

4. Run validation and formatting:

   ```bash
   uv run python scripts/validate-specs.py
   ./scripts/format-specs.sh
   ```

### Updating the glossary

- Add new `##` headings in `specs/glossary.md` following the existing
  format.
- Terms are linked from specs using
  `[term](../glossary.md#term-anchor)`.

______________________________________________________________________

## Repo Settings Recommendations

GitHub repository settings that support this workflow (configure in the
repo's Settings > General page):

- **Default merge method:** Set to "Squash and merge" (under Pull
  Requests). Optionally uncheck "Allow merge commits" and "Allow rebase
  merging" to enforce squash-only.
- **Branch protection on `main`:** Require status checks to pass before
  merging. Select the CI checks (validate, format, build).
