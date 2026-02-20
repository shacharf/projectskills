---
name: pp-init
description: Scaffold a new PP project structure with plan/, templates, and configuration.
disable-model-invocation: true
---

# PP Init

Scaffold the project management structure for a new PP-managed project.

## Instructions

1. **Check if plan/ already exists.** If it does, tell the user and ask if they want
   to reinitialize (which would overwrite templates).

2. **Ask the user for the project name.** Use the AskQuestion tool:
   - "What is the project name?"

3. **Create the plan/ directory** with the following files. Use the templates from
   `assets/` in this skill directory, replacing `{PROJECT_NAME}` with the user's answer.

   - `plan/plan.md` -- from `assets/plan-template.md`
   - `plan/reference.md` -- from `assets/reference-template.md`
   - `plan/AGENTS.md` -- from `assets/agents-template.md`

4. **Copy the PP rule** to the project's `.cursor/rules/` directory:
   - Copy the `pp-conventions.mdc` rule so the project has PP conventions active.
   - Create `.cursor/rules/` if it doesn't exist.

5. **Report success** to the user:
   - List the created files
   - Tell them to run `/pp-plan` next to create their project plan
   - Or run `/pp-next` to let the orchestrator guide them

## Template Locations

Read templates from this skill's assets directory:
- `assets/plan-template.md`
- `assets/reference-template.md`
- `assets/agents-template.md`
- `assets/task-template.md` (used later by pp-task)
