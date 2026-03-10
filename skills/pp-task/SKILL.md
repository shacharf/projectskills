---
name: pp-task
description: Select and plan the next task from plan.md, creating a detailed task-{id}.md file with pipeline-driven progress.
disable-model-invocation: true
---

# PP Task

Select the next incomplete task from plan.md and create a decision-complete task
spec that includes subtasks, interface draft, data structures draft, and
planned architecture updates.

## Instructions

1. **Read `plan/plan.md`.** Find the first `- [ ]` task entry. Extract ID and title.

2. **Read project context:**
   - `docs/catalog/architecture-code-catalog.md`
   - `plan/language.md`
   - `plan/AGENTS.md`
   - `plan/PIPELINE.md` (required for Progress stage IDs)

3. **Check for existing task files.** If `plan/task-{id}.md` exists, ask whether to re-plan.

4. **Read relevant code** based on task description and the Architecture/Code Catalog.

5. **Read architecture context** from `docs/architecture/` when available:
   - `docs/architecture/README.md`
   - `docs/architecture/system-map.yaml`
   - Relevant C4 files (`c4-*.md`)
   - Relevant sequence docs (`sequences/*.md`)
   - ADR index/files (`adrs/*.md`)
   If missing, do not create/modify architecture files in this stage.
   Treat this as project setup drift. For new projects, instruct the user to rerun
   `/pp-init`; for legacy imports, use `/pp-arch-catalog` once.

6. **Build Progress checklist from pipeline stages:**
   - Use ordered `id` values from `plan/PIPELINE.md`
   - Mark only the first stage (`task-planned` in default pipeline) as `[x]`
   - Mark all later stages as `[ ]`

7. **Classify architecture impact** for this task:
   - `none`, `low`, `medium`, or `high`
   - If `low|medium|high`, identify affected architecture artifacts
   - Apply these defaults:
     - decision/tradeoff change -> ADR required
     - workflow/interaction change -> sequence diagram required
     - external actor/system boundary change -> `c4-context.md`
     - service/module/container boundary change -> `c4-container.md`
     - internal component relationship change -> `c4-components.md`
     - structural topology/component relationship change -> `system-map.yaml`

8. **Create `plan/task-{id}.md`** using this structure:

```markdown
# Task {id}: {Title}

## Objective
{Clear statement of what this task accomplishes. 2-3 sentences.}

## Subtasks
- [ ] {Subtask 1}
- [ ] {Subtask 2}

## Acceptance Criteria
- {Specific, testable criterion}
- {Another criterion}

## Dependencies
- {Prior tasks/modules this depends on}

## Reuse Analysis
- Catalog references: `{docs/catalog/architecture-code-catalog.md#section}`
- Architecture references: `{docs/architecture/...}`
- Reuse candidates:
  - `{module-or-contract}`: {reuse/extend reason}
- No-reuse rationale: {Required if no reuse candidates are selected}

## Reuse Plan
- Reuse `{existing module}` for {purpose}
- Extend `{existing contract}` in {file}
- Do not create new module for {behavior} unless rationale is documented above

## Architecture Impact
- Level: {none|low|medium|high}
- Summary: {What architectural boundaries/contracts are affected}

## Required Architecture Artifacts
- ADR: {required|not required} -- {why}
- Sequence Diagram: {required|not required} -- {why}
- C4 / System Map: {required|not required} -- {why}

## ADR Plan
- Action: {update existing | create new}
- File: `docs/architecture/adrs/ADR-xxxx-title.md`
- Decision scope: {what decision this task changes or introduces}
- Index update: {required|not required} -- `docs/architecture/adrs/README.md`

## Sequence Plan
- Action: {update existing | create new}
- File: `docs/architecture/sequences/{workflow-slug}.md`
- Workflow scope: {what interaction flow this task changes or introduces}
- Index update: {required|not required} -- `docs/architecture/sequences/README.md`

## Planned Architecture Updates
- `docs/architecture/system-map.yaml`: {planned change}
- `docs/architecture/README.md`: {planned change}
- `docs/architecture/adrs/...`: {planned change}
- `docs/architecture/sequences/...`: {planned change}
- `{other architecture file}`: {planned change}

## Files to Touch
- Create: `path/to/new/file.ext`
- Modify: `path/to/existing/file.ext`
- Test: `path/to/test-or-check.ext`
- Architecture: `docs/architecture/...`

## Interface Draft
{Public API draft for review by pp-design-review.}

## Data Structures Draft
{Schema/type/model draft for review by pp-design-review.}

## Design Review Notes
{Filled by pp-design-review.}

## Progress
- [x] {first-stage-id}
- [ ] {next-stage-id}
- [ ] ...
```

9. **Plan architecture ownership clearly** for this task:
   - `pp-task` must not edit `docs/architecture/*`.
   - `pp-implement` is the canonical owner of architecture artifact mutations.
   - For ADRs:
     - Prefer updating an existing ADR when the decision identity is unchanged.
     - Otherwise plan a new sequential file: `ADR-0001-title.md`, `ADR-0002-title.md`, ...
   - For sequences:
     - Use stable workflow slugs, not task IDs.
     - Example: `docs/architecture/sequences/user-login.md`
   - When a new ADR or sequence file is planned, also plan the matching index update.
   - Do not bootstrap missing C4/sequence/ADR files from `pp-task`.

10. **Present the task spec** for approval.

11. **Enforce reuse decision completeness** before finalizing task planning:
   - Task must include at least one concrete reuse candidate from catalog/docs, OR
   - A written explicit `No-reuse rationale` in `## Reuse Analysis`.
   - If neither exists, request revision and do not finalize.
   - If ADR or Sequence Diagram is marked `required`, `## Subtasks` must include
     concrete create/update entries for those files.
   - If `C4 / System Map` is marked `required`, `## Planned Architecture Updates`
     must name the exact C4/system-map files to be updated.

12. **Set Work in Progress** in `plan/plan.md` to `task-{id}.md`.

13. **After approval**, suggest `/pp-design-review` or `/pp-next`.

## Key Principles

- Task file progress must match pipeline stage IDs exactly
- `task-{id}.md` is the single source of truth for planning
- `pp-task` is the reuse decision authority for the task
- Task specs must be implementation-ready before code changes start
- Acceptance criteria must be testable
- Always check catalog + architecture docs for reuse opportunities
- Keep task scope focused and self-contained
- Architecture drift is handled as a soft warning at planning time
