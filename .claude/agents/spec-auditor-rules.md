# Spec Auditor Rules

Rules for the CHPL ILS Specification Framework consistency audit.
Each rule has a dimension, severity, check, expected behavior, and
(where applicable) an example finding from the initial audit.

## Files in Scope

| File | Role |
| --- | --- |
| `specs/FRAMEWORK.md` | Universal conventions |
| `specs/glossary.md` | Controlled vocabulary |
| `specs/README.md` | Spec index |
| `specs/guides/report-guide.md` | Report category guide |
| `specs/guides/code-table-guide.md` | Code table category guide |
| `specs/reports/slitemdata.md` | Report spec |
| `specs/code-tables/item-types.md` | Code table spec (registry) |
| `specs/code-tables/location-codes.md` | Code table spec (rules) |
| `README.md` | Project entry point |

______________________________________________________________________

## Dimension: Structure

### S01: Report section ordering

- **Dimension:** Structure
- **Severity:** Error
- **Check:** Report specs have `##` sections in prescribed order
- **Expected:** Purpose, Scope & Audience, Data Sources, Flag Conditions, Output & Delivery, Exclusions & Edge Cases, Open Questions, Known Limitations, Change Log
- **Example finding:** None — all report specs passed on initial audit

### S02: Code table section ordering

- **Dimension:** Structure
- **Severity:** Error
- **Check:** Code table specs have `##` sections in prescribed order
- **Expected:** Purpose, Scope & Audience, Registry or Rules, Sierra Configuration, Open Questions, Change Log
- **Example finding:** `specs/code-tables/location-codes.md` used `## Rules / Codes` instead of `## Rules` (fixed 2026-03-16)

### S03: Title heading matches front matter

- **Dimension:** Structure
- **Severity:** Error
- **Check:** First `#` heading matches `title` front matter field exactly
- **Expected:** `# Item Data Inconsistency Report` matches `title: Item Data Inconsistency Report`
- **Example finding:** None — all specs passed on initial audit

### S04: Horizontal rule consistency

- **Dimension:** Structure
- **Severity:** Warning
- **Check:** Horizontal rules used consistently as section separators
- **Expected:** Reference docs (framework, guides, glossary) use horizontal rules between `##` sections. Specs use them between `###` entries (flag conditions, registry entries, rules) but NOT between `##` sections.
- **Example finding:** Convention established during initial audit. No files needed changing — existing pattern was already consistent.

### S05: Flag condition heading pattern

- **Dimension:** Structure
- **Severity:** Error
- **Check:** Flag condition headings follow `### F{nn} · {Name}` pattern
- **Expected:** `### F01 · Material Type / Item Type Mismatch` — prefix `F` from `schema.yaml` `rule_prefixes` for `report` category
- **Example finding:** None — all flag condition headings passed on initial audit

### S06: Registry entry heading pattern

- **Dimension:** Structure
- **Severity:** Error
- **Check:** Registry entry headings follow `### {PREFIX}-{code} · {Label}`
- **Expected:** `### ITYPE-70 · Book on CD` — prefix from `code_prefix` front matter field
- **Example finding:** None — all registry entry headings passed on initial audit

### S07: Change Log is last section

- **Dimension:** Structure
- **Severity:** Warning
- **Check:** Change Log is the last `##` section in every spec
- **Expected:** No `##` headings appear after `## Change Log`
- **Example finding:** None — all specs passed on initial audit

### S08: Code table rule heading pattern

- **Dimension:** Structure
- **Severity:** Error
- **Check:** Code table rule/category headings follow `### C{nn} · {Name}` pattern
- **Expected:** `### C01 · Branch Locations` — prefix `C` from `schema.yaml` `rule_prefixes` for `code-table` category. Applies to Rules-style code table specs (not Registry-style).
- **Example finding:** None — all rule headings passed on initial audit

______________________________________________________________________

## Dimension: Language

### L01: Present tense

- **Dimension:** Language
- **Severity:** Warning
- **Check:** Rule/condition statements use present tense
- **Expected:** "An item is flagged when..." not "An item will be flagged when..."
- **Example finding:** None — all specs passed on initial audit

### L02: Purpose section structure

- **Dimension:** Language
- **Severity:** Note
- **Check:** Purpose sections follow what-it-does, why-it-matters, optional-context structure
- **Expected:** 1-3 paragraphs. First states what the thing does. Second states why it matters.
- **Example finding:** None — all specs passed on initial audit

### L03: Scope & Audience structure

- **Dimension:** Language
- **Severity:** Warning
- **Check:** Scope & Audience sections use three-part bold-label structure
- **Expected:** `**Audience:**`, `**In scope:**`, `**Out of scope:**` as labeled subsections
- **Example finding:** None — all specs passed on initial audit

### L04: Plain English in rule statements

- **Dimension:** Language
- **Severity:** Warning
- **Check:** Rule/condition statements use plain English, not technical field names
- **Expected:** "item type" not "itype", "location code" not "location_code". Technical names only in `**Technical implementation:**` blocks.
- **Example finding:** None — all specs passed on initial audit

### L05: Status label formatting

- **Dimension:** Language
- **Severity:** Warning
- **Check:** Status labels use consistent formatting
- **Expected:** `**Status:** confirmed` — bold label with colon inside bold, space, lowercase value
- **Example finding:** None — all specs passed on initial audit

### L06: Change Log entry format

- **Dimension:** Language
- **Severity:** Warning
- **Check:** Change Log entries follow standard format
- **Expected:** `- {YYYY-MM-DD} · v{version} · {description} ({team})`
- **Example finding:** `specs/guides/code-table-guide.md` entry was `- 2026-03-13 · Initial stub migrated from FRAMEWORK.md v1.0` — missing version number and team name (fixed 2026-03-16)

### L07: Purpose opening phrasing

- **Dimension:** Language
- **Severity:** Note
- **Check:** Purpose sections do not open by restating the document title verbatim
- **Expected:** "Item type codes classify items for circulation policy..." not "The Item Types code table documents item type codes..."
- **Example finding:** None — all specs passed on initial audit

______________________________________________________________________

## Dimension: Cross-References

### X01: Relative link style

- **Dimension:** Cross-References
- **Severity:** Error
- **Check:** All inter-spec references use relative markdown links with correct prefix
- **Expected:** From `specs/` root: `./glossary.md`. From category subfolders: `../glossary.md`. Never absolute paths.
- **Example finding:** None — all specs passed on initial audit

### X02: Front matter refs have body links

- **Dimension:** Cross-References
- **Severity:** Warning
- **Check:** Every `depends_on` and `related_specs` entry has at least one body-prose link
- **Expected:** If front matter says `depends_on: code-tables/location-codes`, the body should contain a link to `../code-tables/location-codes.md` somewhere
- **Example finding:** `specs/reports/slitemdata.md` listed `code-tables/location-codes` in `depends_on` but had no body link to location-codes.md (fixed 2026-03-16)

### X03: Glossary terms linked on first use

- **Dimension:** Cross-References
- **Severity:** Note
- **Check:** Glossary terms linked on first use per `##` section
- **Expected:** Terms like "item type", "location code", "suppressed" linked to glossary on first appearance in each major section
- **Example finding:** `specs/reports/slitemdata.md` uses glossary terms without linking. Flagged as Note — human decided to skip for now (2026-03-16). Code table specs that define the terms themselves are exempt.

### X04: Registry entry anchor links

- **Dimension:** Cross-References
- **Severity:** Error
- **Check:** References to registry entries use correct MkDocs anchor format
- **Expected:** `item-types.md#itype-70-book-on-cd` (single hyphen). The `·` separator collapses to a single hyphen in MkDocs anchors. Empirically verified 2026-03-16.
- **Example finding:** `specs/FRAMEWORK.md` and `specs/guides/report-guide.md` used `#itype-70--book-on-cd` (double hyphen) — incorrect anchor format (fixed 2026-03-16)

### X05: Guides link to FRAMEWORK.md

- **Dimension:** Cross-References
- **Severity:** Warning
- **Check:** Guide files link to FRAMEWORK.md for shared conventions rather than restating them
- **Expected:** Guides reference Front Matter Schema, Cross-Referencing Conventions via links to FRAMEWORK.md
- **Example finding:** `specs/guides/code-table-guide.md` explains `code_prefix` without linking to FRAMEWORK.md's Front Matter Schema. Noted but not fixed — guide is a stub awaiting full rewrite.

### X06: No orphan references

- **Dimension:** Cross-References
- **Severity:** Error
- **Check:** If FRAMEWORK.md mentions a guide, that guide exists (even as stub)
- **Expected:** Every guide link in the Category Guides table resolves to an existing file
- **Example finding:** None — all referenced guides exist on initial audit

### X07: No dead links

- **Dimension:** Cross-References
- **Severity:** Error
- **Check:** Every `[text](path)` and `[text](path#anchor)` resolves to an existing file and valid heading anchor
- **Expected:** All links resolve. Run `uv run mkdocs build --strict` to catch broken links.
- **Example finding:** `specs/FRAMEWORK.md` and `specs/guides/report-guide.md` had dead anchor links (`#itype-70--book-on-cd` did not match actual MkDocs anchor `#itype-70-book-on-cd`) (fixed 2026-03-16)

______________________________________________________________________

## Dimension: Redundancy

### R01: Front matter docs in FRAMEWORK.md only

- **Dimension:** Redundancy
- **Severity:** Warning
- **Check:** Front matter field documentation lives in FRAMEWORK.md. Guides reference it, do not redefine.
- **Expected:** Guides link to FRAMEWORK.md Front Matter Schema. Audience-appropriate summaries (like report-guide.md's field explanation by team) are acceptable supplemental content, not duplication.
- **Example finding:** None — all guides passed on initial audit

### R02: Section ordering in guides only

- **Dimension:** Redundancy
- **Severity:** Warning
- **Check:** Section structure/ordering lives in category guides. FRAMEWORK.md references guides via Category Guides table.
- **Expected:** FRAMEWORK.md does not prescribe per-category section ordering
- **Example finding:** None — passed on initial audit (framework 2.0 already removed per-category ordering)

### R03: Source-of-truth principle stated once

- **Dimension:** Redundancy
- **Severity:** Note
- **Check:** The source-of-truth principle is stated prominently in FRAMEWORK.md. Other files may reference it but should not restate in different words.
- **Expected:** Canonical statement in FRAMEWORK.md overview. README.md and AGENTS.md restatements are acceptable as entry-point documents. Guide restatements are judgment calls.
- **Example finding:** Principle restated in 4 places (FRAMEWORK.md, README.md, AGENTS.md, report-guide.md). Human decided all are intentional — README.md and AGENTS.md serve as entry points, report-guide.md reinforces for Report Assessment Team audience (2026-03-16).

### R04: Cross-ref conventions in FRAMEWORK.md

- **Dimension:** Redundancy
- **Severity:** Warning
- **Check:** Cross-referencing conventions live in FRAMEWORK.md. Guides show examples but link to framework for full rules.
- **Expected:** report-guide.md's "Working with Code Tables" section links to FRAMEWORK.md Cross-Referencing Conventions
- **Example finding:** None — report-guide.md correctly delegates to FRAMEWORK.md on initial audit

### R05: Glossary definitions in glossary.md only

- **Dimension:** Redundancy
- **Severity:** Warning
- **Check:** Glossary term definitions live in glossary.md. Specs link to terms, do not re-explain inline.
- **Expected:** Specs use terms without redefining them. Code table specs that ARE the canonical definition for their terms are exempt.
- **Example finding:** None — all specs passed on initial audit

### R06: Spec listing in specs/README.md only

- **Dimension:** Redundancy
- **Severity:** Note
- **Check:** The per-spec listing table lives in specs/README.md. Root README.md links to it rather than duplicating.
- **Expected:** Root README.md contains a link to specs/README.md, not a copy of the spec table
- **Example finding:** None — passed on initial audit

______________________________________________________________________

## Dimension: MkDocs

### M01: All files in mkdocs.yml nav

- **Dimension:** MkDocs
- **Severity:** Error
- **Check:** Every spec and guide file appears in `mkdocs.yml` nav section
- **Expected:** All files listed in the Files in Scope table above have corresponding nav entries
- **Example finding:** None — all files present in nav on initial audit

### M02: MkDocs-compatible anchor slugs

- **Dimension:** MkDocs
- **Severity:** Error
- **Check:** Anchor links use MkDocs-compatible slug format
- **Expected:** Lowercase, spaces become hyphens, `·` separator becomes single hyphen, consecutive hyphens collapse. Verified empirically: `### ITYPE-70 · Book on CD` → `#itype-70-book-on-cd` (2026-03-16)
- **Example finding:** See X04/X07 — double-hyphen anchors were incorrect

### M03: Paths relative to docs_dir

- **Dimension:** MkDocs
- **Severity:** Error
- **Check:** All nav paths and file links work from the `docs_dir: specs` root
- **Expected:** Nav paths like `reports/slitemdata.md` (relative to specs/). Internal links use relative paths from their own file location.
- **Example finding:** None — all paths correct on initial audit

### M04: Front matter title on non-spec files

- **Dimension:** MkDocs
- **Severity:** Warning
- **Check:** Non-spec markdown files in MkDocs site have `title` front matter
- **Expected:** Guide files, glossary.md, FRAMEWORK.md have `title` field. specs/README.md is explicitly exempt — MkDocs nav entry ("Home") provides its page title.
- **Example finding:** `specs/glossary.md` had no front matter at all. `specs/FRAMEWORK.md` had `version` and `purpose` but no `title`. Both fixed 2026-03-16. `specs/README.md` intentionally skipped (M04-002).

### M05: No GitHub-specific link features

- **Dimension:** MkDocs
- **Severity:** Warning
- **Check:** No links use GitHub-specific features that fail in MkDocs
- **Expected:** No directory links with trailing `/`. No links to non-markdown files without explicit handling.
- **Example finding:** `specs/README.md` lines 11-15 used directory links (`reports/`, `code-tables/`, etc.) that MkDocs warned about. Links removed — individual spec links in the table below provide navigation (fixed 2026-03-16).

### M06: Nav reflects category organization

- **Dimension:** MkDocs
- **Severity:** Warning
- **Check:** mkdocs.yml nav structure matches actual category folder organization
- **Expected:** Nav sections for Home, Reference, Guides, Reports, Code Tables (etc.) match the actual files
- **Example finding:** None — nav structure correct on initial audit
