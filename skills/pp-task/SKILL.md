---
name: pp-task
description: Select and plan the next task from plan.md, creating a detailed task-{id}.md file with pipeline-driven progress.
disable-model-invocation: true
---

# PP Task

Select the next incomplete task from plan.md and create a detailed task plan.

## Instructions

1. **Read `plan/plan.md`.** Find the first `- [ ]` task entry. Extract ID and title.

2. **Read project context:**
   - `plan/reference.md`
   - `plan/language.md`
   - `plan/AGENTS.md`
   - `plan/PIPELINE.md` (required for Progress stage IDs)

3. **Check for existing task files.** If `plan/task-{id}.md` exists, ask whether to re-plan.

4. **Read relevant code** based on task description and reference.md.

5. **Build Progress checklist from pipeline stages:**
   - Use ordered `id` values from `plan/PIPELINE.md`
   - Mark only the first stage (`task-planned` in default pipeline) as `[x]`
   - Mark all later stages as `[ ]`

6. **Create `plan/task-{id}.md`** using this structure:

```markdown
# Task {id}: {Title}

## Objective
{Clear statement of what this task accomplishes. 2-3 sentences.}

## Acceptance Criteria
- {Specific, testable criterion}
- {Another criterion}

## Dependencies
- {Prior tasks/modules this depends on}

## Files to Touch
- Create: `path/to/new/file.ext`
- Modify: `path/to/existing/file.ext`
- Test: `path/to/test-or-check.ext`

## Interface
{Filled by pp-interface.}

## Progress
- [x] {first-stage-id}
- [ ] {next-stage-id}
- [ ] ...
```

7. **Present the task plan** for approval.

8. **Set Work in Progress** in `plan/plan.md` to `task-{id}.md`.

9. **After approval**, suggest `/pp-next` (or direct stage skill).

## Key Principles

- Task file progress must match pipeline stage IDs exactly
- Acceptance criteria must be testable
- Always check reference.md for reuse opportunities
- Keep task scope focused and self-contained
