# JUnit XML Schemas

This directory contains references to JUnit XML schema definitions.

## Canonical Schema Sources

Rather than duplicating schemas, we reference the authoritative sources:

### Apache Ant / windyroad (de facto standard)

- **Source**: https://github.com/windyroad/JUnit-Schema
- **License**: Apache-2.0
- **Files**: `JUnit.xsd`, `jenkins-junit.xsd`

### Maven Surefire (official Apache)

- **Source**: https://maven.apache.org/surefire/maven-surefire-plugin/xsd/surefire-test-report.xsd
- **License**: Apache-2.0

### JUnit 5 (official)

- **Source**: https://github.com/junit-team/junit5
- **Path**: `platform-tests/src/test/resources/jenkins-junit.xsd`
- **License**: EPL-2.0

## Downloading Schemas

To validate fixtures locally, download schemas:

```bash
# windyroad JUnit XSD
curl -o junit.xsd https://raw.githubusercontent.com/windyroad/JUnit-Schema/master/JUnit.xsd

# Maven Surefire XSD
curl -o surefire-test-report.xsd https://maven.apache.org/surefire/maven-surefire-plugin/xsd/surefire-test-report.xsd

# JUnit 5 Jenkins XSD
curl -o jenkins-junit.xsd https://raw.githubusercontent.com/junit-team/junit5/main/platform-tests/src/test/resources/jenkins-junit.xsd
```

## Validation

Use the `validate-fixtures.py` script:

```bash
# Validate well-formedness only
python scripts/validate-fixtures.py raw/

# Validate against specific schema
python scripts/validate-fixtures.py raw/ --schema schemas/junit.xsd
```

## Notes

- JUnit XML has no single authoritative schema
- Different tools produce slightly different XML structures
- The windyroad schema is the most commonly referenced
- Fixtures in this repository aim for maximum compatibility
