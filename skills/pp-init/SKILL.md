---
name: pp-init
description: Scaffold or migrate a PP project structure with plan/, templates, language profile, and project-specific pipeline configuration.
disable-model-invocation: true
---

# PP Init

Scaffold or migrate PP project management files.

## Instructions

1. **Detect project state:**
   - If `plan/` does not exist: initialize a new PP project
   - If `plan/` exists: run migration-safe init (preserve existing plan content)

2. **Collect project name for new setup.** Use AskQuestion when creating new `plan/`.

3. **Resolve primary language.**
   - Parse optional `/pp-init <language>` argument
   - Canonical: `python`, `arduino`
   - Alias: `py` -> `python`
   - Ask user if missing/invalid

4. **Ensure base files exist** (create if missing):
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

5. **Ensure pipeline config exists:**
   - Create `plan/PIPELINE.md` from `assets/pipeline-template.md` if missing
   - If present, keep user-customized content, but normalize legacy shape to
     canonical schema when needed.
   - Legacy normalization rules:
     - Heading `# PP Pipeline` -> `# Pipeline`
     - Missing `version` -> add `version: 1`
     - Scalar actions (e.g. `actions: pp-task`) ->
       list form:
       `actions:`
       `  - skill: pp-task`
   - Preserve existing stage order and checkbox semantics during normalization.
   - Do not require users to manually rewrite `PIPELINE.md` for these format
     differences.

6. **Run one-time migration for existing tasks (if needed):**
   - Read stage IDs from `plan/PIPELINE.md`
   - For each `plan/task-*.md`, map legacy labels to stage IDs:
     - `task planned` -> `task-planned`
     - `interface designed` -> `design-reviewed`
     - `interface-designed` -> `design-reviewed`
     - `design review` -> `design-reviewed`
     - `implemented` -> `implemented`
     - `reviewed` -> `reviewed`
     - `tested` -> `tested`
     - `completed` -> `completed`
   - Preserve checkbox state and stage order from pipeline where possible

7. **Copy PP rule** to `.cursor/rules/pp-conventions.mdc`.

8. **Report success:**
   - New or migrated mode
   - Selected language
   - Whether `PIPELINE.md` was created or reused
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
