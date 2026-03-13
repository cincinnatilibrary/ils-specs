---
id: item-types
title: Item Types
category: code-table
code_prefix: ITYPE
owner: ILS Team
reviewers:
  - Report Assessment Team
  - Cataloging and Processing
status: draft
version: 0.2.0
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

## Registry

### ITYPE-0 · Book

Standard circulating book for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-2 · Juvenile Book

Standard circulating book for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-3 · Audio Enabled Juvenile Book

Juvenile book with audio enhancement (e.g., Wonderbook).

**Status:** confirmed

______________________________________________________________________

### ITYPE-4 · Teen Book

Standard circulating book for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-5 · Audio Enabled Teen Book

Teen book with audio enhancement.

**Status:** confirmed

______________________________________________________________________

### ITYPE-6 · Leased Book

Book acquired through a leasing program (e.g., McNaughton). Typically returned to
the vendor after a set period rather than permanently added to the collection.

**Status:** confirmed

______________________________________________________________________

### ITYPE-10 · Reference Book

Non-circulating book held in a reference collection.

**Status:** confirmed

______________________________________________________________________

### ITYPE-11 · Reference Juvenile Book

Non-circulating juvenile book held in a reference collection.

**Status:** confirmed

______________________________________________________________________

### ITYPE-12 · Reference Teen Book

Non-circulating teen book held in a reference collection.

**Status:** confirmed

______________________________________________________________________

### ITYPE-15 · Braille

Circulating braille material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-16 · Reference Braille

Non-circulating braille material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-17 · Government Document

Circulating government document.

**Status:** confirmed

______________________________________________________________________

### ITYPE-18 · Reference Government Document

Non-circulating government document.

**Status:** confirmed

______________________________________________________________________

### ITYPE-20 · Large Print Book

Large print book for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-22 · Juvenile Large Print Book

Large print book for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-24 · Teen Large Print Book

Large print book for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-26 · Reference Large Print Book

Non-circulating large print book.

**Status:** confirmed

______________________________________________________________________

### ITYPE-27 · Reference Juv Large Print Book

Non-circulating juvenile large print book.

**Status:** confirmed

______________________________________________________________________

### ITYPE-30 · Magazine

Circulating magazine for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-31 · Juvenile Magazine

Circulating magazine for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-32 · Teen Magazine

Circulating magazine for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-33 · Reference Magazine

Non-circulating magazine.

**Status:** confirmed

______________________________________________________________________

### ITYPE-34 · Reference Juvenile Magazine

Non-circulating juvenile magazine.

**Status:** confirmed

______________________________________________________________________

### ITYPE-35 · Reference Teen Magazine

Non-circulating teen magazine.

**Status:** confirmed

______________________________________________________________________

### ITYPE-37 · Newspaper

Newspaper.

**Status:** confirmed

______________________________________________________________________

### ITYPE-46 · Rare Book

Rare or special collections book. Typically non-circulating with restricted access.

**Status:** confirmed

______________________________________________________________________

### ITYPE-60 · Book on Cassette

Audiobook on cassette tape for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-61 · Juvenile Book on Cassette

Audiobook on cassette tape for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-62 · Reference Book on Cassette

Non-circulating audiobook on cassette tape.

**Status:** confirmed

______________________________________________________________________

### ITYPE-65 · Music on Cassette

Music recording on cassette tape.

**Status:** confirmed

______________________________________________________________________

### ITYPE-66 · Juvenile Music on Cassette

Music recording on cassette tape for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-67 · Reference Music Cassette

Non-circulating music cassette.

**Status:** confirmed

______________________________________________________________________

### ITYPE-70 · Book on CD

Audiobook on compact disc for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-71 · Juvenile Book on CD

Audiobook on compact disc for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-72 · Teen Book on CD

Audiobook on compact disc for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-73 · Reference Book on CD

Non-circulating audiobook on compact disc.

**Status:** confirmed

______________________________________________________________________

### ITYPE-77 · Music on CD

Music recording on compact disc.

**Status:** confirmed

______________________________________________________________________

### ITYPE-78 · Juvenile Music on CD

Music recording on compact disc for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-79 · Reference Music on CD

Non-circulating music on compact disc.

**Status:** confirmed

______________________________________________________________________

### ITYPE-82 · LP Record

Vinyl LP record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-83 · Reference LP Record

Non-circulating vinyl LP record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-89 · Juvenile Preloaded Speaker

Preloaded audio speaker device for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-90 · Playaway

Playaway audiobook device for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-91 · Juvenile Playaway

Playaway audiobook device for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-92 · Teen Playaway

Playaway audiobook device for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-93 · Playaway View

Playaway View video device.

**Status:** confirmed

______________________________________________________________________

### ITYPE-94 · Reference Playaway View

Non-circulating Playaway View video device.

**Status:** confirmed

______________________________________________________________________

### ITYPE-100 · New Release DVDs

Recently released DVDs. May have different loan periods or hold rules than
standard DVDs.

**Status:** confirmed

______________________________________________________________________

### ITYPE-101 · DVD

Standard circulating DVD.

**Status:** confirmed

______________________________________________________________________

### ITYPE-102 · Bluray

Circulating Blu-ray disc.

**Status:** confirmed

______________________________________________________________________

### ITYPE-103 · Reference Video

Non-circulating video material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-104 · Video Kit

Video kit (DVD or Blu-ray with accompanying materials). This item type is
non-floating per the Item Data Inconsistency Report.

**Status:** confirmed

______________________________________________________________________

### ITYPE-105 · Leased DVD

DVD acquired through a leasing program.

**Status:** confirmed

______________________________________________________________________

### ITYPE-110 · MakerSpace Equipment

Equipment available through MakerSpace (e.g., 3D printers, sewing machines).

**Status:** confirmed

______________________________________________________________________

### ITYPE-111 · Portable Technology Device

Portable technology device for patron checkout (e.g., hotspots, Chromebooks).
This item type is non-floating per the Item Data Inconsistency Report.

**Status:** confirmed

______________________________________________________________________

### ITYPE-112 · Charging Kit

Device charging kit for patron use.

**Status:** confirmed

______________________________________________________________________

### ITYPE-113 · Laptop

Laptop computer for patron checkout.

**Status:** confirmed

______________________________________________________________________

### ITYPE-114 · Bike Locks

Bike lock available for patron checkout.

**Status:** confirmed

______________________________________________________________________

### ITYPE-115 · Telescope

Telescope available for patron checkout.

**Status:** confirmed

______________________________________________________________________

### ITYPE-116 · iPad

iPad tablet for patron checkout.

**Status:** confirmed

______________________________________________________________________

### ITYPE-120 · Downloadable Audiobook

Digital audiobook (e.g., OverDrive/Libby). Virtual item record — no physical
piece.

**Status:** confirmed

______________________________________________________________________

### ITYPE-121 · Downloadable Music

Digital music download. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-122 · Downloadable Video

Digital video download or streaming. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-123 · Downloadable Book

Digital ebook (e.g., OverDrive/Libby). Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-124 · E-Newspaper

Electronic newspaper access. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-125 · E-Magazine

Electronic magazine access. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-126 · Web Document

Online document accessible via URL. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-127 · Website

Website resource. Virtual item record.

**Status:** confirmed

______________________________________________________________________

### ITYPE-130 · 16mm Film

16mm film reel.

**Status:** confirmed

______________________________________________________________________

### ITYPE-131 · Architectural Drawing

Architectural drawing or blueprint.

**Status:** confirmed

______________________________________________________________________

### ITYPE-132 · Archival Material

Archival or special collections material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-134 · CD-ROM

Circulating CD-ROM.

**Status:** confirmed

______________________________________________________________________

### ITYPE-135 · Reference CD-ROM

Non-circulating CD-ROM.

**Status:** confirmed

______________________________________________________________________

### ITYPE-136 · Ephemeral

Ephemeral material (pamphlets, flyers, other transient items). Excluded from the
Item Data Inconsistency Report's validation checks.

**Status:** confirmed

______________________________________________________________________

### ITYPE-137 · Globe

Globe.

**Status:** confirmed

______________________________________________________________________

### ITYPE-138 · Unknown Graphic

Graphic material of unspecified type.

**Status:** confirmed

______________________________________________________________________

### ITYPE-139 · Reference Graphic

Non-circulating graphic material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-140 · InterLibrary Loan Item

Item received through interlibrary loan. Temporary item record with special
circulation rules.

**Status:** confirmed

______________________________________________________________________

### ITYPE-141 · Kit

Circulating kit (multiple components packaged together) for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-142 · Juvenile Kit

Circulating kit for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-143 · Teen Kit

Circulating kit for teen patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-144 · Map

Map.

**Status:** confirmed

______________________________________________________________________

### ITYPE-145 · Microfiche

Microfiche. Excluded from the Item Data Inconsistency Report's validation checks.

**Status:** confirmed

______________________________________________________________________

### ITYPE-146 · Microfilm

Microfilm. Excluded from the Item Data Inconsistency Report's validation checks.

**Status:** confirmed

______________________________________________________________________

### ITYPE-147 · Photograph

Photograph.

**Status:** confirmed

______________________________________________________________________

### ITYPE-148 · Picture

Circulating picture or art print.

**Status:** confirmed

______________________________________________________________________

### ITYPE-149 · Reference Picture

Non-circulating picture or art print.

**Status:** confirmed

______________________________________________________________________

### ITYPE-151 · Poster/Print

Circulating poster or print.

**Status:** confirmed

______________________________________________________________________

### ITYPE-152 · Reference Poster/Print

Non-circulating poster or print.

**Status:** confirmed

______________________________________________________________________

### ITYPE-154 · Reference Print

Non-circulating print material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-155 · Reference Realia

Non-circulating realia (three-dimensional object).

**Status:** confirmed

______________________________________________________________________

### ITYPE-157 · Music Score

Circulating music score for adult patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-158 · Music Score (Branches)

Circulating music score held at branch locations.

**Status:** confirmed

______________________________________________________________________

### ITYPE-159 · Juvenile Music Score

Circulating music score for juvenile patrons.

**Status:** confirmed

______________________________________________________________________

### ITYPE-160 · Juvenile Music Score (Branches)

Circulating juvenile music score held at branch locations.

**Status:** confirmed

______________________________________________________________________

### ITYPE-161 · Reference Music Score

Non-circulating music score.

**Status:** confirmed

______________________________________________________________________

### ITYPE-162 · Reference Juvenile Music Score

Non-circulating juvenile music score.

**Status:** confirmed

______________________________________________________________________

### ITYPE-163 · Slides

Slide collection. Excluded from the Item Data Inconsistency Report's validation
checks.

**Status:** confirmed

______________________________________________________________________

### ITYPE-165 · Order

On-order item. Placeholder record created at time of purchase before the physical
item arrives.

**Status:** confirmed

______________________________________________________________________

### ITYPE-199 · Cleanup

Item flagged for cleanup or review. Used as a marker for items needing
administrative attention.

**Status:** confirmed

______________________________________________________________________

### ITYPE-200 · OhioLINK Book

Book borrowed through OhioLINK consortium.

**Status:** confirmed

______________________________________________________________________

### ITYPE-201 · OhioLINK Curr Cent

OhioLINK curriculum center material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-202 · OhioLINK Periodical

OhioLINK periodical.

**Status:** confirmed

______________________________________________________________________

### ITYPE-203 · OhioLINK Sound Record

OhioLINK sound recording.

**Status:** confirmed

______________________________________________________________________

### ITYPE-204 · OhioLINK Comp. software

OhioLINK computer software.

**Status:** confirmed

______________________________________________________________________

### ITYPE-205 · OhioLINK Audio-Visual

OhioLINK audio-visual material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-206 · OhioLINK Microform

OhioLINK microform.

**Status:** confirmed

______________________________________________________________________

### ITYPE-207 · OhioLINK Non-Circ

OhioLINK non-circulating material.

**Status:** confirmed

______________________________________________________________________

### ITYPE-208 · OhioLINK Media

OhioLINK media.

**Status:** confirmed

______________________________________________________________________

### ITYPE-209 · OhioLINK Microforms

OhioLINK microforms.

**Status:** confirmed

______________________________________________________________________

### ITYPE-210 · OhioLINK Circulating Periodical

OhioLINK circulating periodical.

**Status:** confirmed

______________________________________________________________________

### ITYPE-212 · OhioLINK Circulating Periodical

OhioLINK circulating periodical (additional code).

**Status:** confirmed

______________________________________________________________________

### ITYPE-230 · Rapido Item

Item borrowed through Rapido interlibrary loan service.

**Status:** confirmed

______________________________________________________________________

### ITYPE-231 · Rapido Movie

Movie borrowed through Rapido interlibrary loan service.

**Status:** confirmed

______________________________________________________________________

### ITYPE-232 · Rapido Non-Requestable

Rapido item that is not requestable.

**Status:** confirmed

______________________________________________________________________

### ITYPE-233 · Rapido Test

Rapido test item type.

**Status:** confirmed

## Sierra Configuration

Item types are managed in Sierra admin under the item type code table
(Admin > System Codes > Item Type). Each code has a description and is associated
with loan rules through the loan rule matrix.

The `Sierra::Items` module provides `itype_names_hash()` to map numeric codes to
their human-readable descriptions. As of the last analysis, the module queries
Sierra directly for this mapping rather than maintaining a static list.

## Open Questions

1. **Item type / loan rule relationship:** Should this spec document the loan
   rule implications of each item type, or should that live in separate
   loan-rule specs?

2. **Non-floating item types:** The Item Data Inconsistency Report identifies
   item types 104 and 111 as non-floating. What does this mean for their
   circulation behavior, and are there other non-floating types?

## Change Log

- 2026-03-13 · v0.2.0 · Complete code registry from Sierra export; add code_prefix convention (ILS Team)
- 2026-03-13 · v0.1.0 · Initial stub with types referenced by slitemdata report (ILS Team)
