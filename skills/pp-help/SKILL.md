---
name: pp-help
description: Display the complete PP workflow guide, available commands, and usage instructions.
disable-model-invocation: true
---

# PP Help

Display the PP (Project Planning & Implementing) workflow guide.

## Instructions

Print the following guide to the user:

---

**PP -- Project Planning & Implementing**

A human-guided project lifecycle managed through project-local skills and a
project-specific pipeline in `plan/PIPELINE.md`.

### Quick Start

1. `/pp-init <language>` -- scaffold or migrate project planning files
2. `/pp-arch-catalog` -- **Legacy only** - bootstrap architecture documentation for an existing project once.
3. `/pp-plan` -- create or revise the task plan
4. `/pp-next` -- run the next stage from the pipeline, repeat this stage until done.

`<language>` supports: `python`, `arduino` (`py` alias supported).

### Available Commands

| Command | Purpose |
|---------|---------|
| `/pp-init <language>` | Scaffold/migrate `plan/` files and the full architecture baseline |
| `/pp-plan` | Create or revise project task list |
| `/pp-task` | Plan next task, create full `task-{id}.md` spec (subtasks, drafts, architecture updates; no architecture bootstrap) |
| `/pp-design-review` | Review and gate task spec before implementation |
| `/pp-implement` | Implement active task and own ongoing architecture doc updates |
| `/pp-code-review` | Review implementation code and artifacts |
| `/pp-test` | Create and run minimal verification |
| `/pp-commit` | Create a focused task commit |
| `/pp-done` | Finalize task docs, patch catalog deltas, mark task done, and own task-end commit policy |
| `/pp-pipeline` | Validate and summarize pipeline config |
| `/pp-pipeline-edit` | Edit pipeline config (wizard), or use `summary` / `print` modes |
| `/pp-todo` | Add/list future-reference TODO items in `plan/todo.md` (not pipeline-driven) |
| `/pp-arch-catalog` | Bootstrap legacy repo architecture/catalog artifacts once |
| `/pp-next` | Orchestrator based on `PIPELINE.md` |
| `/pp-next auto` | Auto-advance with per-stage gate rules |
| `/pp-next continue-task` | Bypass approval gates until the current task is completed |
| `/pp-next continue-all` | Bypass approval gates until all remaining tasks are completed |
| `/pp-status` | Show project and active stage status |
| `/pp-help` | Show this guide |

### Pipeline-Driven Workflow

`/pp-next` uses ordered stages in `plan/PIPELINE.md`.
Default pipeline:

`task-planned -> design-reviewed -> implemented -> code-reviewed -> tested -> completed`

Projects can customize stage order, approval gates, and auto-skip behavior in
`plan/PIPELINE.md`.

### `/pp-next` Controls

In **step mode** (`/pp-next`), the orchestrator prompts for:

- `yes` -- run the current stage actions
- `skip` -- mark current stage as complete and move on
- `replan` -- run `/pp-plan` to revise tasks
- `auto` -- switch to auto mode
- `continue-task` -- bypass approval gates until the current task is completed
- `continue-all` -- bypass approval gates until all remaining tasks are completed
- `stop` -- pause orchestration

In **auto mode** (`/pp-next auto`):

- Stages with `auto_behavior: skip` are auto-marked complete
- Stages with `approval_gate: true` pause for approval before continuing
- Stages with `approval_gate: false` continue automatically

In **continue modes**:

- `/pp-next continue-task` runs the current workflow to the end of one task
- `/pp-next continue-all` continues across tasks until the project is complete
- Both modes still honor `auto_behavior: skip`
- Both modes ignore `approval_gate`
- Both modes stop and ask the user if a real decision is required
- End-of-task git commit is mandatory only in continue modes, and `pp-done` owns that policy
- Internally, `/pp-next` passes normalized orchestration policy to downstream skills instead of requiring them to infer behavior from command names
- In automatic modes, any stage that does not mark itself complete causes orchestration to pause and surface the blocker

### Approval Gates

Approval is per stage via `approval_gate: true|false` in `plan/PIPELINE.md`.
`approval_gate` is honored by `/pp-next auto` and step-mode prompts; it is ignored by the continue modes.

### Pipeline Editing

- `/pp-pipeline-edit` starts a guided edit wizard with preview before apply.
- `/pp-pipeline-edit summary` prints stage summary (`id`, `label`, gate, auto, actions).
- `/pp-pipeline-edit print` prints raw `plan/PIPELINE.md`.
- Structural edits migrate only the active task (from Work in Progress). If none
  is active, pipeline is edited without task migration.

### Plan Files

- `plan/plan.md` -- task list and active task pointer
- `plan/PIPELINE.md` -- ordered stage config (source of truth for workflow)
- `plan/language.md` -- language/toolchain profile
- `plan/task-{id}.md` -- task plan and stage progress
- `plan/AGENTS.md` -- coding standards
- `docs/catalog/architecture-code-catalog.md` -- generated architecture/code catalog
- `docs/architecture/` -- architecture artifacts and planned updates

---
