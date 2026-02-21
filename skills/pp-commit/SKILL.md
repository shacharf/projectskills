---
name: pp-commit
description: Prepare and suggest a focused commit for the active task changes.
disable-model-invocation: true
---

# PP Commit

Prepare commit guidance for the active task.

## Instructions

1. **Find the active task.** Read `## Work in Progress` in `plan/plan.md`.
   If empty, tell the user there is no active task.

2. **Read active task file** and extract task ID/title.

3. **Show current git change set** for user review:
   - Use `git status --short`
   - If available, include a short staged/unstaged summary

4. **Suggest a commit message**:
   - Default: `Task {id}: {task title}`

5. **Ask the user** whether to commit now or continue without committing.

6. **Mark progress:**
   - Check `[x] committed` in task `## Progress` only after user confirms commit
     was created (or explicitly approves marking this stage complete).

7. **Tell the user** to run `/pp-done` or `/pp-next` next.
