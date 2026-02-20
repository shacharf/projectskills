# Language Profile

Language: arduino

## Runtime / Toolchain
- Arduino C++
- CLI baseline: `arduino-cli`

## Build / Test Defaults
- Validate by compiling the sketch with `arduino-cli compile`
- When hardware is available, validate behavior with a focused smoke check (serial output, sensor read, actuator command)

## File Conventions
- Primary sketch entrypoint: `.ino`
- Additional modules: `.h/.cpp`

## Dependency Conventions
- Use Arduino Library Manager libraries where possible
- Record required boards platform and libraries in project docs

## pp-test Validation Checklist
- Compile succeeds for target board profile
- At least one acceptance criterion is verified via script or documented hardware smoke check
- Report actual command(s) and output before marking tested
