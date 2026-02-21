---
name: pp-stage-runner
description: Execute one pipeline stage by running one-or-many skills declared in plan/PIPELINE.md.
disable-model-invocation: true
---

# PP Stage Runner

Run a single stage from `plan/PIPELINE.md` by executing its action skills in order.

## Instructions

1. **Inputs required:**
   - Stage ID to run
   - Active task file (from `plan/plan.md` Work in Progress)

2. **Load pipeline config.** Read `plan/PIPELINE.md` and find the target stage.
   If not found, report an error.

3. **Validate stage config:**
   - `actions` exists and has at least one entry
   - Every action has `skill: pp-*`

4. **Execute actions in order:**
   - For each action `skill`, read that skill's `SKILL.md` and execute it inline
   - Stop at first failure
   - Report which action failed and why

5. **Post-run validation:**
   - Confirm target stage ID is checked `[x]` in active task `## Progress`
   - If not checked, report mismatch and stop

6. **Return result:**
   - Success/failure
   - Skills executed
   - Any blockers for the next stage

## Notes

- This skill is an internal orchestration primitive used by `/pp-next`.
- It does not choose the next stage; it only executes the stage it is given.
