---
name: pp-next
description: PP orchestrator. Determines and executes the next step from plan/PIPELINE.md. Supports step and auto modes.
disable-model-invocation: true
---

# PP Next -- Orchestrator

Drive the project-specific PP pipeline from `plan/PIPELINE.md`.

## Mode Selection

- `/pp-next` -- step mode (default): show next stage, ask user to confirm
- `/pp-next auto` -- auto mode: execute stages automatically, pause at approval gates

Check user input after slash command. If it includes `auto`, use auto mode.

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

### Step 2: Resolve Stage Metadata

From `plan/PIPELINE.md` for current stage ID:
- `label`
- `actions` (one-or-many skills)
- `approval_gate`
- `auto_behavior`

If stage ID in task Progress is missing from pipeline stages, report config mismatch.

### Step 3: Execute (Step Mode)

Present state and ask:

```
PP Status: Task {id} - {title}
Current stage: {stage_id} ({label})
Next action(s): {skill list}

What would you like to do?
  [yes]    - Run this stage
  [skip]   - Mark this stage done and continue
  [replan] - Revise project plan
  [auto]   - Switch to auto mode
  [stop]   - Pause here
```

Then:
- **yes**: execute stage via `pp-stage-runner`
- **skip**: mark current stage ID `[x]` in task Progress, then re-derive state
- **replan**: follow `pp-plan`
- **auto**: switch to auto mode
- **stop**: exit cleanly

### Step 4: Execute (Auto Mode)

1. Determine next stage.
2. If stage `auto_behavior: skip`, mark `[x]` and continue.
3. If stage has `approval_gate: true`:
   - Execute stage
   - Present result
   - Ask for approval before continuing
4. If stage has `approval_gate: false`:
   - Execute stage immediately
   - Continue to next stage

### Step 5: After Each Stage

1. Verify the stage ID was checked `[x]` in task Progress.
2. Re-derive state.
3. In step mode: show next stage and ask again.
4. In auto mode: continue until pause condition or project completion.

## Error Handling

- If action skill fails, report failure and switch to step mode.
- If pipeline config is missing/malformed, report exact issue and suggest `/pp-pipeline`.
- If task Progress and pipeline stage IDs diverge, report mismatch and suggest migration via `/pp-init`.
