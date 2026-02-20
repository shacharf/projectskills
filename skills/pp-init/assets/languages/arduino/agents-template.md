# Coding Standards

## Language & Runtime
- Arduino C++ targeting Arduino boards
- Prefer standard Arduino core APIs and stable community libraries

## Style
- Keep naming descriptive and consistent with existing sketch/module style
- Keep functions short and focused
- Avoid dynamic allocation unless clearly necessary for the target board

## Architecture
- Keep the sketch responsibilities clear (`setup()` for initialization, `loop()` for runtime flow)
- Move reusable logic into `.h/.cpp` modules when sketch complexity grows
- Keep hardware pin mapping and board-specific constants centralized

## Code Reuse
- Prefer established Arduino libraries over hand-rolled protocol/device code
- Check `plan/reference.md` before adding new modules
- Consolidate repeated hardware or parsing logic into shared helpers

## Error Handling
- Validate hardware assumptions early during setup
- Emit actionable diagnostics through serial logging where possible
- Fail safe when peripherals are unavailable or misconfigured

## Documentation
- Document pin mappings, board assumptions, and external wiring dependencies
- Keep task and reference docs self-contained for future contributors

## Testing
- Per-task verification should include compile validation and one focused behavior check
- Tests/checks should be runnable with a single command when possible
