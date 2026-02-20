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
   - `plan/task-{id}.md` -- the full task plan including approved interface
   - `plan/reference.md` -- existing modules, their APIs, reuse notes
   - `plan/AGENTS.md` -- coding standards
   - Source files listed in "Files to Touch"
   - Any existing code that the interface references for reuse

3. **Implement the code:**
   - Follow the approved interface signatures exactly
   - Follow AGENTS.md coding standards
   - Use existing python packages over hand-rolling solutions
   - Reuse existing project modules referenced in the interface
   - If you find duplicated or similar code, generalize it into a shared utility

4. **Create/modify files** as specified in "Files to Touch":
   - New files: create with proper module structure, imports, type hints
   - Modified files: make targeted changes, preserve existing functionality
   - Update `__init__.py` or imports as needed

5. **Handle dependencies:**
   - If new packages are needed, add them to `requirements.txt` (or equivalent)
   - Update any configuration files if the task requires it

6. **Check `[x] implemented`** in the task's Progress section.

7. **Report to the user:**
   - List files created/modified
   - Summarize what was implemented
   - Note any deviations from the interface or open questions
   - Suggest running `/pp-review` or `/pp-test` next (or `/pp-next`)

## Key Principles

- Follow the approved interface exactly
- Reuse, don't duplicate
- Use existing python modules
- Keep modules focused: one responsibility per file
- Type hints on all function signatures
- Fail fast on invalid input with clear error messages
