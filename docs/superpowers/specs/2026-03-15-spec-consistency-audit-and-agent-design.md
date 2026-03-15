# Design: Spec Consistency Audit & Audit Agent

## Problem

The ILS Specification Framework is young (8 commits, 3 specs) and already
showing early signs of inconsistency across documents:

- Section ordering and naming varies between specs of the same category
- Language conventions from the style guide (present tense, plain English,
  "what vs. why" separation) may not be applied uniformly
- Cross-references use different link styles or are missing where they
  should exist
- Content is potentially restated across FRAMEWORK.md, category guides,
  and individual specs rather than living in one canonical place
- Links that work on GitHub may not work in the MkDocs-published site

These issues compound as the project grows. Without a systematic audit
now and a reusable agent to enforce consistency going forward, each new
spec risks introducing drift that becomes harder to correct later.

## Goals

1. Perform a comprehensive, dimension-centric audit of all spec ecosystem
   files (9 markdown files) across five consistency dimensions.
2. Fix all issues found during the audit.
3. Capture every finding as a named rule with an example, forming a
   regression suite.
4. Build a reusable Spec Audit Agent that enforces these rules in two
   modes (review and fix), cooperating with human reviewers from the ILS
   Team and Report Assessment Team.

## Non-Goals

- Writing new specs (loan-rule, workflow, policy categories)
- Completing the code-table-guide stub beyond what the audit requires
- Changes to the validation script or CI pipeline
- Changing the front matter schema

## Deliverables

1. **Audit findings and fixes** applied directly to spec files
2. **Agent definition** at `.claude/agents/spec-auditor.md`
3. **Agent rules file** at `.claude/agents/spec-auditor-rules.md`

______________________________________________________________________

## Phase 1: Dimension-Centric Audit

Five passes across all documents, each focused on one consistency
concern. Issues are fixed as discovered. Each finding is recorded as a
rule for the agent.

### Pre-Flight: Known Deviations

Before starting the dimension passes, acknowledge the current state of
files that do not yet conform to the conventions they will be audited
against. These are not failures — they are the starting conditions the
audit will resolve.

| File | Deviation | Resolution |
| --- | --- | --- |
| `specs/code-tables/location-codes.md` | Uses "Rules / Codes" section heading instead of "Registry"; uses `C01`/`C02` rule-style identifiers instead of `LOC-xxx` registry entries; missing `code_prefix` front matter field | Audit will determine whether this file should use registry format (like item-types.md) or a separate "rules/categories" structure. See S08. |
| `specs/guides/code-table-guide.md` | Stub — does not prescribe a full section ordering. S02 references an ordering that the guide does not yet define. | Phase 1 Pass 1 will codify the code-table section ordering in the guide as a prerequisite to auditing against it. |
| `specs/glossary.md` | No YAML front matter at all (no `title` field) | Will be addressed under M04. |
| `specs/guides/code-table-guide.md` | Change log entry missing version number and team per L06 format | Will be fixed during Pass 2. |

### Files in Scope

| File                              | Role                          |
| --------------------------------- | ----------------------------- |
| `specs/FRAMEWORK.md`              | Universal conventions         |
| `specs/glossary.md`               | Controlled vocabulary         |
| `specs/README.md`                 | Spec index                    |
| `specs/guides/report-guide.md`    | Report category guide         |
| `specs/guides/code-table-guide.md`| Code table category guide     |
| `specs/reports/slitemdata.md`     | Report spec                   |
| `specs/code-tables/item-types.md` | Code table spec               |
| `specs/code-tables/location-codes.md` | Code table spec           |
| `README.md`                       | Project entry point           |

### Dimension 1: Structure & Layout

Check that every spec follows the section ordering prescribed by its
category guide, and that headings use consistent levels, naming, and
formatting.

**Rules:**

- S01 (Error): Report specs must have sections in this order:
  1. Purpose
  2. Scope & Audience
  3. Data Sources
  4. Flag Conditions
  5. Output & Delivery
  6. Exclusions & Edge Cases
  7. Open Questions
  8. Known Limitations
  9. Change Log
- S02 (Error): Code table specs must have sections in this order:
  1. Purpose
  2. Scope & Audience
  3. Registry (for code-value listings) or Rules (for structural
     categories) — see S08
  4. Sierra Configuration
  5. Open Questions
  6. Change Log
  - **Note:** This ordering must be codified in the code-table-guide
    during Phase 1 Pass 1 before auditing against it. The current
    guide stub does not prescribe it.
- S03 (Error): All specs start with an `# {title}` heading that matches
  the front matter `title` field exactly.
- S04 (Warning): Horizontal rules are used consistently as section
  separators.
  - Current state: FRAMEWORK.md, guides, and glossary use them;
    specs vary. Audit will determine one convention.
- S05 (Error): Flag condition headings follow `### F{nn} · {Name}`
  pattern. The prefix `F` comes from `schema.yaml` `rule_prefixes`
  for the `report` category.
- S06 (Error): Registry entry headings follow
  `### {PREFIX}-{code} · {Label}`, where `{PREFIX}` is the
  `code_prefix` front matter field.
- S07 (Warning): Every spec ends with a Change Log section as the last
  section.
- S08 (Error): Code table rule/category headings follow
  `### C{nn} · {Name}` pattern. The prefix `C` comes from
  `schema.yaml` `rule_prefixes` for the `code-table` category.
  - This applies to code table specs that describe structural
    categories (like location-codes.md) rather than individual
    code-value registries (like item-types.md).
  - A code table spec uses EITHER a Registry section (S06 headings)
    OR a Rules section (S08 headings), not both.
  - `code_prefix` is required for Registry-style specs (it provides
    the heading prefix). It is not required for Rules-style specs.

### Dimension 2: Language & Tone

Check for consistent phrasing conventions, present tense, plain English
per the style guide, and non-repetitive language in parallel sections.

**Rules:**

- L01 (Warning): Present tense throughout.
  - Correct: "An item is flagged when..."
  - Incorrect: "An item will be flagged when..."
- L02 (Note): Purpose sections across specs use similar structure:
  1. What it does (1-2 sentences)
  2. Why it matters (1-2 sentences)
  3. Optional additional context (1 paragraph max)
- L03 (Warning): Scope & Audience sections use consistent three-part
  structure:
  - `**Audience:**` — who uses this
  - `**In scope:**` — what is covered
  - `**Out of scope:**` — what is excluded
- L04 (Warning): Plain English in rule/condition statements.
  - Use "item type" not "itype"
  - Use "location code" not "location_code"
  - Technical names belong only in Technical Implementation notes
- L05 (Warning): Status labels use consistent formatting:
  `**Status:** {value}` (bold label, colon inside bold, space,
  lowercase value).
- L06 (Warning): Change Log entries follow the format:
  `- {YYYY-MM-DD} · v{version} · {description} ({team})`
  - Known deviation: `code-table-guide.md` entry is missing version
    and team name.
- L07 (Note): Avoid opening Purpose sections with the document title
  restated verbatim.
  - Correct: "Item type codes classify items for circulation policy..."
  - Avoid: "The Item Types code table documents item type codes..."

### Dimension 3: Cross-References & Linking

Check that every link resolves, link style is consistent, and things
that should be linked are linked.

**Rules:**

- X01 (Error): All inter-spec references use relative markdown links.
  - From `specs/` root: `./glossary.md`, `./FRAMEWORK.md`
  - From category subfolders: `../glossary.md`, `../FRAMEWORK.md`
  - Never absolute paths or bare filenames
- X02 (Warning): Front matter `depends_on` and `related_specs` entries
  each have at least one corresponding body-prose link in the document.
- X03 (Note): Glossary terms are linked on first use per major section
  (not every occurrence, but at least once where the term first appears
  in each `##`-level section).
- X04 (Error): Registry entries referenced from other specs use anchor
  links. The anchor slug must match the actual MkDocs-generated anchor
  for the heading.
  - The canonical anchor format must be tested against
    `uv run mkdocs build --strict` during Phase 1 Pass 5. The `·`
    separator produces a slug that needs empirical verification
    (e.g., `### ITYPE-70 · Book on CD` may produce
    `#itype-70--book-on-cd` or `#itype-70-book-on-cd` depending on
    whether MkDocs collapses consecutive hyphens).
  - Once verified, document the canonical form in this rule.
- X05 (Warning): Guide files link back to FRAMEWORK.md for shared
  conventions rather than restating them.
- X06 (Error): No orphan references — if FRAMEWORK.md mentions a guide,
  that guide exists (even as a stub).
- X07 (Error): No dead links — every `[text](path)` and
  `[text](path#anchor)` resolves to an existing file and (where
  applicable) a valid heading anchor.

### Dimension 4: Redundancy & Ownership

Check that content lives in one canonical place with links from
elsewhere, not restated in multiple locations.

**Rules:**

- R01 (Warning): Front matter field documentation lives in FRAMEWORK.md
  only. Guides reference it with a link, do not redefine fields.
- R02 (Warning): Section structure and ordering lives in category guides
  only. FRAMEWORK.md references the guides via the Category Guides
  table.
- R03 (Note): The source-of-truth principle is stated once prominently
  in FRAMEWORK.md's overview.
  - Other documents (guides, specs/README.md, root README.md) may
    reference it but should not restate it in different words.
  - This is a judgment call — flagged for human decision when found.
- R04 (Warning): Cross-referencing conventions live in FRAMEWORK.md.
  Guides show examples but link to the framework for full rules.
- R05 (Warning): Glossary term definitions live in glossary.md only.
  Specs link to glossary terms, do not re-explain inline.
- R06 (Note): The "what specs exist" listing lives in specs/README.md
  only. Root README.md links to it rather than duplicating the table.

### Dimension 5: MkDocs Compatibility

Check that everything works when published through MkDocs Material to
GitHub Pages.

**Rules:**

- M01 (Error): Every spec and guide file appears in `mkdocs.yml` nav.
- M02 (Error): Anchor links use MkDocs-compatible slug format:
  - Lowercase
  - Spaces become hyphens
  - Special characters (including `·`) become hyphens
  - Whether consecutive hyphens collapse must be empirically verified
    during Phase 1 Pass 5 (see X04)
- M03 (Error): The `docs_dir: specs` setting means all nav paths and
  links are relative to `specs/` — verify paths work from that root.
- M04 (Warning): Non-spec markdown files that appear in the MkDocs site
  should have a front matter `title` field for MkDocs page titles.
  This applies to:
  - Guide files (`specs/guides/*.md`)
  - `specs/glossary.md` (currently has no front matter at all)
  - `specs/FRAMEWORK.md` (has `version` and `purpose` but no `title`)
  - `specs/README.md` (no front matter)
  - Spec files already have `title` in their required front matter.
- M05 (Warning): No links use GitHub-specific features that fail in
  MkDocs:
  - Directory links with trailing `/`
  - Links to non-markdown files without explicit handling
- M06 (Warning): Nav structure in mkdocs.yml reflects the actual
  category organization and includes all published documents.

**Validation:** Run `uv run mkdocs build --strict` to catch broken
links and missing nav entries.

______________________________________________________________________

## Phase 2: Spec Audit Agent

### Overview

A Claude Code agent at `.claude/agents/spec-auditor.md` that performs
consistency audits across the spec ecosystem. It operates in two modes
and cooperates with human reviewers.

### Agent Identity

- Documentation consistency reviewer for the CHPL ILS Specification
  Framework
- Understands: framework conventions, category guides, glossary, MkDocs
  publishing pipeline
- Cooperates with two primary human audiences:
  - **ILS Team** — technical, maintains framework and tooling
  - **Report Assessment Team** — non-technical, owns report spec content

### Modes

#### Review Mode (default)

1. Read all spec ecosystem files listed in the Files in Scope table
2. Read the rules file (`.claude/agents/spec-auditor-rules.md`)
3. Apply each rule set (S, L, X, R, M) across all files
4. Produce a structured findings report organized by:
   - Dimension (Structure, Language, Cross-References, Redundancy, MkDocs)
   - Then by file within each dimension
   - Then by severity within each file
5. Do NOT modify any files
6. Use these severity levels:
   - **Error** — violates a hard convention (missing required section,
     broken link, wrong heading pattern)
   - **Warning** — inconsistency that should be fixed (language drift,
     missing glossary link, redundant content)
   - **Note** — suggestion for improvement (could link this term, section
     is unusually long or short compared to peers)
7. When a finding is ambiguous (might be intentional), say so explicitly:
   - "This may be intentional for emphasis. Flagging for human decision."

#### Fix Mode

1. Perform all review mode steps (1-4) to identify issues

2. Group related fixes into batches:
   - Mechanical fixes (link corrections, heading format, status line
     formatting) are grouped by file
   - Judgment calls (language rewording, redundancy elimination) are
     presented individually
3. For each batch:
   a. Present the proposed changes with plain-English explanations
   b. Explain WHY each change is being made, not just what changed
   c. Use language suitable for the Report Assessment Team — avoid
      developer jargon in explanations
   d. Wait for human approval before applying
   e. Apply approved changes
   f. Move to the next batch
4. After all batches are processed, run the full rule set again to
   verify no regressions were introduced by the fixes
5. Present a summary of what was changed and what was skipped

#### Regressions Mode

1. Read the rules file and load only rules that have example findings
   with file paths (these are the regression baselines)
2. Check each baseline finding against the current file state
3. Report:
   - **Clean** — previously fixed issue has not recurred
   - **Regression** — issue has recurred (elevated severity, includes
     note about when it was originally found)
4. Do NOT check for new issues — only check known baselines
5. Do NOT modify any files
6. This mode is fast and focused — useful as a pre-commit check or
   after bulk edits

### Rule Sets

Rules are maintained in `.claude/agents/spec-auditor-rules.md` so they
can be updated independently of the agent prompt.

Each rule has this structure:

```markdown
### {ID}: {Short name}

- **Dimension:** {Structure | Language | Cross-References | Redundancy | MkDocs}
- **Severity:** {Error | Warning | Note}
- **Check:** {What to look for — one sentence}
- **Expected:** {What correct looks like — one sentence or brief example}
- **Example finding:** {A specific issue found in the Phase 1 audit,
  with file path and description}
```

### Regression Guard

1. The Phase 1 audit findings are captured in the rules file as example
   findings with file paths and descriptions.
2. On every run, the agent checks that previously-fixed issues have not
   recurred.
3. If a fixed issue reappears:
   - Flag it with elevated severity (Warning becomes Error)
   - Include a note: "This issue was previously found and fixed on
     {date}. It has recurred."
4. New findings discovered in subsequent runs can be added to the rules
   file, expanding the regression suite over time.

### Onboarding New Categories

When a new category guide is written (e.g., loan-rule-guide.md):

1. Add section-ordering rules to the rules file following the pattern
   of S01/S02 (the guide prescribes the ordering; the rule enforces it)
2. Add the heading pattern rule following S05/S06/S08 (using the
   `rule_prefixes` value from `schema.yaml` for the new category)
3. Run the agent in review mode to check any existing specs in the new
   category against the new rules
4. Add the guide to the agent's startup checklist (step 4 reads all
   guides in `specs/guides/`)

No changes to the agent prompt are needed — only the rules file grows.

### Schema.yaml Integration

The agent reads `specs/schema.yaml` at startup (step 3 in the startup
checklist) and uses it as a source of truth for:

- Valid categories and their folder names (used by S01, S02)
- Rule identifier prefixes per category (used by S05, S08)
- Required front matter fields per category (cross-referenced with
  the validation script, not duplicated)
- Valid status values (used by L05)

### Cooperation Model

The agent is designed to work WITH humans, not replace their judgment:

1. **Ambiguity handling:**
   - When a finding could be intentional, flag it as a question rather
     than an error
   - Example: "This section restates the source-of-truth principle. This
     may be intentional for emphasis, or it may be redundancy worth
     removing. Flagging for human decision."

2. **Audience awareness:**
   - When explaining findings or proposed fixes, use plain English
   - Avoid developer jargon (say "the link to the glossary is missing"
     not "relative path anchor resolution failed")
   - When a fix involves technical details (MkDocs slugs, anchor
     format), explain the WHY in plain terms and the WHAT in technical
     terms

3. **Batch approval:**
   - Mechanical fixes (safe, objective) are batched together for
     efficiency
   - Judgment calls (subjective, context-dependent) are presented one at
     a time
   - The human can approve, reject, or modify any proposed change

4. **Progressive disclosure:**
   - Start with a summary count (e.g., "Found 12 issues: 3 errors,
     7 warnings, 2 notes")
   - Then present dimension by dimension
   - Let the human decide how deep to go

### User-Facing Invocation Guide

#### Prerequisites

- Working directory is the `ils-specs` repository root
- All spec files are present and parseable

#### Commands

```bash
# Full audit, review only (default)
# Reads all spec files, reports issues, changes nothing
claude --agent spec-auditor

# Full audit, fix mode
# Identifies issues and proposes corrections for approval
claude --agent spec-auditor "fix"

# Audit a single file, review only
claude --agent spec-auditor "review specs/reports/slitemdata.md"

# Audit a single file, fix mode
claude --agent spec-auditor "fix specs/reports/slitemdata.md"

# Audit a single dimension across all files
claude --agent spec-auditor "review --dimension cross-references"

# Check for regressions only (previously fixed issues)
claude --agent spec-auditor "regressions"
```

#### What to Expect

- **Review mode:** A structured report printed to your terminal,
  organized by dimension and file. No files are modified. Review the
  findings and decide which to address.
- **Fix mode:** The agent presents batches of proposed changes. For
  each batch, you see what will change and why. Type "yes" to approve,
  "no" to skip, or provide feedback to adjust the fix. After all
  batches, the agent re-runs its checks to confirm no regressions.
- **Single file:** Same as above but scoped to one file. Useful when
  you have just written or edited a spec and want a quick check before
  committing.
- **Single dimension:** Same as full audit but only runs one rule set.
  Useful for focused work (e.g., "I just fixed a bunch of links, check
  only cross-references").

#### Providing Context

When invoking the agent, you can provide additional context:

- **"We just added a new spec"** — the agent will pay extra attention
  to the new file and check that it is properly indexed in
  specs/README.md, linked in mkdocs.yml nav, and follows its category
  guide
- **"Focus on report specs"** — limits the audit to report category
  files plus the report guide
- **"The Report Assessment Team will review these findings"** — the
  agent adjusts its output language to be fully non-technical

### Agent-Facing Startup Checklist

When the agent starts, it must:

1. Read `.claude/agents/spec-auditor-rules.md` to load the current rule
   sets and regression baselines
2. Read `specs/FRAMEWORK.md` to load current universal conventions
3. Read `specs/schema.yaml` to load valid categories, statuses, and
   required fields
4. Read all category guides in `specs/guides/` to load section ordering
   requirements
5. Read `mkdocs.yml` to load the current nav structure
6. Determine mode from the user's invocation:
   - No argument or "review": review mode
   - "fix": fix mode
   - File path argument: scope to that file
   - "--dimension {name}": scope to that dimension
   - "regressions": regression check only
7. Execute the appropriate audit pass(es)
8. Format output according to the mode and any audience context provided

______________________________________________________________________

## Execution Order

Phase 1 and Phase 2 are sequential:

1. **Phase 1 — Audit**
   - Pass 1: Structure & Layout
   - Pass 2: Language & Tone
   - Pass 3: Cross-References & Linking
   - Pass 4: Redundancy & Ownership
   - Pass 5: MkDocs Compatibility
   - After each pass: fix issues, record findings as rules
2. **Phase 2 — Agent**
   - Write agent definition (`.claude/agents/spec-auditor.md`)
   - Write rules file with all Phase 1 findings
     (`.claude/agents/spec-auditor-rules.md`)
   - Run the agent in review mode against the (now fixed) specs to
     verify a clean baseline
   - Commit both files

______________________________________________________________________

## Design Decisions

1. **Dimension-centric, not document-centric.** Cross-document issues
   (redundancy, linking consistency) surface naturally when you examine
   one concern across all files rather than all concerns within one file.

2. **Rules in a separate file.** The agent prompt defines behavior; the
   rules file defines what to check. This lets rules grow independently
   as the project evolves without modifying the agent prompt.

3. **Two modes, same rules.** Review and fix mode apply identical checks.
   The only difference is whether the agent proposes changes. This
   ensures review mode is an accurate preview of what fix mode would do.

4. **Regression guard from day one.** Phase 1 findings become the
   baseline. This means the agent is useful immediately — it can catch
   regressions even before new rules are added.

5. **Cooperation over automation.** The agent flags and proposes; humans
   decide. Judgment calls (language, redundancy) are never auto-applied.
   This builds trust with the Report Assessment Team, who may not be
   comfortable with automated changes to documents they own.

6. **Enumerated instructions throughout.** Agent prompts use numbered
   steps, bulleted checklists, and explicit conditional logic rather than
   prose paragraphs. This produces more reliable agent behavior.
