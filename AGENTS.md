# AGENTS.md — AI Agent Instructions for ils-specs

## What This Repository Is

This is the **ILS Specification Framework** for Cincinnati & Hamilton County
Public Library (CHPL). It contains structured Markdown specification documents
that define business logic for the library's Integrated Library System (Sierra).

**Core principle: Specifications are the source of truth.** The system should
reflect what the specs say, not the other way around. Never suggest that a spec
should be updated to match current system behavior unless explicitly asked.

## Repository Structure

```
ils-specs/
├── AGENTS.md                  # This file — agent instructions
├── README.md                  # Human-readable project overview
├── .editorconfig              # Editor settings (indentation, line endings)
├── .markdownlint.json         # markdownlint config aligned with mdformat
├── .mdformat.toml             # mdformat config (wrap, numbering)
├── .gitignore
├── pyproject.toml             # Python project config (uv)
├── uv.lock                    # Locked dependencies
├── .githooks/
│   └── pre-commit             # Markdown formatting check
├── scripts/
│   ├── validate-specs.py      # Front matter and cross-reference validator
│   └── format-specs.sh        # Auto-format all markdown files
└── specs/
    ├── README.md              # Reader entry point with navigable index
    ├── FRAMEWORK.md           # How to write specs — format, schema, style guide
    ├── glossary.md            # Controlled vocabulary with anchored terms
    ├── schema.yaml            # Machine-readable schema (categories, statuses, etc.)
    ├── reports/               # Report specifications
    ├── code-tables/           # Code table specifications
    ├── loan-rules/            # Loan rule specifications
    ├── workflows/             # Workflow specifications
    └── policies/              # Policy specifications
```

## Key Files You Must Read Before Modifying Specs

1. **`specs/FRAMEWORK.md`** — the authoritative guide for spec format, front
   matter schema, body sections, rules format, and style guide. All specs must
   conform to this framework.
2. **`specs/schema.yaml`** — machine-readable companion to FRAMEWORK.md. If you
   change valid categories, statuses, or required fields, update both files and
   keep their versions aligned.
3. **`specs/glossary.md`** — controlled vocabulary. Link to it when using terms
   that have specific meanings (e.g., "hold-filled", "item type", "suppressed").

## Working with Specs

### Creating a New Spec

1. Read `specs/FRAMEWORK.md` for the format
2. Determine the category (`report`, `code-table`, `loan-rule`, `workflow`, `policy`)
3. Create the file at `specs/{category-folder}/{id}.md`
4. Include all required front matter fields (see `schema.yaml` for the list)
5. Follow the body section structure for that category
6. Add the spec to the index table in `specs/README.md`
7. Run validation: `uv run python scripts/validate-specs.py`
8. Run formatting: `./scripts/format-specs.sh`

### Modifying an Existing Spec

1. Read the spec and understand its current state
2. Make changes following the framework style guide
3. **Bump the version** — PATCH for typos, MINOR for clarifications, MAJOR for
   business logic changes
4. **Update `last_updated`** to today's date
5. **Add a change log entry** at the bottom of the spec
6. Run validation: `uv run python scripts/validate-specs.py`
7. Run formatting: `./scripts/format-specs.sh`

### Cross-Referencing

Specs reference each other in two ways:

- **Front matter** (`depends_on`, `related_specs`): use `category-folder/id`
  format (e.g., `code-tables/location-codes`)
- **Body prose**: use relative Markdown links (e.g.,
  `[Location Codes](../code-tables/location-codes.md)`)
- **Glossary**: link with `[term](../glossary.md#term-anchor)` from category
  folders, `[term](./glossary.md#term-anchor)` from specs root

### Adding Glossary Terms

Add new terms when a word has a specific meaning in this context that could be
misread. Each term is an `##` heading in `glossary.md`. See the existing entries
for the format (definition, "not to be confused with", Sierra context).

## Tooling

### Validation

```bash
uv run python scripts/validate-specs.py
```

This checks all spec files for:

- Required front matter fields
- Valid category and status values
- Semver format
- Cross-reference resolution (depends_on, related_specs)
- Version alignment between schema.yaml and FRAMEWORK.md

**Always run this before committing spec changes.**

### Formatting

```bash
uv run mdformat --check specs/    # Check formatting
./scripts/format-specs.sh          # Auto-format all spec files
```

Markdown formatting is enforced by a pre-commit hook that runs `mdformat --check`
on staged `.md` files. If the hook blocks your commit, run the format script and
re-stage.

Configuration lives in `.mdformat.toml`. Plugins: `mdformat-frontmatter` (YAML
front matter) and `mdformat-gfm` (GFM tables).

Editor config (`.editorconfig`) and markdownlint config (`.markdownlint.json`)
are checked in and aligned with mdformat — don't modify them independently.

### Dependencies

This is a `uv`-managed Python project. Dependencies are declared in
`pyproject.toml` and locked in `uv.lock`.

```bash
uv sync          # Install dependencies
uv run <cmd>     # Run commands in the project environment
```

## Commit Message Format

Use conventional commits:

```
docs(reports): add slmissing specification
docs(code-tables): update location-codes with new branch codes
feat(scripts): add glossary link checker
chore: bump framework version to 1.1.0
```

- `docs` for spec content changes
- `feat` for new tooling
- `fix` for corrections to tooling
- `chore` for maintenance (version bumps, index updates, .gitkeep cleanup)

Scope is the category folder or `scripts` for tooling changes.

## What Not to Do

- **Do not edit past change log entries** in specs — they are historical record.
  Append new entries only.
- **Do not remove or renumber rule identifiers** (F01, C01, etc.) — they are
  stable references. Mark deprecated rules with `Status: deprecated` instead.
- **Do not paste SQL, Perl, or large code blocks** into specs. The spec describes
  intent; the implementation lives elsewhere.
- **Do not weaken schema.yaml** — you may add new categories or fields, but do
  not remove existing ones without understanding the impact on existing specs.
- **Do not skip validation** before committing.

## Audience Awareness

The primary audience for spec *content* is non-technical library staff (the Report
Assessment Team, branch managers, cataloging staff). Write specs in plain English.
Technical details go in "Technical implementation" notes within rules, clearly
separated from the plain-English statements.

The audience for *tooling and this file* is developers and AI agents.
