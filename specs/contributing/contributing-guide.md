---
title: Contributing Guide
---

# Contributing Guide

______________________________________________________________________

## Introduction

This repository is the source of truth for ILS business logic at
Cincinnati & Hamilton County Public Library (CHPL). Every specification
document here — report specs, code table definitions, loan rules, and
more — describes what the library's systems should do and why, in plain
English that both technical and non-technical staff can read and verify.

This guide is for **Report Assessment Team** and **ILS Team** members
who need to make changes to specifications. You will learn how to edit a
spec using the GitHub web interface, what fields to update when you make
a change, and how to submit your changes for review.

______________________________________________________________________

## Quick Start: Editing a Spec

You do not need to install any software. All editing happens in your web
browser.

1. Navigate to the spec on the published site at
   <https://cincinnatilibrary.github.io/ils-specs/>.
2. Click the **pencil icon** (edit icon) in the top right of the page —
   this opens the file in the GitHub editor.
3. Make your changes in the editor.
4. Update the required fields — `version`, `last_updated`, and the
   Change Log entry. (The next section explains exactly how.)
5. Scroll down to the **"Propose changes"** section.
6. Write a brief summary of what you changed and why.
7. Select **"Create a new branch for this commit and start a pull
   request"**.
8. Click **"Propose changes"**, then **"Create pull request"** on the
   next screen.

That's it. A maintainer will review your change and merge it if
everything looks good.

______________________________________________________________________

## What to Update When You Make a Change

Every change to a specification requires three updates. If you forget
one, the reviewer will catch it — but getting all three right up front
makes the process faster for everyone.

### 1. Bump the version

Specifications use semantic versioning — three numbers separated by
dots (MAJOR.MINOR.PATCH). Which number you increment depends on the
kind of change:

- **PATCH** (e.g., 0.2.0 to 0.2.1): typos, formatting fixes, wording
  improvements that do not change meaning.
- **MINOR** (e.g., 0.2.1 to 0.3.0): clarifications, new content, or
  status changes that do not alter business logic.
- **MAJOR** (e.g., 0.3.0 to 1.0.0): changes to business logic or
  rules — anything that would change how a report runs or how a code is
  interpreted.

When you bump MINOR, reset PATCH to 0. When you bump MAJOR, reset both
MINOR and PATCH to 0.

### 2. Update `last_updated`

Set `last_updated` in the front matter to today's date in YYYY-MM-DD
format (e.g., `2026-03-16`).

### 3. Add a changelog entry

Add a line to the **Change Log** section at the bottom of the document,
following this format:

```
- YYYY-MM-DD · vX.Y.Z · Description of the change (Team)
```

For example:

```
- 2026-03-16 · v0.3.0 · Confirm flag F01 status (Report Assessment Team)
```

See [Versioning Convention](../FRAMEWORK.md#versioning-convention) for
the full versioning rules.

______________________________________________________________________

## Common Tasks

These recipes walk through specific editing scenarios. Each one tells
you what to change, what version bump to use, and what the changelog
entry should look like.

### Fixing a typo or wording

**Scenario:** You noticed a misspelling, a grammatical error, or awkward
phrasing. The meaning of the text does not change.

- **What changes:** the text content only.
- **Version bump:** PATCH.
- **Front matter changes:** `version` (PATCH bump), `last_updated`.
- **Changelog entry example:** "Fix typo in Scope & Audience section"

### Updating a flag status

**Scenario:** The Report Assessment Team has reviewed a flag condition
and wants to change its status from `proposed` to `confirmed`.

- **What changes:** the `Status:` line on a flag condition.
- **Version bump:** MINOR — this is a meaningful change. The team is
  formally confirming that a rule is correct.
- **Front matter changes:** `version` (MINOR bump), `last_updated`.
- **Changelog entry example:** "Confirm flag F01 status"

### Adding a new flag condition

**Scenario:** You need to add a new condition to a report spec — a new
situation that the report should check for.

- **What changes:** a new `### FNN · Title` section added to Flag
  Conditions.
- **Version bump:** MINOR.
- **Front matter changes:** `version` (MINOR bump), `last_updated`.
- **Assign the next available number.** If the last flag is F04, the new
  one is F05. Flag IDs are permanent — they are never reused, even if
  an earlier flag is deprecated.
- **Set the initial status to `proposed`.** The Report Assessment Team
  will confirm it during review.
- **Changelog entry example:** "Add flag F05 for duplicate barcode
  detection"

See the [Report Specification Guide](../guides/report-guide.md) for the
full flag condition format and what each part should contain.

### Updating report metadata

**Scenario:** You need to change the report schedule, who receives the
output, or the scope description.

- **What changes:** front matter fields like `schedule` or
  `output_delivered_to`, or body sections like Scope & Audience.
- **Version bump:** MINOR for clarifications or small adjustments.
  MAJOR if the change alters who receives the report or fundamentally
  changes its scope.
- **Front matter changes:** `version` (appropriate bump), `last_updated`.
- **Changelog entry example:** "Update delivery schedule to biweekly" or
  "Add Technical Services to report recipients"

For more detail on specific spec types, see the category guides:

- [Report Specification Guide](../guides/report-guide.md)
- [Code Table Guide](../guides/code-table-guide.md)

______________________________________________________________________

## Pull Request Expectations

Here is what happens after you submit a pull request.

### 1. CI checks run automatically

Three checks run on every pull request:

- **Spec validation** — verifies that front matter fields are present
  and cross-references point to real files.
- **Formatting check** — confirms that the Markdown follows the
  project's consistent style.
- **Site build** — ensures the published site still builds correctly
  with your changes.

### 2. A maintainer reviews your PR

The reviewer checks that:

- The version was bumped appropriately.
- The `last_updated` date is set.
- A changelog entry was added.
- The change itself is correct.

### 3. Your PR is squash-merged

All your commits become one clean commit in the main branch. You do not
need to worry about keeping your commit history tidy.

### 4. Changes go live

After merge, the site rebuilds automatically. Your changes appear on the
published site within a few minutes.

### If CI fails

The pull request page will show which check failed. Common failures and
what to do:

- **"Missing required field"** — you may have accidentally deleted a
  front matter field. Check that all the fields between the `---`
  markers are still there.
- **"Markdown formatting check failed"** — the formatting is slightly
  off. The maintainer can usually fix this during review, so don't
  worry too much.
- **"Build failed"** — a link may be broken. Check that any links you
  added or changed are correct.

______________________________________________________________________

## Commit & PR Conventions

- **Write a clear, descriptive PR title.** Examples: "Fix typo in
  slitemdata F03 description" or "Confirm F01 status in slitemdata."
- **Fill in the PR template.** The template will remind you of the
  checklist items (version bump, last_updated, changelog) — just check
  them off.
- **Don't worry about commit message format.** Pull requests are
  squash-merged, so the maintainer writes the final commit message.

______________________________________________________________________

## Getting Help

- **Questions about spec content** — what a report should check, what a
  code means, whether a flag condition is correct: contact the
  **ILS Team**.
- **Questions about this workflow** — how to edit a file, what went
  wrong with a pull request, how to fix a CI failure: contact the
  **ILS Team**.
- **Reference documents:**
  - [Framework](../FRAMEWORK.md) — versioning rules, front matter
    schema, style guide
  - [Report Specification Guide](../guides/report-guide.md) — how
    report specs are structured
  - [Code Table Guide](../guides/code-table-guide.md) — how code table
    specs are structured
