---
name: pp-pipeline-edit
description: Edit plan/PIPELINE.md safely with preview/confirm, plus summary and print modes.
disable-model-invocation: true
---

# PP Pipeline Edit

Edit `plan/PIPELINE.md` using safe operations. Supports read-only CLI modes for
summary and raw file output.

## Invocation Modes

- `/pp-pipeline-edit` -> interactive edit wizard
- `/pp-pipeline-edit summary` -> print pipeline summary
- `/pp-pipeline-edit print` -> print raw `plan/PIPELINE.md`

If the argument is not one of `summary` or `print`, run wizard mode.

## Common Preconditions

1. Check `plan/` exists. If not, tell user to run `/pp-init`.
2. Read `plan/PIPELINE.md`. If missing, tell user to run `/pp-init`.
3. For `print` mode:
   - Print raw file as-is (no schema validation required).
4. For `summary` and wizard modes:
   - Accept canonical schema and legacy schema variants.
   - Normalize legacy format in-memory first, then validate.
5. Legacy normalization compatibility:
   - Heading `# PP Pipeline` is accepted and normalized to `# Pipeline`
   - Missing `version` is accepted and normalized to `version: 1`
   - Scalar action values like `actions: pp-task` are accepted and normalized to:
     - `actions:`
     - `  - skill: pp-task`
6. Validate schema before summary/edit apply:
   - `# Pipeline`, `version`, `## Stages`
   - Stage fields: `id`, `label`, `actions`, `approval_gate`, `auto_behavior`
   - Unique kebab-case stage IDs
   - `auto_behavior` in `{run, skip}`
   - `actions` has one or more `skill` entries starting with `pp-`

## Mode: `summary`

Print a concise summary only:
- Ordered stages
- For each stage: `id`, `label`, `approval_gate`, `auto_behavior`, action skills
- Total stage count
- If legacy format was normalized in-memory, mention that in output.

Do not modify any files.

## Mode: `print`

Print the full raw content of `plan/PIPELINE.md` exactly as stored.

Do not modify any files.

## Mode: Wizard (default)

### Supported edit operations (safe core)
- add stage
- remove stage
- move stage
- rename stage id
- edit stage metadata (`label`, `approval_gate`, `auto_behavior`)
- edit stage actions

### Active-task-only migration rule

If an edit changes stage IDs/order/membership, migrate **only the active task**:

1. Read `## Work in Progress` in `plan/plan.md`.
2. If active task filename exists:
   - Update only that `plan/task-{id}.md` Progress section to match pipeline edit.
3. If no active task exists:
   - Do not touch any task files.
   - Warn explicitly: `No active task; skipped progress migration.`

Do not migrate non-active tasks in this skill.

### Preview and confirmation

Before writing:
- Show proposed pipeline change summary (old -> new)
- Show active-task migration impact (if active task exists)

Then require explicit confirmation:
- `apply` -> write changes
- `cancel` -> no writes

### Apply behavior

- Apply pipeline changes and active-task migration together.
- If source file was in legacy shape, write canonical schema on apply.
- Re-validate `plan/PIPELINE.md` after apply.
- If rename causes task-progress conflict (both old/new IDs already present),
  block apply and report the exact conflict.

## Output After Successful Apply

- Operations performed
- Whether active task was migrated
- Reminder of next useful commands:
  - `/pp-pipeline`
  - `/pp-pipeline-edit summary`
  - `/pp-status`
  - `/pp-next`
