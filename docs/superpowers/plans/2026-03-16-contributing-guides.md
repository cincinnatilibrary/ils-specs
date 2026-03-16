# Contributing & Maintainer Guides — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add contributor workflow documentation, a maintainer operations guide, and supporting GitHub configuration to the ILS specs repo.

**Architecture:** Two Markdown guides in `specs/contributing/`, a PR template, a root CONTRIBUTING.md pointer, plus integration updates to mkdocs nav, validate-specs.py, AGENTS.md, and specs/README.md. All documentation — no application code.

**Tech Stack:** Markdown, MkDocs Material, YAML front matter, Python (one-line edit to validate-specs.py)

**Design spec:** `docs/superpowers/specs/2026-03-16-contributing-guides-design.md`

---

## File Map

### Files to create

| File | Responsibility |
|------|---------------|
| `specs/contributing/contributing-guide.md` | How both teams edit specs and submit PRs via GitHub web UI |
| `specs/contributing/maintainer-guide.md` | How the ILS Team runs tooling, reviews PRs, manages the framework |
| `.github/PULL_REQUEST_TEMPLATE.md` | Checklist auto-populated on every new PR |
| `CONTRIBUTING.md` (repo root) | Lightweight pointer GitHub auto-surfaces on PRs |

### Files to modify

| File | Change |
|------|--------|
| `scripts/validate-specs.py:33` | Add `"contributing"` to `SKIP_DIRS` |
| `mkdocs.yml:22-34` | Add Contributing section to `nav` |
| `AGENTS.md:15-48` | Update repo structure tree; add cross-reference to contributing guide |
| `specs/README.md` | Add Contributing section with links |

---

## Chunk 1: Scaffolding and GitHub Configuration

### Task 1: Update validate-specs.py SKIP_DIRS

Must happen first so CI doesn't fail when contributing guide files are added.

**Files:**
- Modify: `scripts/validate-specs.py:33`

- [ ] **Step 1: Edit SKIP_DIRS**

Change line 33 from:

```python
SKIP_DIRS = {"guides"}
```

to:

```python
SKIP_DIRS = {"guides", "contributing"}
```

- [ ] **Step 2: Verify validation still passes**

Run: `uv run python scripts/validate-specs.py`
Expected: All existing specs PASS, no errors. The `contributing/` directory is now excluded.

- [ ] **Step 3: Commit**

```bash
git add scripts/validate-specs.py
git commit -m "chore(scripts): add contributing to validate-specs SKIP_DIRS"
```

---

### Task 2: Add PR template

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Create the PR template**

Write `.github/PULL_REQUEST_TEMPLATE.md` with this exact content:

```markdown
## What changed

<!-- Brief description of your changes -->

## Checklist

- [ ] Updated `version` in front matter (PATCH / MINOR / MAJOR)
- [ ] Updated `last_updated` to today's date
- [ ] Added changelog entry
- [ ] Changes follow the [Framework conventions](https://cincinnatilibrary.github.io/ils-specs/FRAMEWORK/)

## Notes for reviewer

<!-- Optional: anything the reviewer should know -->
```

- [ ] **Step 2: Commit**

```bash
git add .github/PULL_REQUEST_TEMPLATE.md
git commit -m "chore(github): add pull request template with spec checklist"
```

---

### Task 3: Add root CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md` (repo root)

- [ ] **Step 1: Create the pointer file**

Write `CONTRIBUTING.md` with this exact content:

```markdown
# Contributing to CHPL ILS Specifications

Thank you for helping improve our ILS specifications.

For a complete guide on how to make changes, submit pull requests,
and what to expect during review, see the
[Contributing Guide](https://cincinnatilibrary.github.io/ils-specs/contributing/contributing-guide/)
on the published site.

For maintainers managing the framework, scripts, and deployments, see the
[Maintainer Guide](https://cincinnatilibrary.github.io/ils-specs/contributing/maintainer-guide/).
```

Note: `CONTRIBUTING.md` is outside the scope of `format-specs.sh` and CI's
mdformat check (which only covers `specs/` and `AGENTS.md`). This is fine —
it's a simple pointer file. If the format script's scope expands in the
future, consider adding `CONTRIBUTING.md` to it.

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add root CONTRIBUTING.md pointing to published guides"
```

---

## Chunk 2: Contributing Guide

### Task 4: Write the contributing guide

This is the primary deliverable. Both teams (Report Assessment Team and ILS Team)
use this document. It assumes GitHub web UI as the primary editing workflow.

**Files:**
- Create: `specs/contributing/contributing-guide.md`

**Reference while writing:**
- `specs/FRAMEWORK.md` — versioning rules (lines 89-93), style guide (lines 222-253)
- `specs/guides/report-guide.md` — for tone and audience calibration
- `specs/reports/slitemdata.md` — concrete example to reference in recipes
- Design spec deliverable 1 (sections 1-7)

- [ ] **Step 1: Write the contributing guide**

Write `specs/contributing/contributing-guide.md` with the following structure.
Use `title`-only front matter (matching `specs/guides/` convention).

```yaml
---
title: Contributing Guide
---
```

**Section 1 — Introduction:**
- One paragraph: what this repo is (ILS specs for CHPL, source of truth for
  business logic)
- Who this guide is for: Report Assessment Team and ILS Team members making
  changes to specifications
- What you'll learn: how to edit specs, what to update, how to submit changes

**Section 2 — Quick Start: Editing a Spec:**
Step-by-step walkthrough of the edit pencil workflow. Numbered steps:
1. Navigate to the spec on the published site
   (https://cincinnatilibrary.github.io/ils-specs/)
2. Click the pencil icon (edit icon) in the top right of the page — this opens
   the file in the GitHub editor
3. Make your changes in the editor
4. Update the required fields (version, last_updated, changelog — covered in
   detail in the next section)
5. Scroll down to the "Propose changes" section
6. Write a brief summary of what you changed and why
7. Select "Create a new branch for this commit and start a pull request"
8. Click "Propose changes", then "Create pull request" on the next screen

**Section 3 — What to Update When You Make a Change:**
Three things every change requires, with a brief explanation and link to
FRAMEWORK.md for full details:

1. **Bump the version** — explain PATCH/MINOR/MAJOR with one-line examples:
   - PATCH (e.g., 0.2.0 → 0.2.1): typos, formatting fixes
   - MINOR (e.g., 0.2.1 → 0.3.0): clarifications, new content that doesn't
     change business logic
   - MAJOR (e.g., 0.3.0 → 1.0.0): changes to business logic or rules
2. **Update `last_updated`** — set to today's date in YYYY-MM-DD format
3. **Add a changelog entry** — format: `- YYYY-MM-DD · vX.Y.Z · Description (Team)`

Link to [Versioning Convention](../FRAMEWORK.md#versioning-convention) for
full details.

**Section 4 — Common Tasks:**
Step-by-step recipes mirroring the Quick Start format. Each recipe states:
the scenario, which fields change, and what version bump to use.

Recipe 1 — **Fixing a typo or wording:**
- What changes: the text content only
- Version bump: PATCH
- Front matter changes: `version` (PATCH bump), `last_updated`
- Changelog: "Fix typo in [section]"

Recipe 2 — **Updating a flag status** (e.g., `proposed` → `confirmed`):
- What changes: the `Status:` line on a flag condition
- Version bump: MINOR (this is a meaningful change — the team is formally
  confirming a rule)
- Front matter changes: `version` (MINOR bump), `last_updated`
- Changelog: "Confirm flag F01 status"

Recipe 3 — **Adding a new flag condition:**
- What changes: a new `### FNN · Title` section added to Flag Conditions
- Version bump: MINOR
- Assign the next available number (flag IDs are never reused)
- Initial status should be `proposed`
- Link to [Report Specification Guide](../guides/report-guide.md) for the
  full flag condition format

Recipe 4 — **Updating report metadata** (schedule, delivery, scope):
- What changes: front matter fields like `schedule`, `output_delivered_to`,
  or body sections like Scope & Audience
- Version bump: MINOR for clarifications, MAJOR if it changes who receives
  the report or fundamentally changes scope

Link to category-specific guides for more detail:
- [Report Specification Guide](../guides/report-guide.md)
- [Code Table Guide](../guides/code-table-guide.md)

**Section 5 — Pull Request Expectations:**
What happens after you submit a PR:
1. **CI checks run automatically** — three checks:
   - Spec validation (front matter fields, cross-references)
   - Formatting check (consistent Markdown style)
   - Site build (ensures the published site still builds)
2. **A maintainer reviews your PR** — they check that version was bumped,
   last_updated is set, changelog entry was added, and the change is correct
3. **Your PR is squash-merged** — all your commits become one clean commit
   in the main branch
4. **Changes go live** — after merge, the site rebuilds and your changes
   appear on the published site within a few minutes

If CI fails, the PR page will show which check failed. Common failures:
- "Missing required field" — you may have deleted a front matter field by
  accident
- "Markdown formatting check failed" — the formatting is slightly off; the
  maintainer can fix this during review
- "Build failed" — a link may be broken; check that any links you added or
  changed are correct

**Section 6 — Commit & PR Conventions:**
- Write a clear, descriptive PR title (e.g., "Fix typo in slitemdata F03
  description" or "Confirm F01 status in slitemdata")
- The PR template will remind you of the checklist items — just fill it in
- Don't worry about commit message format — PRs are squash-merged, so the
  maintainer writes the final commit message

**Section 7 — Getting Help:**
- For questions about spec content (what a report should check, what a code
  means): contact the ILS Team
- For questions about this workflow (how to edit, what went wrong with a PR):
  contact the ILS Team
- Reference the [Framework](../FRAMEWORK.md) and category guides for writing
  conventions

Use horizontal rules (`___` — matching the project convention in FRAMEWORK.md)
to separate major sections.

- [ ] **Step 2: Run formatting**

Run: `./scripts/format-specs.sh`

This ensures the new file matches the project's mdformat configuration.

- [ ] **Step 3: Verify validation passes**

Run: `uv run python scripts/validate-specs.py`
Expected: All existing specs PASS. The contributing guide should NOT appear
in the output (it's in SKIP_DIRS).

- [ ] **Step 4: Verify site builds**

Run: `uv run mkdocs build --strict 2>&1 | tail -5`
Expected: Build succeeds. (The nav entry hasn't been added yet, so the file
won't appear in navigation, but it shouldn't break the build either.)

- [ ] **Step 5: Commit**

```bash
git add specs/contributing/contributing-guide.md
git commit -m "docs(contributing): add contributing guide for spec editors"
```

---

## Chunk 3: Maintainer Guide

### Task 5: Write the maintainer guide

For the ILS Team. Covers local development, scripts, CI, deployment, PR review
workflow, and framework maintenance.

**Files:**
- Create: `specs/contributing/maintainer-guide.md`

**Reference while writing:**
- `scripts/validate-specs.py` — what it checks, how it works
- `scripts/format-specs.sh` — what it does
- `.github/workflows/ci.yml` — CI steps
- `.github/workflows/deploy-pages.yml` — deployment steps
- `.githooks/pre-commit` — hook behavior
- `mkdocs.yml` — site config, `edit_uri`
- `pyproject.toml` — dependencies
- `specs/FRAMEWORK.md` — framework versioning rules
- `specs/schema.yaml` — machine-readable schema
- Design spec deliverable 2 (sections 1-9)

- [ ] **Step 1: Write the maintainer guide**

Write `specs/contributing/maintainer-guide.md` with the following structure.
Use `title`-only front matter:

```yaml
---
title: Maintainer Guide
---
```

**Section 1 — Introduction:**
- Who this is for: ILS Team members who maintain the framework, review PRs,
  and manage the repository
- Prerequisite: read the [Contributing Guide](./contributing-guide.md) first
  — it covers the contributor workflow that this guide builds on

**Section 2 — Repository Overview:**
Brief orientation to key directories and files:

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

**Section 3 — Local Development Setup:**
Numbered steps:
1. Clone the repository: `git clone https://github.com/cincinnatilibrary/ils-specs.git`
2. Install uv (Python package manager): link to https://docs.astral.sh/uv/getting-started/installation/
3. Install dependencies: `uv sync`
4. Enable the pre-commit hook: `git config core.hooksPath .githooks`
   - Note: this project uses a custom hook in `.githooks/pre-commit`, not the
     `pre-commit` framework. The hook runs `mdformat --check` on staged Markdown
     files before each commit.
5. Preview the site locally: `uv run mkdocs serve` — opens at http://127.0.0.1:8000

**Section 4 — Scripts & Tooling:**

**validate-specs.py** (`scripts/validate-specs.py`):
- What it checks: required front matter fields, valid category/status values,
  semver format, cross-reference resolution (`depends_on`/`related_specs`
  point to existing files), schema.yaml/FRAMEWORK.md version alignment
- How to run: `uv run python scripts/validate-specs.py`
- Reading output: `PASS` = no issues; `FAIL` = errors that must be fixed
  (blocks CI); `WARN` = advisory warnings
- Skips non-spec directories (`guides/`, `contributing/`) and root-level
  files (`README.md`, `FRAMEWORK.md`, `glossary.md`, `schema.yaml`)

**format-specs.sh** (`scripts/format-specs.sh`):
- What it does: runs `mdformat` on all Markdown files in `specs/`, plus
  `README.md` and `AGENTS.md` at the repo root
- How to run: `./scripts/format-specs.sh`
- When to run: before committing, or after the pre-commit hook blocks a
  commit due to formatting drift

**mdformat** (manual usage):
- Check formatting without changing files: `uv run mdformat --check specs/`
- Format a single file: `uv run mdformat specs/path/to/file.md`
- Configuration: `.mdformat.toml` (wrap mode, number lists), aligned with
  `.editorconfig` and `.markdownlint.json`

**Section 5 — CI Pipeline:**
What runs on every PR to `main` (`.github/workflows/ci.yml`):

| Step | Command | What it catches |
|------|---------|----------------|
| Validate specs | `uv run python scripts/validate-specs.py` | Missing fields, invalid values, broken cross-references |
| Check formatting | `uv run mdformat --check specs/ AGENTS.md` | Formatting inconsistencies in all Markdown under `specs/` and `AGENTS.md` |
| Build site | `uv run mkdocs build --strict` | Broken links, invalid nav references, MkDocs config errors |

All three steps must pass for a PR to be mergeable. If a step fails, the PR
page shows which step failed and the error output.

**Section 6 — Deployment:**
How the published site gets updated (`.github/workflows/deploy-pages.yml`):
- Triggers automatically on every push to `main` (including PR merges)
- Builds the site with `mkdocs build --strict`
- Deploys to GitHub Pages
- No manual steps required — merge a PR and the site updates within minutes

Note on the edit pencil: the `edit_uri: edit/main/specs/` setting in
`mkdocs.yml` powers the edit icon on every page of the published site. It
constructs a link to the GitHub editor for that file on the `main` branch.
If the branch name or `specs/` directory ever changes, this setting must be
updated to match.

**Section 7 — Reviewing & Merging PRs:**
The gatekeeper workflow:
1. **Check CI status** — all three checks (validate, format, build) must pass.
   If format fails and the content is correct, you can fix formatting locally
   and push to the contributor's branch, or ask them to run the formatter.
2. **Review the diff** — verify:
   - Version was bumped appropriately (PATCH/MINOR/MAJOR)
   - `last_updated` is set to today's (or a recent) date
   - A changelog entry was added
   - The content change is correct
3. **Squash and merge** — use the "Squash and merge" button. Write the squash
   commit message in conventional commit format:
   - `docs(reports): confirm F01 status in slitemdata`
   - `docs(code-tables): fix typo in item-types ITYPE-70 description`
   - `docs(framework): add new schedule convention example`

**Section 8 — Framework Maintenance:**
When and how to update the framework itself:

**FRAMEWORK.md and schema.yaml:**
- These two files must stay in sync. The `framework_version` in `schema.yaml`
  must match the `version` in FRAMEWORK.md front matter.
- The validation script warns if they drift.
- When updating: edit both files, bump the version, and commit together.

**Adding a new spec category:**
1. Add the category to `schema.yaml` under `categories` and `category_folders`
2. Add any category-specific required fields to `required_fields`
3. Add a rule prefix to `rule_prefixes`
4. Update FRAMEWORK.md Document Categories table
5. Create the folder under `specs/` (with a `.gitkeep` if empty)
6. Add a guide stub in `specs/guides/`
7. Add nav entries in `mkdocs.yml`

**Adding a new spec:**
1. Create the file in the appropriate category folder
2. Add it to `specs/README.md` under the right category table
3. Add it to the `nav` section in `mkdocs.yml`
4. Run validation and formatting

**Updating the glossary:**
- Add new `##` headings in `specs/glossary.md` following the existing format
- Terms are linked from specs using `[term](../glossary.md#term-anchor)`

**Section 9 — Repo Settings Recommendations:**
GitHub repository settings that support this workflow (configure in the repo's
Settings > General page):
- **Default merge method:** Set to "Squash and merge" (under Pull Requests).
  Optionally uncheck "Allow merge commits" and "Allow rebase merging" to
  enforce squash-only.
- **Branch protection on `main`:** Require status checks to pass before
  merging. Select the CI checks (validate, format, build).

Use horizontal rules (`___`) between major sections (matching project convention).

- [ ] **Step 2: Run formatting**

Run: `./scripts/format-specs.sh`

- [ ] **Step 3: Verify validation passes**

Run: `uv run python scripts/validate-specs.py`
Expected: All existing specs PASS. The maintainer guide should NOT appear.

- [ ] **Step 4: Verify site builds**

Run: `uv run mkdocs build --strict 2>&1 | tail -5`
Expected: Build succeeds.

- [ ] **Step 5: Commit**

```bash
git add specs/contributing/maintainer-guide.md
git commit -m "docs(contributing): add maintainer guide for ILS Team"
```

---

## Chunk 4: Integration Updates

### Task 6: Update mkdocs.yml navigation

**Files:**
- Modify: `mkdocs.yml:22-34`

- [ ] **Step 1: Add Contributing section to nav**

Replace the current `nav` block (lines 22-34) with:

```yaml
nav:
  - Home: README.md
  - Reference:
      - Framework: FRAMEWORK.md
      - Glossary: glossary.md
  - Guides:
      - Report Specifications: guides/report-guide.md
      - Code Tables: guides/code-table-guide.md
  - Contributing:
      - Contributing Guide: contributing/contributing-guide.md
      - Maintainer Guide: contributing/maintainer-guide.md
  - Reports:
      - reports/slitemdata.md
  - Code Tables:
      - code-tables/location-codes.md
      - code-tables/item-types.md
```

The Reports and Code Tables entries keep their current format (no explicit
titles) to avoid unrelated changes.

- [ ] **Step 2: Verify site builds with new nav**

Run: `uv run mkdocs build --strict 2>&1 | tail -5`
Expected: Build succeeds. The Contributing section now appears in navigation.

- [ ] **Step 3: Preview locally (optional)**

Run: `uv run mkdocs serve`
Verify: Contributing section appears in the left sidebar. Both guides render
correctly. Edit pencil icon works on the contributing guide pages.

- [ ] **Step 4: Commit**

```bash
git add mkdocs.yml
git commit -m "docs(mkdocs): add Contributing section to site navigation"
```

---

### Task 7: Update AGENTS.md

**Files:**
- Modify: `AGENTS.md:15-48` (repo structure tree)

- [ ] **Step 1: Update the repository structure tree**

In the tree diagram (lines 15-48), add the `contributing/` directory under
`specs/`. Insert after the `guides/` entry:

```
    ├── contributing/          # Contributor and maintainer workflow guides
    │   ├── contributing-guide.md  # How to edit specs and submit PRs
    │   └── maintainer-guide.md    # Operations guide for the ILS Team
```

- [ ] **Step 2: Add cross-reference note**

After the "Audience Awareness" section (line 207-end), add a new section:

```markdown
## Human Contributor Guides

For human contributor workflows (how to edit specs, submit PRs, review and
merge), see the [Contributing Guide](https://cincinnatilibrary.github.io/ils-specs/contributing/contributing-guide/)
and [Maintainer Guide](https://cincinnatilibrary.github.io/ils-specs/contributing/maintainer-guide/)
on the published site. This file (AGENTS.md) is the authoritative source for
AI agent procedures.
```

- [ ] **Step 3: Run formatting**

Run: `./scripts/format-specs.sh`

(AGENTS.md is included in the format script's scope.)

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "docs(agents): add contributing directory and cross-reference to contributor guides"
```

---

### Task 8: Update specs/README.md

**Files:**
- Modify: `specs/README.md`

- [ ] **Step 1: Add Contributing section**

After the last line of the "Reference Documents" section (line 20, the
glossary link) and before `## Active Specs` (line 22), add:

```markdown
## Contributing

- [Contributing Guide](contributing/contributing-guide.md) — How to edit specs and submit pull requests
- [Maintainer Guide](contributing/maintainer-guide.md) — Operations guide for the ILS Team
```

- [ ] **Step 2: Run formatting**

Run: `./scripts/format-specs.sh`

- [ ] **Step 3: Commit**

```bash
git add specs/README.md
git commit -m "docs: add contributing section to specs index"
```

---

## Chunk 5: Final Validation

### Task 9: Run full CI checks locally

- [ ] **Step 1: Run validation**

Run: `uv run python scripts/validate-specs.py`
Expected: All specs PASS, no errors. Contributing guides do not appear in output.

- [ ] **Step 2: Run formatting check**

Run: `uv run mdformat --check specs/ AGENTS.md`
Expected: All files pass formatting check.

- [ ] **Step 3: Run strict site build**

Run: `uv run mkdocs build --strict`
Expected: Build succeeds with no warnings or errors. All nav entries resolve.

- [ ] **Step 4: Preview the site**

Run: `uv run mkdocs serve`
Manually verify:
- Contributing section appears in left sidebar navigation
- Contributing Guide renders with all 7 sections
- Maintainer Guide renders with all 9 sections
- Edit pencil icon works on both guide pages
- Links to FRAMEWORK.md, report-guide.md, and code-table-guide.md work
- Horizontal rules render consistently with other pages

- [ ] **Step 5: Verify PR template**

The PR template can't be tested locally — it activates when opening a PR on
GitHub. Verify the file exists at `.github/PULL_REQUEST_TEMPLATE.md` and
contains the expected content.

- [ ] **Step 6: Verify CONTRIBUTING.md**

Confirm `CONTRIBUTING.md` exists at the repo root with links to the published
guide URLs. (GitHub auto-surfaces this when opening PRs and on the repo's
"Contributing" link.)
