---
id: item-types
title: Item Types
category: code-table
owner: ILS Team
reviewers:
  - Report Assessment Team
  - Cataloging and Processing
status: draft
version: 0.1.0
last_updated: 2026-03-13
---

# Item Types

## Purpose

Item type codes (itypes) are numeric codes on item records that classify items for
circulation policy purposes. The item type determines checkout period, renewal
limits, fine rates, hold eligibility, and other loan rules. Item types also play a
key role in reporting — many reports filter or group by item type.

## Scope & Audience

**Audience:** Cataloging staff assign item types when creating item records.
Circulation staff encounter them when item behavior (loan period, fines) seems
unexpected. ILS Team manages the code table and associated loan rules.

**In scope:** All item type codes currently defined in Sierra for CHPL.

**Out of scope:** Item types from partner libraries in INN-Reach.

## Rules / Codes

The full code list needs to be exported from Sierra. The following codes are
specifically referenced in the Item Data Inconsistency Report's exclusion logic.

### C01 · Item Type 136

This item type is excluded from the Item Data Inconsistency Report's validation
checks. Its purpose and description need to be confirmed.

**Status:** proposed

______________________________________________________________________

### C02 · Item Type 145

This item type is excluded from the Item Data Inconsistency Report's validation
checks. Its purpose and description need to be confirmed.

**Status:** proposed

______________________________________________________________________

### C03 · Item Type 146

This item type is excluded from the Item Data Inconsistency Report's validation
checks. Its purpose and description need to be confirmed.

**Status:** proposed

______________________________________________________________________

### C04 · Item Type 163

This item type is excluded from the Item Data Inconsistency Report's validation
checks. Its purpose and description need to be confirmed.

**Status:** proposed

## Sierra Configuration

Item types are managed in Sierra admin under the item type code table
(Admin > System Codes > Item Type). Each code has a description and is associated
with loan rules through the loan rule matrix.

The `Sierra::Items` module provides `itype_names_hash()` to map numeric codes to
their human-readable descriptions. As of the last analysis, the module queries
Sierra directly for this mapping rather than maintaining a static list.

## Open Questions

1. **Full code list:** The complete list of item types and their descriptions
   needs to be exported from Sierra and documented here. The `itype_names_hash()`
   function in `Sierra::Items` can provide this.

2. **Excluded types (136, 145, 146, 163):** Why are these types excluded from
   the Item Data Inconsistency Report? Are they test types, system types, or
   special-purpose types that should not be validated?

3. **Item type / loan rule relationship:** Should this spec document the loan
   rule implications of each item type, or should that live in separate
   loan-rule specs?

4. **Non-floating item types:** The Item Data Inconsistency Report identifies
   item types 104 and 111 as non-floating. What does this mean for their
   circulation behavior, and are there other non-floating types?

## Change Log

- 2026-03-13 · v0.1.0 · Initial stub with types referenced by slitemdata report (ILS Team)
