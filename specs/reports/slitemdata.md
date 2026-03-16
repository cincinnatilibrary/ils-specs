---
id: slitemdata
title: Item Data Inconsistency Report
category: report
owner: ILS Team
reviewers:
  - Report Assessment Team
status: draft
version: 0.2.1
last_updated: 2026-03-16
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

# Item Data Inconsistency Report

## Purpose

This report identifies items in the catalog whose data is internally inconsistent
— where the item type, location code, bibliographic material type, or audience
designation do not match the expected combinations. These mismatches typically
indicate cataloging errors, items that were moved without corresponding metadata
updates, or changes to code tables that were not propagated to existing items.

Left uncorrected, inconsistent item data causes items to circulate under wrong
loan rules, appear in incorrect locations on the public catalog, or be missed by
collection management reports that filter by item type or location.

This is one of the highest-priority shelf-list reports, running monthly.

## Scope & Audience

**Audience:** Branch managers and Cataloging and Processing staff receive this
report. Branch managers use it to identify items on their shelves that need
correction. Cataloging staff use it to identify systemic patterns (e.g., a batch
of items loaded with the wrong item type).

**In scope:** All non-suppressed items in the catalog that are not excluded by
the filters described in Exclusions & Edge Cases below.

**Out of scope:** Suppressed items, items with certain item types reserved for
special purposes (see exclusions), and items with statuses indicating they are
not in active circulation.

## Data Sources

The report queries the Sierra ILS PostgreSQL database, joining across several
views:

| Table / View                              | Purpose                                                  |
| ----------------------------------------- | -------------------------------------------------------- |
| `sierra_view.item_view`                   | Item records: item type, location, status, last checkout |
| `sierra_view.bib_view`                    | Bib records: material type (bcode2), suppression status  |
| `sierra_view.bib_record_property`         | Title and author for display                             |
| `sierra_view.bib_record_item_record_link` | Links items to their bib records                         |
| `sierra_view.varfield_view`               | Barcode (item varfield) and call number (bib varfield)   |

The report also uses internal mapping tables (hardcoded in the script) that define
which combinations of item type, location, bcode2, and audience are considered
valid. These mapping tables are the core business logic of the report and are
described in the flag rules below.

## Flag Conditions

Each flag condition causes an item to appear in the report output. An item may be
flagged for multiple reasons. Flag conditions reference
[item types](../code-tables/item-types.md) and
[location codes](../code-tables/location-codes.md) defined in the code table
specifications.

### F01 · Material Type / Item Type Mismatch

An item is flagged when its bibliographic material type code is not consistent with
its item type. For example, an item typed as a DVD should not be attached to a bib
record with a material type indicating it is a book.

This rule catches items where the bib record format and the item-level
classification disagree, which can cause incorrect shelving, wrong loan periods,
and misleading catalog displays.

**Technical implementation:** The script maintains a mapping (`%itypes_for_bcode2`)
with 27 bcode2 values, each mapped to a set of permitted item type codes. An item
is flagged when its `itype_code_num` is not in the permitted set for its bib's
`bcode2` value.

**Status:** proposed

______________________________________________________________________

### F02 · Location / Item Type Mismatch

An item is flagged when its location code is not permitted for its item type. For
example, an item type designated for the children's collection should not appear in
an adult collection location.

This rule catches items that were shelved or assigned to the wrong area, which
affects both patron discovery and collection management workflows.

**Technical implementation:** The script maintains two mappings:

- `%locns_for_itype` (65-68 item types mapped to permitted location suffixes) for
  branch locations
- `%main_locns_for_itype` (71-72 item types mapped to permitted locations) for
  Main Library specifically, which has a different location code structure

An item is flagged when its `location_code` is not in the permitted set for its
`itype_code_num`. Main Library items are checked against the Main-specific mapping.

**Status:** proposed

______________________________________________________________________

### F03 · Audience / Item Type Mismatch

An item is flagged when its audience designation does not match its item type. The
audience codes are: adult (`a`), teen (`t`), and juvenile (`j`). For example, a
juvenile item type should not have an adult audience code.

This rule ensures that items are correctly classified by age group, which affects
display in the catalog, placement in age-appropriate collections, and filtering in
patron-facing search results.

**Technical implementation:** The script maintains a mapping
(`%itypes_for_audience`) with 3 audience keys, each mapped to a set of permitted
item type codes.

**Edge cases:** Some item types may be valid for multiple audience designations
(e.g., certain media formats used across age groups).

**Status:** proposed

______________________________________________________________________

### F04 · Non-Floating Item in Wrong Branch

An item is flagged when it has a non-floating item type but is located at a branch
that does not match its expected home branch. Floating items are allowed to reside
at any branch, but non-floating items should return to their home branch after
circulation.

**Technical implementation:** The script maintains a mapping
(`%branch_prefixes_for_nonfloating_itypes`) that maps specific non-floating item
types (e.g., 104, 111) to the branch prefixes where they belong.

**Status:** proposed

## Output & Delivery

The report produces output per branch, containing the following fields for each
flagged item:

| Field                  | Description                        |
| ---------------------- | ---------------------------------- |
| Item record number     | Sierra item record identifier      |
| Item type code         | Numeric item type                  |
| Location code          | Current location assignment        |
| Last checkout date     | When the item was last checked out |
| Material type (bcode2) | Bibliographic format code          |
| Bib record number      | Sierra bib record identifier       |
| Title                  | Best title from bib record         |
| Author                 | Best author from bib record        |
| Barcode                | Item barcode                       |
| Call number            | Bib call number                    |

Output is delivered as XML files, one per branch, transferred to a web server for
staff access.

## Exclusions & Edge Cases

The following items are excluded from the report before flag rules are applied:

| Exclusion                                         | Reason                                                            |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| Suppressed items (`is_suppressed = TRUE`)         | Not in active collection                                          |
| Bib suppress code `s` (`bcode3 = 's'`)            | Bib-level suppression                                             |
| Material type unset (`bcode2 = '-'`)              | No material type to validate against                              |
| Item message code `f` (`item_message_code = 'f'`) | Meaning to be confirmed                                           |
| Item types 136, 145, 146, 163                     | Reserved types excluded from validation (meaning to be confirmed) |
| Item statuses `p` and `u`                         | Meaning to be confirmed                                           |

The report processes items in chunks (by Sierra internal ID ranges) to manage
memory and database load on the Sierra server.

## Open Questions

These need to be resolved with the Report Assessment Team and ILS Team:

1. **Excluded item types (136, 145, 146, 163):** What do these item types
   represent? Why are they excluded? This should be documented in the
   [item types](../code-tables/item-types.md) code table spec.

2. **Excluded item statuses (`p`, `u`):** What do these status codes mean in
   CHPL's Sierra configuration? Are there other statuses that should be excluded?

3. **Item message code `f`:** What does this code mean and why are items with it
   excluded?

4. **Mapping table maintenance:** The valid combination mappings (bcode2/itype,
   location/itype, audience/itype) are currently hardcoded in the Perl script.
   Should these be maintained externally (e.g., in a configuration file or as
   part of this spec)?

5. **Main Library special handling:** The report has separate location mappings
   for Main Library. Is this still necessary? Are there other branches that need
   special handling?

6. **Output format:** The current output is XML delivered via FTP. As the platform
   migrates to Datasette/SQLite, what should the output format become?

7. **TODOs in existing code:** The Perl script contains multiple TODO comments
   questioning whether certain exclusions are correct and whether mapping tables
   should be externalized. These suggest the original developer had similar
   questions about the business logic.

## Known Limitations

- The valid combination mappings are maintained in the script source code, not in
  an external configuration. Changes to what constitutes a "valid" combination
  require a code change. This is a known maintenance burden and a candidate for
  improvement in the platform migration.

- The report runs on a monthly schedule. Items that become inconsistent mid-month
  are not flagged until the next run.

- The report cannot detect *why* an inconsistency exists — only that one does.
  Staff must investigate each flagged item to determine the correct resolution.

## Change Log

- 2026-03-13 · v0.1.0 · Initial draft, distilled from Perl script analysis (ILS Team)
- 2026-03-13 · v0.2.0 · Rename "Rules / Conditions" to "Flag Conditions" per framework 2.0 (ILS Team)
- 2026-03-16 · v0.2.1 · Add code table cross-reference links in Flag Conditions intro (ILS Team)
