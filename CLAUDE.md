# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

jux-test-fixtures is a **curated collection of JUnit XML test fixtures** crafted specifically for testing the Jux ecosystem. Unlike `junit-xml-test-fixtures` (which aggregates upstream submodules), this project contains custom-crafted samples designed to:

- Cover major JUnit XML dialects (pytest, Maven Surefire, Polarion, Cucumber, Jenkins)
- Test edge cases and boundary conditions
- Provide signed XML samples for signature verification testing
- Include py-juxlib enriched samples with environment metadata
- Populate Jux server instances for development and testing

## Repository Structure

```
jux-test-fixtures/
├── CLAUDE.md                  # This file
├── CLAUDE.local.md            # Local config (git-ignored)
├── README.md                  # User documentation
├── .gitignore
│
├── raw/                       # Base JUnit XML without enrichment
│   ├── pytest/                # pytest xunit1 and xunit2 formats
│   ├── maven-surefire/        # Maven Surefire/Failsafe format
│   ├── polarion/              # Polarion ALM xUnit format
│   ├── cucumber/              # Cucumber/BDD JUnit format
│   ├── jenkins/               # Jenkins JUnit format
│   └── generic/               # Standard JUnit XML
│
├── enriched/                  # Raw + py-juxlib metadata properties
│   ├── pytest/
│   ├── maven-surefire/
│   ├── polarion/
│   ├── cucumber/
│   ├── jenkins/
│   └── generic/
│
├── signed/                    # Enriched + XMLDSig signatures
│   ├── pytest/
│   ├── maven-surefire/
│   ├── polarion/
│   ├── cucumber/
│   ├── jenkins/
│   └── generic/
│
├── edge-cases/                # Boundary conditions and special cases
│   ├── empty-testsuite.xml
│   ├── unicode-content.xml
│   ├── nested-testsuites.xml
│   ├── large-properties.xml
│   ├── special-characters.xml
│   ├── zero-tests.xml
│   ├── all-skipped.xml
│   ├── all-failed.xml
│   ├── missing-attributes.xml
│   └── malformed/             # Invalid XML for error handling tests
│
├── schemas/                   # XSD schemas for validation
│   └── README.md              # Links to canonical schemas
│
└── scripts/                   # Fixture generation and signing scripts
    ├── sign-fixtures.py       # Sign raw/enriched fixtures
    ├── enrich-fixtures.py     # Add py-juxlib metadata
    └── validate-fixtures.py   # Validate against schemas
```

## Fixture Categories

### Raw Fixtures (`raw/`)

Base JUnit XML files without any Jux-specific enrichment. These represent what testing frameworks produce natively.

### Enriched Fixtures (`enriched/`)

Raw fixtures enhanced with py-juxlib environment metadata as `<property>` elements:

```xml
<properties>
  <!-- py-juxlib metadata -->
  <property name="jux.hostname" value="build-server-01"/>
  <property name="jux.username" value="ci-user"/>
  <property name="jux.platform" value="Linux 6.1.0-x86_64"/>
  <property name="jux.python_version" value="3.12.1"/>
  <property name="jux.timestamp" value="2026-01-20T10:30:00Z"/>
  <property name="jux.project_name" value="my-project"/>
  <property name="jux.git_commit" value="abc123def456"/>
  <property name="jux.git_branch" value="main"/>
  <property name="jux.git_status" value="clean"/>
  <property name="jux.ci_provider" value="github"/>
  <property name="jux.ci_build_id" value="12345"/>
</properties>
```

### Signed Fixtures (`signed/`)

Enriched fixtures with XMLDSig enveloped signatures. Used for testing:

- Signature verification in Jux server
- Signature validation in py-juxlib
- Tamper detection

### Edge Cases (`edge-cases/`)

Fixtures testing boundary conditions:

| File | Purpose |
|------|---------|
| `empty-testsuite.xml` | Testsuite with no testcases |
| `unicode-content.xml` | Unicode in names, messages, output |
| `nested-testsuites.xml` | Multiple levels of nesting |
| `large-properties.xml` | Many properties, long values |
| `special-characters.xml` | XML entities, CDATA, reserved chars |
| `zero-tests.xml` | tests="0" attribute |
| `all-skipped.xml` | All tests skipped |
| `all-failed.xml` | All tests failed |
| `missing-attributes.xml` | Optional attributes omitted |
| `malformed/*.xml` | Invalid XML for error handling |

## Dialect Coverage

### pytest (`pytest/`)

Both `xunit1` (legacy) and `xunit2` (modern) formats:

- `xunit1-basic.xml` - Basic xunit1 format
- `xunit1-properties.xml` - xunit1 with custom properties
- `xunit2-basic.xml` - Basic xunit2 format
- `xunit2-properties.xml` - xunit2 with record_property
- `xunit2-markers.xml` - Tests with pytest markers

### Maven Surefire (`maven-surefire/`)

Standard Maven test report format:

- `basic.xml` - Single test class
- `multiple-classes.xml` - Multiple test classes
- `parameterized.xml` - Parameterized tests
- `with-output.xml` - System out/err captured

### Polarion (`polarion/`)

Polarion ALM xUnit format with custom properties:

- `basic.xml` - Basic Polarion format
- `with-testcase-id.xml` - Linked to Polarion test cases
- `with-requirements.xml` - Linked to requirements (verifies)
- `with-project-info.xml` - Project and testrun metadata

### Cucumber (`cucumber/`)

BDD/Gherkin-based JUnit output:

- `basic.xml` - Simple feature/scenario
- `scenario-outline.xml` - Parameterized scenarios
- `with-tags.xml` - Cucumber tags as properties
- `nested-features.xml` - Multiple features

### Jenkins (`jenkins/`)

Jenkins-compatible JUnit format:

- `basic.xml` - Standard Jenkins format
- `with-attachments.xml` - Test attachments
- `pipeline.xml` - Pipeline stage results

### Generic (`generic/`)

Standard JUnit XML without vendor-specific extensions:

- `basic.xml` - Minimal valid JUnit XML
- `complete.xml` - All standard elements
- `with-skipped.xml` - Skipped tests
- `with-failures.xml` - Failed tests
- `with-errors.xml` - Test errors
- `mixed-results.xml` - Pass/fail/skip/error mix

## Usage

### For Jux Server Testing

```bash
# Copy fixtures to Jux test data
cp -r jux-test-fixtures/signed/* ../jux/test/fixtures/junit_xml/

# Import into running Jux server
for f in jux-test-fixtures/signed/**/*.xml; do
  curl -X POST http://localhost:4000/api/reports \
    -H "Content-Type: application/xml" \
    -d @"$f"
done
```

### For py-juxlib Testing

```bash
# Use fixtures in pytest
cp -r jux-test-fixtures/raw/* ../py-juxlib/tests/fixtures/

# Reference in tests
from pathlib import Path
FIXTURES = Path(__file__).parent / "fixtures"
```

### For pytest-jux Testing

```bash
# Copy all fixture types
cp -r jux-test-fixtures/{raw,enriched,signed} ../pytest-jux/tests/fixtures/
```

## Scripts

### `scripts/enrich-fixtures.py`

Adds py-juxlib metadata properties to raw fixtures:

```bash
python scripts/enrich-fixtures.py raw/ enriched/
```

### `scripts/sign-fixtures.py`

Signs enriched fixtures using test keys:

```bash
python scripts/sign-fixtures.py enriched/ signed/ --key test-key.pem
```

### `scripts/validate-fixtures.py`

Validates fixtures against schemas:

```bash
python scripts/validate-fixtures.py raw/ --schema schemas/junit-10.xsd
```

## Naming Conventions

- Use lowercase with hyphens: `xunit2-basic.xml`
- Prefix with format variant where applicable: `xunit1-`, `xunit2-`
- Suffix special cases: `-with-output.xml`, `-parameterized.xml`
- Edge cases use descriptive names: `all-skipped.xml`

## AI Development Guidelines

### Adding New Fixtures

1. Create raw version first in appropriate dialect directory
2. Run `enrich-fixtures.py` to create enriched version
3. Run `sign-fixtures.py` to create signed version
4. Update README.md fixture list

### Fixture Content Guidelines

- Use realistic but fictional test names and data
- Include varied results (pass, fail, skip, error)
- Add system output where format supports it
- Use reasonable durations (0.001 - 5.0 seconds)
- Include timestamps in ISO 8601 format

### When Adding Dialects

1. Create dialect directory in `raw/`, `enriched/`, `signed/`
2. Add at least `basic.xml` fixture
3. Document format specifics in this file
4. Add validation to `scripts/validate-fixtures.py`

## Related Projects

| Project | Relationship |
|---------|--------------|
| `junit-xml-test-fixtures` | Upstream reference collection (submodules) |
| `jux` | Server that consumes these fixtures |
| `pytest-jux` | Client that produces similar XML |
| `behave-jux` | Client that produces similar XML |
| `py-juxlib` | Library defining metadata format |
| `jux-openapi` | API contract for fixture submission |

## License

Apache-2.0

All fixtures are original works created specifically for the Jux project.
