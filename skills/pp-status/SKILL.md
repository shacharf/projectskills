---
name: pp-status
description: Show current PP project state including dynamic pipeline stage progress and next action.
disable-model-invocation: true
---

# PP Status

Show project state derived from `plan/plan.md` and `plan/PIPELINE.md`.

## Instructions

1. **Check that plan/ exists.** If not, tell user to run `/pp-init`.

2. **Read `plan/plan.md`.** Extract:
   - Project name
   - Tasks under `## Tasks`
   - Completed vs incomplete counts

3. **Read `plan/PIPELINE.md`.**
   - Extract ordered stage IDs/labels
   - If missing, report and suggest `/pp-init`

4. **Read `## Work in Progress` from `plan/plan.md`:**
   - If filename exists -> read active task Progress
   - If empty -> no active task

5. **Determine next action:**
   - No tasks -> `/pp-plan`
   - Active task -> first unchecked stage ID and mapped action skill list
   - No active task + unchecked tasks -> `/pp-task`
   - No active task + all tasks complete -> project complete

6. **Display summary:**

```
PP Project Status: {project name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tasks: {completed}/{total} complete

{task checklist from plan.md}

{if active task}
Active Task: {task title}
  Progress:
    [x] {stage_id} ({label})
    [ ] {stage_id} ({label})  <- current

Next action: {skill(s)} (or /pp-next)
```
