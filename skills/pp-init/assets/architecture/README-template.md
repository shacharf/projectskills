# Architecture

## Overview
{High-level architecture summary.}

## Update Policy
- `/pp-init` scaffolds this baseline for new projects.
- `/pp-arch-catalog` may bootstrap this baseline once for legacy projects.
- After bootstrap/init, `pp-implement` owns ongoing updates to `docs/architecture/*`.

## Artifact Index
- `system-map.yaml`
- `c4-context.md`
- `c4-container.md`
- `c4-components.md`
- `sequences/`
- `adrs/`
- `../catalog/architecture-code-catalog.md`

## Artifact Rules
- Update `c4-context.md` when external actors or system boundaries change.
- Update `c4-container.md` when service/module/container boundaries change.
- Update `c4-components.md` when internal component relationships change.
- Update `system-map.yaml` when structural topology or component relationships change.
- Add new ADRs using sequential file names: `ADR-0001-title.md`, `ADR-0002-title.md`, ...
- Add/update sequence diagrams using stable workflow slugs: `sequences/{workflow-slug}.md`
