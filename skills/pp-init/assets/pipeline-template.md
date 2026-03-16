# Pipeline
version: 1

## Defaults
mode: step
on_error: pause

## Stages
- id: task-planned
  label: Task Planned
  actions:
    - skill: pp-task
  approval_gate: true
  auto_behavior: run

- id: design-reviewed
  label: Design Reviewed
  actions:
    - skill: pp-design-review
  approval_gate: true
  auto_behavior: run

- id: implemented
  label: Implemented
  actions:
    - skill: pp-implement
  approval_gate: false
  auto_behavior: run

- id: code-reviewed
  label: Code Reviewed
  actions:
    - skill: pp-code-review
  approval_gate: false
  auto_behavior: run

- id: tested
  label: Tested
  actions:
    - skill: pp-test
  approval_gate: false
  auto_behavior: run

- id: completed
  label: Completed
  actions:
    - skill: pp-done
  approval_gate: false
  auto_behavior: run
