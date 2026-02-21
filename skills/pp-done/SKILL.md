---
name: pp-done
description: Complete the current task. Update reference.md and plan.md. Mark task as done.
disable-model-invocation: true
---

# PP Done

Complete the active task, commit final task artifacts, and close planning state.

## Instructions

1. **Find the active task.** Read `## Work in Progress` in `plan/plan.md`.
   If empty, report there is no active task.

2. **Verify completion prerequisites:**
   - Read `plan/PIPELINE.md` and identify final stage ID (default: `completed`)
   - Confirm all required pre-final stages in task Progress are `[x]`
   - If testing stage exists and is unchecked, warn and ask whether to proceed

3. **Write task summary** in `task-{id}.md` under `## Summary`:
   - What was done
   - Key decisions
   - Files created/modified
   - Dependencies added

4. **Update `plan/reference.md`** with created/updated modules and reuse notes.

5. **Update `plan/plan.md`:**
   - Mark this task `[x]` in `## Tasks`

6. **Mark final stage complete** in task Progress (`[x] completed` in default pipeline).

7. **Clear `## Work in Progress`** in `plan/plan.md`.

8. **Prepare commit for final task artifacts:**
   - Show `git status --short`
   - Suggest default commit message: `Task {id}: complete {task title}`
   - Ask user to confirm commit now or proceed without commit
   - If user confirms commit:
     - Execute `pp-commit` and pass context (task id/title + suggested message)
     - Ensure commit includes:
       - implementation changes
       - `plan/task-{id}.md` summary updates
       - `plan/reference.md` updates
       - `plan/plan.md` task completion + WIP clear updates
     - If commit fails, report failure and keep status as `commit pending`
   - If user declines commit, continue with status `commit skipped by user`

9. **Report result:**
   - Summary of completion
   - Commit status (`committed`, `commit pending`, or `commit skipped by user`)
   - reference.md changes
   - Remaining task count
   - Suggest `/pp-task` or `/pp-next`

## Notes

- If the project pipeline includes a dedicated commit stage, avoid duplicate
  commits and follow pipeline order.
