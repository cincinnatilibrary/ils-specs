#!/usr/bin/env python3
"""Validate front matter and cross-references for all spec files.

Checks:
  - schema.yaml and FRAMEWORK.md version alignment
  - Required fields present (per schema.yaml)
  - Valid category and status values (per schema.yaml)
  - Version looks like semver
  - depends_on and related_specs paths resolve to existing files

Usage:
  python3 scripts/validate-specs.py

Follows Ray's script conventions: progress to stderr, results to stdout.
"""

import os
import re
import sys
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS_DIR = os.path.join(REPO_ROOT, "specs")
SCHEMA_PATH = os.path.join(SPECS_DIR, "schema.yaml")
FRAMEWORK_PATH = os.path.join(SPECS_DIR, "FRAMEWORK.md")

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Files in specs/ that are not spec documents
SKIP_FILES = {"README.md", "FRAMEWORK.md", "glossary.md", "schema.yaml"}


def load_schema():
    """Load the machine-readable schema from schema.yaml."""
    with open(SCHEMA_PATH) as f:
        return yaml.safe_load(f)


def get_framework_version():
    """Extract the version string from FRAMEWORK.md's header."""
    with open(FRAMEWORK_PATH) as f:
        for line in f:
            if line.startswith("**Version:**"):
                # Extract version from "**Version:** 1.0.0"
                match = re.search(r"\d+\.\d+\.\d+", line)
                if match:
                    return match.group(0)
    return None


def check_version_alignment(schema):
    """Check that schema.yaml framework_version matches FRAMEWORK.md."""
    schema_version = schema.get("framework_version")
    framework_version = get_framework_version()

    if schema_version and framework_version:
        if schema_version != framework_version:
            return (
                "WARN",
                f"schema.yaml framework_version ({schema_version}) does not match "
                f"FRAMEWORK.md version ({framework_version}) — update one or both",
            )
    elif not framework_version:
        return ("WARN", "Could not extract version from FRAMEWORK.md header")

    return None


def find_spec_files():
    """Find all .md files in specs/ subdirectories (category folders)."""
    specs = []
    for root, dirs, files in os.walk(SPECS_DIR):
        # Skip the specs/ root directory files
        if root == SPECS_DIR:
            continue
        for f in sorted(files):
            if f.endswith(".md") and f not in SKIP_FILES and f != ".gitkeep":
                specs.append(os.path.join(root, f))
    return specs


def parse_front_matter(filepath):
    """Extract and parse YAML front matter from a markdown file."""
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---")
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return {"_parse_error": str(e)}


def validate_spec(filepath, fm, schema):
    """Validate a single spec file. Returns list of (level, message) tuples."""
    issues = []

    valid_categories = set(schema.get("categories", []))
    valid_statuses = set(schema.get("statuses", []))
    required_all = schema.get("required_fields", {}).get("all", [])
    required_by_category = {
        k: v for k, v in schema.get("required_fields", {}).items() if k != "all"
    }

    if fm is None:
        issues.append(("ERROR", "No YAML front matter found"))
        return issues

    if "_parse_error" in fm:
        issues.append(("ERROR", f"YAML parse error: {fm['_parse_error']}"))
        return issues

    # Required fields (all categories)
    for field in required_all:
        if field not in fm:
            issues.append(("ERROR", f"Missing required field: {field}"))

    # Valid category
    if "category" in fm and fm["category"] not in valid_categories:
        issues.append(
            ("ERROR", f"Invalid category: {fm['category']} (expected one of {sorted(valid_categories)})")
        )

    # Valid status
    if "status" in fm and fm["status"] not in valid_statuses:
        issues.append(
            ("ERROR", f"Invalid status: {fm['status']} (expected one of {sorted(valid_statuses)})")
        )

    # Semver
    if "version" in fm:
        version = str(fm["version"])
        if not SEMVER_RE.match(version):
            issues.append(("WARN", f"Version '{version}' does not look like semver (MAJOR.MINOR.PATCH)"))

    # Category-specific required fields
    category = fm.get("category")
    if category and category in required_by_category:
        for field in required_by_category[category]:
            if field not in fm:
                issues.append(("WARN", f"Field '{field}' is required for {category} specs"))

    # Cross-reference resolution
    for field in ("depends_on", "related_specs"):
        refs = fm.get(field, []) or []
        for ref in refs:
            ref_path = os.path.join(SPECS_DIR, ref + ".md")
            if not os.path.exists(ref_path):
                issues.append(("WARN", f"{field} '{ref}' does not resolve to an existing file"))

    return issues


def main():
    # Load schema
    if not os.path.exists(SCHEMA_PATH):
        print(f"ERROR: schema.yaml not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)

    schema = load_schema()
    print(f"Loaded schema (framework_version: {schema.get('framework_version', '?')})", file=sys.stderr)

    # Check version alignment
    version_issue = check_version_alignment(schema)
    if version_issue:
        print(f"  {version_issue[0]}: {version_issue[1]}")
    else:
        print("  PASS  schema.yaml / FRAMEWORK.md version alignment")

    # Find and validate specs
    specs = find_spec_files()

    if not specs:
        print("No spec files found in specs/ subdirectories.", file=sys.stderr)
        sys.exit(0)

    print(f"Validating {len(specs)} spec file(s)...", file=sys.stderr)

    total_errors = 0
    total_warns = 0

    for filepath in specs:
        relpath = os.path.relpath(filepath, REPO_ROOT)
        fm = parse_front_matter(filepath)
        issues = validate_spec(filepath, fm, schema)

        errors = [i for i in issues if i[0] == "ERROR"]
        warns = [i for i in issues if i[0] == "WARN"]
        total_errors += len(errors)
        total_warns += len(warns)

        if not issues:
            print(f"  PASS  {relpath}")
        else:
            status = "FAIL" if errors else "WARN"
            print(f"  {status}  {relpath}")
            for level, msg in issues:
                print(f"        {level}: {msg}")

    print()
    print(f"Results: {len(specs)} files, {total_errors} errors, {total_warns} warnings")

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
