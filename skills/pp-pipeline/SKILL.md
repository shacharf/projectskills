---
name: pp-pipeline
description: Validate and explain the active project pipeline from plan/PIPELINE.md.
disable-model-invocation: true
---

# PP Pipeline

Validate and summarize the project-specific pipeline configuration.

## Instructions

1. **Check that `plan/` exists.** If not, tell the user to run `/pp-init`.

2. **Read `plan/PIPELINE.md`.** If missing, tell the user to run `/pp-init` to
   generate or migrate pipeline config.

3. **Validate required structure:**
   - `# Pipeline`
   - `version:`
   - `## Stages`
   - At least one stage with:
     - `id` (kebab-case, unique)
     - `label`
     - `actions` list with one or more `skill` names
     - `approval_gate` boolean
     - `auto_behavior` in `{run, skip}`

4. **Validate references:**
   - Every action skill name is non-empty and starts with `pp-`
   - Stage IDs are unique
   - If active task exists, its Progress items map to stage IDs

5. **Report pipeline summary:**
   - Ordered stage list (`id`, `label`)
   - Which stages are approval gates
   - Which stages are auto-skipped
   - Any validation errors and concrete fixes

6. **If valid**, suggest `/pp-next` to execute using this pipeline.
