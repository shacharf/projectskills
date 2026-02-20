---
name: pp-done
description: Complete the current task. Update reference.md and plan.md. Mark task as done.
disable-model-invocation: true
---

# PP Done

Complete the current task: summarize what was done, update project documentation,
and mark the task as finished.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user there is no active task.

2. **Verify test evidence.** Apply verification-before-completion discipline:
   - Check that "tested" is marked `[x]` in Progress
   - If not tested, warn the user and ask if they want to proceed anyway

3. **Write the task summary** in `task-{id}.md`. Add a `## Summary` section:

```markdown
## Summary
- **What was done:** {Brief description of what was built/changed}
- **Key decisions:** {Any design decisions made during implementation}
- **Files created:** {list of new files}
- **Files modified:** {list of changed files}
- **Dependencies added:** {any new packages or modules}
```

4. **Update plan/reference.md.** Add a new entry under `## Modules` for each
   module created or significantly modified:

```markdown
### Module: {path/to/module.py} (Task {id})
- **Purpose:** {what this module does}
- **Key functions/classes:** {public API}
- **Decisions:** {why it was built this way}
- **Reuse:** {how other tasks can use this module}
```

   If the task modified an existing module, update that module's entry in
   reference.md rather than creating a duplicate.

5. **Update plan/plan.md.** Change the task's checkbox from `- [ ]` to `- [x]`:
   ```
   - [x] {id}. {Task title}
   ```

6. **Check `[x] completed`** in the task's Progress section.

7. **Clear Work in Progress** in `plan/plan.md`. Set the `## Work in Progress`
   section to empty (remove the filename).

8. **Report to the user:**
   - Summary of what was completed
   - What was added to reference.md
   - How many tasks remain in plan.md
   - Suggest `/pp-task` or `/pp-next` for the next task, or note if the project
     is complete

## Key Principles

- reference.md entries must be concise and actionable (focus on reuse)
- Plan files must stay self-contained after updates
- The summary captures decisions for future context, not just what was done
