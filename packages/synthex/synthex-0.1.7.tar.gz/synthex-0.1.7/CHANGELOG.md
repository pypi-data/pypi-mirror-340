## Release v0.1.7 - April 13, 2025

### Fixed

- Fixed bug causing Pydantic to `raise ImportError('email-validator is not installed)`
- Fixed bug causing `Jobs.generate_data()` to crash when parameter `output_path` contains a file name but not a path.
- Fixed bug causing `Jobs.generate_data()` to generate an incorrect number of datapoints.

### Changes

- Updated `JobOutputType` and `JobOutputSchemaDefinition`

### Additions

- Added `JobOutputFieldDatatype`

## Release v0.1.6 - April 11, 2025

### Additions

- Added CHANGELOG.md
- Added CONTRIBUTING.mg
- Added CODEOWNERS
- Added CODE_OF_CONDUCT.md
- Added SECURITY.md
- Added bug_report.md
- Added feature_request.md
- Added pull_request_template.md
- Added sanitation logic for the `output_path` parameter of `Jobs.generate_data()`
- Added unit tests for `Jobs.generate_data()`
- Added unit tests for `Synthex.__init__()`

### Changes

- Updated README.md
- Updated name of most test files
- Updated python-publish.yml to include a 'run tests' step

### Removals

- Removed `main.py`