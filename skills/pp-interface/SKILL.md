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
   - The active `plan/task-{id}.md` (objective, acceptance criteria, dependencies)
   - `plan/reference.md` (existing modules and their APIs for reuse)
   - Relevant source files mentioned in the task's "Files to Touch" section

3. **Design the interface.** Based on the task requirements, propose:
   - Function signatures with type hints and docstrings
   - Class interfaces (if applicable)
   - CLI arguments or config schema (if applicable)
   - Data structures and their relationships

   Focus on the PUBLIC API only -- what other modules will call. Internal
   implementation details come later.

4. **Check for reuse.** Cross-reference with reference.md:
   - Can existing modules be extended rather than creating new ones?
   - Are there existing data structures to reuse?
   - Can existing utilities be generalized to cover this use case?

5. **Write the interface** into the `## Interface` section of `task-{id}.md`:

```markdown
## Interface

### {module_name}.py

\```python
def function_name(param: Type, param2: Type) -> ReturnType:
    """One-line description.

    Args:
        param: What this is.
        param2: What this is.

    Returns:
        What this returns.
    """
    ...
\```

### Reuse from existing modules
- Uses `{module}` from Task {n} for {purpose}
```

6. **Check `[x] interface designed`** in the task's Progress section.

7. **Present the interface** to the user for approval. Show:
   - The proposed signatures
   - What existing code will be reused
   - Any design decisions and trade-offs

8. **Wait for approval.** The user may:
   - Approve as-is
   - Request changes (revise and re-present)
   - Ask for alternative approaches

9. **After approval**, tell the user to run `/pp-implement` or `/pp-next`.

## Key Principles

- Interface-first: define WHAT before HOW
- Reuse existing modules from reference.md
- Type hints on everything
- Docstrings on all public functions
- Keep interfaces minimal -- expose only what's needed
