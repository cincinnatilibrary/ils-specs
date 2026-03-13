# Design: FRAMEWORK.md Refactor and Report Specification Guide

## Problem

The current `specs/FRAMEWORK.md` tries to be a universal schema for five
different spec categories (report, code-table, loan-rule, workflow, policy).
This creates several issues:

- The "Rules Subsection Format" uses developer-oriented concepts (stable
  identifiers, rule prefixes) without clearly explaining their purpose to
  non-technical users.
- Terms like "code" and "rules" mean different things depending on the
  category, but the framework treats them uniformly.
- Body structure guidance (which sections are required, what goes in them)
  varies by category but is presented in a single monolithic table.
- The document's audience is unclear — it's simultaneously aimed at AI agents
  generating specs, ILS Team members maintaining them, and non-technical
  library staff who need to own the content.

The Report Assessment Team is the most immediate audience. They need to be able
to read, validate, and eventually write report specifications. The current
framework doesn't give them a clear, approachable guide for doing that.

## Goals

1. Make FRAMEWORK.md focused on what's truly universal across all spec types.
2. Create a report-specific guide that the Report Assessment Team can use to
   understand, validate, and write report specifications.
3. Preserve existing conventions that work (front matter schema, versioning,
   cross-referencing) while clarifying the ones that confuse (rules format,
   prefixes, per-rule status).
4. Establish the pattern for future category-specific guides (code-table,
   loan-rule, etc.) without writing them all now.

## Non-Goals

- Writing guides for all five categories. Only the report guide is in scope
  now. Code-table guide is a stub/future work.
- Changing the front matter schema. The mechanical structure is fine; it's
  the human-facing guidance that needs work.

## Design

### Change 1: Slim down FRAMEWORK.md

FRAMEWORK.md retains only content that applies to ALL spec categories:

**Kept (as-is or with minor edits):**

- Overview — what specs are, why they exist
- Document Categories — the category/folder table
- Front Matter Schema — YAML fields, versioning convention, relationship
  fields, schedule convention
- Cross-Referencing Conventions — front matter refs, body prose links,
  registry entry links, glossary links
- Glossary Conventions — term format, contextual definitions
- File Naming Convention
- Style Guide — general writing principles (plain English, present tense,
  separate what from why, spec is not the script, version bumps matter,
  unresolved things in Open Questions)
- Machine-Readable Schema — reference to schema.yaml

**Removed (moves to category guides):**

- Body Structure table (section requirements differ by category)
- Section Guidance block (each guide explains its own sections)
- Rules Subsection Format (each guide uses its own natural term for the
  "heart of the document" section)
- Registry Definitions Format (moves to code-table guide)
- Minimum Viable Spec (each guide defines its own minimum)

**Added:**

- A "Category Guides" section listing the per-category guides with brief
  descriptions and links. Initially only the report guide exists; others
  are listed as "planned."

### Change 1a: Rename slitemdata's "Rules / Conditions" heading

The existing `specs/reports/slitemdata.md` uses `## Rules / Conditions` as
its section heading. Rename it to `## Flag Conditions` so it matches the
report guide's terminology. This is a trivial, non-breaking edit that
prevents immediate confusion when the Report Assessment Team reads the
guide and then opens the only existing report spec.

### Change 2: Create report guide at `specs/guides/report-guide.md`

Structured as a short concept introduction followed by an annotated
walkthrough of a real spec (slitemdata).

#### Part 1: "What is a Report Specification?" (~half page)

Establishes:

- A report specification describes an automated report generated from ILS
  data. It defines what records the report examines (items, patrons, bibs,
  transactions, etc.), what conditions cause a record to appear in the
  output, and who receives the results and what they do with them.
- The spec is the source of truth — code is written to match the spec, not
  the other way around.
- Two workflows exist: (a) existing reports get translated from code into a
  spec draft, then the Report Assessment Team validates and takes ownership;
  (b) new reports start as a spec written by the Report Assessment Team,
  then the ILS Team implements from it.
- The Report Assessment Team owns the *what* and *why*. The ILS Team owns
  the *how*.
- Reports examine record properties (item type, location, material type,
  patron type, etc.) that are defined in code table documents. The report
  spec references those documents — it doesn't redefine them.

#### Part 2: "Anatomy of a Report Spec" (annotated walkthrough)

Walks through slitemdata section by section. Each section gets:

- What this section is for
- Who typically writes/maintains it
- How much detail is expected
- Common pitfalls or tips

**Sections covered:**

01. **Front matter** — "the identity card for the spec." Each field explained
    in plain language. Notes which fields the Report Assessment Team cares
    about vs. which are ILS Team territory.

02. **Purpose** — what the report does and why it matters. Written so anyone
    at the library could read it and understand. 1-3 paragraphs. Don't
    describe implementation here.

03. **Scope & Audience** — who gets the report, what they do with it, what
    records are in/out of scope.

04. **Data Sources** — what ILS tables and fields the report depends on.
    Annotation notes this is ILS Team territory; Report Assessment Team can
    skip this section when reading/writing.

05. **Flag Conditions** — the heart of the document. This is the renamed
    "Rules / Conditions / Policy Statements" section for reports. Each flag
    condition describes a situation that causes a record to appear in the
    report output.

    Key conventions explained here:

    - Each condition gets a stable identifier (F01, F02, etc.) — a shared
      label everyone can point at. "Let's revisit F03" is easier than "let's
      revisit that one about audience mismatches." Identifiers are permanent;
      if a condition is removed, its number is retired, not reused.
    - Each flag condition contains:
      - A **plain-English statement** of the condition (Report Assessment
        Team owns this)
      - **Elaboration or rationale** — why this condition matters, any
        exceptions
      - **Technical implementation note** — how it's implemented in the
        script/query (ILS Team owns this)
      - **Edge cases** specific to this condition (if any)
      - **Status** — tracks whether the condition has been validated
    - Full annotated walkthrough of one flag (F01) showing all parts.

06. **Output & Delivery** — what the report produces (format, columns/fields),
    where it goes, who receives it.

07. **Exclusions & Edge Cases** — what's intentionally left out of the report
    and why. Valuable for future maintainers who might otherwise "fix"
    something that was deliberately designed that way.

08. **Open Questions** — unresolved decisions. Includes who needs to decide.
    Entries are removed or moved to the change log once resolved.

09. **Known Limitations** — constraints outside anyone's control (e.g., "the
    ILS does not expose field X, so the report approximates with Y").

10. **Change Log** — breadcrumb trail of meaningful changes. Doesn't
    duplicate git history.

#### Part 3: "Status: How a Report Spec Matures"

Explains the two levels of status in plain language:

- **Document-level status** (in front matter): `draft` means the spec is
  being written; `active` means it's implemented and in use; `deprecated`
  means it's no longer current.
- **Per-flag status** (on each flag condition): `proposed` means the
  condition has been written but not yet validated by the Report Assessment
  Team; `confirmed` means they've reviewed it and agree it's correct;
  `under-review` means it's being reconsidered; `deprecated` means it's no
  longer applied.
- How they relate: a `draft` spec can have `confirmed` flags (some
  conditions validated while the doc is still being completed). An `active`
  spec can have `proposed` flags (new conditions added that haven't been
  reviewed yet).

#### Part 4: "Minimum Viable Report Spec"

What you need before the spec is useful:

- All required front matter fields populated
- Purpose section written
- At least one flag condition (even if `proposed`)
- Change log entry for the initial draft

"A draft with open questions is better than no spec at all."

#### Part 5: "Working with Code Tables"

Brief explanation of the relationship:

- Reports check record properties. Those properties (item types, location
  codes, patron types, etc.) are defined in code table documents.
- When a flag condition references a specific code or set of codes, link to
  the code table document rather than copying its contents.
- Example showing how slitemdata references item-types and location-codes.

### Change 3: Stub for code-table guide

Create `specs/guides/code-table-guide.md` as a placeholder. Move the
Registry Definitions Format content from the current FRAMEWORK.md into it
as a starting point, with a note that it needs the same annotated-example
treatment as the report guide.

### Change 4: Update validation script

The validation script (`scripts/validate-specs.py`) walks all subdirectories
of `specs/` and attempts to parse any `.md` file as a spec with required
front matter. Guide files are not specs and will fail validation. Update the
validator to skip the `specs/guides/` directory.

Additionally, the validator's `get_framework_version()` function looks for a
`**Version:**` line in FRAMEWORK.md body text, but the version is actually
stored in the YAML front matter. Fix the extractor to read from front matter
so the framework/schema version alignment check works correctly.

### Change 5: Update AGENTS.md

AGENTS.md currently tells agents to read FRAMEWORK.md for "body sections,
rules format, and style guide." After the refactor, body sections and rules
format move to category guides. Update AGENTS.md to reference the guide
structure — when creating a new spec, agents should read the relevant
category guide for body structure, not just FRAMEWORK.md.

### Change 6: Update mkdocs.yml

Add a "Guides" section to the MkDocs nav so the report guide and code-table
guide stub appear in the published site.

## File Changes Summary

| File                               | Action                                                             |
| ---------------------------------- | ------------------------------------------------------------------ |
| `specs/FRAMEWORK.md`               | Trim to universal content, add Category Guides section, bump 2.0.0 |
| `specs/reports/slitemdata.md`      | Rename "Rules / Conditions" heading to "Flag Conditions"           |
| `specs/guides/report-guide.md`     | New — full report specification guide                              |
| `specs/guides/code-table-guide.md` | New — stub with registry format content                            |
| `specs/schema.yaml`                | Update `framework_version` to 2.0.0                                |
| `scripts/validate-specs.py`        | Skip `guides/` dir; fix framework version extraction from YAML     |
| `AGENTS.md`                        | Reference category guides for body structure                       |
| `mkdocs.yml`                       | Add Guides section to nav                                          |

## Design Decisions

1. **Guide location:** `specs/guides/` — keeps guides co-located with the
   specs they describe. The validator is updated to skip this directory.

2. **FRAMEWORK.md version:** Bumped to 2.0.0. This is a major structural
   change — body structure, rules format, and minimum viable spec sections
   are removed (breaking change for anything relying on those sections).

3. **`code_prefix` documentation:** Stays in FRAMEWORK.md's Front Matter
   Schema section with the existing "optional (code-table only)" annotation.
   It's a front matter field, and all front matter fields are documented in
   the framework regardless of which categories use them.

4. **Guide front matter:** Guide files get a minimal `title` field in YAML
   front matter for MkDocs rendering, but are not treated as specs by the
   validator.

5. **Cross-referencing in report guide:** Part 5 ("Working with Code
   Tables") shows examples but points back to FRAMEWORK.md's
   Cross-Referencing Conventions for the full linking syntax, avoiding
   duplication.
