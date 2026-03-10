---
name: pp-design-review
description: Review and iterate the active task spec as a hard gate before implementation, covering interface, data structures, subtasks, and architecture updates.
disable-model-invocation: true
---

# PP Design Review

Review the active `task-{id}.md` and either approve it for implementation or
return required changes.

## Instructions

1. **Find the active task.** Read `## Work in Progress` in `plan/plan.md` and
   load that `plan/task-{id}.md`. If WIP is empty, tell user to run `/pp-task`.

2. **Read full design context:**
   - Active task file (all sections)
   - `docs/catalog/architecture-code-catalog.md`
   - `plan/language.md`
   - `plan/AGENTS.md`
   - Architecture docs referenced by the task under `docs/architecture/`

3. **Evaluate design quality as a gate:**
   - Subtasks are ordered, coherent, and sufficient for delivery
   - Reuse analysis and reuse plan are complete and actionable
   - Interface draft is clear and implementable
   - Data structures draft is consistent with interface and constraints
   - Planned architecture updates are explicit and scoped
   - Required ADR and sequence work is represented as explicit subtasks when applicable
   - ADR plans use a concrete sequential file target or an existing ADR file
   - Sequence plans use a stable workflow-slug file name, not a task-specific name
   - Acceptance criteria are testable and map to planned work

4. **Cross-check architecture consistency:**
   - Task interface/data changes align with `system-map.yaml`
   - Required C4/sequence/ADR updates are present in planned updates
   - C4 file selection matches the change type:
     - external boundary -> `c4-context.md`
     - container/module boundary -> `c4-container.md`
     - internal component relationship -> `c4-components.md`
     - topology relationship -> `system-map.yaml`
   - `Required Architecture Artifacts`, `ADR Plan`, and `Sequence Plan` are internally consistent
   - Missing artifacts are called out explicitly

5. **Produce one of two outcomes:**
   - **Pass**: write concise approval notes into `## Design Review Notes`
   - **Changes requested**: write an actionable remediation checklist into
     `## Design Review Notes`

6. **If pass, check `[x] design-reviewed`** in task Progress.
   If changes are requested, keep stage unchecked.

7. **Present the decision**:
   - `pass` with key confirmations, or
   - `changes requested` with exact required edits before rerun

8. **Next step guidance:**
   - If pass: suggest `/pp-implement` or `/pp-next`
   - If changes requested: suggest `/pp-task` (re-plan) then rerun review

## Key Principles

- Hard gate before implementation
- No silent approvals
- Require alignment across subtasks, interface, data models, and architecture
- Keep review notes short, explicit, and actionable
