# Framework Refactor and Report Guide Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor FRAMEWORK.md to universal-only content and create a report specification guide with annotated examples for the Report Assessment Team.

**Architecture:** Split the monolithic FRAMEWORK.md into a universal foundation doc plus per-category guides. The report guide uses an annotated walkthrough of slitemdata.md as its teaching tool. Supporting files (validator, schema, AGENTS.md, mkdocs.yml) are updated to match.

**Tech Stack:** Markdown, Python (validate-specs.py), MkDocs Material, YAML

**Design spec:** `docs/superpowers/specs/2026-03-13-framework-refactor-and-report-guide-design.md`

______________________________________________________________________

## Chunk 1: Tooling and Infrastructure

### Task 1: Fix validation script to skip guides/ and read version from front matter

**Files:**

- Modify: `scripts/validate-specs.py:30` (SKIP_FILES / directory skip)

- Modify: `scripts/validate-specs.py:39-48` (get_framework_version)

- [ ] **Step 1: Add guides/ directory skip to find_spec_files()**

In `find_spec_files()` (line 69-79), add `"guides"` to a set of skipped
directory names so that files in `specs/guides/` are not treated as specs:

```python
# Directories under specs/ that are not category folders
SKIP_DIRS = {"guides"}
```

Then in the `os.walk` loop, filter out skipped dirs:

```python
def find_spec_files():
    """Find all .md files in specs/ subdirectories (category folders)."""
    specs = []
    for root, dirs, files in os.walk(SPECS_DIR):
        # Skip the specs/ root directory files
        if root == SPECS_DIR:
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            continue
        for f in sorted(files):
            if f.endswith(".md") and f not in SKIP_FILES and f != ".gitkeep":
                specs.append(os.path.join(root, f))
    return specs
```

- [ ] **Step 2: Fix get_framework_version() to read from YAML front matter**

Replace the current body-text search with YAML front matter parsing:

```python
def get_framework_version():
    """Extract the version string from FRAMEWORK.md's YAML front matter."""
    with open(FRAMEWORK_PATH) as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) >= 3:
        try:
            fm = yaml.safe_load(parts[1])
            if fm and "version" in fm:
                return str(fm["version"])
        except yaml.YAMLError:
            pass
    return None
```

- [ ] **Step 3: Run validation to confirm it passes with current files**

Run: `uv run python scripts/validate-specs.py`
Expected: All specs PASS, version alignment now works (was previously
warning because the body-text search couldn't find the version).

- [ ] **Step 4: Commit**

```bash
git add scripts/validate-specs.py
git commit -m "fix(scripts): skip guides/ dir and read framework version from front matter"
```

______________________________________________________________________

## Chunk 2: FRAMEWORK.md Refactor

### Task 2: Slim down FRAMEWORK.md to universal content

**Files:**

- Modify: `specs/FRAMEWORK.md`

- [ ] **Step 1: Bump version to 2.0.0 in front matter**

Change line 2 from `version: 1.0.0` to `version: 2.0.0`.

- [ ] **Step 2: Replace "Sierra" with "ILS" in category descriptions**

In the Document Categories table (lines 30-36), replace Sierra-specific
references with "ILS":

| Category     | Folder         | Description                                                      |
| ------------ | -------------- | ---------------------------------------------------------------- |
| `report`     | `reports/`     | Automated or scheduled report generated from ILS data            |
| `code-table` | `code-tables/` | An ILS code set (location codes, item types, patron types, etc.) |
| `loan-rule`  | `loan-rules/`  | A lending policy or loan rule configuration                      |
| `workflow`   | `workflows/`   | An operational process that involves the ILS                     |
| `policy`     | `policies/`    | A library policy that has ILS implications                       |

- [ ] **Step 3: Remove Body Structure section (lines 115-194)**

Delete the entire `## Body Structure` section including the table,
`### Section Guidance`, and all the per-section guidance paragraphs.
This content moves to category-specific guides.

- [ ] **Step 4: Remove Rules Subsection Format section (lines 198-262)**

Delete the entire `## Rules Subsection Format` section including the
prefix table, the numbered list of rule contents, the note on status
values, and the example. This content moves to category guides.

- [ ] **Step 5: Remove Registry Definitions Format section (lines 266-294)**

Delete the entire `## Registry Definitions Format` section. This content
moves to the code-table guide.

- [ ] **Step 6: Remove Minimum Viable Spec section (lines 439-451)**

Delete the entire `## Minimum Viable Spec` section. Each category guide
defines its own minimum.

- [ ] **Step 7: Add Category Guides section**

Insert a new `## Category Guides` section after the Front Matter Schema
section (after the Schedule Convention subsection). This replaces the
removed Body Structure section:

```markdown
## Category Guides

Each spec category has its own guide that explains the body sections,
the format for the "heart of the document" section, and what a minimum
viable spec looks like. Read the guide for your category before writing
or reviewing a spec.

| Category   | Guide                                                      | Status  |
| ---------- | ---------------------------------------------------------- | ------- |
| Report     | [Report Specification Guide](./guides/report-guide.md)     | Active  |
| Code Table | [Code Table Guide](./guides/code-table-guide.md)           | Stub    |
| Loan Rule  | Planned                                                    | —       |
| Workflow   | Planned                                                    | —       |
| Policy     | Planned                                                    | —       |

The [Specification Framework](./FRAMEWORK.md) (this document) covers
what is common to all categories: front matter, versioning, cross-
referencing, glossary conventions, and the style guide.
```

- [ ] **Step 8: Update Style Guide heading**

Rename `### Writing Rules and Conditions` to `### Writing Specs` since
the style guide is now universal and not tied to the "rules" concept.

- [ ] **Step 9: Run formatting and validation**

```bash
./scripts/format-specs.sh
uv run python scripts/validate-specs.py
```

- [ ] **Step 10: Commit**

```bash
git add specs/FRAMEWORK.md
git commit -m "docs(framework): refactor to universal content only (v2.0.0)

Remove Body Structure, Rules Subsection Format, Registry Definitions,
and Minimum Viable Spec sections. These move to category-specific guides.
Add Category Guides section with links."
```

### Task 3: Update schema.yaml version

**Files:**

- Modify: `specs/schema.yaml:7`

- [ ] **Step 1: Bump framework_version to 2.0.0**

Change `framework_version: "1.0.0"` to `framework_version: "2.0.0"`.

- [ ] **Step 2: Run validation to confirm alignment**

```bash
uv run python scripts/validate-specs.py
```

Expected: version alignment check passes (no warning).

- [ ] **Step 3: Commit**

```bash
git add specs/schema.yaml
git commit -m "chore: bump schema framework_version to 2.0.0"
```

______________________________________________________________________

## Chunk 3: Report Guide

### Task 4: Rename slitemdata "Rules / Conditions" heading

**Files:**

- Modify: `specs/reports/slitemdata.md:72`

- [ ] **Step 1: Rename the heading**

Change `## Rules / Conditions` to `## Flag Conditions`.

- [ ] **Step 2: Bump version and update last_updated**

Change `version: 0.1.0` to `version: 0.2.0` and update `last_updated`.

- [ ] **Step 3: Add change log entry**

Add to the Change Log:

```
- 2026-03-13 · v0.2.0 · Rename "Rules / Conditions" to "Flag Conditions" per framework 2.0 (ILS Team)
```

- [ ] **Step 4: Run formatting**

```bash
./scripts/format-specs.sh
```

- [ ] **Step 5: Commit**

```bash
git add specs/reports/slitemdata.md
git commit -m "docs(reports): rename Rules/Conditions to Flag Conditions in slitemdata"
```

### Task 5: Create report specification guide

**Files:**

- Create: `specs/guides/report-guide.md`

This is the largest task. The guide has five parts as defined in the design
spec. It uses slitemdata as the annotated example throughout.

- [ ] **Step 1: Create the guides directory**

```bash
mkdir -p specs/guides
```

- [ ] **Step 2: Write the report guide**

Create `specs/guides/report-guide.md` with the following content. The
guide uses a minimal YAML front matter block for MkDocs rendering only
(not treated as a spec by the validator).

````markdown
---
title: Report Specification Guide
---

# Report Specification Guide

______________________________________________________________________

## What is a Report Specification?

A report specification describes an automated report generated from ILS
data. It defines what records the report examines, what conditions cause
a record to appear in the output, and who receives the results and what
they do with them.

**The specification is the source of truth.** Code is written to match the
specification, not the other way around. When a report needs to change, the
specification is updated first, and then the code is updated to match.

There are two ways a report specification comes into being:

1. **Existing reports:** An existing report's code is translated into a
   specification draft. The Report Assessment Team then reviews the draft,
   validates that it accurately describes what the report should do, and
   takes ownership of the document going forward.

2. **New reports:** The Report Assessment Team writes a specification
   describing what a new report should check and who should receive it.
   The ILS Team then implements the report from the specification.

In both cases, the Report Assessment Team owns the **what** and **why** —
what the report checks and why it matters. The ILS Team owns the **how** —
how the report is implemented technically.

Reports examine record properties — item type, location code, material
type, patron type, and others — that are defined in
[code table](./code-table-guide.md) documents. The report specification
references those documents rather than redefining the codes. This keeps
one source of truth for each code and avoids conflicting definitions.

______________________________________________________________________

## Anatomy of a Report Spec

This section walks through each part of a report specification, using the
[Item Data Inconsistency Report](../reports/slitemdata.md) as a real
example. Each section includes what it is for, who maintains it, and tips
for writing it well.

### Front Matter

The front matter is the block of structured fields at the very top of the
document, between the `---` markers. Think of it as the identity card for
the specification — it tells you at a glance what this spec is, who owns
it, and what state it is in.

Here is the front matter from the Item Data Inconsistency Report:

```yaml
---
id: slitemdata
title: Item Data Inconsistency Report
category: report
owner: ILS Team
reviewers:
  - Report Assessment Team
status: draft
version: 0.2.0
last_updated: 2026-03-13
implementation:
  - Reports/shelflist/SierraItemData-2024-06-03.pl
schedule: Monthly, 1st of month
output_delivered_to:
  - Branch managers
  - Cataloging and Processing
depends_on:
  - code-tables/location-codes
  - code-tables/item-types
related_specs:
  - reports/slmissing
---
````

**Fields the Report Assessment Team should care about:**

- **`title`** — the human-readable name of the report.
- **`owner`** — the team responsible for maintaining this specification.
- **`reviewers`** — who should review changes. If you are on this list,
  you will be asked to validate changes to the specification.
- **`status`** — is this spec a `draft` (still being written), `active`
  (implemented and in use), or `deprecated` (no longer current)?
- **`schedule`** — how often the report runs and when.
- **`output_delivered_to`** — who receives the report output.

**Fields the ILS Team typically manages:**

- **`id`** — a short, unique identifier used as the filename.
- **`implementation`** — path(s) to the script that runs this report.
- **`depends_on`** / **`related_specs`** — links to other specifications
  that this report relies on or relates to.

For the full list of fields and their rules, see the
[Front Matter Schema](../FRAMEWORK.md#front-matter-schema) in the
framework document.

### Purpose

The Purpose section explains what this report does and why it exists, in
language that anyone at the library can understand. It should answer: what
problem does this report solve, or what need does it serve?

**Tips:**

- Write 1-3 paragraphs. Don't describe how the report works technically —
  just explain what it does and why it matters.
- Imagine explaining it to a colleague who knows the library but has never
  seen this report before.

**From the example:**

> This report identifies items in the catalog whose data is internally
> inconsistent — where the item type, location code, bibliographic material
> type, or audience designation do not match the expected combinations.

This tells you immediately what the report looks for, without mentioning
any table names or field codes.

### Scope & Audience

This section answers: who receives this report and what do they do with it?
What records are included, and what is intentionally left out?

**Tips:**

- Name the specific teams or roles that use this report.
- Be clear about what is in scope and out of scope — this prevents
  misunderstandings about what the report covers.

### Data Sources

This section lists the ILS tables, fields, or external data the report
depends on. It provides enough information for someone auditing or updating
the implementation to know where to look.

**Note for the Report Assessment Team:** This section is primarily ILS Team
territory. You do not need to write or maintain it, but you may find it
helpful for understanding where the data comes from.

### Flag Conditions

This is the heart of the document. Each flag condition describes a specific
situation that causes a record to appear in the report output.

#### How flag conditions are identified

Each condition gets a short identifier like **F01**, **F02**, **F03**, and
so on. This gives everyone — staff, the ILS Team, and any tools working
with the document — a shared label to point at. "Let's revisit F03" is
easier than "let's revisit that one about audience mismatches."

These identifiers are permanent. If a flag condition is removed or no
longer applies, its number is retired, not reused. This means references
to "F02" always mean the same condition, even years later.

#### What each flag condition contains

Here is F01 from the Item Data Inconsistency Report, annotated:

> **`### F01 · Material Type / Item Type Mismatch`**
>
> *The heading: the identifier (F01), a separator (·), and a short
> descriptive name.*

> **An item is flagged when its bibliographic material type code is not
> consistent with its item type. For example, an item typed as a DVD
> should not be attached to a bib record with a material type indicating
> it is a book.**
>
> *The plain-English statement: one or two sentences that describe the
> condition. A non-technical person should be able to read this and say
> "yes, that's what we want" or "no, that's not right."*
> ***The Report Assessment Team owns this part.***

> **This rule catches items where the bib record format and the item-level
> classification disagree, which can cause incorrect shelving, wrong loan
> periods, and misleading catalog displays.**
>
> *The rationale: why does this condition matter? What goes wrong if
> it is not caught?*

> **Technical implementation: The script maintains a mapping with 27
> bcode2 values, each mapped to a set of permitted item type codes. An
> item is flagged when its itype_code_num is not in the permitted set
> for its bib's bcode2 value.**
>
> *The technical note: how the condition is implemented in the script.
> This section uses field names and technical details.*
> ***The ILS Team owns this part.***

> **Status: proposed**
>
> *The status: has the Report Assessment Team confirmed this condition?
> See the Status section below for what each value means.*

Not every flag condition needs all of these parts. A simple condition
might just have the plain-English statement and a status. But the
statement and status should always be present.

### Output & Delivery

This section describes what the report actually produces — the format of
the output, what columns or fields are included, and how and where it is
delivered to the people who use it.

**Tips:**

- A table listing the output fields with brief descriptions works well
  (see the slitemdata example).
- Note the delivery method (email, file server, web application, etc.).

### Exclusions & Edge Cases

This section documents what is intentionally left out of the report and
why. This is especially valuable for future maintainers who might
otherwise try to "fix" something that was deliberately designed that way.

**Tips:**

- A table with two columns — what is excluded and why — works well.
- If you are not sure why something is excluded, note that in
  [Open Questions](#open-questions) instead.

### Open Questions

Things that have not yet been decided, or where the business logic is
unclear. Each question should note who needs to make the decision.

Open questions are a normal, healthy part of a draft specification. They
show that the authors were thorough enough to identify what they did not
know. Remove or move questions to the Change Log once they are resolved.

### Known Limitations

Constraints that are outside anyone's control — things the ILS does not
support, data that is not available, or timing limitations. Documenting
these prevents people from wasting time trying to solve problems that
cannot be solved from this side.

### Change Log

A brief record of meaningful changes to this specification. It does not
need to duplicate the full version control history — just enough for
someone skimming the document to understand how the spec has evolved.

Format:

```
- 2026-03-13 · v0.1.0 · Initial draft (ILS Team)
- 2026-03-13 · v0.2.0 · Rename section heading per framework 2.0 (ILS Team)
```

______________________________________________________________________

## Status: How a Report Spec Matures

There are two levels of status in a report specification, and they track
different things.

### Document-level status

The `status` field in the front matter tracks the lifecycle of the
specification document as a whole:

- **`draft`** — the spec is being written. It may be incomplete, have
  open questions, or contain conditions that have not been validated yet.
- **`active`** — the spec is complete, implemented, and in use. The report
  runs according to this specification.
- **`deprecated`** — the spec is no longer current. It is kept for
  historical reference but should not be used for new work.

### Per-flag status

The `Status` line on each flag condition tracks whether that specific
condition has been validated by the Report Assessment Team:

- **`proposed`** — the condition has been written (often by the ILS Team
  or an automated tool) but has not been reviewed by the Report Assessment
  Team yet.
- **`confirmed`** — the Report Assessment Team has reviewed this condition
  and agrees it is correct.
- **`under-review`** — this condition is being reconsidered. Something
  may need to change.
- **`deprecated`** — this condition is no longer applied. The identifier
  (F01, F02, etc.) is kept so old references still make sense, but the
  condition is no longer checked.

### How they relate

These two status levels are independent:

- A **draft** spec can have **confirmed** flags — some conditions may be
  validated while the overall document is still being completed.
- An **active** spec can have **proposed** flags — new conditions may be
  added that have not been reviewed yet.
- The word "deprecated" appears in both but means different things: a
  deprecated flag is no longer checked; a deprecated spec is no longer the
  current reference document.

______________________________________________________________________

## Minimum Viable Report Spec

A report specification does not need to be perfect to be useful. The
minimum content needed to start working with a report spec is:

- All required front matter fields filled in (see
  [Front Matter Schema](../FRAMEWORK.md#front-matter-schema))
- A Purpose section explaining what the report does and why
- At least one flag condition (even if its status is `proposed`)
- A Change Log entry for the initial draft

A draft with open questions is better than no spec at all. Start with
what you know, mark what you don't know as Open Questions, and refine
from there.

______________________________________________________________________

## Working with Code Tables

Reports check record properties — item type, location code, material type,
patron type, and others. These properties are defined in **code table**
specifications, not in the report spec.

When a flag condition references a specific code or set of codes, **link
to the code table document** rather than copying the code definitions into
the report spec. This way, if a code definition changes, it only needs to
be updated in one place.

**Example from the Item Data Inconsistency Report:**

The report's front matter declares its dependencies:

```yaml
depends_on:
  - code-tables/location-codes
  - code-tables/item-types
```

And in the body, you can link directly to specific codes:

```markdown
See [Book on CD](../code-tables/item-types.md#itype-70--book-on-cd) for
details on this item type.
```

For the full set of cross-referencing conventions (including glossary links
and other patterns), see
[Cross-Referencing Conventions](../FRAMEWORK.md#cross-referencing-conventions)
in the framework document.

````

- [ ] **Step 3: Run formatting**

```bash
uv run mdformat specs/guides/report-guide.md
````

- [ ] **Step 4: Run validation to confirm guides/ is skipped**

```bash
uv run python scripts/validate-specs.py
```

Expected: report-guide.md does NOT appear in the output (skipped). All
existing specs still pass.

- [ ] **Step 5: Commit**

```bash
git add specs/guides/report-guide.md
git commit -m "docs(guides): add report specification guide

Annotated walkthrough of a real report spec (slitemdata), aimed at the
Report Assessment Team. Covers flag conditions, status levels, minimum
viable spec, and working with code tables."
```

______________________________________________________________________

## Chunk 4: Supporting Files

### Task 6: Create code-table guide stub

**Files:**

- Create: `specs/guides/code-table-guide.md`

- [ ] **Step 1: Write the stub**

Create `specs/guides/code-table-guide.md` with content migrated from
FRAMEWORK.md's Registry Definitions Format section, plus a note that
the guide needs the annotated-example treatment:

````markdown
---
title: Code Table Guide
---

# Code Table Guide

> **Note:** This guide is a stub. It contains the registry format
> conventions migrated from FRAMEWORK.md v1.0. A full annotated-example
> guide (like the [Report Specification Guide](./report-guide.md)) is
> planned.

______________________________________________________________________

## What is a Code Table Specification?

A code table specification documents a set of codes defined in the ILS —
location codes, item types, patron types, and similar value sets. It
serves as a human-readable registry of what each code means, who uses it,
and why it exists.

Code table specs are referenced by report specifications and other
documents that need to check record properties against valid values.

______________________________________________________________________

## Registry Format

Code-table specs include a **Registry** section that lists all defined
values in the code table. Each entry's identifier is the spec's
`code_prefix` (declared in front matter) followed by a dash and the
code value — for example, `ITYPE-70`, `PTYPE-3`, `LOC-avo`. These
identifiers are stable because they are tied to the system code.

### Registry Entry Format

```markdown
### ITYPE-70 · Book on CD

Audiobook on compact disc for adult patrons.

**Status:** confirmed
````

The heading pattern is `### {PREFIX}-{CODE} · {Label}`. The body is a
brief description. Add additional notes only when there is something
notable about the code.

The `code_prefix` front matter field declares the prefix:

```yaml
code_prefix: ITYPE    # → headings like ITYPE-70, ITYPE-101
code_prefix: LOC      # → headings like LOC-avo, LOC-main
code_prefix: PTYPE    # → headings like PTYPE-3, PTYPE-196
```

______________________________________________________________________

## Change Log

- 2026-03-13 · Initial stub migrated from FRAMEWORK.md v1.0

````

- [ ] **Step 2: Run formatting**

```bash
uv run mdformat specs/guides/code-table-guide.md
````

- [ ] **Step 3: Commit**

```bash
git add specs/guides/code-table-guide.md
git commit -m "docs(guides): add code-table guide stub with registry format"
```

### Task 7: Update AGENTS.md

**Files:**

- Modify: `AGENTS.md`

- [ ] **Step 1: Add guides/ to repository structure**

In the tree diagram (lines 35-44), add the guides directory:

```
└── specs/
    ├── README.md              # Reader entry point with navigable index
    ├── FRAMEWORK.md           # Common conventions: front matter, versioning, style
    ├── glossary.md            # Controlled vocabulary with anchored terms
    ├── schema.yaml            # Machine-readable schema (categories, statuses, etc.)
    ├── guides/                # Category-specific writing guides
    │   ├── report-guide.md    # How to write report specifications
    │   └── code-table-guide.md # How to write code table specifications (stub)
    ├── reports/               # Report specifications
    ├── code-tables/           # Code table specifications
    ├── loan-rules/            # Loan rule specifications
    ├── workflows/             # Workflow specifications
    └── policies/              # Policy specifications
```

- [ ] **Step 2: Update "Key Files" section**

Update the description of FRAMEWORK.md (line 49-51) and add the guides:

```markdown
1. **`specs/FRAMEWORK.md`** — common conventions for all spec types: front
   matter schema, versioning, cross-referencing, glossary, and style guide.
2. **`specs/guides/report-guide.md`** — how to write and read report
   specifications. Includes annotated examples and explains flag conditions,
   status levels, and working with code tables.
3. **`specs/schema.yaml`** — machine-readable companion to FRAMEWORK.md. If
   you change valid categories, statuses, or required fields, update both
   files and keep their versions aligned.
4. **`specs/glossary.md`** — controlled vocabulary. Link to it when using
   terms that have specific meanings (e.g., "hold-filled", "item type",
   "suppressed").
```

- [ ] **Step 3: Update "Creating a New Spec" steps**

Update steps 1-2 and 5 to reference category guides:

```markdown
1. Read `specs/FRAMEWORK.md` for common conventions (front matter, versioning,
   style guide)
2. Determine the category (`report`, `code-table`, `loan-rule`, `workflow`,
   `policy`)
3. Read the category guide in `specs/guides/` for body structure and section
   requirements (e.g., `specs/guides/report-guide.md` for reports)
4. Create the file at `specs/{category-folder}/{id}.md`
5. Include all required front matter fields (see `schema.yaml` for the list)
6. Follow the body section structure from the category guide
7. Add the spec to the index table in `specs/README.md`
8. Run validation: `uv run python scripts/validate-specs.py`
9. Run formatting: `./scripts/format-specs.sh`
```

- [ ] **Step 4: Run formatting**

```bash
uv run mdformat AGENTS.md
```

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md
git commit -m "docs: update AGENTS.md to reference category guides"
```

### Task 8: Update mkdocs.yml

**Files:**

- Modify: `mkdocs.yml`

- [ ] **Step 1: Add Guides section to nav**

Update the nav to include the guides between Reference and Reports:

```yaml
nav:
  - Home: README.md
  - Reference:
      - Framework: FRAMEWORK.md
      - Glossary: glossary.md
  - Guides:
      - Report Specifications: guides/report-guide.md
      - Code Tables: guides/code-table-guide.md
  - Reports:
      - reports/slitemdata.md
  - Code Tables:
      - code-tables/location-codes.md
      - code-tables/item-types.md
```

- [ ] **Step 2: Test the site build**

```bash
uv run mkdocs build --strict
```

Expected: Build succeeds with no warnings or errors.

- [ ] **Step 3: Commit**

```bash
git add mkdocs.yml
git commit -m "chore: add Guides section to mkdocs nav"
```

______________________________________________________________________

## Chunk 5: Final Validation

### Task 9: Full validation pass

- [ ] **Step 1: Run validation**

```bash
uv run python scripts/validate-specs.py
```

Expected: All specs pass, version alignment passes, no warnings.

- [ ] **Step 2: Run formatting check**

```bash
uv run mdformat --check specs/ AGENTS.md README.md
```

Expected: All files formatted correctly.

- [ ] **Step 3: Run MkDocs build**

```bash
uv run mkdocs build --strict
```

Expected: Clean build, no warnings.

- [ ] **Step 4: Review the report guide in browser (optional)**

```bash
uv run mkdocs serve
```

Open http://127.0.0.1:8000 and navigate to the Report Specification Guide
to verify it renders correctly and all links work.
