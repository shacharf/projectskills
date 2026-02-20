---
name: pp-help
description: Display the complete PP workflow guide, available commands, and usage instructions.
disable-model-invocation: true
---

# PP Help

Display the PP (Project Planning & Implementing) workflow guide to the user.

## Instructions

Print the following guide to the user:

---

**PP -- Project Planning & Implementing**

A human-gated project lifecycle managed through Cursor skills.

### Quick Start

1. `/pp-init <language>` -- scaffold a new project (creates `plan/` with templates)
2. `/pp-plan` -- brainstorm and create the project plan
3. `/pp-next` -- advance to the next step (the orchestrator)

`<language>` supports: `python`, `arduino` (`py` alias supported). If omitted,
`/pp-init` prompts for language.

### Available Commands

| Command | Purpose |
|---------|---------|
| `/pp-init <language>` | Scaffold project: creates `plan/plan.md`, `reference.md`, `language.md`, `AGENTS.md` |
| `/pp-plan` | Create or revise the project plan through brainstorming |
| `/pp-task` | Plan the next task from plan.md, create `task-{id}.md` |
| `/pp-interface` | Design the public interface/API for the current task |
| `/pp-implement` | Implement the current task |
| `/pp-review` | Review the implementation (optional) |
| `/pp-test` | Create and run a minimal test/check |
| `/pp-done` | Complete the task, update reference.md and plan.md |
| `/pp-next` | Orchestrator: determine and run the next step |
| `/pp-next auto` | Auto-advance through steps, pausing at approval gates |
| `/pp-status` | Show current project state |
| `/pp-help` | Show this guide |

### Workflow

```
pp-init → pp-plan → [approve] → pp-task → [approve] → pp-interface → [approve]
→ pp-implement → pp-review (optional) → pp-test → pp-done → pp-task (next) ...
```

### Orchestrator Modes

- **Step mode** (`/pp-next`): shows the next step, asks you to confirm
  - `yes` -- run this step
  - `skip` -- skip to next step
  - `replan` -- go back to planning
  - `auto` -- switch to auto mode
  - `stop` -- pause, resume later with `/pp-next`
- **Auto mode** (`/pp-next auto`): runs steps automatically, pausing at approval gates

### Approval Gates (always pause)

- After plan creation (pp-plan)
- After task planning (pp-task)
- After interface design (pp-interface)

### Replanning

Call `/pp-plan` at any time to revise the task list. Completed tasks stay checked.
Or say "replan" at any orchestrator prompt.

### Plan Files

- `plan/plan.md` -- task list with checkboxes (source of truth)
- `plan/reference.md` -- accumulated project knowledge
- `plan/language.md` -- selected language/toolchain profile
- `plan/task-{id}.md` -- current task plan and progress
- `plan/AGENTS.md` -- coding standards for selected language

---
