---
name: pp-next
description: PP orchestrator. Determines and executes the next step from plan/PIPELINE.md. Supports step, auto, and continue modes.
disable-model-invocation: true
---

# PP Next -- Orchestrator

Drive the project-specific PP pipeline from `plan/PIPELINE.md`.

## Mode Selection

- `/pp-next` -- step mode (default): show next stage, ask user to confirm
- `/pp-next auto` -- auto mode: execute stages automatically, pause at approval gates
- `/pp-next continue-task` -- continue mode: bypass approval gates until the current task is completed
- `/pp-next continue-all` -- continue mode: bypass approval gates until all remaining tasks are completed

Check user input after slash command:
- if it includes `continue-all`, use continue-all mode
- else if it includes `continue-task`, use continue-task mode
- else if it includes `auto`, use auto mode
- otherwise use step mode

Normalize the selected mode into downstream orchestration context:
- step -> `gate_policy: respect`, `commit_policy: optional`, `run_scope: step`
- auto -> `gate_policy: respect`, `commit_policy: optional`, `run_scope: task`
- continue-task -> `gate_policy: bypass`, `commit_policy: mandatory`, `run_scope: task`
- continue-all -> `gate_policy: bypass`, `commit_policy: mandatory`, `run_scope: project`

## Instructions

### Step 1: Derive Current State

1. **Check if `plan/` exists.** If not -> tell user to run `/pp-init`.

2. **Read `plan/plan.md`.** Determine:
   - Project has tasks or needs `/pp-plan`
   - Current `## Work in Progress` task file

3. **Read `plan/PIPELINE.md`.** If missing -> tell user to run `/pp-init` to
   migrate/generate pipeline config.

4. **Determine active stage:**
   - If no tasks -> state `needs-plan` (next action: `/pp-plan`)
   - If WIP empty and unchecked tasks remain -> state `needs-task` (next action: `/pp-task`)
   - If WIP task exists -> read its `## Progress` and find first unchecked stage ID
   - If all stage IDs are checked -> task pipeline is complete; move to next task
     (or project-complete if none remain)

### Step 2: Resolve Stage Metadata and Orchestration Policy

From `plan/PIPELINE.md` for current stage ID:
- `label`
- `actions` (one-or-many skills)
- `approval_gate`
- `auto_behavior`

Carry forward the normalized orchestration context for downstream skills:
- `gate_policy`
- `commit_policy`
- `run_scope`

If stage ID in task Progress is missing from pipeline stages, report config mismatch.

### Step 3: Execute (Step Mode)

Present state and ask:

```
PP Status: Task {id} - {title}
Current stage: {stage_id} ({label})
Next action(s): {skill list}

What would you like to do?
  [yes]           - Run this stage
  [skip]          - Mark this stage done and continue
  [replan]        - Revise project plan
  [auto]          - Switch to auto mode
  [continue-task] - Bypass approval gates until this task is completed
  [continue-all]  - Bypass approval gates until all tasks are completed
  [stop]          - Pause here
```

Then:
- **yes**: execute stage via `pp-stage-runner`
- **skip**: mark current stage ID `[x]` in task Progress, then re-derive state
- **replan**: follow `pp-plan`
- **auto**: switch to auto mode
- **continue-task**: switch to continue-task mode
- **continue-all**: switch to continue-all mode
- **stop**: exit cleanly

### Step 4: Execute (Automatic Modes)

1. Re-derive current state before each loop iteration.
2. If state is `needs-plan`, stop and tell the user to run `/pp-plan`.
3. If state is `needs-task`:
   - In `auto`, run `pp-task`, present the result, and ask for approval before continuing because the task-planned stage is approval-gated.
   - In `continue-task`, run `pp-task` to create/select the next task, treat that task as the target task, then continue until it is completed.
   - In `continue-all`, run `pp-task` to create/select the next task, then continue.
4. If current stage `auto_behavior: skip`, mark `[x]` and continue.
5. If `gate_policy: respect` and stage has `approval_gate: true`:
   - Execute stage
   - Present result
   - Ask for approval before continuing
6. If `gate_policy: respect` and stage has `approval_gate: false`, execute stage immediately and continue.
7. If `gate_policy: bypass`:
   - Ignore `approval_gate`
   - Execute the stage immediately
   - Preserve the normalized orchestration context when invoking downstream skills, especially `pp-done`
8. In every automatic mode, stop immediately and ask the user if a real decision is required, including:
   - re-plan/overwrite choice for an existing task file
   - design review, review, or test output that requires user judgment to proceed
   - commit conflict or any git state that cannot be resolved deterministically

### Step 5: After Each Stage

1. Verify the stage ID was checked `[x]` in task Progress.
2. Re-derive state.
3. In step mode: show next stage and ask again.
4. In auto mode: continue until a pause condition or project completion.
5. In continue-task mode:
   - continue until the target task reaches final completion and its `commit_policy: mandatory` commit succeeds
   - then stop cleanly
6. In continue-all mode:
   - if the active task is complete and unchecked tasks remain, continue to the next task
   - stop only on project completion or a pause condition

## Error Handling

- If action skill fails, report failure and stop the automatic flow.
- If pipeline config is missing/malformed, report exact issue and suggest `/pp-pipeline`.
- If task Progress and pipeline stage IDs diverge, report mismatch and suggest migration via `/pp-init`.
- If a run with `commit_policy: mandatory` reaches task completion but the required commit fails, stop and report `commit required`.
