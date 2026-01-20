#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 Georges Martin <jrjsmrtn@gmail.com>
"""
Sign JUnit XML fixtures with XMLDSig enveloped signatures.

This script uses py-juxlib's signing module to add digital signatures
to enriched JUnit XML fixtures for tamper-proof verification testing.

Usage:
    python sign-fixtures.py <enriched_dir> <signed_dir> --key <private_key.pem>

Example:
    python sign-fixtures.py enriched/ signed/ --key test-key.pem
    python sign-fixtures.py enriched/pytest/ signed/pytest/ --key ~/.ssh/jux/dev-key.pem

Prerequisites:
    - py-juxlib must be installed: pip install py-juxlib
    - A private key file (RSA or ECDSA) in PEM format

Generating a test key:
    openssl genrsa -out test-key.pem 2048
    # or for ECDSA:
    openssl ecparam -name prime256v1 -genkey -noout -out test-key.pem
"""

import argparse
import sys
from pathlib import Path

try:
    from lxml import etree

    from juxlib.signing import load_private_key, sign_xml
except ImportError as e:
    print(f"Error: Required dependency not found: {e}")
    print("\nPlease install py-juxlib:")
    print("  pip install py-juxlib")
    print("  # or")
    print("  uv pip install py-juxlib")
    sys.exit(1)


def sign_file(input_path: Path, output_path: Path, private_key) -> bool:
    """Sign a single JUnit XML file."""
    try:
        # Parse XML
        tree = etree.parse(str(input_path))
        root = tree.getroot()

        # Sign the XML
        signed_root = sign_xml(root, private_key)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write signed XML
        signed_tree = etree.ElementTree(signed_root)
        signed_tree.write(
            str(output_path),
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
        )

        print(f"Signed: {input_path} -> {output_path}")
        return True

    except etree.XMLSyntaxError as e:
        print(f"Error parsing {input_path}: {e}")
        return False
    except Exception as e:
        print(f"Error signing {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sign JUnit XML fixtures with XMLDSig signatures"
    )
    parser.add_argument(
        "enriched_dir", type=Path, help="Directory containing enriched fixtures"
    )
    parser.add_argument(
        "signed_dir", type=Path, help="Output directory for signed fixtures"
    )
    parser.add_argument(
        "--key",
        type=Path,
        required=True,
        help="Path to private key file (PEM format)",
    )
    parser.add_argument(
        "--cert",
        type=Path,
        help="Optional X.509 certificate to include in signature",
    )

    args = parser.parse_args()

    # Load private key
    try:
        private_key = load_private_key(args.key)
        print(f"Loaded private key from {args.key}")
    except Exception as e:
        print(f"Error loading private key: {e}")
        return 1

    # Load certificate if provided
    cert = None
    if args.cert:
        cert = args.cert.read_text()
        print(f"Loaded certificate from {args.cert}")

    # Process all XML files
    success_count = 0
    error_count = 0

    for xml_file in args.enriched_dir.rglob("*.xml"):
        relative_path = xml_file.relative_to(args.enriched_dir)
        output_path = args.signed_dir / relative_path

        if sign_file(xml_file, output_path, private_key):
            success_count += 1
        else:
            error_count += 1

    print(f"\nProcessed {success_count + error_count} files:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
