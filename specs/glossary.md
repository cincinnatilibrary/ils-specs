# Glossary

Terms used across ILS specifications at CHPL. When a term has a specific meaning
in this context that differs from casual usage, it is defined here.

## How to Link to This Glossary

From spec files in category subfolders (e.g., `specs/reports/`):

```markdown
A [hold-filled](../glossary.md#hold-filled) transaction is recorded when...
```

From files in the `specs/` root (e.g., `FRAMEWORK.md`):

```markdown
See the definition of [item type](./glossary.md#item-type) for details.
```

## Contextual Definitions

Most terms have a single definition. When a term has genuinely different meanings
in different contexts, context subsections appear under the term heading (see
`FRAMEWORK.md` for the convention). This is optional and used only when the
ambiguity would cause real confusion.

______________________________________________________________________

## barcode

The scannable identifier affixed to a physical item in the library's collection.
Each item should have a unique barcode. The barcode is the primary way staff and
self-checkout machines identify an item during circulation transactions.

**Not to be confused with:** The item record number, which is Sierra's internal
identifier for the item record. Barcodes are physical; record numbers are system
identifiers.

**Sierra context:** Stored as a varfield on the item record (varfield type code
`b`, record type code `i`).

______________________________________________________________________

## bib record

A bibliographic record describing a single title (book, DVD, audiobook, etc.) in
the library catalog. A bib record contains metadata like title, author, subject
headings, and publication information. One bib record can have many items attached
to it (e.g., multiple copies at different branches).

**Not to be confused with:** An item record, which represents a specific physical
copy. The bib record describes *what* something is; the item record describes
*where a particular copy is* and its current status.

**Sierra context:** Records in `sierra_view.bib_view` and
`sierra_view.bib_record_property`. Linked to item records through
`sierra_view.bib_record_item_record_link`.

______________________________________________________________________

## bcode2

The bibliographic material type code. A single-character code on the bib record
that indicates the format of the material (e.g., book, DVD, audiobook, large print).

**Not to be confused with:** Item type (itype), which is a numeric code on the
*item* record used for loan rules. A bib record has one bcode2; each attached item
has its own itype. These should be consistent but mismatches occur and are flagged
by reports like the Item Data Inconsistency Report.

**Sierra context:** Field `bcode2` on `sierra_view.bib_view`.

______________________________________________________________________

## call number

The classification number (typically Dewey Decimal or a local scheme) that
determines an item's position on the shelf. Used by staff and patrons to locate
physical items in the library.

**Sierra context:** Stored as a varfield on the bib record (varfield type code
`c`, record type code `b`).

______________________________________________________________________

## item

A specific physical piece in the library's collection — one copy of a book, one
DVD disc, one audiobook set. Each item has its own barcode, location, status, and
circulation history. Multiple items can be attached to a single bib record (e.g.,
five copies of the same novel at different branches).

**Not to be confused with:** A bib record, which describes the title. "Item"
always means a specific physical copy.

**Sierra context:** Records in `sierra_view.item_view`. Each item has an
`itype_code_num`, `location_code`, `item_status_code`, and other fields.

______________________________________________________________________

## item type

A numeric code on the item record that classifies the item for loan rule purposes.
The item type determines checkout period, renewal limits, fine rates, and other
circulation policies. For example, different item types distinguish DVDs from books,
new materials from regular collection, and reference items from circulating items.

Also referred to as "itype" in technical contexts.

**Not to be confused with:** bcode2 (the bibliographic material type), which is on
the bib record and describes format. Item type is on the *item* record and drives
*circulation policy*.

**Sierra context:** Field `itype_code_num` on `sierra_view.item_view`. Managed in
Sierra admin under the item type code table.

______________________________________________________________________

## location code

A short string code indicating where an item is housed or assigned within the
library system. Location codes encode both the branch (e.g., Main, Avondale,
Westwood) and the collection within that branch (e.g., adult fiction, children's
nonfiction, reference).

**Not to be confused with:** A branch name, which is the human-readable name of a
library building. A location code is more granular — one branch has many location
codes for its different collections and shelving areas.

**Sierra context:** Field `location_code` on `sierra_view.item_view`. Managed in
Sierra admin under the location code table. The `Sierra::Locations` module provides
helper functions for classifying location codes (branch prefix, offsite, virtual,
administrative).

______________________________________________________________________

## suppressed

A flag on a record (bib or item) indicating it should be hidden from public-facing
displays — the online catalog, discovery layer, and patron-facing search results.
Suppressed records still exist in Sierra and can be found by staff, but patrons
cannot see or place holds on them.

Suppression is used for records that are in process, being cataloged, withdrawn but
not yet deleted, or otherwise not ready for public access.

**Sierra context:** Boolean field `is_suppressed` on `sierra_view.item_view` and
`sierra_view.bib_view`.
