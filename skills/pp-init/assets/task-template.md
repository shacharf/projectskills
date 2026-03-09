# Task {ID}: {TITLE}

## Objective
{What this task accomplishes.}

## Subtasks
- [ ] {Subtask 1}
- [ ] {Subtask 2}

## Acceptance Criteria
- {Criterion 1}
- {Criterion 2}

## Dependencies
- {What prior work or modules this task depends on. Reference docs/catalog/architecture-code-catalog.md.}

## Reuse Analysis
- Catalog references: `docs/catalog/architecture-code-catalog.md#...`
- Architecture references: `docs/architecture/...`
- Reuse candidates:
  - `{module-or-contract}`: {reuse/extend reason}
- No-reuse rationale: {Required if no reuse candidates are selected}

## Reuse Plan
- Reuse `{existing module}` for {purpose}
- Extend `{existing contract}` in {file}
- Do not create new module for {behavior} without explicit rationale

## Architecture Impact
- Level: {none|low|medium|high}
- Summary: {What boundaries/contracts change.}

## Required Architecture Artifacts
- ADR: {required|not required} -- {why}
- Sequence Diagram: {required|not required} -- {why}
- C4 / System Map: {required|not required} -- {why}

## ADR Plan
- File: `docs/architecture/adrs/ADR-xxxx-title.md`
- Decision scope: {what decision this task changes or introduces}

## Sequence Plan
- File: `docs/architecture/sequences/{workflow}.md`
- Workflow scope: {what interaction flow this task changes or introduces}

## Planned Architecture Updates
- `docs/architecture/system-map.yaml`: {planned update}
- `docs/architecture/README.md`: {planned update}
- `docs/architecture/adrs/...`: {planned update}
- `docs/architecture/sequences/...`: {planned update}

## Files to Touch
- Create: `path/to/new/file.ext`
- Modify: `path/to/existing/file.ext`
- Test: `path/to/test-or-check.ext`
- Architecture: `docs/architecture/...`

## Interface Draft
{Draft public signatures/contracts. Reviewed by pp-design-review.}

## Data Structures Draft
{Draft schemas/models/contracts. Reviewed by pp-design-review.}

## Design Review Notes
{Filled by pp-design-review.}

## Progress
{Generated from plan/PIPELINE.md stage IDs by pp-task.}
