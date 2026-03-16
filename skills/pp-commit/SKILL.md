---
name: pp-commit
description: Create a focused commit for the active task changes.
disable-model-invocation: true
---

# PP Commit

Create a focused commit for the active task.

## Instructions

1. **Resolve task context:**
   - If caller supplied task file, task ID, or task title, use that context
   - Otherwise read `## Work in Progress` in `plan/plan.md`
   - If neither caller context nor WIP is available, report there is no active task to commit

2. **Read the task file** and extract task ID/title when not already supplied.

3. **Show current git change set** for user review:
   - Use `git status --short`
   - If available, include a short staged/unstaged summary

4. **Determine commit message**:
   - Default: `Task {id}: {task title}`
   - If caller supplied an explicit message, use it

5. **Attempt the commit autonomously:**
   - Stage the intended task changes
   - Create the commit using the chosen message
   - Do not ask the user whether to proceed
   - If the repository state blocks a safe deterministic commit, stop and report the blocker

6. **Mark progress:**
   - Check `[x] committed` in the resolved task file `## Progress` only after the commit is actually created
   - If there is no `committed` stage in task Progress, do not invent one

7. **Tell the user** to run `/pp-done` or `/pp-next` next.
