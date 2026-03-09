---
name: pp-review
description: Review the implementation of the current task against acceptance criteria and coding standards.
disable-model-invocation: true
---

# PP Review

Review the implementation of the current task. This step is optional and can be
skipped in auto mode.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user to run `/pp-task` first.

2. **Read context:**
   - `plan/task-{id}.md` -- acceptance criteria and approved interface
   - `plan/AGENTS.md` -- coding standards
   - `docs/catalog/architecture-code-catalog.md` -- existing patterns to check consistency against
   - Architecture artifacts referenced by the task (`ADR Plan`, `Sequence Plan`, planned updates)
   - All source files created or modified by the implementation

3. **Dispatch the code-reviewer.** Use the `requesting-code-review` skill to
   dispatch the built-in code-reviewer subagent. The review should check:

   - **Correctness:** Does the implementation satisfy all acceptance criteria?
   - **Interface compliance:** Does the code match the approved interface?
   - **Coding standards:** Does it follow AGENTS.md conventions?
   - **Reuse:** Are there missed opportunities to reuse existing code?
     Prioritize gaps against the task's approved `## Reuse Plan`.
   - **Architecture artifact completion:** Were required ADR and sequence files actually updated?
   - **Architecture compatibility:** Are ADR, sequence, C4, and system-map changes consistent with the implementation?
   - **Edge cases:** Are inputs validated? Are errors handled?
   - **API clarity:** Are public APIs well-named and documented?

4. **Present findings** to the user:
   - Issues found (if any), categorized by severity
   - Suggestions for improvement
   - Confirmation of what looks good

5. **Check `[x] reviewed`** in the task's Progress section.

6. **Tell the user** to run `/pp-test` or `/pp-next` next.

## If Review Finds Issues

If significant issues are found:
- List them clearly with file paths and line references
- Suggest specific fixes
- The user may choose to fix issues before proceeding, or proceed anyway
- Do NOT automatically modify code during review -- just report findings
