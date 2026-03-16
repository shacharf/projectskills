---
name: pp-code-review
description: Review the implementation of the current task against acceptance criteria and coding standards.
disable-model-invocation: true
---

# PP Code Review

Review the implementation of the current task. This stage is read-only. If
issues are found, report them and leave the stage incomplete.

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

3. **Perform the review directly in this stage.** The review should check:

   - **Correctness:** Does the implementation satisfy all acceptance criteria?
   - **Interface compliance:** Does the code match the approved interface?
   - **Coding standards:** Does it follow AGENTS.md conventions?
   - **Reuse:** Are there missed opportunities to reuse existing code?
     Prioritize gaps against the task's approved `## Reuse Plan`.
   - **Architecture artifact completion:** Were required ADR and sequence files actually updated?
   - **Architecture compatibility:** Are ADR, sequence, C4, and system-map changes consistent with the implementation?
   - **Architecture ownership:** Were architecture mutations made through normal implementation work, not delegated to `pp-arch-catalog`?
   - **Artifact indexing:** If new ADR or sequence files were created, were the matching index files updated?
   - **C4 targeting:** Was the correct C4 file updated for the type of change?
   - **Edge cases:** Are inputs validated? Are errors handled?
   - **API clarity:** Are public APIs well-named and documented?

4. **Present findings** to the user:
   - Final outcome: `pass` or `issues-found`
   - Issues found (if any), categorized by severity
   - Suggestions for improvement
   - Confirmation of what looks good

5. **Mark progress only on pass:**
   - If the outcome is `pass`, check `[x] code-reviewed` in the task's Progress section
   - If the outcome is `issues-found`, do not mark the stage complete

6. **Tell the user** what to do next:
   - If the outcome is `pass`, suggest `/pp-test` or `/pp-next`
   - If the outcome is `issues-found`, suggest `/pp-implement` or `/pp-next`

## If Review Finds Issues

If significant issues are found:
- List them clearly with file paths and line references
- Suggest specific fixes
- The user decides what to do next; do not continue automatically from this stage
- Do NOT automatically modify code during review -- just report findings
- Do NOT mark `code-reviewed` complete
