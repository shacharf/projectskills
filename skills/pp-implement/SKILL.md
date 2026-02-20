---
name: pp-implement
description: Implement the current task following the approved interface. Updates task progress.
disable-model-invocation: true
---

# PP Implement

Implement the current task's modules following the approved interface.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user to run `/pp-task` first.

2. **Read all context:**
   - `plan/task-{id}.md` -- full task plan including approved interface
   - `plan/reference.md` -- existing modules, APIs, reuse notes
   - `plan/language.md` -- language/toolchain profile for this project
   - `plan/AGENTS.md` -- coding standards for the selected language
   - Source files listed in "Files to Touch"
   - Any existing code that the interface references for reuse

3. **Implement the code:**
   - Follow approved interface signatures exactly
   - Follow `plan/AGENTS.md` standards
   - Prefer established ecosystem libraries/packages where appropriate
   - Reuse existing project modules referenced in the interface
   - If duplicated code is found, generalize into a shared utility

4. **Create/modify files** as specified in "Files to Touch":
   - New files: create with correct module/file structure for the language profile
   - Modified files: make targeted changes, preserve existing functionality
   - Update exports/imports/build wiring as needed

5. **Handle dependencies and config:**
   - If new dependencies are needed, update the project's existing dependency mechanism
   - Update configuration/build files when task requirements need it

6. **Check `[x] implemented`** in the task's Progress section.

7. **Report to the user:**
   - List files created/modified
   - Summarize what was implemented
   - Note any deviations from interface or open questions
   - Suggest `/pp-review` or `/pp-test` next (or `/pp-next`)

## Key Principles

- Follow the approved interface exactly
- Reuse, don't duplicate
- Respect language profile + project coding standards
- Keep modules/files focused on one responsibility
- Fail fast on invalid input with clear error messages
