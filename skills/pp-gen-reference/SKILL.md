---
name: pp-gen-reference
description: Generate or refresh plan/reference.md by scanning an existing repo to create a project overview, architecture summary, entry points, and a public interface index. Use when you need a structured project index or after significant code changes to keep reference.md current.
---

# PP Gen Reference

Generate a structured project reference document from the current repository.

## Instructions

1. **Ensure PP files exist.** If `plan/` or `plan/language.md` is missing, tell the user to run `/pp-init <language>` first and stop.

2. **Read context:**
   - `plan/language.md` (primary language)
   - `plan/plan.md` (project name if available)
   - `plan/reference.md` (preserve manual notes section if present)
   - `README*` and language manifests (`pyproject.toml`, `setup.cfg`, `setup.py`) when available

3. **Run the generator script.** Use:

```bash
python3 skills/pp-gen-reference/scripts/generate_reference.py
```

4. **Confirm output.** Report:
   - `plan/reference.md` updated
   - Summary of key sections (overview, entry points, interfaces)
   - Any limitations or missing signals found during extraction

## Output Contract

The generator must produce `plan/reference.md` with these sections (in order):

- `## Overview`
- `## Architecture`
- `## Entry Points`
- `## Interfaces (Generated)`
- `## Data Models / Schemas`
- `## External Dependencies / Services`
- `## Notes (Manual)` (preserve existing content verbatim)

## Extraction Rules

- Ignore `node_modules/`, `.git/`, build artifacts, and ignored files.
- **Python:** Use AST to index public top-level classes/functions (no leading `_`).
- **Arduino/C++:** Heuristic extraction for public class and function signatures.
- Detect CLI/HTTP/config surfaces when present (argparse/click/typer/FastAPI/Flask).

## Key Principles

- Prefer accurate public interfaces over internal symbols.
- Preserve manual notes in reference.md on every run.
- Keep output concise and scannable.
