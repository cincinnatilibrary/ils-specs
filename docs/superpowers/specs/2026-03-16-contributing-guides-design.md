# Contributing & Maintainer Guides — Design Spec

**Date:** 2026-03-16
**Status:** Approved

## Problem

The ILS Specifications repo has no contributor workflow documentation. The Report
Assessment Team and ILS Team need clear guidance on how to propose changes to
specs, what's expected in a PR, and (for maintainers) how the tooling,
CI pipeline, and deployment work.

## Audience

- **Report Assessment Team** — primary contributors, editing report specs via
  the GitHub web UI
- **ILS Team** — maintainers who also contribute, manage the framework, scripts,
  and deployments

## Approach

**Approach 2: Docs + GitHub configuration.** Two guides in the published site
plus supporting GitHub configuration files.

### Deliverables

#### 1. Contributing Guide (`specs/contributing/contributing-guide.md`)

For both teams. Covers:

1. **Introduction** — What this repo is, "specs as source of truth" in brief,
   who this guide is for
2. **Quick Start: Editing a Spec** — Step-by-step edit pencil workflow:
   find spec on site → click edit icon → make changes → describe changes →
   create branch and PR → submit
3. **What to Update When You Make a Change** — Concise restatement of
   FRAMEWORK.md versioning rules: bump `version` (PATCH/MINOR/MAJOR), update
   `last_updated`, add changelog entry. Links to FRAMEWORK.md for full details.
4. **Common Tasks** — Step-by-step recipes (mirroring the Quick Start format
   with explicit UI actions) for: fixing a typo, updating a flag status,
   adding a new flag condition, updating report metadata. Each recipe shows
   which front matter fields change and what the version bump should be.
   Links to category guides (Report Guide, Code Table Guide) for specifics.
5. **Pull Request Expectations** — CI runs automatically (validation, formatting,
   build). A maintainer reviews and squash-merges. Common CI failure explanations.
   Changes go live after merge.
6. **Commit & PR Conventions** — Descriptive PR titles. PR template checklist
   handles reminders. Don't worry about commit messages (squash merge).
7. **Getting Help** — Who to contact, where to ask questions.

#### 2. Maintainer Guide (`specs/contributing/maintainer-guide.md`)

For ILS Team. Assumes familiarity with the Contributing Guide. Covers:

1. **Introduction** — Audience, prerequisite (read Contributing Guide first)
2. **Repository Overview** — Orientation to repo structure: `specs/`, `scripts/`,
   `.github/workflows/`, `overrides/`, `mkdocs.yml`
3. **Local Development Setup** — Clone, install `uv`, `uv sync`,
   `mkdocs serve` for local preview, pre-commit hook setup via
   `git config core.hooksPath .githooks` (project uses a custom hook, not
   the `pre-commit` framework)
4. **Scripts & Tooling** — `scripts/validate-specs.py` (what it checks, how to
   run, how to read output), `scripts/format-specs.sh` (auto-formatting),
   `mdformat` (manual usage)
5. **CI Pipeline** — What runs on PRs (`ci.yml`): validation → format check
   (covers all Markdown under `specs/`, including contributing guides) →
   strict site build. What each step catches, what failures look like.
6. **Deployment** — How GitHub Pages works (`deploy-pages.yml`): triggers on
   push to main, builds and deploys automatically. No manual steps.
   Document the `edit_uri` setting in `mkdocs.yml` that powers the edit
   pencil icon, so future maintainers understand the dependency.
7. **Reviewing & Merging PRs** — Gatekeeper workflow: check CI status, review
   diff (version bump, `last_updated`, changelog), use "Squash and merge",
   conventional commit format for squash message.
8. **Framework Maintenance** — When/how to update FRAMEWORK.md and schema.yaml
   (keep versions aligned), adding a new spec category, updating the glossary,
   updating mkdocs.yml navigation for new specs.
9. **Repo Settings Recommendations** — Default merge method: squash. Branch
   protection on `main` (require CI to pass).

#### 3. PR Template (`.github/PULL_REQUEST_TEMPLATE.md`)

Auto-populates when anyone opens a PR:

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

#### 4. Root CONTRIBUTING.md

Lightweight pointer GitHub auto-surfaces on PRs:

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

#### 5. Navigation Update (`mkdocs.yml`)

Add new "Contributing" section to nav:

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

Note: The existing Reports and Code Tables entries are left in their current
format (no explicit titles) to avoid unrelated changes in this PR.

#### 6. Validation Script Update (`scripts/validate-specs.py`)

Add `"contributing"` to the `SKIP_DIRS` set so the validator does not attempt
to parse the contributing guides as spec documents:

```python
SKIP_DIRS = {"guides", "contributing"}
```

#### 7. AGENTS.md Update

Update the repository structure tree in AGENTS.md to include the new
`specs/contributing/` directory. Add a cross-reference noting that human
contributor workflows are documented in the Contributing Guide, while
AGENTS.md remains the authoritative source for AI agent procedures.

#### 8. specs/README.md Update

Add a "Contributing" section to the specs index page linking to the
Contributing Guide and Maintainer Guide.

#### 9. Front Matter Convention

Contributing guide files follow the same convention as existing guide files
in `specs/guides/` — minimal front matter with a `title` field only:

```yaml
---
title: Contributing Guide
---
```

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Two separate guides (contributing + maintainer) | Keeps contributor guide approachable; doesn't bury Report Assessment Team in technical details |
| New "Contributing" top-level nav section | Differentiates process docs from content guides |
| GitHub web UI as primary workflow | Matches how both teams work |
| Squash merge as default | Keeps history clean despite many small edits |
| Single gatekeeper review | Current team size; guide documents path to distributing this |
| PR template with checklist | Reduces review burden; reminds contributors of version/date/changelog |
| Root CONTRIBUTING.md as pointer only | Single source of truth on the published site |
| No issue templates (yet) | Can add later if demand arises |
