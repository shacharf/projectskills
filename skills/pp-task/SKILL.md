---
name: pp-task
description: Select and plan the next task from plan.md, creating a detailed task-{id}.md file.
disable-model-invocation: true
---

# PP Task

Select the next incomplete task from plan.md and create a detailed task plan.

## Instructions

1. **Read plan/plan.md.** Find the first `- [ ]` task entry. Extract its ID number
   and title.

2. **Read plan/reference.md** to understand what has been built so far, what modules
   exist, and what can be reused.

3. **Check for existing task files.** If `plan/task-{id}.md` already exists for this
   task, tell the user and ask if they want to re-plan it.

4. **Read relevant code.** Based on the task description and reference.md, identify
   which source files are relevant. Read them to understand the current codebase state.
   Use the pp-researcher subagent for deeper exploration if the codebase is large.

5. **Create plan/task-{id}.md** using this structure:

```markdown
# Task {id}: {Title}

## Objective
{Clear statement of what this task accomplishes. 2-3 sentences.}

## Acceptance Criteria
- {Specific, testable criterion}
- {Another criterion}
- ...

## Dependencies
- {What prior tasks or modules this depends on}
- {Reference specific modules from reference.md}

## Files to Touch
- Create: `path/to/new/file.py`
- Modify: `path/to/existing/file.py`
- Test: `tests/path/to/test.py`

## Interface Sketch
{Brief description of the public API this task will create. Details filled by pp-interface.}

## Progress
- [x] task planned
- [ ] interface designed
- [ ] implemented
- [ ] reviewed
- [ ] tested
- [ ] completed
```

6. **Mark "task planned" as `[x]`** in the Progress checklist since we just did it.

7. **Present the task plan** to the user for approval. They may:
   - Approve as-is
   - Request changes to scope, criteria, or approach
   - Ask to pick a different task

8. **Set Work in Progress** in `plan/plan.md`. Update the `## Work in Progress`
   section to contain the new task filename (e.g., `task-3.md`).

9. **After approval**, tell the user to run `/pp-interface` or `/pp-next` to
   design the interface.

## Key Principles

- Keep tasks scoped: one coherent unit of work
- Acceptance criteria must be specific and testable
- Always check reference.md for reuse opportunities
- The task file must be self-contained for the implementer
