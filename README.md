<!--
SPDX-License-Identifier: Apache-2.0
SPDX-FileCopyrightText: 2026 Georges Martin <jrjsmrtn@gmail.com>
-->

# Jux Test Fixtures

Curated collection of JUnit XML test fixtures for the Jux ecosystem.

## Overview

This repository contains hand-crafted JUnit XML samples designed to test the Jux tools ecosystem, including:

- **Major JUnit XML dialects**: pytest (xunit1/xunit2), Maven Surefire, Polarion ALM, Cucumber, Jenkins
- **Edge cases**: Empty suites, Unicode content, nested structures, boundary conditions
- **Signed samples**: XMLDSig-signed fixtures for signature verification testing
- **Enriched samples**: Fixtures with py-juxlib environment metadata

## Quick Start

```bash
# Clone the repository
git clone <repository-url> jux-test-fixtures
cd jux-test-fixtures

# Use fixtures in your tests
ls raw/pytest/
ls enriched/generic/
ls signed/polarion/
```

## Directory Structure

```
jux-test-fixtures/
├── raw/                    # Base JUnit XML (no enrichment)
│   ├── pytest/             # pytest xunit1 and xunit2
│   ├── maven-surefire/     # Maven Surefire format
│   ├── polarion/           # Polarion ALM xUnit
│   ├── cucumber/           # BDD/Cucumber format
│   ├── jenkins/            # Jenkins format
│   └── generic/            # Standard JUnit XML
│
├── enriched/               # Raw + py-juxlib metadata
│   └── (same structure)
│
├── signed/                 # Enriched + XMLDSig signatures
│   └── (same structure)
│
├── edge-cases/             # Boundary conditions
│   └── malformed/          # Invalid XML for error testing
│
├── schemas/                # XSD schemas
└── scripts/                # Generation scripts
```

## Fixture Types

### Raw Fixtures

Base JUnit XML as produced by testing frameworks, without modifications.

### Enriched Fixtures

Raw fixtures enhanced with py-juxlib environment metadata:

```xml
<testsuite name="tests" tests="3" failures="1" errors="0" skipped="0">
  <properties>
    <property name="jux.hostname" value="build-server"/>
    <property name="jux.git_commit" value="abc123"/>
    <property name="jux.ci_provider" value="github"/>
    <!-- ... more metadata ... -->
  </properties>
  <testcase name="test_example" classname="tests.test_module"/>
</testsuite>
```

### Signed Fixtures

Enriched fixtures with XMLDSig enveloped signatures for tamper-proof verification.

## Supported Dialects

| Dialect | Format Variants | Key Features |
|---------|-----------------|--------------|
| pytest | xunit1, xunit2 | record_property, markers |
| Maven Surefire | Standard | System out/err, parameterized |
| Polarion | xUnit + properties | testcase-id, verifies, project-id |
| Cucumber | BDD/Gherkin | Features, scenarios, tags |
| Jenkins | Standard | Attachments, pipeline stages |
| Generic | Standard JUnit | All standard elements |

## Edge Cases

Test boundary conditions and error handling:

- `empty-testsuite.xml` - Testsuite with no test cases
- `unicode-content.xml` - Unicode in names and messages
- `nested-testsuites.xml` - Deep nesting of testsuites
- `all-skipped.xml` - All tests skipped
- `all-failed.xml` - All tests failed
- `special-characters.xml` - XML entities and reserved characters
- `malformed/` - Invalid XML for error handling tests

## Usage Examples

### Jux Server

```bash
# Import fixtures into Jux
for f in signed/**/*.xml; do
  curl -X POST http://localhost:4000/api/reports \
    -H "Content-Type: application/xml" \
    -d @"$f"
done
```

### py-juxlib

```python
from pathlib import Path

FIXTURES = Path("jux-test-fixtures")

def test_parse_pytest_xunit2():
    xml_path = FIXTURES / "raw" / "pytest" / "xunit2-basic.xml"
    # ... test parsing
```

### pytest-jux

```python
import pytest
from pathlib import Path

@pytest.fixture
def fixture_dir():
    return Path(__file__).parent.parent / "jux-test-fixtures"

def test_signature_verification(fixture_dir):
    signed_xml = fixture_dir / "signed" / "generic" / "basic.xml"
    # ... verify signature
```

## Scripts

Generate and validate fixtures:

```bash
# Enrich raw fixtures with metadata
python scripts/enrich-fixtures.py raw/ enriched/

# Sign enriched fixtures
python scripts/sign-fixtures.py enriched/ signed/ --key test-key.pem

# Validate against schemas
python scripts/validate-fixtures.py raw/ --schema schemas/junit-10.xsd
```

## Related Projects

- [jux](../jux/) - Server that receives and analyzes JUnit XML
- [pytest-jux](../pytest-jux/) - pytest plugin for signing and publishing
- [behave-jux](../behave-jux/) - behave plugin for signing and publishing
- [py-juxlib](../py-juxlib/) - Shared Python library
- [junit-xml-test-fixtures](../junit-xml-test-fixtures/) - Upstream reference collection

## Contributing

When adding new fixtures:

1. Create the raw version first
2. Document the dialect and any special features
3. Add enriched and signed versions if applicable
4. Update this README

## License

Apache-2.0

All fixtures are original works created for the Jux project.
