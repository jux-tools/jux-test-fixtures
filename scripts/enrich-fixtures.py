#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Georges Martin <jrjsmrtn@gmail.com>
"""
Enrich raw JUnit XML fixtures with py-juxlib environment metadata.

This script adds jux.* properties to testsuite/testsuites elements,
simulating what py-juxlib would add during test execution.

Usage:
    python enrich-fixtures.py <raw_dir> <enriched_dir> [--metadata-file <file>]

Example:
    python enrich-fixtures.py raw/ enriched/
    python enrich-fixtures.py raw/pytest/ enriched/pytest/ --metadata-file sample-metadata.json
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

# Default sample metadata for enrichment
DEFAULT_METADATA = {
    "jux.hostname": "build-server-01",
    "jux.username": "ci-user",
    "jux.platform": "Linux-6.1.0-x86_64",
    "jux.python_version": "3.12.1",
    "jux.timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "jux.project_name": "sample-project",
    "jux.git_commit": "abc123def456789012345678901234567890abcd",
    "jux.git_branch": "main",
    "jux.git_status": "clean",
    "jux.git_remote": "https://github.com/example/sample-project.git",
    "jux.ci_provider": "github",
    "jux.ci_build_id": "12345",
    "jux.ci_build_url": "https://github.com/example/sample-project/actions/runs/12345",
}


def add_metadata_properties(root: ET.Element, metadata: dict) -> None:
    """Add metadata as properties to the root element."""
    # Find or create properties element
    properties = root.find("properties")
    if properties is None:
        properties = ET.Element("properties")
        # Insert at the beginning
        root.insert(0, properties)

    # Add metadata properties
    for name, value in metadata.items():
        prop = ET.SubElement(properties, "property")
        prop.set("name", name)
        prop.set("value", str(value))


def enrich_file(input_path: Path, output_path: Path, metadata: dict) -> bool:
    """Enrich a single JUnit XML file with metadata."""
    try:
        tree = ET.parse(input_path)
        root = tree.getroot()

        # Handle both testsuite and testsuites root elements
        if root.tag == "testsuites":
            add_metadata_properties(root, metadata)
        elif root.tag == "testsuite":
            add_metadata_properties(root, metadata)
        else:
            print(f"Warning: Unknown root element '{root.tag}' in {input_path}")
            return False

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write with XML declaration
        tree.write(
            output_path,
            encoding="UTF-8",
            xml_declaration=True,
        )

        print(f"Enriched: {input_path} -> {output_path}")
        return True

    except ET.ParseError as e:
        print(f"Error parsing {input_path}: {e}")
        return False
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Enrich raw JUnit XML fixtures with py-juxlib metadata"
    )
    parser.add_argument("raw_dir", type=Path, help="Directory containing raw fixtures")
    parser.add_argument(
        "enriched_dir", type=Path, help="Output directory for enriched fixtures"
    )
    parser.add_argument(
        "--metadata-file",
        type=Path,
        help="JSON file with custom metadata values",
    )

    args = parser.parse_args()

    # Load metadata
    metadata = DEFAULT_METADATA.copy()
    if args.metadata_file:
        with open(args.metadata_file) as f:
            custom_metadata = json.load(f)
            metadata.update(custom_metadata)

    # Process all XML files
    success_count = 0
    error_count = 0

    for xml_file in args.raw_dir.rglob("*.xml"):
        relative_path = xml_file.relative_to(args.raw_dir)
        output_path = args.enriched_dir / relative_path

        if enrich_file(xml_file, output_path, metadata):
            success_count += 1
        else:
            error_count += 1

    print(f"\nProcessed {success_count + error_count} files:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
