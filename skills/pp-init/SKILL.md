---
name: pp-init
description: Scaffold a new PP project structure with plan/, templates, and language profile configuration.
disable-model-invocation: true
---

# PP Init

Scaffold the project management structure for a new PP-managed project.

## Instructions

1. **Check if `plan/` already exists.** If it does, tell the user and ask if they want
   to reinitialize (which would overwrite templates).

2. **Collect project name.** Use AskQuestion:
   - "What is the project name?"

3. **Resolve primary language.**
   - Parse optional command argument from `/pp-init <language>`.
   - Supported canonical values: `python`, `arduino`.
   - Supported alias: `py` -> `python`.
   - If no argument is provided, ask the user to choose language (`python` or `arduino`).
   - If value is invalid, show valid options and ask again.

4. **Create `plan/` directory** with generic templates from this skill's `assets/`
   directory, replacing `{PROJECT_NAME}` where applicable:

   - `plan/plan.md` -- from `assets/plan-template.md`
   - `plan/reference.md` -- from `assets/reference-template.md`

5. **Generate language profile files** from this skill's language assets:
   - `plan/language.md` -- from `assets/languages/{language}/language-template.md`
   - `plan/AGENTS.md` -- from `assets/languages/{language}/agents-template.md`

6. **Copy the PP rule** to the project's `.cursor/rules/` directory:
   - Copy `pp-conventions.mdc` so PP conventions are active.
   - Create `.cursor/rules/` if it does not exist.

7. **Report success** to the user:
   - Show project name + selected language
   - List created files
   - Tell them to run `/pp-plan` next, or `/pp-next` for orchestration

## Template Locations

### Generic templates (`skills/pp-init/assets/`)
- `assets/plan-template.md`
- `assets/reference-template.md`
- `assets/task-template.md` (used later by `pp-task`)

### Language templates (`assets/languages/{language}/`)
- `agents-template.md`
- `language-template.md`
