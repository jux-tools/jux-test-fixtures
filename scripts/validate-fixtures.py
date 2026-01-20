#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Georges Martin <jrjsmrtn@gmail.com>
"""
Validate JUnit XML fixtures against XSD schemas.

This script validates XML fixtures to ensure they conform to
JUnit XML schema specifications.

Usage:
    python validate-fixtures.py <fixtures_dir> [--schema <schema.xsd>]

Example:
    python validate-fixtures.py raw/
    python validate-fixtures.py raw/pytest/ --schema schemas/junit-10.xsd

Prerequisites:
    - lxml must be installed: pip install lxml
"""

import argparse
import sys
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("Error: lxml is required for validation")
    print("Install with: pip install lxml")
    sys.exit(1)


def validate_well_formed(xml_path: Path) -> tuple[bool, str | None]:
    """Check if XML is well-formed."""
    try:
        etree.parse(str(xml_path))
        return True, None
    except etree.XMLSyntaxError as e:
        return False, str(e)


def validate_against_schema(xml_path: Path, schema: etree.XMLSchema) -> tuple[bool, str | None]:
    """Validate XML against an XSD schema."""
    try:
        doc = etree.parse(str(xml_path))
        schema.assertValid(doc)
        return True, None
    except etree.DocumentInvalid as e:
        return False, str(e)
    except etree.XMLSyntaxError as e:
        return False, f"XML syntax error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Validate JUnit XML fixtures"
    )
    parser.add_argument(
        "fixtures_dir", type=Path, help="Directory containing fixtures to validate"
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="XSD schema file to validate against (optional)",
    )
    parser.add_argument(
        "--include-malformed",
        action="store_true",
        help="Include malformed fixtures in validation (expect failures)",
    )

    args = parser.parse_args()

    # Load schema if provided
    schema = None
    if args.schema:
        try:
            schema_doc = etree.parse(str(args.schema))
            schema = etree.XMLSchema(schema_doc)
            print(f"Loaded schema: {args.schema}")
        except Exception as e:
            print(f"Error loading schema: {e}")
            return 1

    # Collect files to validate
    xml_files = list(args.fixtures_dir.rglob("*.xml"))

    # Optionally exclude malformed directory
    if not args.include_malformed:
        xml_files = [f for f in xml_files if "malformed" not in str(f)]

    print(f"Found {len(xml_files)} XML files to validate\n")

    # Validate files
    valid_count = 0
    invalid_count = 0
    errors = []

    for xml_file in sorted(xml_files):
        # First check well-formedness
        is_well_formed, error = validate_well_formed(xml_file)

        if not is_well_formed:
            invalid_count += 1
            errors.append((xml_file, f"Not well-formed: {error}"))
            print(f"INVALID: {xml_file.relative_to(args.fixtures_dir)}")
            continue

        # Then validate against schema if provided
        if schema:
            is_valid, error = validate_against_schema(xml_file, schema)
            if not is_valid:
                invalid_count += 1
                errors.append((xml_file, f"Schema validation failed: {error}"))
                print(f"INVALID: {xml_file.relative_to(args.fixtures_dir)}")
                continue

        valid_count += 1
        print(f"VALID:   {xml_file.relative_to(args.fixtures_dir)}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Validation Results:")
    print(f"  Valid:   {valid_count}")
    print(f"  Invalid: {invalid_count}")
    print(f"  Total:   {len(xml_files)}")

    if errors:
        print(f"\nErrors:")
        for file_path, error in errors:
            print(f"  {file_path.relative_to(args.fixtures_dir)}:")
            print(f"    {error[:200]}...")

    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
