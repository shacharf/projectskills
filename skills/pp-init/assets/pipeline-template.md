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

- id: interface-designed
  label: Interface Designed
  actions:
    - skill: pp-interface
  approval_gate: true
  auto_behavior: run

- id: implemented
  label: Implemented
  actions:
    - skill: pp-implement
  approval_gate: false
  auto_behavior: run

- id: reviewed
  label: Reviewed
  actions:
    - skill: pp-review
  approval_gate: false
  auto_behavior: skip

- id: tested
  label: Tested
  actions:
    - skill: pp-test
  approval_gate: false
  auto_behavior: run

- id: committed
  label: Committed
  actions:
    - skill: pp-commit
  approval_gate: false
  auto_behavior: run

- id: completed
  label: Completed
  actions:
    - skill: pp-done
  approval_gate: false
  auto_behavior: run
