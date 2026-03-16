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

## Anatomy of a Code Table Spec

Code table specifications follow this section ordering after the
front matter and title heading:

1. **Purpose** — what the code table is, why it matters
2. **Scope & Audience** — who uses it, what is in/out of scope
3. **Registry** or **Rules** — the heart of the document (see below)
4. **Sierra Configuration** — how the codes are managed in Sierra admin
5. **Open Questions** — unresolved decisions
6. **Change Log** — version history

A code table spec uses EITHER a **Registry** section (for individual
code-value listings, like item types) OR a **Rules** section (for
structural categories, like location code classifications). See
[Registry Format](#registry-format) below for registry-style specs.
Rules-style specs use headings like `### C01 · Branch Locations`, where
the `C` prefix comes from `schema.yaml` `rule_prefixes` for the
`code-table` category.

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
```

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
