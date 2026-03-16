---
version: 2.0.0
purpose: Defines the standard format, front matter schema, and style guide for ILS business logic specification documents at Cincinnati & Hamilton County Public Library (CHPL). All spec documents should conform to this framework.
---

# CHPL ILS Specification Framework

______________________________________________________________________

## Overview

Specification documents ("specs") are the authoritative, human-readable source of
truth for ILS business logic at CHPL. They exist independently and serve as:

- A shared reference between the ILS Team, the Report Assessment Team, and other
  stakeholders
- The basis for implementing or auditing scripts, reports, and ILS configuration
- Institutional knowledge that persists through staff turnover and system migrations
- A version-controlled record of why decisions were made, not just what they are

Specs are plain Markdown files stored in version control. Front matter is YAML.

______________________________________________________________________

## Document Categories

The `category` field in front matter must be one of the following. The category
determines which body sections are required and which folder the spec lives in.

| Category     | Folder         | Description                                                      |
| ------------ | -------------- | ---------------------------------------------------------------- |
| `report`     | `reports/`     | Automated or scheduled report generated from ILS data            |
| `code-table` | `code-tables/` | An ILS code set (location codes, item types, patron types, etc.) |
| `loan-rule`  | `loan-rules/`  | A lending policy or loan rule configuration                      |
| `workflow`   | `workflows/`   | An operational process that involves the ILS                     |
| `policy`     | `policies/`    | A library policy that has ILS implications                       |

New categories may be added as needed; update this framework document when they are.

______________________________________________________________________

## Front Matter Schema

Every spec document must begin with a YAML front matter block. Fields marked
**required** must be present. Fields marked *optional* may be omitted if not
applicable, but should not be left blank — either populate them or remove them.

```yaml
---
# Identity
id: slitemdata                    # required — unique within its category, lowercase,
                                  # hyphens only (e.g. slitemdata, ptype-196, loan-rule-dvd)
title: "Item Data Inconsistency Report"  # required — human-readable title
category: report                  # required — see Document Categories above

# Ownership & Status
owner: "ILS Team"                 # required — team or person responsible for this spec
                                  # (e.g. "ILS Team", "Materials Selection & Acquisition",
                                  # "Cataloging and Processing")
reviewers:                        # optional — teams or individuals who should review
  - "Report Assessment Team"      # changes to this spec
status: draft                     # required — one of: draft | active | deprecated
                                  #   draft: being written, not yet in use
                                  #   active: implemented and in use
                                  #   deprecated: no longer in use, kept for reference
version: "0.1.0"                  # required — semantic version (MAJOR.MINOR.PATCH)
last_updated: 2026-03-13          # required — ISO date

# Implementation
implementation:                   # optional — path(s) to the script or Sierra config
  - "Reports/shelflist/slitemdata.pl"  # that implements this spec
code_prefix: ITYPE               # optional (code-table only) — prefix for registry
                                  # entry identifiers (e.g., ITYPE-70, LOC-avo, PTYPE-3)
schedule: "Monthly, 1st of month" # optional (required for reports) — human-readable
                                  # schedule, starting with frequency word
output_delivered_to:              # optional (required for reports) — who receives output
  - "Branch managers"

# Relationships
depends_on:                       # optional — specs this one structurally depends on,
  - code-tables/location-codes    # using category-folder/id format (matches file paths)
  - code-tables/item-types
related_specs:                    # optional — "see also" references (same format)
  - reports/slmissing
---
```

### Versioning Convention

- **PATCH** — typos, formatting corrections
- **MINOR** — clarifications or additions that do not change business logic
- **MAJOR** — changes to business logic or rules

### Relationship Fields

- **`depends_on`** — "this spec cannot be fully understood without these." A
  structural dependency. Uses `category-folder/id` format, which matches the
  actual file path under `specs/`.
- **`related_specs`** — "you might also want to read these." A see-also reference,
  not a dependency. Same format.

### Schedule Convention

For reports, the `schedule` field should start with a frequency word for
consistency across specs:

- `"Daily, at 6:00 AM"`
- `"Weekly, Monday morning"`
- `"Monthly, 1st of month"`
- `"Monthly, 15th of month"`
- `"Quarterly, January/April/July/October"`

______________________________________________________________________

## Category Guides

Each spec category has its own guide that explains the body sections,
the format for the "heart of the document" section, and what a minimum
viable spec looks like. Read the guide for your category before writing
or reviewing a spec.

| Category   | Guide                                                  | Status |
| ---------- | ------------------------------------------------------ | ------ |
| Report     | [Report Specification Guide](./guides/report-guide.md) | Active |
| Code Table | [Code Table Guide](./guides/code-table-guide.md)       | Stub   |
| Loan Rule  | Planned                                                | —      |
| Workflow   | Planned                                                | —      |
| Policy     | Planned                                                | —      |

This framework document covers what is common to all categories: front matter,
versioning, cross-referencing, glossary conventions, and the style guide.

______________________________________________________________________

## Cross-Referencing Conventions

Specs reference each other using three patterns. Use them together as appropriate.

### 1. Front Matter (structured, machine-readable)

```yaml
depends_on:
  - code-tables/location-codes
related_specs:
  - reports/slmissing
```

These references use `category-folder/id` format, matching the file path under
`specs/`. They enable tooling to build dependency graphs and answer questions like
"what reports depend on location codes?"

### 2. Body Prose (relative Markdown links)

```markdown
This report flags items whose item type is not permitted for their location.
See [Location Codes](../code-tables/location-codes.md) for the canonical list
of valid location/item-type combinations.
```

Use relative links so they work when browsing the repository directly.

### 3. Registry Entry Links

```markdown
See [Book on CD](../code-tables/item-types.md#itype-70-book-on-cd) for details
on this item type.
```

Registry entry headings produce standard Markdown anchors. The anchor is the
heading text, lowercased, with spaces and the `·` replaced by hyphens.

### 4. Glossary Links

```markdown
A [hold-filled](../glossary.md#hold-filled) transaction is recorded when the
patron picks up the item.
```

**Path note:** From specs in category subfolders (e.g., `specs/reports/`), link to
the glossary with `../glossary.md#term`. From files in the `specs/` root (like this
framework document), use `./glossary.md#term`.

______________________________________________________________________

## Glossary Conventions

The glossary (`specs/glossary.md`) is a controlled vocabulary for terms used across
specs. See the glossary file itself for the full preamble and linking instructions.

### Term Format

Each term gets an `##` heading (which creates a linkable anchor) followed by:

- A definition
- **"Not to be confused with:"** (when the term is commonly misused or ambiguous)
- **"Sierra context:"** (the Sierra-specific implementation detail)

### Contextual Definitions

When a term has genuinely different meanings in different contexts, use context
subsections under the term heading:

```markdown
## hold-filled

### Context: circulation
The moment the item leaves the library in the patron's hands. Generates a
transaction record.

**Sierra context:** Transaction type `f` in `circ_trans`.

### Context: operations
The act of paging an item from the shelf and placing it on the hold shelf for
patron pickup. Does not generate a circulation transaction.
```

This convention is optional — most terms will not need it. Use it only when the
ambiguity would cause real confusion in specs.

______________________________________________________________________

## Style Guide

### Writing Specs

- **Write in plain English.** Avoid jargon where plain words will do. Sierra field
  names and technical terms belong in the Technical Implementation note, not in the
  plain-English rule statement. Avoid abbreviations and initialisms when possible or
  practical — write "item type" not "itype" in rule statements, "patron type" not
  "ptype."

- **Write in the present tense.** "An item is flagged when..." not "An item will be
  flagged when..."

- **Be specific about codes and values.** When a rule refers to a specific location
  code, item type, or patron type, name it explicitly. Vague rules are unauditable.

- **Separate what from why.** The rule statement says what happens. The rationale
  says why. Don't mix them.

- **The spec is not the script.** Do not paste SQL or Perl into a spec document
  except as a very brief illustrative snippet. The spec describes intent; the script
  is the implementation. They should be independently readable.

- **Version bumps matter.** Any change to a rule statement — even a clarification —
  warrants a minor version bump and a change log entry. Changes to business logic
  warrant a major version bump.

- **Unresolved things belong in Open Questions.** Don't leave ambiguity buried in
  rule prose. If something isn't decided, say so explicitly in Open Questions with
  a note on who needs to decide it.

______________________________________________________________________

## File Naming Convention

Spec files live in their category folder and are named by their `id`:

```
specs/{category-folder}/{id}.md
```

Examples:

```
specs/reports/slitemdata.md
specs/code-tables/location-codes.md
specs/loan-rules/dvd-checkout.md
specs/workflows/duplicate-barcode-resolution.md
```

The `id` should be lowercase with hyphens. It must be unique within its category.

______________________________________________________________________

## Machine-Readable Schema

The file `specs/schema.yaml` is the machine-readable companion to this document.
It contains the valid values for categories, statuses, required fields, and rule
prefixes in a format that validation tooling can consume directly.

When updating this framework document, also update `schema.yaml` to match. The
validation script (`scripts/validate-specs.py`) checks that the `framework_version`
in `schema.yaml` matches the version in this document's header and will warn if
they drift.
