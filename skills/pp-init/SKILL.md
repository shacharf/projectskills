---
name: pp-init
description: Initialize a fresh PP project structure with plan/, templates, language profile, and project-specific pipeline configuration.
disable-model-invocation: true
---

# PP Init

Initialize PP project management files for a fresh project.

## Instructions

1. **Detect project state:**
   - If `plan/` already exists: stop and tell the user `pp-init` is for fresh initialization only
   - If `plan/` does not exist: initialize a new PP project

2. **Resolve primary language from the command argument.**
   - Require `/pp-init <language>`
   - Canonical: `python`, `arduino`
   - Alias: `py` -> `python`
   - If missing or invalid, fail with a short usage message; do not ask questions

3. **Derive project name automatically.**
   - Use the current working directory basename as `{PROJECT_NAME}`
   - Do not ask the user for project name

4. **Create the PP baseline files:**
   - `plan/plan.md` from `assets/plan-template.md`
   - `plan/language.md` from `assets/languages/{language}/language-template.md`
   - `plan/AGENTS.md` from `assets/languages/{language}/agents-template.md`
   - `docs/architecture/README.md` from `assets/architecture/README-template.md`
   - `docs/architecture/system-map.yaml` from `assets/architecture/system-map-template.yaml`
   - `docs/architecture/c4-context.md` from `assets/architecture/c4-context-template.md`
   - `docs/architecture/c4-container.md` from `assets/architecture/c4-container-template.md`
   - `docs/architecture/c4-components.md` from `assets/architecture/c4-components-template.md`
   - `docs/architecture/sequences/README.md` from `assets/architecture/sequences-README-template.md`
   - `docs/architecture/sequences/request-flow.md` from `assets/architecture/sequence-template.md`
   - `docs/architecture/adrs/README.md` from `assets/architecture/adrs-README-template.md`
   - `docs/architecture/adrs/ADR-0001-architecture-baseline.md` from `assets/architecture/ADR-0001-template.md`
   - `docs/catalog/architecture-code-catalog.md` from `assets/catalog-template.md`
   - Treat these files as the architecture baseline only; after init, ongoing
     updates belong to `pp-implement`, not `pp-task` or `pp-arch-catalog`

5. **Create pipeline config:**
   - Create `plan/PIPELINE.md` directly from `assets/pipeline-template.md`
   - Do not normalize legacy formats
   - Do not preserve or merge existing pipeline content

6. **Copy PP rule** to `.cursor/rules/pp-conventions.mdc`.

7. **Report success:**
   - Fresh initialization completed
   - Derived project name
   - Selected language
   - Baseline files created
   - Tell user to run `/pp-pipeline`, `/pp-plan`, or `/pp-next`

## Template Locations

### Generic templates (`skills/pp-init/assets/`)
- `assets/plan-template.md`
- `assets/catalog-template.md`
- `assets/task-template.md`
- `assets/pipeline-template.md`
- `assets/architecture/README-template.md`
- `assets/architecture/system-map-template.yaml`
- `assets/architecture/c4-context-template.md`
- `assets/architecture/c4-container-template.md`
- `assets/architecture/c4-components-template.md`
- `assets/architecture/sequences-README-template.md`
- `assets/architecture/sequence-template.md`
- `assets/architecture/adrs-README-template.md`
- `assets/architecture/ADR-0001-template.md`

### Language templates (`assets/languages/{language}/`)
- `agents-template.md`
- `language-template.md`
