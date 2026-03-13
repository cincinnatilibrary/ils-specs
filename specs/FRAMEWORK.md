---
version: 1.0.0
purpose: Defines the standard format, front matter schema, and style guide for ILS business logic specification documents at Cincinnati & Hamilton County Public Library (CHPL). All spec documents should conform to this framework.
---

# CHPL ILS Specification Framework

______________________________________________________________________

## Overview

Specification documents ("specs") are the authoritative, human-readable source of
truth for ILS business logic at CHPL. They exist independently and serve as:

- A shared reference between the ILS Team, the Report Assessment Team, and other
  stakeholders
- The basis for implementing or auditing scripts, reports, and Sierra configuration
- Institutional knowledge that persists through staff turnover and system migrations
- A version-controlled record of why decisions were made, not just what they are

Specs are plain Markdown files stored in version control. Front matter is YAML.

______________________________________________________________________

## Document Categories

The `category` field in front matter must be one of the following. The category
determines which body sections are required and which folder the spec lives in.

| Category     | Folder         | Description                                                        |
| ------------ | -------------- | ------------------------------------------------------------------ |
| `report`     | `reports/`     | Automated or scheduled report generated from Sierra data           |
| `code-table` | `code-tables/` | A Sierra code set (location codes, item types, patron types, etc.) |
| `loan-rule`  | `loan-rules/`  | A lending policy or loan rule configuration                        |
| `workflow`   | `workflows/`   | An operational process that involves Sierra                        |
| `policy`     | `policies/`    | A library policy that has ILS implications                         |

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

## Body Structure

The body follows the front matter. Sections marked **[required]** must appear in
every spec of that category. Sections marked **[recommended]** should appear unless
genuinely not applicable. Sections marked **[optional]** are included at the
author's discretion.

Not every section will have the same depth in every document. A simple code table
spec might have a one-paragraph Purpose and a straightforward Codes section. A
complex report spec might need several pages. Write as much as the subject warrants,
no more.

| #   | Section                                | Required for          | Purpose                                         |
| --- | -------------------------------------- | --------------------- | ----------------------------------------------- |
| 1   | Purpose                                | all                   | Plain English explanation of why this exists    |
| 2   | Scope & Audience                       | all                   | Who uses it, what's in/out of scope             |
| 3   | Data Sources                           | report, workflow      | Sierra tables, fields, external data            |
| 4   | Rules / Conditions / Policy Statements | all                   | One subsection per rule — heart of the document |
| 5   | Output & Delivery                      | report                | Format, destination, recipients                 |
| 6   | Sierra Configuration                   | loan-rule, code-table | Bridge to current ILS implementation            |
| 7   | Exclusions & Edge Cases                | recommended, all      | Intentionally out of scope, and why             |
| 8   | Open Questions                         | optional, all         | Unresolved decisions, who needs to decide       |
| 9   | Known Limitations                      | optional, all         | Constraints outside your control                |
| 10  | Change Log                             | all                   | Brief record of meaningful changes              |

### Section Guidance

**Purpose \[required — all categories\]:** A plain-English explanation of what this
thing is and why it exists. Write for an audience that knows the library but may
not know Sierra. Answer: what problem does this solve, or what need does it serve?
Do not describe implementation here. Do not list rules here. Just explain the "why."
One to three paragraphs is typical.

**Scope & Audience \[required — all categories\]:** Who uses this, and what decisions
does it inform? Who is *not* the audience? Are there any locations, collections, or
patron types that are explicitly in or out of scope? For reports: who receives the
output, and what do they do with it? For code tables: which collections, locations,
or patron types does this code set apply to?

**Data Sources \[required — report, workflow\]:** What Sierra tables, fields, or
external data does this depend on? This does not need to be an exhaustive schema
reference — just enough to orient someone who needs to audit or update the
implementation.

**Rules / Conditions / Policy Statements \[required — all categories\]:** This is the
heart of the document. Each rule, flag condition, code definition, or policy
statement gets its own subsection. See the Rules Subsection Format below.

**Output & Delivery \[required — report\]:** What does the report produce? Describe
the output format, the columns or fields present, and how and where it is delivered.

**Sierra Configuration \[required — loan-rule, code-table\]:** How is this implemented
in Sierra specifically? Describe the relevant Sierra admin screens, configuration
fields, or code values. This section acknowledges that the spec stands independently
but provides a bridge to the current implementation.

**Exclusions & Edge Cases \[recommended — all categories\]:** Things that are
intentionally out of scope, and why. Known edge cases and how they are handled. This
section is especially valuable for future maintainers who might otherwise "fix"
something that was deliberately designed a certain way.

**Open Questions \[optional — all categories\]:** Things that have not yet been
decided, or where the business rule is unclear. Include who needs to make the
decision. Remove entries from this section (or move them to the change log) once
they are resolved.

**Known Limitations \[optional — all categories\]:** Things that are wrong or
incomplete but outside the spec's control. For example, "Sierra does not expose
field X, so the report approximates with Y." Document these so nobody wastes time
trying to fix constraints that cannot be changed from this side.

**Change Log \[required — all categories\]:** A brief record of meaningful changes to
this spec. Does not need to duplicate git history — just enough for a human skimming
the document to understand how the spec has evolved. Format:

```
## Change Log

- 2026-03-13 · v0.1.0 · Initial draft (ILS Team)
```

______________________________________________________________________

## Rules Subsection Format

Each rule gets a stable identifier (never reused or renumbered) with a
category-specific prefix:

| Category        | Prefix | Example                                   |
| --------------- | ------ | ----------------------------------------- |
| report flag     | `F`    | `### F01 · Location / Item Type Mismatch` |
| code-table rule | `C`    | `### C01 · Main Library`                  |
| loan rule       | `L`    | `### L01 · Standard DVD Checkout`         |
| policy          | `P`    | `### P01 · Card Expiration`               |
| workflow step   | `S`    | `### S01 · Page Item From Shelf`          |

Each rule subsection should contain, in roughly this order:

1. **A plain-English statement of the rule.** One or two sentences. Write it so
   that a non-technical stakeholder can read it and say "yes, that's what we want"
   or "no, that's not right." **This is the part the Assessment Team owns.**

2. **Elaboration or rationale.** Why does this rule exist? Are there exceptions?
   This can be a paragraph or a short list.

3. **Technical implementation note.** A brief description of how the rule is
   implemented in the script or Sierra configuration. This can reference field
   names, table names, or module names. **This is the part the ILS Team owns.**
   Keep this concise — it is not a substitute for code comments.

4. **Edge cases specific to this rule.** Anything that doesn't fit the general
   exclusions section.

5. **Status.** One of: `confirmed` | `proposed` | `under-review` | `deprecated`.
   The Assessment Team should confirm each rule before it is marked `confirmed`.

**Note on status values:** The rule-level `Status` field (`confirmed`, `proposed`,
`under-review`, `deprecated`) tracks whether a specific business rule has been
validated. This is distinct from the spec-level `status` field in front matter
(`draft`, `active`, `deprecated`), which tracks the lifecycle of the document as a
whole. A `draft` spec can contain `confirmed` rules, and an `active` spec can have
some rules still `proposed`. The word `deprecated` appears in both but means
different things: a deprecated rule is no longer applied; a deprecated spec is no
longer the current reference.

### Example

```markdown
### F01 · Location / Item Type Mismatch

An item is flagged when its item type code is not permitted for its assigned
location code. For example, a DVD item type should not appear in a branch
location designated for print materials only.

This rule catches items that were either miscataloged at intake or had their
location changed without a corresponding item type update. Left uncorrected,
these items may circulate under the wrong loan rules.

**Technical implementation:** Checked against the valid itype/location mapping
in `Sierra::Locations`. Any item whose itype is not in the permitted set for
its location_code is included.

**Edge cases:** Items in transit (status `t`) are excluded — the location code
reflects the destination, not the current home, and mismatches during transit
are expected and transient.

**Status:** confirmed
```

______________________________________________________________________

## Registry Definitions Format

Code-table specs may include a **Registry** section that enumerates all defined
values in a Sierra code table. Each entry's identifier is the spec's
`code_prefix` (declared in front matter) followed by a dash and the Sierra code
value — e.g., `ITYPE-70`, `PTYPE-3`, `LOC-avo`. These identifiers are inherently
stable because they are tied to the system code.

### Registry Entry Format

```markdown
### ITYPE-70 · Book on CD

Audiobook on compact disc for adult patrons.

**Status:** confirmed
```

The heading pattern is `### {PREFIX}-{CODE} · {Label}`. The body is a brief
description. Add additional notes only when there is something notable about
the code.

The `code_prefix` front matter field declares the prefix:

```yaml
code_prefix: ITYPE    # → headings like ITYPE-70, ITYPE-101
code_prefix: LOC      # → headings like LOC-avo, LOC-main
code_prefix: PTYPE    # → headings like PTYPE-3, PTYPE-196
```

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
See [Book on CD](../code-tables/item-types.md#itype-70--book-on-cd) for details
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

### Writing Rules and Conditions

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

## Minimum Viable Spec

When writing a new spec from scratch, the minimum required content before it should
be marked `status: active` is:

- All required front matter fields populated
- Purpose section written
- At least one confirmed rule in the Rules section
- Change log entry for the initial draft

A spec with `status: draft` and Open Questions is better than no spec. Don't let
perfect be the enemy of useful.

______________________________________________________________________

## Machine-Readable Schema

The file `specs/schema.yaml` is the machine-readable companion to this document.
It contains the valid values for categories, statuses, required fields, and rule
prefixes in a format that validation tooling can consume directly.

When updating this framework document, also update `schema.yaml` to match. The
validation script (`scripts/validate-specs.py`) checks that the `framework_version`
in `schema.yaml` matches the version in this document's header and will warn if
they drift.
