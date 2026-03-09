#!/usr/bin/env python3
import ast
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


ROOT = os.getcwd()
PLAN_DIR = os.path.join(ROOT, "plan")
LANGUAGE_PATH = os.path.join(PLAN_DIR, "language.md")
PLAN_PATH = os.path.join(PLAN_DIR, "plan.md")
LEGACY_REFERENCE_PATH = os.path.join(PLAN_DIR, "reference.md")
CATALOG_PATH = os.path.join(ROOT, "docs", "catalog", "architecture-code-catalog.md")

ARCH_DIR = os.path.join(ROOT, "docs", "architecture")
SEQUENCES_DIR = os.path.join(ARCH_DIR, "sequences")
ADRS_DIR = os.path.join(ARCH_DIR, "adrs")
SYSTEM_MAP_PATH = os.path.join(ARCH_DIR, "system-map.yaml")

ENTRYPOINT_CANDIDATES = ["__main__.py", "main.py", "cli.py", "app.py"]
PY_MANIFESTS = ["pyproject.toml", "setup.cfg", "setup.py", "requirements.txt"]

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "plan",
}


@dataclass
class InterfaceItem:
    path: str
    signatures: List[str]


@dataclass
class ModelItem:
    name: str
    source: str


@dataclass
class EntryPoint:
    path: str
    purpose: str


def read_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def find_project_name() -> str:
    plan = read_file(PLAN_PATH) or ""
    for line in plan.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.basename(ROOT)


def read_language() -> str:
    content = read_file(LANGUAGE_PATH) or ""
    for line in content.splitlines():
        if line.lower().startswith("language:"):
            return line.split(":", 1)[1].strip().lower()
    return ""


def git_ls_files() -> List[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return []
    raw = result.stdout.decode("utf-8", errors="ignore")
    return [p for p in raw.split("\x00") if p]


def walk_files() -> List[str]:
    files = []
    for root, dirs, filenames in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for name in filenames:
            files.append(os.path.join(root, name))
    return files


def list_repo_files() -> List[str]:
    files = git_ls_files()
    if files:
        return files
    return [os.path.relpath(p, ROOT) for p in walk_files()]


def is_text_file(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        if b"\x00" in chunk:
            return False
    except OSError:
        return False
    return True


def split_manual_section(existing: Optional[str], marker: str) -> str:
    if not existing:
        return ""
    if marker not in existing:
        return ""
    parts = existing.split(marker, 1)
    tail = parts[1]
    lines = tail.splitlines()
    content_lines = []
    for line in lines[1:]:
        if line.startswith("## "):
            break
        content_lines.append(line)
    return "\n".join(content_lines).strip("\n")


def detect_readme(files: List[str]) -> Optional[str]:
    for name in files:
        base = os.path.basename(name).lower()
        if base.startswith("readme"):
            return name
    return None


def summarize_overview(readme_text: str, manifests: Dict[str, str], language: str) -> str:
    summary_lines = []
    if readme_text:
        for line in readme_text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                summary_lines.append(line)
            if len(" ".join(summary_lines)) > 300:
                break
    summary = " ".join(summary_lines).strip()
    if summary:
        summary = summary[:500]
    language_str = language if language else "unknown"
    if summary:
        return f"{summary} Primary language: {language_str}."
    if manifests:
        return (
            f"Project with manifests: {', '.join(sorted(manifests.keys()))}. "
            f"Primary language: {language_str}."
        )
    return f"Repository overview. Primary language: {language_str}."


def find_entrypoints(files: List[str]) -> List[EntryPoint]:
    entrypoints = []
    for path in files:
        base = os.path.basename(path)
        if base in ENTRYPOINT_CANDIDATES:
            entrypoints.append(EntryPoint(path=path, purpose="Executable entry point"))
        if path.endswith(".ino"):
            entrypoints.append(EntryPoint(path=path, purpose="Arduino sketch entry point"))
    return entrypoints


def summarize_architecture(files: List[str], entrypoints: List[EntryPoint]) -> str:
    top_levels = set()
    for path in files:
        parts = path.split(os.sep)
        if parts:
            top_levels.add(parts[0])
    tops = ", ".join(sorted(p for p in top_levels if p))
    entry_text = ", ".join(ep.path for ep in entrypoints) if entrypoints else "no explicit entry points detected"
    if tops:
        return f"Top-level areas: {tops}. Entry points: {entry_text}."
    return f"Entry points: {entry_text}."


def parse_pyproject(path: str) -> Dict[str, List[str]]:
    data: Dict[str, List[str]] = {}
    try:
        import tomllib  # py3.11
    except Exception:
        return data
    content = read_file(path)
    if not content:
        return data
    try:
        parsed = tomllib.loads(content)
    except Exception:
        return data
    project = parsed.get("project", {})
    scripts = project.get("scripts", {})
    if isinstance(scripts, dict):
        data["scripts"] = [f"{k} = {v}" for k, v in scripts.items()]
    deps = project.get("dependencies", [])
    if isinstance(deps, list):
        data["dependencies"] = deps
    return data


def extract_python_interfaces(path: str) -> Tuple[List[str], List[ModelItem]]:
    content = read_file(path)
    if not content:
        return [], []
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return [], []
    signatures = []
    models: List[ModelItem] = []

    def format_args(args: ast.arguments) -> str:
        parts = []
        for arg, default in zip(args.args, [None] * (len(args.args) - len(args.defaults)) + args.defaults):
            name = arg.arg
            if default is not None:
                try:
                    default_str = ast.unparse(default)
                except Exception:
                    default_str = "..."
                parts.append(f"{name}={default_str}")
            else:
                parts.append(name)
        if args.vararg:
            parts.append(f"*{args.vararg.arg}")
        for arg, default in zip(args.kwonlyargs, args.kw_defaults):
            name = arg.arg
            if default is not None:
                try:
                    default_str = ast.unparse(default)
                except Exception:
                    default_str = "..."
                parts.append(f"{name}={default_str}")
            else:
                parts.append(name)
        if args.kwarg:
            parts.append(f"**{args.kwarg.arg}")
        return ", ".join(parts)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            args = format_args(node.args)
            ret = ""
            if node.returns is not None:
                try:
                    ret = f" -> {ast.unparse(node.returns)}"
                except Exception:
                    ret = ""
            signatures.append(f"def {node.name}({args}){ret}")
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            signatures.append(f"class {node.name}:")
            is_dataclass = any(isinstance(dec, ast.Name) and dec.id == "dataclass" for dec in node.decorator_list)
            is_pydantic = any(isinstance(base, ast.Name) and base.id == "BaseModel" for base in node.bases)
            if is_dataclass or is_pydantic:
                models.append(ModelItem(name=node.name, source=path))
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    args = format_args(item.args)
                    signatures.append(f"  def {item.name}({args})")
    return signatures, models


def extract_arduino_interfaces(path: str) -> Tuple[List[str], List[ModelItem]]:
    content = read_file(path)
    if not content:
        return [], []
    signatures = []
    models: List[ModelItem] = []
    func_re = re.compile(
        r"^\s*(?!static\b)([\w:<>]+(?:\s+[\w:<>]+)*)\s+(\w+)\s*\(([^;]*?)\)\s*(?:const)?\s*\{",
        re.MULTILINE,
    )
    class_re = re.compile(r"^\s*(class|struct)\s+(\w+)", re.MULTILINE)
    for match in class_re.finditer(content):
        name = match.group(2)
        signatures.append(f"class {name}")
    for match in func_re.finditer(content):
        ret = match.group(1)
        name = match.group(2)
        args = " ".join(match.group(3).split())
        signatures.append(f"{ret} {name}({args})")
    return signatures, models


def detect_dependencies(manifests: Dict[str, str], pyproject_data: Dict[str, List[str]]) -> List[str]:
    deps = []
    if "dependencies" in pyproject_data:
        deps.extend(pyproject_data["dependencies"])
    reqs = manifests.get("requirements.txt")
    if reqs:
        for line in reqs.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            deps.append(line)
    return deps


def detect_surfaces_python(files: List[str]) -> List[str]:
    tokens = {
        "argparse": "CLI: argparse",
        "click": "CLI: click",
        "typer": "CLI: typer",
        "fastapi": "HTTP: FastAPI",
        "flask": "HTTP: Flask",
    }
    found = set()
    for path in files:
        if not path.endswith(".py"):
            continue
        text = read_file(os.path.join(ROOT, path))
        if not text:
            continue
        lowered = text.lower()
        for token, label in tokens.items():
            if token in lowered:
                found.add(label)
    return sorted(found)


def collect_interfaces(files: List[str], language: str) -> Tuple[List[InterfaceItem], List[ModelItem]]:
    interfaces: List[InterfaceItem] = []
    models: List[ModelItem] = []
    if language == "python":
        for path in files:
            if not path.endswith(".py"):
                continue
            abs_path = os.path.join(ROOT, path)
            if not is_text_file(abs_path):
                continue
            sigs, found_models = extract_python_interfaces(abs_path)
            if sigs:
                interfaces.append(InterfaceItem(path=path, signatures=sigs))
            models.extend(found_models)
        surfaces = detect_surfaces_python(files)
        if surfaces:
            interfaces.append(InterfaceItem(path="Detected surfaces", signatures=surfaces))
    elif language == "arduino":
        for path in files:
            if not any(path.endswith(ext) for ext in [".ino", ".h", ".hpp", ".c", ".cpp"]):
                continue
            abs_path = os.path.join(ROOT, path)
            if not is_text_file(abs_path):
                continue
            sigs, found_models = extract_arduino_interfaces(abs_path)
            if sigs:
                interfaces.append(InterfaceItem(path=path, signatures=sigs))
            models.extend(found_models)
    return interfaces, models


def load_manifests(files: List[str]) -> Dict[str, str]:
    manifests: Dict[str, str] = {}
    for name in PY_MANIFESTS:
        if name in files:
            text = read_file(os.path.join(ROOT, name))
            if text is not None:
                manifests[name] = text
    return manifests


def build_reference(
    project_name: str,
    overview: str,
    architecture: str,
    entrypoints: List[EntryPoint],
    interfaces: List[InterfaceItem],
    models: List[ModelItem],
    dependencies: List[str],
    task_change_log: str,
    reuse_notes: str,
    interface_deltas: str,
    architecture_artifact_notes: str,
    manual_notes: str,
) -> str:
    lines = []
    lines.append(f"# {project_name} Architecture/Code Catalog")
    lines.append("")
    lines.append("## Overview")
    lines.append(overview or "")
    lines.append("")
    lines.append("## Architecture")
    lines.append(architecture or "")
    lines.append("")
    lines.append("## Entry Points")
    if entrypoints:
        for ep in entrypoints:
            lines.append(f"- {ep.path} — {ep.purpose}")
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("## Interfaces (Generated)")
    if interfaces:
        for item in interfaces:
            lines.append(f"### {item.path}")
            lines.append("```text")
            for sig in item.signatures:
                lines.append(sig)
            lines.append("```")
            lines.append("")
    else:
        lines.append("- None detected")
        lines.append("")
    lines.append("## Data Models / Schemas")
    if models:
        for model in models:
            lines.append(f"- {model.name} — {model.source}")
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("## External Dependencies / Services")
    if dependencies:
        for dep in dependencies:
            lines.append(f"- {dep}")
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("## Task Change Log")
    lines.append(task_change_log or "")
    lines.append("")
    lines.append("## Reuse Notes (Manual)")
    lines.append(reuse_notes or "")
    lines.append("")
    lines.append("## Interface Deltas (Manual)")
    lines.append(interface_deltas or "")
    lines.append("")
    lines.append("## Architecture Artifact Notes (Manual)")
    lines.append(architecture_artifact_notes or "")
    lines.append("")
    lines.append("## Notes (Manual)")
    lines.append(manual_notes or "")
    lines.append("")
    return "\n".join(lines)


def top_components(files: List[str], limit: int = 8) -> List[str]:
    seen = []
    for path in files:
        if path.startswith("docs/") or path.startswith("plan/"):
            continue
        top = path.split("/", 1)[0]
        if top not in seen:
            seen.append(top)
    return seen[:limit]


def c4_context_md(project_name: str, dependencies: List[str]) -> str:
    deps = dependencies[:3] if dependencies else ["External Service"]
    dep_nodes = "\n".join([f'    S --> D{i}["{dep}"]' for i, dep in enumerate(deps, 1)])
    return f"""# C4 Context

```mermaid
flowchart LR
    U["User"] --> S["{project_name}"]
{dep_nodes}
```
"""


def c4_container_md(project_name: str, entrypoints: List[EntryPoint], components: List[str]) -> str:
    entries = [ep.path for ep in entrypoints[:4]] or ["main application"]
    comp = components[:6] or ["core"]
    entry_nodes = "\n".join([f'    U --> E{i}["{e}"]' for i, e in enumerate(entries, 1)])
    comp_nodes = "\n".join([f'    E1 --> C{i}["{c}"]' for i, c in enumerate(comp, 1)])
    return f"""# C4 Container

```mermaid
flowchart LR
    U["User"] --> SYS["{project_name}"]
{entry_nodes}
{comp_nodes}
```
"""


def c4_components_md(interfaces: List[InterfaceItem]) -> str:
    items = [i.path for i in interfaces if i.path != "Detected surfaces"][:8]
    if not items:
        items = ["component-a", "component-b"]
    lines = []
    for idx, item in enumerate(items, 1):
        lines.append(f'    C{idx}["{item}"]')
        if idx > 1:
            lines.append(f"    C{idx-1} --> C{idx}")
    graph = "\n".join(lines)
    return f"""# C4 Components

```mermaid
flowchart LR
{graph}
```
"""


def sequence_md(project_name: str, entrypoints: List[EntryPoint]) -> str:
    ep = entrypoints[0].path if entrypoints else "application entrypoint"
    return f"""# Request Flow

```mermaid
sequenceDiagram
    actor User
    participant App as {project_name}
    participant EP as {ep}
    User->>App: Trigger operation
    App->>EP: Execute entry flow
    EP-->>App: Return result
    App-->>User: Response
```
"""


def architecture_readme_md(project_name: str) -> str:
    return f"""# Architecture

## Overview
This directory contains architecture artifacts and the generated code catalog for **{project_name}**.

## Artifact Index
- `system-map.yaml`
- `c4-context.md`
- `c4-container.md`
- `c4-components.md`
- `sequences/request-flow.md`
- `adrs/`

## Diagram Index
- C4 Context: `c4-context.md`
- C4 Container: `c4-container.md`
- C4 Components: `c4-components.md`
- Sequence: `sequences/request-flow.md`
"""


def system_map_yaml(project_name: str, components: List[str], entrypoints: List[EntryPoint]) -> str:
    c_lines = "\n".join([f"  - name: {c}\n    type: component" for c in (components[:8] or ["core"])])
    r_lines = []
    for ep in entrypoints[:6]:
        target = components[0] if components else "core"
        r_lines.append(f"  - from: {ep.path}\n    to: {target}\n    kind: invokes")
    if not r_lines:
        r_lines.append("  - from: user\n    to: core\n    kind: invokes")
    rel = "\n".join(r_lines)
    return f"""version: 1
system: "{project_name}"
components:
{c_lines}
relationships:
{rel}
planned_changes: []
"""


def write_architecture_docs(
    project_name: str,
    entrypoints: List[EntryPoint],
    interfaces: List[InterfaceItem],
    dependencies: List[str],
    files: List[str],
) -> None:
    comps = top_components(files)
    write_file(os.path.join(ARCH_DIR, "README.md"), architecture_readme_md(project_name))
    write_file(os.path.join(ARCH_DIR, "c4-context.md"), c4_context_md(project_name, dependencies))
    write_file(os.path.join(ARCH_DIR, "c4-container.md"), c4_container_md(project_name, entrypoints, comps))
    write_file(os.path.join(ARCH_DIR, "c4-components.md"), c4_components_md(interfaces))
    write_file(os.path.join(SEQUENCES_DIR, "request-flow.md"), sequence_md(project_name, entrypoints))
    write_file(SYSTEM_MAP_PATH, system_map_yaml(project_name, comps, entrypoints))

    os.makedirs(ADRS_DIR, exist_ok=True)
    adr_files = [n for n in os.listdir(ADRS_DIR) if n.lower().endswith(".md")]
    if not adr_files:
        write_file(
            os.path.join(ADRS_DIR, "ADR-0001-architecture-catalog-baseline.md"),
            """# ADR-0001: Architecture/Code Catalog Baseline

## Status
Accepted

## Context
The project requires a consistent architecture documentation baseline with generated artifacts.

## Decision
Adopt generated architecture artifacts under `docs/architecture/` and maintain
`docs/catalog/architecture-code-catalog.md` as the Architecture/Code Catalog.

## Consequences
- Faster onboarding and planning quality.
- Requires keeping docs synchronized with implementation.
""",
        )


def main() -> int:
    if not os.path.isdir(PLAN_DIR):
        print("Missing plan/ directory. Run /pp-init first.", file=sys.stderr)
        return 1
    if not os.path.exists(LANGUAGE_PATH):
        print("Missing plan/language.md. Run /pp-init <language> first.", file=sys.stderr)
        return 1

    project_name = find_project_name()
    language = read_language()
    files = list_repo_files()
    readme_path = detect_readme(files)
    readme_text = read_file(os.path.join(ROOT, readme_path)) if readme_path else ""

    manifests = load_manifests(files)
    pyproject_data = parse_pyproject(os.path.join(ROOT, "pyproject.toml")) if "pyproject.toml" in manifests else {}

    entrypoints = find_entrypoints(files)
    overview = summarize_overview(readme_text or "", manifests, language)
    architecture = summarize_architecture(files, entrypoints)
    interfaces, models = collect_interfaces(files, language)
    dependencies = detect_dependencies(manifests, pyproject_data)
    existing_catalog = read_file(CATALOG_PATH)
    task_change_log = split_manual_section(existing_catalog, "## Task Change Log")
    reuse_notes = split_manual_section(existing_catalog, "## Reuse Notes (Manual)")
    interface_deltas = split_manual_section(existing_catalog, "## Interface Deltas (Manual)")
    architecture_artifact_notes = split_manual_section(existing_catalog, "## Architecture Artifact Notes (Manual)")
    manual_notes = split_manual_section(existing_catalog, "## Notes (Manual)")
    if not manual_notes:
        manual_notes = split_manual_section(read_file(LEGACY_REFERENCE_PATH), "## Notes (Manual)")

    reference_content = build_reference(
        project_name=project_name,
        overview=overview,
        architecture=architecture,
        entrypoints=entrypoints,
        interfaces=interfaces,
        models=models,
        dependencies=dependencies,
        task_change_log=task_change_log,
        reuse_notes=reuse_notes,
        interface_deltas=interface_deltas,
        architecture_artifact_notes=architecture_artifact_notes,
        manual_notes=manual_notes,
    )

    write_file(CATALOG_PATH, reference_content)
    write_architecture_docs(project_name, entrypoints, interfaces, dependencies, files)

    print(f"Updated {CATALOG_PATH}")
    print(f"Updated {os.path.join(ARCH_DIR, 'README.md')}")
    print(f"Updated {os.path.join(ARCH_DIR, 'c4-context.md')}")
    print(f"Updated {os.path.join(ARCH_DIR, 'c4-container.md')}")
    print(f"Updated {os.path.join(ARCH_DIR, 'c4-components.md')}")
    print(f"Updated {os.path.join(SEQUENCES_DIR, 'request-flow.md')}")
    print(f"Updated {SYSTEM_MAP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
