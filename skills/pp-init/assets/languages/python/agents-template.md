# Coding Standards

## Language & Runtime
- Python 3.12+
- Use type hints on all public function signatures
- Prefer dataclasses or pydantic for structured data where appropriate

## Style
- Follow PEP 8
- Max line length: 100 characters
- Use descriptive variable names; avoid single-letter names outside loops

## Architecture
- Keep modules focused: one responsibility per file
- Public API at the top of each module, private helpers below
- Add `__all__` when the module exposes a stable public API

## Code Reuse
- Before writing new code, prefer established Python packages where appropriate
- Check `docs/catalog/architecture-code-catalog.md` for existing modules before introducing new ones
- Generalize duplicated patterns into shared utilities

## Error Handling
- Use explicit exceptions, not bare `except`
- Include context in error messages (what failed and with which inputs)
- Fail fast on invalid input

## Documentation
- Docstrings on public functions and classes
- Keep task and reference docs self-contained so another contributor can continue work

## Testing
- Minimal tests per task, focused on acceptance criteria
- Tests should run with a single command
