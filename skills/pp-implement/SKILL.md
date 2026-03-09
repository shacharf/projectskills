---
name: pp-implement
description: Implement the current task by executing planned subtasks and applying continuous architecture updates. Updates task progress.
disable-model-invocation: true
---

# PP Implement

Implement the current task by executing its planned subtasks, approved design,
and architecture updates.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user to run `/pp-task` first.

2. **Read all context:**
   - `plan/task-{id}.md` -- full task spec including subtasks and approved design
   - `docs/catalog/architecture-code-catalog.md` -- existing modules, APIs, reuse notes
   - `plan/language.md` -- language/toolchain profile for this project
   - `plan/AGENTS.md` -- coding standards for the selected language
   - Source files listed in "Files to Touch"
   - Architecture files listed in "Planned Architecture Updates"
   - Any existing code/contracts referenced by the task drafts

3. **Implement planned subtasks in order:**
   - Update subtask checkboxes in `task-{id}.md` as work is completed
   - Follow `## Reuse Plan`; do not perform fresh reuse discovery unless blocked
   - Follow approved interface and data structure decisions exactly
   - Follow `plan/AGENTS.md` standards
   - Prefer established ecosystem libraries/packages where appropriate
   - Reuse existing project modules referenced in the task spec
   - If duplicated code is found, generalize into a shared utility

4. **Create/modify files** as specified in "Files to Touch":
   - New files: create with correct module/file structure for the language profile
   - Modified files: make targeted changes, preserve existing functionality
   - Update exports/imports/build wiring as needed

5. **Apply architecture updates continuously:**
   - Update architecture docs as related subtasks land (do not defer all updates)
   - Keep `docs/architecture/system-map.yaml` synchronized with implemented changes
   - Update referenced C4/sequence/ADR docs from planned updates
   - Before completing stage, run a final architecture consistency pass against code

6. **Handle dependencies and config:**
   - If new dependencies are needed, update the project's existing dependency mechanism
   - Update configuration/build files when task requirements need it

7. **Check `[x] implemented`** in the task's Progress section.

8. **Report to the user:**
   - List files created/modified
   - Summarize completed subtasks
   - Confirm reused modules/contracts from `## Reuse Plan`
   - Summarize architecture files updated
   - Note any deviations from reviewed design or open questions
   - Suggest `/pp-review` or `/pp-test` next (or `/pp-next`)

## Key Principles

- Execute subtasks from the approved task spec
- Follow approved interface/data structure decisions exactly
- Reuse, don't duplicate
- Respect language profile + project coding standards
- Keep modules/files focused on one responsibility
- Keep architecture docs synchronized with implementation
- Fail fast on invalid input with clear error messages
