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
   - `plan/reference.md` from `assets/reference-template.md`
   - `plan/language.md` from `assets/languages/{language}/language-template.md`
   - `plan/AGENTS.md` from `assets/languages/{language}/agents-template.md`

5. **Ensure pipeline config exists:**
   - Create `plan/PIPELINE.md` from `assets/pipeline-template.md` if missing
   - If present, keep user-customized content

6. **Run one-time migration for existing tasks (if needed):**
   - Read stage IDs from `plan/PIPELINE.md`
   - For each `plan/task-*.md`, map legacy labels to stage IDs:
     - `task planned` -> `task-planned`
     - `interface designed` -> `interface-designed`
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
- `assets/reference-template.md`
- `assets/task-template.md`
- `assets/pipeline-template.md`

### Language templates (`assets/languages/{language}/`)
- `agents-template.md`
- `language-template.md`
