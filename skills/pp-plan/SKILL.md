---
name: pp-plan
description: Create or revise the project plan through structured brainstorming. Writes plan/plan.md.
disable-model-invocation: true
---

# PP Plan

Create or revise the project plan through a structured brainstorming process.
This skill does its own brainstorming -- it does NOT delegate to external
brainstorming or writing-plans skills.

## Instructions

### Phase 1: Understand Context

1. **Read existing files** if they exist:
   - `plan/plan.md` (existing plan, if revising)
   - `plan/reference.md` (completed work, if any)
   - Any project description or requirements the user provides

2. **If this is a new plan** (plan.md has no tasks), ask the user:
   - "What are you building? Describe the project in a few sentences."
   - Wait for their response before proceeding.

3. **If this is a revision** (plan.md has tasks), show the current task list and ask:
   - "What would you like to change about the plan?"

### Phase 2: Research and Explore

4. **Ask clarifying questions** one at a time. Focus on:
   - What is the core functionality?
   - What are the constraints (language, framework, platform)?
   - What does success look like?
   - Are there existing codebases or APIs to integrate with?

   Use the AskQuestion tool for structured questions when possible.
   Ask a maximum of 3-5 questions total -- don't over-interrogate.

5. **Research if needed.** If the project involves unfamiliar technology or APIs,
   use web search (parallel-web-search skill) to gather relevant information.

### Phase 3: Propose the Plan

6. **Propose 2-3 approaches** if there are meaningful architectural choices.
   Keep this brief -- a few sentences per approach with trade-offs and your
   recommendation. Skip this if the architecture is straightforward.

7. **Write the task list.** Break the project into ordered tasks where:
   - Each task is a coherent unit of work (half-day to 2 days)
   - Tasks are ordered by dependency (build foundations first)
   - Each task description is specific enough to act on
   - The list is complete enough to deliver the project

8. **Present the plan** to the user for approval. Show:
   - Brief overview (2-3 sentences)
   - The numbered task list
   - Any risks or open questions

### Phase 4: Finalize

9. **Wait for human approval.** The user may:
   - Approve as-is
   - Request changes (revise and re-present)
   - Add/remove/reorder tasks

10. **Write plan/plan.md** with the approved content:

```markdown
# {Project Name}

## Overview
{2-3 sentence project description}

## Tasks
- [ ] 1. {Task title}: {one-line description}
- [ ] 2. {Task title}: {one-line description}
...
```

11. **Preserve completed tasks.** If revising an existing plan, keep any `[x]`
    tasks as-is. Only modify incomplete tasks.

12. **Tell the user** to run `/pp-task` or `/pp-next` to start the first task.

## Key Principles

- Keep the plan concise -- task titles + one-line descriptions, not paragraphs
- Order tasks by dependency and logical progression
- Each task should be independently testable
- The plan must be self-contained: anyone reading it can understand the project
