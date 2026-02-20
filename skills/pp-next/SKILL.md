---
name: pp-next
description: PP orchestrator. Determines and executes the next step in the project lifecycle. Supports step and auto modes.
disable-model-invocation: true
---

# PP Next -- Orchestrator

Drive the PP pipeline. Determine the next step and either ask for confirmation
(step mode) or auto-advance (auto mode).

## Mode Selection

- `/pp-next` -- step mode (default): show next step, ask user to confirm
- `/pp-next auto` -- auto mode: execute steps automatically, pause at approval gates

Check the user's input after the slash command. If they typed "auto" (or similar),
use auto mode. Otherwise use step mode.

## Instructions

### Step 1: Derive Current State

Read `plan/plan.md` to determine where we are:

1. **Check if plan/ exists.** If not → tell user to run `/pp-init`.

2. **Read plan/plan.md.** Check if it has a `## Tasks` section with entries.
   - No tasks → state is **needs-plan**. Next action: `/pp-plan`.

3. **Read the `## Work in Progress` section** in plan.md.
   - If it contains a filename (e.g., `task-3.md`) → read `plan/{filename}`.
     The first unchecked `[ ]` item in its `## Progress` section is the **current step**.
   - If WIP is empty (blank or contains `none`):
     - Find the first `- [ ]` task in the `## Tasks` list.
     - If found → state is **needs-task**. Next action: `/pp-task`.
     - If all tasks are `[x]` → state is **project-complete**.

### Step 2: Map Progress Item to Skill

| Progress Item | Skill to Run | Approval Gate? |
|---------------|-------------|----------------|
| task planned | pp-task | Yes |
| interface designed | pp-interface | Yes |
| implemented | pp-implement | No |
| reviewed | pp-review | No (skippable) |
| tested | pp-test | No |
| completed | pp-done | No |

Special states:
- **needs-plan** → pp-plan (approval gate: yes)
- **needs-task** → pp-task (approval gate: yes)
- **project-complete** → congratulate user, suggest `/pp-plan` to add more tasks

### Step 3: Execute (Step Mode)

In step mode, present the state and ask the user:

```
PP Status: Task {id} - {title}
Current step: {step name}
Next action: /pp-{skill}

What would you like to do?
  [yes]    - Run this step
  [skip]   - Skip to the next step
  [replan] - Revise the project plan
  [auto]   - Switch to auto mode
  [stop]   - Pause here
```

Use the AskQuestion tool with these options. Then:

- **yes**: Execute the corresponding skill's instructions inline (read the skill's
  SKILL.md and follow its instructions).
- **skip**: Mark the current progress item as `[x]` in the task file and re-derive
  state. Then present the next step.
- **replan**: Follow the pp-plan skill instructions to revise plan.md.
- **auto**: Switch to auto mode (see below).
- **stop**: Tell the user they can resume later with `/pp-next`.

### Step 4: Execute (Auto Mode)

In auto mode, execute steps sequentially without asking, EXCEPT at approval gates:

1. Determine next step (same as step mode)
2. If the step has an **approval gate** (pp-plan, pp-task, pp-interface):
   - Execute the skill
   - Present the result to the user
   - Ask for approval before continuing
3. If the step has **no approval gate** (pp-implement, pp-review, pp-test, pp-done):
   - Execute the skill immediately
   - Report the result
   - Continue to the next step
4. **pp-review is auto-skipped** in auto mode: mark `[x] reviewed` and continue.
5. After pp-done completes, check if more tasks remain. If yes, continue with
   pp-task for the next one. If no, report project complete.

### Step 5: After Each Step

After executing any step:
1. Verify the progress item was checked `[x]` in the task file
2. Re-derive state for the next iteration
3. In step mode: present the next step and ask again
4. In auto mode: continue to the next step

## Error Handling

- If a step fails (e.g., test fails), report the failure and switch to step mode
  so the user can decide how to proceed.
- If plan files are missing or malformed, report the issue and suggest `/pp-init`
  or manual fixes.
