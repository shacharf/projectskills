# Coding Standards

## Language & Runtime
- Python 3.10+
- Use type hints on all function signatures
- Use dataclasses or pydantic for structured data

## Style
- Follow PEP 8
- Max line length: 100 characters
- Use descriptive variable names; avoid single-letter names outside loops

## Architecture
- Keep modules focused: one responsibility per file
- Public API at the top of each module, private helpers below
- Use existing python packages over hand-rolling solutions

## Code Reuse
- Before writing new code, check reference.md for existing modules
- If you find duplicated or similar code, generalize it into a shared utility
- Import from existing project modules rather than copy-pasting

## Error Handling
- Use explicit exceptions, not bare try/except
- Include context in error messages (what failed, with what input)
- Fail fast on invalid input

## Documentation
- Docstrings on all public functions (one-line summary + args if non-obvious)
- No redundant comments that restate the code
- Keep plan/ docs self-contained: anyone reading them can continue work

## Testing
- Minimal tests per task, not comprehensive suites
- Test the core behavior described in acceptance criteria
- Tests should be runnable with a single command
