---
name: pp-todo
description: Add or list lightweight future-reference TODO notes in plan/todo.md.
disable-model-invocation: true
---

# PP Todo

Maintain a simple TODO list for future reference only. This command is not
pipeline-driven and must not affect task planning or stage progress.

## Invocation Modes

- `/pp-todo` -> list TODO items
- `/pp-todo list` -> list TODO items
- `/pp-todo "text"` -> append a new TODO item

If the argument is exactly `list` or empty, run list mode.
Otherwise, treat the full argument as TODO text to append.

## Instructions

1. Check that `plan/` exists. If not, tell the user to run `/pp-init`.
2. Use `plan/todo.md` as the canonical TODO file.
3. If `plan/todo.md` does not exist, create it with:

```markdown
# TODO
```

4. **List mode:**
   - Print TODO items from `plan/todo.md`.
   - If there are no `- [ ]` items, print `No TODO items yet.`.
5. **Add mode:**
   - Validate text is not empty after trimming.
   - Append a new unchecked item:
     - `- [ ] {text}`
   - Confirm the item was added.
6. Never modify:
   - `plan/plan.md`
   - `plan/PIPELINE.md`
   - `plan/task-*.md`
   - `plan/reference.md`

## Output Style

- Keep responses concise.
- For list mode, show items in their file order.
- For add mode, echo the added text.
