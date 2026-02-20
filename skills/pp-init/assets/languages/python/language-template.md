# Language Profile

Language: python

## Runtime / Toolchain
- Python 3.12+
- Package and environment tooling is project-dependent

## Build / Test Defaults
- Preferred test runner: `pytest`
- Fallback allowed: focused executable smoke script when `pytest` is not suitable

## File Conventions
- Source: `.py`
- Tests: `tests/test_*.py` by default

## Dependency Conventions
- Use existing dependency mechanism in the project (`pyproject.toml`, `requirements.txt`, or equivalent)
- Keep dependency additions minimal and justified

## pp-test Validation Checklist
- Verify core acceptance criteria with one focused test
- Run the test and report actual command + output
- Do not mark tested without execution evidence
