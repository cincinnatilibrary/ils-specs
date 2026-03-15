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

- S01: Report specs must have sections in this order:
  1. Purpose
  2. Scope & Audience
  3. Data Sources
  4. Flag Conditions
  5. Output & Delivery
  6. Exclusions & Edge Cases
  7. Open Questions
  8. Known Limitations
  9. Change Log
- S02: Code table specs must have sections in this order:
  1. Purpose
  2. Scope & Audience
  3. Registry
  4. Sierra Configuration
  5. Open Questions
  6. Change Log
- S03: All specs start with an `# {title}` heading that matches the
  front matter `title` field exactly.
- S04: Horizontal rules are used consistently as section separators.
  - Current state: FRAMEWORK.md, guides, and glossary use them;
    specs vary. Audit will determine one convention.
- S05: Flag condition headings follow `### F{nn} · {Name}` pattern.
- S06: Registry entry headings follow `### {PREFIX}-{code} · {Label}`.
- S07: Every spec ends with a Change Log section as the last section.

### Dimension 2: Language & Tone

Check for consistent phrasing conventions, present tense, plain English
per the style guide, and non-repetitive language in parallel sections.

**Rules:**

- L01: Present tense throughout.
  - Correct: "An item is flagged when..."
  - Incorrect: "An item will be flagged when..."
- L02: Purpose sections across specs use similar structure:
  1. What it does (1-2 sentences)
  2. Why it matters (1-2 sentences)
  3. Optional additional context (1 paragraph max)
- L03: Scope & Audience sections use consistent three-part structure:
  - `**Audience:**` — who uses this
  - `**In scope:**` — what is covered
  - `**Out of scope:**` — what is excluded
- L04: Plain English in rule/condition statements.
  - Use "item type" not "itype"
  - Use "location code" not "location_code"
  - Technical names belong only in Technical Implementation notes
- L05: Status labels use consistent formatting: `**Status:** {value}`
  (bold label, colon inside bold, space, lowercase value).
- L06: Change Log entries follow the format:
  `- {YYYY-MM-DD} · v{version} · {description} ({team})`
- L07: Avoid opening Purpose sections with the document title restated
  verbatim.
  - Correct: "Item type codes classify items for circulation policy..."
  - Avoid: "The Item Types code table documents item type codes..."

### Dimension 3: Cross-References & Linking

Check that every link resolves, link style is consistent, and things
that should be linked are linked.

**Rules:**

- X01: All inter-spec references use relative markdown links.
  - From `specs/` root: `./glossary.md`, `./FRAMEWORK.md`
  - From category subfolders: `../glossary.md`, `../FRAMEWORK.md`
  - Never absolute paths or bare filenames
- X02: Front matter `depends_on` and `related_specs` entries each have
  at least one corresponding body-prose link in the document.
- X03: Glossary terms are linked on first use per major section (not
  every occurrence, but at least once where the term first appears in
  each `##`-level section).
- X04: Registry entries referenced from other specs use anchor links:
  `item-types.md#itype-70--book-on-cd`
- X05: Guide files link back to FRAMEWORK.md for shared conventions
  rather than restating them.
- X06: No orphan references — if FRAMEWORK.md mentions a guide, that
  guide exists (even as a stub).
- X07: No dead links — every `[text](path)` and `[text](path#anchor)`
  resolves to an existing file and (where applicable) a valid heading
  anchor.

### Dimension 4: Redundancy & Ownership

Check that content lives in one canonical place with links from
elsewhere, not restated in multiple locations.

**Rules:**

- R01: Front matter field documentation lives in FRAMEWORK.md only.
  - Guides reference it with a link, do not redefine fields.
- R02: Section structure and ordering lives in category guides only.
  - FRAMEWORK.md references the guides via the Category Guides table.
- R03: The source-of-truth principle is stated once prominently in
  FRAMEWORK.md's overview.
  - Other documents (guides, specs/README.md, root README.md) may
    reference it but should not restate it in different words.
- R04: Cross-referencing conventions live in FRAMEWORK.md.
  - Guides show examples but link to the framework for full rules.
- R05: Glossary term definitions live in glossary.md only.
  - Specs link to glossary terms, do not re-explain inline.
- R06: The "what specs exist" listing lives in specs/README.md only.
  - Root README.md links to it rather than duplicating the table.

### Dimension 5: MkDocs Compatibility

Check that everything works when published through MkDocs Material to
GitHub Pages.

**Rules:**

- M01: Every spec and guide file appears in `mkdocs.yml` nav.
- M02: Anchor links use MkDocs-compatible slug format:
  - Lowercase
  - Spaces become hyphens
  - Special characters (including `·`) become hyphens
  - Consecutive hyphens collapse
- M03: The `docs_dir: specs` setting means all nav paths and links are
  relative to `specs/` — verify paths work from that root.
- M04: Guide files have a front matter `title` field for MkDocs page
  titles.
- M05: No links use GitHub-specific features that fail in MkDocs:
  - Directory links with trailing `/`
  - Links to non-markdown files without explicit handling
- M06: Nav structure in mkdocs.yml reflects the actual category
  organization and includes all published documents.

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
