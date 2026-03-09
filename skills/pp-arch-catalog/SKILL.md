---
name: pp-arch-catalog
description: Bootstrap a legacy repo into the PP Architecture/Code Catalog and architecture documentation baseline, including C4 Mermaid docs, sequence diagrams, ADR baseline, and system-map.yaml.
---

# PP Arch Catalog

Bootstrap a legacy repository into the PP Architecture/Code Catalog and
architecture-doc baseline.

## Instructions

1. **Use this skill only for legacy/bootstrap cases.**
   - Intended use: existing repo that lacks PP architecture artifacts
   - Normal new-project flow should use `/pp-init`, not this skill

2. **Ensure PP files exist.** If `plan/` or `plan/language.md` is missing, tell the user to run `/pp-init <language>` first and stop.

3. **Read context:**
   - `plan/language.md` (primary language)
   - `plan/plan.md` (project name if available)
   - `docs/catalog/architecture-code-catalog.md` (preserve manual notes section if present)
   - `plan/reference.md` (legacy import source, if present)
   - `docs/architecture/*` (reuse existing artifacts when available)
   - `README*` and language manifests (`pyproject.toml`, `setup.cfg`, `setup.py`) when available

4. **Run the generator script.** Use:

```bash
python3 skills/pp-arch-catalog/scripts/generate_catalog.py
```

5. **Confirm output.** Report:
   - `docs/catalog/architecture-code-catalog.md` updated as Architecture/Code Catalog
   - `docs/architecture/README.md` updated
   - C4 docs, sequence diagram docs, ADR baseline, and `system-map.yaml` updated/generated
   - Any limitations or missing signals found during extraction

## Output Contract

The generator must produce/update:

### `docs/catalog/architecture-code-catalog.md` (Architecture/Code Catalog)
- `## Overview`
- `## Architecture`
- `## Entry Points`
- `## Interfaces (Generated)`
- `## Data Models / Schemas`
- `## External Dependencies / Services`
- `## Task Change Log` (preserve existing content verbatim)
- `## Reuse Notes (Manual)` (preserve existing content verbatim)
- `## Interface Deltas (Manual)` (preserve existing content verbatim)
- `## Architecture Artifact Notes (Manual)` (preserve existing content verbatim)
- `## Notes (Manual)` (preserve existing content verbatim)

### `docs/architecture/`
- `README.md`
- `c4-context.md` (Mermaid in markdown)
- `c4-container.md` (Mermaid in markdown)
- `c4-components.md` (Mermaid in markdown)
- `sequences/request-flow.md` (Mermaid `sequenceDiagram`)
- `adrs/ADR-0001-architecture-catalog-baseline.md` (if no ADR exists)
- `system-map.yaml`

## Extraction Rules

- Ignore `node_modules/`, `.git/`, build artifacts, and ignored files.
- **Python:** Use AST to index public top-level classes/functions (no leading `_`).
- **Arduino/C++:** Heuristic extraction for public class and function signatures.
- Detect CLI/HTTP/config surfaces when present (argparse/click/typer/FastAPI/Flask).

## Key Principles

- Prefer accurate public interfaces over internal symbols.
- Preserve manual notes in catalog on every run.
- Generate all diagrams as Mermaid embedded in markdown.
- Keep output concise and scannable.
