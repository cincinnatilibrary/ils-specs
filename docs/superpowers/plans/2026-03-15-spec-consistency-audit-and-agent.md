# Spec Consistency Audit & Audit Agent Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit all spec ecosystem files for consistency across five dimensions, fix issues, and build a reusable Spec Audit Agent.

**Architecture:** Two sequential phases. Phase 1 runs five audit passes (structure, language, cross-references, redundancy, MkDocs) across 9 markdown files, fixing issues and recording findings. Phase 2 uses those findings to build a Claude Code agent with review, fix, and regressions modes.

**Tech Stack:** Markdown, YAML front matter, MkDocs Material, mdformat, Python (validate-specs.py)

**Spec:** `docs/superpowers/specs/2026-03-15-spec-consistency-audit-and-agent-design.md`

---

## Chunk 1: Phase 1 — Audit Passes 1-3

### Task 1: Pre-Flight — Codify Code Table Section Ordering

The code-table-guide is a stub that does not prescribe section ordering.
Rule S02 requires this ordering to exist before we can audit against it.
This task adds the section ordering to the guide as a prerequisite.

**Files:**

- Modify: `specs/guides/code-table-guide.md`

- [ ] **Step 1: Read the current code-table-guide**

Read `specs/guides/code-table-guide.md`. Note it is a stub with only
"What is a Code Table Specification?", "Registry Format", and
"Change Log" sections.

- [ ] **Step 2: Add section ordering to the guide**

Add a new `## Anatomy of a Code Table Spec` section after "What is a
Code Table Specification?" and before "Registry Format". This section
prescribes the required sections for code table specs:

```markdown
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
```

- [ ] **Step 3: Run formatting**

Run: `./scripts/format-specs.sh`

- [ ] **Step 4: Commit**

```bash
git add specs/guides/code-table-guide.md
git commit -m "docs(guides): add section ordering to code-table guide"
```

______________________________________________________________________

### Task 2: Pass 1 — Structure & Layout Audit (Report Spec)

Audit `specs/reports/slitemdata.md` against rule S01 (report section
ordering), S03 (title match), S04 (horizontal rules), S05 (flag
heading pattern), S07 (Change Log last).

**Files:**

- Modify: `specs/reports/slitemdata.md` (if issues found)

- [ ] **Step 1: Read slitemdata.md and check S01 section order**

Read `specs/reports/slitemdata.md`. Check that `##` sections appear in
this order: Purpose, Scope & Audience, Data Sources, Flag Conditions,
Output & Delivery, Exclusions & Edge Cases, Open Questions, Known
Limitations, Change Log.

Current state from file read: Purpose (line 26), Scope & Audience (40),
Data Sources (54), Flag Conditions (72), Output & Delivery (153),
Exclusions & Edge Cases (174), Open Questions (190), Known Limitations
(221), Change Log (234). **S01: PASS.**

- [ ] **Step 2: Check S03 — title heading matches front matter**

Front matter `title: Item Data Inconsistency Report` (line 3).
H1: `# Item Data Inconsistency Report` (line 24). **S03: PASS.**

- [ ] **Step 3: Check S04 — horizontal rule consistency**

slitemdata.md uses `______` horizontal rules between F01-F02, F02-F03,
F03-F04, but NOT after F04 (before Output & Delivery at line 153).
Also no horizontal rules between other `##` sections.

**Finding S04-001:** Inconsistent horizontal rule usage. Rules appear
between flag conditions but not between top-level sections. Will
determine convention in step 5 (cross-file decision).

- [ ] **Step 4: Check S05 — flag condition headings**

Pattern required: `### F{nn} · {Name}`
- `### F01 · Material Type / Item Type Mismatch` (line 77) — PASS
- `### F02 · Location / Item Type Mismatch` (line 96) — PASS
- `### F03 · Audience / Item Type Mismatch` (line 119) — PASS
- `### F04 · Non-Floating Item in Wrong Branch` (line 140) — PASS

**S05: PASS.**

- [ ] **Step 5: Check S07 — Change Log is last section**

Change Log is the last `##` section (line 234). **S07: PASS.**

- [ ] **Step 6: Record findings**

Note finding S04-001 for the rules file. No edits needed to
slitemdata.md for structure (all other rules pass).

______________________________________________________________________

### Task 3: Pass 1 — Structure & Layout Audit (Code Table Specs)

Audit `specs/code-tables/item-types.md` and
`specs/code-tables/location-codes.md` against S02, S03, S04, S06, S07,
S08.

**Files:**

- Modify: `specs/code-tables/location-codes.md` (section heading rename)

- [ ] **Step 1: Read item-types.md and check S02 section order**

Read the first 50 lines plus the end of the file. Check `##` sections:
Purpose (line 17), Scope & Audience (line 25), Registry (line 34),
Sierra Configuration (line 972), Open Questions (line 982), Change Log
(line 992). **S02: PASS.**

- [ ] **Step 2: Check item-types.md S03, S06, S07**

- S03: front matter `title: Item Types`, H1 `# Item Types`. **PASS.**
- S06: Registry headings follow `### ITYPE-{n} · {Label}`. Spot check:
  `### ITYPE-0 · Book`, `### ITYPE-70 · Book on CD`,
  `### ITYPE-199 · Cleanup`. **PASS.**
- S07: Change Log is last section. **PASS.**

- [ ] **Step 3: Read location-codes.md and check S02 section order**

Read `specs/code-tables/location-codes.md`. Check `##` sections:
Purpose (line 16), Scope & Audience (line 24), Rules / Codes (line 35),
Sierra Configuration (line 99), Open Questions (line 108), Change Log
(line 121).

**Finding S02-001:** Section heading is `## Rules / Codes` but per S02
and the newly codified code-table-guide, it should be `## Rules` (for
a Rules-style code table spec). The `/ Codes` suffix is non-standard.

- [ ] **Step 4: Fix location-codes.md section heading**

Change `## Rules / Codes` to `## Rules` at line 35.

```markdown
## Rules
```

Also update the intro text below the heading. Current:
`The full code list needs to be exported from Sierra. The following are structural`
`categories identified from the \`Sierra::Locations\` module.`

This is fine as-is — it describes what the Rules section contains.

- [ ] **Step 5: Check location-codes.md S03, S07, S08**

- S03: front matter `title: Location Codes`, H1 `# Location Codes`.
  **PASS.**
- S07: Change Log is last section. **PASS.**
- S08: Headings follow `### C{nn} · {Name}`:
  `### C01 · Branch Locations`, `### C02 · Offsite Locations`, etc.
  **PASS.**

- [ ] **Step 6: Determine S04 horizontal rule convention**

Current state across all files:
- FRAMEWORK.md: `______` between all `##` sections
- report-guide.md: `______` between all `##` sections
- code-table-guide.md: `______` between all `##` sections
- glossary.md: `______` between all `##` term entries
- item-types.md: `______` between all `###` registry entries, none
  between `##` sections
- location-codes.md: `______` between all `###` rule entries, none
  between `##` sections
- slitemdata.md: `______` between `###` flag conditions, none between
  `##` sections

**Convention decision:** The pattern is consistent — reference docs
(framework, guides, glossary) use horizontal rules between `##`
sections. Specs use them between `###` entries (flag conditions,
registry entries, rules) but NOT between `##` sections.

This is actually a sensible distinction: specs have many `###` entries
that need visual separation, while their `##` sections are already
visually separated by headings. The reference docs are longer-form prose
where `##` sections benefit from extra visual separation.

**S04 resolution:** Document this as the convention. No files need
changing — the current pattern is consistent.

- [ ] **Step 7: Run formatting and commit**

```bash
./scripts/format-specs.sh
git add specs/code-tables/location-codes.md
git commit -m "docs(code-tables): rename 'Rules / Codes' to 'Rules' per S02 convention"
```

______________________________________________________________________

### Task 4: Pass 2 — Language & Tone Audit

Audit all 3 specs and both guides for L01-L07.

**Files:**

- Modify: `specs/guides/code-table-guide.md` (L06 change log fix)
- Modify: `specs/code-tables/item-types.md` (L04 if found)
- Other files as needed

- [ ] **Step 1: Check L01 — present tense across all specs**

Search all spec files for future tense indicators ("will be", "will
have", "will produce", "will run", "should be flagged"):

```bash
grep -n "will be\|will have\|will produce\|will run" specs/reports/*.md specs/code-tables/*.md
```

Review any hits. If they are in future-tense rule statements (not
describing future work in Open Questions), fix them.

Note: Open Questions naturally use future tense ("should these be...").
That is acceptable — L01 applies to rule/condition statements, not
discussion sections.

- [ ] **Step 2: Check L02 — Purpose section structure**

Read the Purpose section of each spec:

- `slitemdata.md`: 3 paragraphs (what it does, why it matters,
  priority context). **PASS.**
- `item-types.md`: 1 paragraph (what it does + why it matters
  combined). **PASS** — single paragraph is within "1-2 sentences"
  range.
- `location-codes.md`: 1 paragraph (what it does + why it matters
  combined). **PASS.**

- [ ] **Step 3: Check L03 — Scope & Audience structure**

Check each spec for the three-part structure:

- `slitemdata.md`: Has `**Audience:**`, `**In scope:**`,
  `**Out of scope:**`. **PASS.**
- `item-types.md`: Has `**Audience:**`, `**In scope:**`,
  `**Out of scope:**`. **PASS.**
- `location-codes.md`: Has `**Audience:**`, `**In scope:**`,
  `**Out of scope:**`. **PASS.**

- [ ] **Step 4: Check L04 — plain English in rule statements**

Search for technical field names in non-technical sections:

```bash
grep -n "itype_code_num\|location_code\|bcode2\|is_suppressed" specs/reports/slitemdata.md
```

Review hits — these should only appear in `**Technical implementation:**`
blocks and Data Sources/Exclusions tables, not in plain-English rule
statements.

slitemdata.md F01 plain-English statement: "An item is flagged when its
bibliographic material type code is not consistent with its item type."
Uses "material type code" and "item type" — good, plain English.
Technical implementation block: uses `itype_code_num`, `bcode2` —
appropriate. **PASS.**

item-types.md Purpose (line 19): "Item type codes (itypes) are numeric
codes on item records..." — uses "(itypes)" as a parenthetical
clarification, not as the primary term. **PASS** — this is in the
Purpose, not a rule statement.

- [ ] **Step 5: Check L05 — Status label formatting**

Search for Status lines across all specs:

```bash
grep -n "^\*\*Status:" specs/reports/*.md specs/code-tables/*.md
```

Expected format: `**Status:** {value}` (bold label with colon inside
bold, space, lowercase value).

Check that all Status lines match. Common deviations: colon outside
bold, capitalized value, missing space.

- [ ] **Step 6: Fix L06 — code-table-guide Change Log**

Current (line 60):
```
- 2026-03-13 · Initial stub migrated from FRAMEWORK.md v1.0
```

Expected per L06:
```
- 2026-03-13 · v0.1.0 · Initial stub migrated from FRAMEWORK.md (ILS Team)
```

Fix this entry.

- [ ] **Step 7: Check L07 — Purpose opening phrasing**

- slitemdata.md: "This report identifies items..." — does not restate
  title. **PASS.**
- item-types.md: "Item type codes (itypes) are numeric codes..." —
  close to title but adds context. **PASS.**
- location-codes.md: "Location codes identify where an item is
  housed..." — does not restate title. **PASS.**

- [ ] **Step 8: Run formatting and commit**

```bash
./scripts/format-specs.sh
git add specs/guides/code-table-guide.md
# Also add any other spec files that were modified during L01-L07 checks
git commit -m "docs: fix language and tone issues (L01-L07 audit pass)"
```

______________________________________________________________________

### Task 5: Pass 3 — Cross-References & Linking Audit

Audit all files for X01-X07. This pass has the most concrete findings
from the pre-audit research.

**Files:**

- Modify: `specs/FRAMEWORK.md` (fix anchor link)
- Modify: `specs/guides/report-guide.md` (fix anchor link)
- Modify: `specs/README.md` (fix directory links)
- Other files as needed

- [ ] **Step 1: Check X01 — relative link style**

Search for all markdown links in spec files:

```bash
grep -oP '\]\([^)]+\)' specs/**/*.md specs/*.md
```

Verify:
- Links from `specs/` root use `./` prefix
- Links from category subfolders use `../`
- No absolute paths or bare filenames

- [ ] **Step 2: Check X02 — front matter refs have body links**

`slitemdata.md` front matter:
- `depends_on: code-tables/location-codes` — check body for a link to
  location-codes.md.
- `depends_on: code-tables/item-types` — body link at line 196:
  `[item types](../code-tables/item-types.md)`. **PASS.**
- `related_specs: reports/slmissing` — `slmissing` does not exist yet.
  No body link expected for a spec that does not exist.

**Finding X02-001:** `slitemdata.md` lists `code-tables/location-codes`
in `depends_on` but has no body-prose link to `location-codes.md`. The
item-types dependency has a body link but location-codes does not.

**Fix:** Add a link to location-codes.md in the slitemdata.md body.
Natural placement is in the Scope & Audience or Flag Conditions intro,
e.g.:

```markdown
Each flag condition causes an item to appear in the report output. An
item may be flagged for multiple reasons. Flag conditions reference
[item types](../code-tables/item-types.md) and
[location codes](../code-tables/location-codes.md) defined in the
code table specifications.
```

- [ ] **Step 3: Fix X04/X07 — broken anchor links (CONFIRMED)**

**Finding X07-001:** Two files contain `#itype-70--book-on-cd` (double
hyphen) but the actual MkDocs anchor is `#itype-70-book-on-cd` (single
hyphen). This was empirically verified.

Fix in `specs/FRAMEWORK.md` line 165:
```markdown
# Before:
See [Book on CD](../code-tables/item-types.md#itype-70--book-on-cd) for details
# After:
See [Book on CD](../code-tables/item-types.md#itype-70-book-on-cd) for details
```

Fix in `specs/guides/report-guide.md` line 352:
```markdown
# Before:
See [Book on CD](../code-tables/item-types.md#itype-70--book-on-cd) for
# After:
See [Book on CD](../code-tables/item-types.md#itype-70-book-on-cd) for
```

- [ ] **Step 4: Check X03 — glossary terms linked on first use**

Identify glossary terms used in spec body text by cross-referencing
the glossary headings (`specs/glossary.md`) with spec content:

Glossary terms: barcode, bib record, bcode2, call number, item,
item type, location code, suppressed.

For each spec, check if these terms are linked to the glossary on
first use in each `##` section:

`slitemdata.md`:
- "item type" appears in Purpose (line 28) — not linked. **NOTE.**
- "location code" appears in Purpose (line 29) — not linked. **NOTE.**
- "suppressed" appears in Scope & Audience (line 47) — not linked.
  **NOTE.**
- "bcode2" appears in Data Sources table — technical context, linking
  optional. **PASS.**
- "barcode" appears in Output table — not linked. **NOTE.**

`item-types.md` and `location-codes.md`: These ARE the glossary
definitions for their respective terms. Linking to the glossary would
be circular. **PASS.**

**Finding X03-001:** `slitemdata.md` uses several glossary terms
("item type", "location code", "suppressed", "barcode") without
linking to the glossary. Per X03 (Note severity), these should be
linked on first use per `##` section.

**Fix:** Add glossary links on first use in slitemdata.md. Example
for the Purpose section:

```markdown
This report identifies items in the catalog whose data is internally
inconsistent — where the [item type](../glossary.md#item-type),
[location code](../glossary.md#location-code), bibliographic material
type, or audience designation do not match the expected combinations.
```

This is a Note-severity finding. Apply if it improves readability; skip
if it clutters the prose. Flag for human decision.

- [ ] **Step 5: Check X05 — guides link to FRAMEWORK.md**

`report-guide.md` links to FRAMEWORK.md:
- Line 103: `[Front Matter Schema](../FRAMEWORK.md#front-matter-schema)`
- Line 317: `[Front Matter Schema](../FRAMEWORK.md#front-matter-schema)`
- Line 358: `[Cross-Referencing Conventions](../FRAMEWORK.md#cross-referencing-conventions)`

**PASS.** Guide links to framework for shared conventions.

`code-table-guide.md`: Does not link to FRAMEWORK.md. It should link
to the Front Matter Schema for the `code_prefix` field.

**Finding X05-001:** code-table-guide.md should link to FRAMEWORK.md
for front matter field documentation rather than explaining
`code_prefix` inline.

- [ ] **Step 6: Check X06 — orphan references**

FRAMEWORK.md Category Guides table (lines 122-129) lists:
- Report → `./guides/report-guide.md` — exists. **PASS.**
- Code Table → `./guides/code-table-guide.md` — exists. **PASS.**
- Loan Rule → "Planned" (no link) — **PASS** (no orphan).
- Workflow → "Planned" — **PASS.**
- Policy → "Planned" — **PASS.**

**X06: PASS.**

- [ ] **Step 7: Check X07 — all links resolve**

For every `[text](path)` link in spec files, verify the target file
exists. Use the link list from step 1. Pay special attention to:
- Links with anchors (verify the heading exists in the target)
- Links to guides (relative path correctness)

The glossary example links at lines 11 and 17 of `glossary.md` use
paths that start from the wrong directory (`../glossary.md` from
within glossary.md itself). These are in code blocks (examples), not
actual links, so they do not break. **PASS** — they are illustrative.

- [ ] **Step 8: Apply all cross-reference fixes and commit**

```bash
./scripts/format-specs.sh
git add specs/FRAMEWORK.md specs/guides/report-guide.md specs/reports/slitemdata.md
git commit -m "fix(cross-refs): correct anchors, add missing body links, glossary links (X02-X07)"
```

______________________________________________________________________

## Chunk 2: Phase 1 — Audit Passes 4-5

### Task 6: Pass 4 — Redundancy & Ownership Audit

Audit all files for R01-R06.

**Files:**

- Potentially modify: `specs/guides/report-guide.md`, `README.md`

- [ ] **Step 1: Check R01 — front matter docs in FRAMEWORK.md only**

`report-guide.md` "Front Matter" section (lines 52-104): Explains
fields in plain language with which team cares about which. Links to
FRAMEWORK.md for full schema.

This is NOT a duplication — it is audience-appropriate guidance that
supplements the framework. The guide explains "what the Report
Assessment Team should care about" vs. "what the ILS Team manages."
**PASS** — this is appropriate guide content, not redundant
redefinition.

`code-table-guide.md`: Explains `code_prefix` inline (lines 48-54).
This is minimal and supplemental. **PASS** — but should add a link to
FRAMEWORK.md (see X05-001).

- [ ] **Step 2: Check R02 — section ordering in guides only**

FRAMEWORK.md no longer contains section ordering for individual
categories (removed in framework 2.0). The Category Guides table
(lines 122-129) points to the guides. **PASS.**

- [ ] **Step 3: Check R03 — source-of-truth restatements**

The phrase "source of truth" appears in these spec-ecosystem files:
1. `FRAMEWORK.md` overview: "authoritative, human-readable source of
   truth" (line 13) — **canonical statement**
2. `README.md` (root): "Specifications are the source of truth" (line 8)
3. `report-guide.md`: "The specification is the source of truth" (line 16)
4. `AGENTS.md`: "Specifications are the source of truth" (line 9)

**Finding R03-001:** The principle is restated in 3 additional places
beyond FRAMEWORK.md. The root README.md and AGENTS.md restatements are
appropriate — they are entry points for different audiences (humans and
AI agents respectively) and need to establish the principle immediately.

The report-guide.md restatement (line 16) is a judgment call. It
reinforces the principle for the Report Assessment Team audience. Flag
for human decision: keep as-is (intentional emphasis for the primary
guide audience) or replace with a link to FRAMEWORK.md.

- [ ] **Step 4: Check R04 — cross-ref conventions in FRAMEWORK.md**

`report-guide.md` Part 5 "Working with Code Tables" (lines 328-359):
Shows examples of cross-referencing and links to FRAMEWORK.md for full
conventions at line 358. **PASS** — correctly delegates to framework.

- [ ] **Step 5: Check R05 — glossary definitions in glossary.md only**

Search specs for inline definitions of glossary terms:

```bash
grep -n "bcode2\|item type\|location code\|suppressed" specs/reports/slitemdata.md
```

`slitemdata.md` uses glossary terms but does not redefine them inline.
The Data Sources table references `bcode2` and `is_suppressed` as field
names, which is appropriate in a technical context.

item-types.md and location-codes.md: These ARE the canonical definitions
for their respective code tables, so they define the terms. **PASS.**

- [ ] **Step 6: Check R06 — spec listing in specs/README.md only**

Root `README.md`: Lists categories but links to `specs/README.md` for
the index (line 26: "Start with [specs/README.md](specs/README.md)").
Does not duplicate the per-spec table. **PASS.**

- [ ] **Step 7: Record findings and commit if any fixes needed**

Record R03-001 for the rules file (judgment call, flagged for human
decision). If no file changes needed, skip commit.

______________________________________________________________________

### Task 7: Pass 5 — MkDocs Compatibility Audit

Audit all files for M01-M06. Run `uv run mkdocs build --strict`.

**Files:**

- Modify: `specs/README.md` (fix directory links)
- Modify: `specs/glossary.md` (add front matter)
- Modify: `mkdocs.yml` (if nav issues found)

- [ ] **Step 1: Check M01 — all files in mkdocs.yml nav**

Current nav in `mkdocs.yml`:
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

All 8 spec-ecosystem files under `specs/` are present. **M01: PASS.**

- [ ] **Step 2: Verify M02 — anchor slug format (CONFIRMED)**

Empirically verified from MkDocs build output:
- `### ITYPE-70 · Book on CD` → `id="itype-70-book-on-cd"`
- `### C01 · Branch Locations` → `id="c01-branch-locations"`
- `### F01 · Material Type / Item Type Mismatch` → `id="f01-material-type-item-type-mismatch"`

**Canonical format:** The `·` separator and surrounding spaces are
collapsed to a single hyphen. Slashes (`/`) are removed. Consecutive
hyphens do NOT appear in the output — they collapse.

Record this as the verified canonical form for rules X04 and M02.

- [ ] **Step 3: Check M03 — paths relative to specs/ docs_dir**

All nav paths in mkdocs.yml use paths relative to `specs/` (the
`docs_dir`). Links within files use relative paths from their own
location. **PASS.**

- [ ] **Step 4: Fix M04 — add front matter title where missing**

Files needing `title` front matter:

`specs/glossary.md` — currently has NO front matter. Add:
```yaml
---
title: Glossary
---
```

`specs/README.md` — no front matter. MkDocs renders the page title
from the nav entry ("Home": `README.md`) so a front matter `title`
is redundant. **Explicit decision: SKIP.** Record as M04-002 in the
rules file so the agent knows this was intentional, not missed.

`specs/FRAMEWORK.md` — has `version` and `purpose` but no `title`. Add:
```yaml
title: CHPL ILS Specification Framework
```

(Add `title` field to the existing front matter block, keeping
`version` and `purpose`.)

- [ ] **Step 5: Fix M05 — directory links in specs/README.md**

**Finding M05-001:** `specs/README.md` lines 11-15 use directory links
(`reports/`, `code-tables/`, etc.) that MkDocs warns about:
```
INFO - Doc file 'README.md' contains an unrecognized relative link 'reports/'
```

These links work on GitHub (showing directory contents) but are
meaningless in MkDocs. Replace with links to actual spec files or
remove the link wrapping:

Option A (remove links, keep as plain text in table):
```markdown
| reports/         | Reports     | ...
| code-tables/     | Code Tables | ...
```

Option B (link to the first spec in each category):
This is fragile and would need updating.

**Recommendation:** Option A — remove the directory links. The table
below in the same file already links to individual specs. The directory
links are redundant navigation.

- [ ] **Step 6: Check M06 — nav reflects category organization**

Nav has: Home, Reference (Framework, Glossary), Guides (Report, Code
Table), Reports (slitemdata), Code Tables (location-codes, item-types).
This matches the actual file organization. **PASS.**

- [ ] **Step 7: Run mkdocs build --strict and verify clean**

```bash
uv run mkdocs build --strict 2>&1
```

Expected: No warnings after fixing directory links and anchor formats.

- [ ] **Step 8: Run validation and formatting**

```bash
uv run python scripts/validate-specs.py
./scripts/format-specs.sh
```

- [ ] **Step 9: Commit all MkDocs fixes**

```bash
git add specs/glossary.md specs/FRAMEWORK.md specs/README.md
git commit -m "fix(mkdocs): add front matter titles, fix directory links (M04/M05)"
```

______________________________________________________________________

## Chunk 3: Phase 2 — Agent

### Task 8: Write Agent Rules File

Create `.claude/agents/spec-auditor-rules.md` containing all rules from
the design doc plus the specific findings from Phase 1.

**Files:**

- Create: `.claude/agents/spec-auditor-rules.md`

- [ ] **Step 1: Create the rules file**

Write `.claude/agents/spec-auditor-rules.md` with all 34 rules (S01-S08,
L01-L07, X01-X07, R01-R06, M01-M06) using the structure from the design
doc:

```markdown
### {ID}: {Short name}

- **Dimension:** {Structure | Language | Cross-References | Redundancy | MkDocs}
- **Severity:** {Error | Warning | Note}
- **Check:** {What to look for}
- **Expected:** {What correct looks like}
- **Example finding:** {Specific Phase 1 finding with file path}
```

Include all Phase 1 findings as example findings:
- S02-001: `location-codes.md` used "Rules / Codes" heading (fixed)
- S04-001: Horizontal rules convention (resolved — specs use them
  between `###` entries, reference docs between `##` sections)
- L06-001: code-table-guide.md change log missing version/team (fixed)
- X02-001: `slitemdata.md` missing body link for `depends_on:
  code-tables/location-codes` (fixed)
- X03-001: `slitemdata.md` glossary terms not linked on first use
  (judgment call — Note severity)
- X05-001: `code-table-guide.md` missing FRAMEWORK.md link
- X07-001: Double-hyphen anchors in FRAMEWORK.md and report-guide.md
  (fixed to single hyphen)
- R03-001: Source-of-truth restated in 4 places (judgment call)
- M04-001: glossary.md and FRAMEWORK.md missing front matter title
  (fixed)
- M04-002: specs/README.md has no front matter title — explicitly
  skipped because MkDocs nav entry provides the page title
- M05-001: specs/README.md directory links (fixed)

- [ ] **Step 2: Commit the rules file**

```bash
git add .claude/agents/spec-auditor-rules.md
git commit -m "docs(agent): create spec auditor rules file with Phase 1 findings"
```

______________________________________________________________________

### Task 9: Write Agent Definition

Create `.claude/agents/spec-auditor.md` with the agent prompt using
enumerated instructions throughout.

**Files:**

- Create: `.claude/agents/spec-auditor.md`

- [ ] **Step 1: Write agent identity and startup checklist**

Start `.claude/agents/spec-auditor.md` with:

```markdown
# Spec Auditor

You are a documentation consistency reviewer for the CHPL ILS
Specification Framework. You audit spec files for consistency
across five dimensions and cooperate with human reviewers.

## Audiences

- **ILS Team** — technical, maintains framework and tooling
- **Report Assessment Team** — non-technical, owns report spec content

## Startup Checklist

When you start, you must:

1. Read `.claude/agents/spec-auditor-rules.md` to load rules and
   regression baselines
2. Read `specs/FRAMEWORK.md` for universal conventions
3. Read `specs/schema.yaml` for valid categories, statuses, required
   fields, and rule prefixes
4. Read all guides in `specs/guides/` for section ordering
5. Read `mkdocs.yml` for nav structure
6. Determine mode from the user's message:
   - No argument or "review": review mode
   - "fix": fix mode
   - File path argument: scope to that file
   - "--dimension {name}": scope to that dimension
   - "regressions": regression check only
7. Read all spec files listed in the rules file's "Files in Scope"
8. Execute the appropriate audit pass(es)
```

- [ ] **Step 2: Write mode definitions**

Add the three mode sections using numbered steps and explicit
conditional logic:

```markdown
## Review Mode (default)

1. Apply each rule set (S, L, X, R, M) across all in-scope files
2. For each rule, check the condition described in "Check" field
3. Compare against the "Expected" field
4. Record findings with these severity levels:
   - **Error** — violates a hard convention
   - **Warning** — inconsistency that should be fixed
   - **Note** — suggestion for improvement
5. Produce output organized by:
   - Dimension → File → Severity
6. Do NOT modify any files
7. When a finding could be intentional, say so:
   - "This may be intentional. Flagging for human decision."

## Fix Mode

1. Run all review mode steps (1-5) first
2. Group fixes into batches:
   - Mechanical fixes (links, headings, formatting): batch by file
   - Judgment calls (language, redundancy): present individually
3. For each batch:
   a. Present proposed changes with plain-English explanations
   b. Explain WHY, not just what
   c. Use language the Report Assessment Team can understand
   d. Wait for human approval
   e. Apply approved changes
   f. Move to next batch
4. Re-run all rules to check for regressions
5. Present summary of changes and skips

## Regressions Mode

1. Load only rules that have "Example finding" entries
2. Check each example finding against current file state
3. Report: Clean (not recurred) or Regression (recurred)
4. If regression found: elevate severity and note original date
5. Do NOT check for new issues
6. Do NOT modify files
```

- [ ] **Step 3: Write cooperation model**

Add the cooperation model section:

```markdown
## Cooperation Model

1. **Ambiguity:** Flag as question, not error. Example: "This
   section restates the source-of-truth principle. This may be
   intentional for emphasis. Flagging for human decision."
2. **Audience awareness:** Use plain English. Say "the link to
   the glossary is missing" not "relative path anchor resolution
   failed."
3. **Batch approval:** Mechanical fixes batched. Judgment calls
   individual. Human can approve, reject, or modify.
4. **Progressive disclosure:** Start with summary count, then
   dimension by dimension. Let human decide depth.
```

- [ ] **Step 4: Write output format and rules file reference**

Add the output format and rules file reference:

```markdown
## Output Format

Start every audit with:
```
Spec Auditor — {mode} mode
Files in scope: {count}
Rules loaded: {count}
```

Then for each dimension with findings:
```
## {Dimension Name}

### {file path}
- {SEVERITY} [{rule ID}]: {description}
```

End with:
```
Summary: {errors} errors, {warnings} warnings, {notes} notes
```

## Rules File

Read `.claude/agents/spec-auditor-rules.md` for the complete rule
set. Each rule specifies:
- What to check
- What correct looks like
- An example of a real finding from the initial audit

When the rules file and this prompt disagree, the rules file wins
for what-to-check decisions. This prompt wins for how-to-behave
decisions.
```

- [ ] **Step 5: Commit the agent definition**

```bash
git add .claude/agents/spec-auditor.md
git commit -m "feat(agent): create spec-auditor agent with review, fix, regressions modes"
```

______________________________________________________________________

### Task 10: Verify Agent Baseline

Run the agent in review mode against the (now fixed) specs to verify
a clean baseline.

**Files:**

- No modifications expected

- [ ] **Step 1: Run the agent in review mode**

```bash
claude --agent spec-auditor
```

Expected: The agent reads all files, applies all rules, and reports a
clean (or near-clean) baseline. Any remaining findings should be Notes
or intentional judgment calls (like R03-001), not Errors or Warnings.

- [ ] **Step 2: If issues found, fix and re-run**

If the agent finds issues that were missed in Phase 1, fix them and
add the findings to the rules file as new example findings. Re-run
until clean.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "docs: clean baseline after spec-auditor verification"
```

______________________________________________________________________

## Summary

| Task | Phase | Description | Key Files |
| --- | --- | --- | --- |
| 1 | 1 Pre-flight | Codify code-table section ordering | `code-table-guide.md` |
| 2 | 1 Pass 1 | Structure audit — report spec | `slitemdata.md` |
| 3 | 1 Pass 1 | Structure audit — code table specs | `location-codes.md` |
| 4 | 1 Pass 2 | Language & tone audit | `code-table-guide.md`, all specs |
| 5 | 1 Pass 3 | Cross-references & linking audit | `FRAMEWORK.md`, `report-guide.md` |
| 6 | 1 Pass 4 | Redundancy & ownership audit | All files (mostly read-only) |
| 7 | 1 Pass 5 | MkDocs compatibility audit | `glossary.md`, `README.md`, `FRAMEWORK.md` |
| 8 | 2 | Write agent rules file | `spec-auditor-rules.md` |
| 9 | 2 | Write agent definition | `spec-auditor.md` |
| 10 | 2 | Verify agent baseline | All files |
