---
name: pp-interface
description: Design the public interface/API for the current task before implementation. Updates task file.
disable-model-invocation: true
---

# PP Interface

Design the public interface/API for the current task before writing implementation.

## Instructions

1. **Find the active task.** Read the `## Work in Progress` section in `plan/plan.md`
   to get the current task filename. Read that file from `plan/`. If WIP is empty,
   tell the user to run `/pp-task` first.

2. **Read context:**
   - Active `plan/task-{id}.md` (objective, acceptance criteria, dependencies)
   - `plan/reference.md` (existing modules/APIs for reuse)
   - `plan/language.md` (language/toolchain constraints)
   - Relevant source files mentioned in "Files to Touch"

3. **Design the interface.** Based on task requirements, propose:
   - Public function/method signatures with parameter and return types
   - Class/module interfaces where applicable
   - CLI arguments or config schema where applicable
   - Data contracts and relationships

   Focus on PUBLIC API only: what other modules/components will call.

4. **Check for reuse.** Cross-reference with reference.md:
   - Can existing modules be extended instead of creating new ones?
   - Are there existing data contracts to reuse?
   - Can utilities be generalized for this use case?

5. **Write the interface** into `## Interface` section of `task-{id}.md`:

```markdown
## Interface

### {path/to/module-or-file.ext}

\```text
{Public signatures / command schema / config contract}
\```

### Reuse from existing modules
- Uses `{module}` from Task {n} for {purpose}
```

6. **Check `[x] interface-designed`** in task Progress.

7. **Present the interface** for user approval:
   - Proposed signatures/contracts
   - Existing code to reuse
   - Design decisions/trade-offs

8. **Wait for approval.** User may approve, request changes, or ask alternatives.

9. **After approval**, tell user to run `/pp-implement` or `/pp-next`.

## Key Principles

- Interface-first: define WHAT before HOW
- Reuse existing modules from reference.md
- Keep interface notation consistent with selected language profile
- Keep interfaces minimal; expose only what is needed
