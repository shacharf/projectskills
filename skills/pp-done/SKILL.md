---
name: pp-done
description: Complete the current task. Update reference.md and plan.md. Mark task as done.
disable-model-invocation: true
---

# PP Done

Complete the active task and close planning artifacts. Commit handling belongs to
`pp-commit` when present in the pipeline.

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
   - Clear `## Work in Progress`

6. **Mark final stage complete** in task Progress (`[x] completed` in default pipeline).

7. **Report result:**
   - Summary of completion
   - reference.md changes
   - Remaining task count
   - Suggest `/pp-task` or `/pp-next`

## Notes

- Do not suggest or perform commit operations here.
- If pipeline includes a commit stage, that is handled by `pp-commit`.
