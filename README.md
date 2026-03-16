# CHPL ILS Specifications

Specification documents for ILS (Integrated Library System) business logic at
Cincinnati & Hamilton County Public Library.

## Overview

**Specifications are the source of truth.** These documents define what the
system *should* do. The ILS configuration and report implementations reflect
these specs, not the other way around.

## What's Here

This repository contains structured specifications for:

- **Reports** — automated reports generated from Sierra data
- **Code Tables** — Sierra code sets (location codes, item types, patron types, etc.)
- **Loan Rules** — lending policies and loan rule configurations
- **Workflows** — operational processes that involve Sierra
- **Policies** — library policies with ILS implications

All specs live in the `specs/` directory, organized by category.

## Getting Started

- **Browse online:** [cincinnatilibrary.github.io/ils-specs](https://cincinnatilibrary.github.io/ils-specs/)
- **Reading specs:** Start with [specs/README.md](specs/README.md) for a
  navigable index of all specifications.
- **Writing specs:** Read [specs/FRAMEWORK.md](specs/FRAMEWORK.md) for the
  format, front matter schema, and style guide.
- **Glossary:** See [specs/glossary.md](specs/glossary.md) for definitions of
  terms that have specific meanings in this context.

## Who Maintains This

- **Spec content** is owned by the teams listed in each spec's `owner` field
  (typically ILS Team, Report Assessment Team, or department-specific teams).
- **Framework and tooling** is maintained by the ILS Team.

## Contributing

All changes to specifications go through version control. When modifying a spec:

1. Update the `version` field (see FRAMEWORK.md for semver conventions)
2. Add a change log entry
3. Update `last_updated` to today's date
