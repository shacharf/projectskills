---
name: pp-status
description: Show current PP project state including task progress and next action.
disable-model-invocation: true
---

# PP Status

Show the current project state at a glance.

## Instructions

1. **Check that plan/ exists.** If not, tell the user to run `/pp-init` first.

2. **Read plan/plan.md.** Extract:
   - Project name (from the `#` heading)
   - The task list under `## Tasks`
   - Count completed `[x]` vs incomplete `[ ]` tasks

3. **Read the `## Work in Progress` section** in plan.md.
   - If it contains a filename → read `plan/{filename}` and extract its `## Progress` checklist.
   - If empty → no task is currently active.

4. **Determine the next action:**
   - No tasks in plan.md → next action is `/pp-plan`
   - WIP has a filename → next action is the first unchecked Progress step in that task
   - WIP is empty + unchecked tasks remain → next action is `/pp-task`
   - WIP is empty + all tasks are `[x]` → project is complete

5. **Display a summary** in this format:

```
PP Project Status: {project name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tasks: {completed}/{total} complete

{For each task in plan.md, show:}
  [x] 1. Task name
  [x] 2. Task name
  [ ] 3. Task name  ← active
  [ ] 4. Task name

{If active task exists:}
Active Task: {task title}
  Progress:
    [x] task planned
    [x] interface designed
    [ ] implemented  ← current step
    [ ] reviewed
    [ ] tested
    [ ] completed

Next action: /pp-implement (or /pp-next to advance)
```
