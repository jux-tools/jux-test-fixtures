# Signed Fixtures

This directory contains XMLDSig-signed JUnit XML fixtures.

## Generating Signed Fixtures

Signed fixtures must be generated locally using the `sign-fixtures.py` script
because they require a private key for signing.

### Quick Start

1. Generate a test signing key:

```bash
# RSA key (recommended for testing)
openssl genrsa -out test-key.pem 2048

# Or ECDSA key
openssl ecparam -name prime256v1 -genkey -noout -out test-key.pem
```

2. Install py-juxlib:

```bash
uv pip install ../py-juxlib
# or
pip install -e ../py-juxlib
```

3. Sign the enriched fixtures:

```bash
python scripts/sign-fixtures.py enriched/ signed/ --key test-key.pem
```

## Structure

After generation, the signed directory will mirror the enriched directory:

```
signed/
├── generic/
│   ├── basic.xml          # Signed version of enriched/generic/basic.xml
│   └── complete.xml
├── pytest/
│   └── xunit2-basic.xml
├── polarion/
│   └── with-testcase-id.xml
├── cucumber/
│   └── basic.xml
├── maven-surefire/
│   └── basic.xml
└── jenkins/
    └── basic.xml
```

## Signature Format

The signatures use XMLDSig enveloped signatures:

- Algorithm: RSA-SHA256 or ECDSA-SHA256 (based on key type)
- Digest: SHA256
- Canonicalization: C14N (Canonical XML)

Example signature structure:

```xml
<testsuite name="...">
  <properties>...</properties>
  <testcase .../>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo>
      <CanonicalizationMethod Algorithm="..."/>
      <SignatureMethod Algorithm="..."/>
      <Reference URI="">
        <Transforms>...</Transforms>
        <DigestMethod Algorithm="..."/>
        <DigestValue>...</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>...</SignatureValue>
    <KeyInfo>...</KeyInfo>
  </Signature>
</testsuite>
```

## Verifying Signatures

Use py-juxlib to verify signatures:

```python
from juxlib.signing import verify_signature, load_public_key
from lxml import etree

tree = etree.parse("signed/generic/basic.xml")
public_key = load_public_key("test-key.pub")

is_valid = verify_signature(tree.getroot(), public_key)
print(f"Signature valid: {is_valid}")
```

## Notes

- Do not commit private keys to the repository
- The `.gitignore` excludes `*.pem` and `*.key` files
- For CI/CD, generate keys as part of the test setup
