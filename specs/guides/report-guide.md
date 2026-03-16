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
```

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
See [Book on CD](../code-tables/item-types.md#itype-70-book-on-cd) for
details on this item type.
```

For the full set of cross-referencing conventions (including glossary links
and other patterns), see
[Cross-Referencing Conventions](../FRAMEWORK.md#cross-referencing-conventions)
in the framework document.
