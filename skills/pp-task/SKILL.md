---
name: pp-task
description: Select and plan the next task from plan.md, creating a detailed task-{id}.md file.
disable-model-invocation: true
---

# PP Task

Select the next incomplete task from plan.md and create a detailed task plan.

## Instructions

1. **Read `plan/plan.md`.** Find the first `- [ ]` task entry. Extract ID and title.

2. **Read project context:**
   - `plan/reference.md` for existing modules and reuse opportunities
   - `plan/language.md` for language/toolchain constraints
   - `plan/AGENTS.md` for coding and testing standards

3. **Check for existing task files.** If `plan/task-{id}.md` already exists,
   tell the user and ask whether to re-plan it.

4. **Read relevant code.** Based on task description and reference.md, identify
   and read likely impacted source files. Use `pp-researcher` for deep exploration
   in larger codebases.

5. **Create `plan/task-{id}.md`** using this structure:

```markdown
# Task {id}: {Title}

## Objective
{Clear statement of what this task accomplishes. 2-3 sentences.}

## Acceptance Criteria
- {Specific, testable criterion}
- {Another criterion}
- ...

## Dependencies
- {Prior tasks/modules this depends on}
- {Reference specific modules from reference.md}

## Files to Touch
- Create: `path/to/new/file.ext`
- Modify: `path/to/existing/file.ext`
- Test: `path/to/test-or-check.ext`

## Interface Sketch
{Brief public API/contract this task will create. Details filled by pp-interface.}

## Progress
- [x] task planned
- [ ] interface designed
- [ ] implemented
- [ ] reviewed
- [ ] tested
- [ ] completed
```

6. **Mark "task planned" as `[x]`** in Progress.

7. **Present the task plan** for approval. User may approve, request changes,
   or choose a different task.

8. **Set Work in Progress** in `plan/plan.md` to the task filename (e.g. `task-3.md`).

9. **After approval**, tell user to run `/pp-interface` or `/pp-next`.

## Key Principles

- Keep tasks scoped: one coherent unit of work
- Acceptance criteria must be specific and testable
- Always check reference.md for reuse opportunities
- Respect language/profile constraints in task shaping
- Task file must be self-contained for implementer
