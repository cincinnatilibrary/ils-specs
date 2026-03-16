---
id: location-codes
title: Location Codes
category: code-table
owner: ILS Team
reviewers:
  - Report Assessment Team
  - Cataloging and Processing
status: draft
version: 0.1.1
last_updated: 2026-03-16
---

# Location Codes

## Purpose

Location codes identify where an item is housed or assigned within the CHPL system.
They encode both the branch (e.g., Main, Avondale, Westwood) and the collection
within that branch (e.g., adult fiction, children's nonfiction, reference). Location
codes are fundamental to shelving, collection management, circulation routing, and
reporting.

## Scope & Audience

**Audience:** Cataloging staff assign location codes when creating item records.
Branch staff use them to identify where items belong. Reports use them to filter
and group data by branch and collection.

**In scope:** All location codes currently defined in Sierra for CHPL.

**Out of scope:** Location codes from other INN-Reach libraries or consortial
partners.

## Rules

The full code list needs to be exported from Sierra. The following are structural
categories identified from the `Sierra::Locations` module.

### C01 · Branch Locations

Location codes with recognized branch prefixes represent items at physical CHPL
branches. The branch is identified by a prefix in the location code.

**Technical implementation:** The `Sierra::Locations` module provides
`is_branch_prefix()` to test whether a location code prefix corresponds to a
known branch.

**Status:** proposed

______________________________________________________________________

### C02 · Offsite Locations

Location codes designated as offsite represent items stored at remote or
non-public-access facilities.

**Technical implementation:** Identified by `is_location_offsite()` in
`Sierra::Locations`.

**Status:** proposed

______________________________________________________________________

### C03 · Virtual Locations

Location codes designated as virtual represent items that do not have a physical
shelving location (e.g., digital resources, system-level placeholders).

**Technical implementation:** Identified by `is_location_virtual()` in
`Sierra::Locations`.

**Status:** proposed

______________________________________________________________________

### C04 · Administrative Locations

Location codes designated as administrative are used for internal system purposes
and do not represent patron-accessible collections.

**Technical implementation:** Identified by `is_location_administrative()` in
`Sierra::Locations`.

**Status:** proposed

______________________________________________________________________

### C05 · INN-Reach Locations

Location codes designated as INN-Reach represent items from partner libraries
in the INN-Reach consortial borrowing network.

**Technical implementation:** Identified by `is_location_innreach()` in
`Sierra::Locations`.

**Status:** proposed

## Sierra Configuration

Location codes are managed in Sierra admin under the location code table
(Admin > System Codes > Location). Each code has a name, branch association,
and various flags.

The `Sierra::Locations` module also maintains a `location_names_hash()` function
that maps codes to human-readable names.

## Open Questions

1. **Full code list:** The complete list of location codes and their descriptions
   needs to be exported from Sierra and documented here. This stub establishes
   the structural categories only.

2. **Main Library structure:** The Item Data Inconsistency Report has separate
   location/item-type mappings for Main Library. What is structurally different
   about Main Library's location codes?

3. **Code lifecycle:** Are there deprecated location codes still in Sierra that
   should be flagged? How are new codes added — is there a review process?

## Change Log

- 2026-03-13 · v0.1.0 · Initial stub with structural categories from Sierra::Locations (ILS Team)
- 2026-03-16 · v0.1.1 · Rename section heading per code-table guide convention (ILS Team)
