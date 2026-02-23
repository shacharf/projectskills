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
REFERENCE_PATH = os.path.join(PLAN_DIR, "reference.md")
LANGUAGE_PATH = os.path.join(PLAN_DIR, "language.md")
PLAN_PATH = os.path.join(PLAN_DIR, "plan.md")


ENTRYPOINT_CANDIDATES = [
    "__main__.py",
    "main.py",
    "cli.py",
    "app.py",
]

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


def split_manual_notes(existing: Optional[str]) -> str:
    if not existing:
        return ""
    marker = "## Notes (Manual)"
    if marker not in existing:
        return ""
    parts = existing.split(marker, 1)
    tail = parts[1]
    lines = tail.splitlines()
    # Drop the first line (heading remainder) and stop at next heading
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
    language_str = language if language else "Unknown"
    if summary:
        return f"{summary} Primary language: {language_str}."
    if manifests:
        return f"Project with manifests: {', '.join(sorted(manifests.keys()))}. Primary language: {language_str}."
    return f"Repository overview. Primary language: {language_str}."


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


def find_entrypoints(files: List[str]) -> List[EntryPoint]:
    entrypoints = []
    for path in files:
        base = os.path.basename(path)
        if base in ENTRYPOINT_CANDIDATES:
            entrypoints.append(EntryPoint(path=path, purpose="Executable entry point"))
        if path.endswith(".ino"):
            entrypoints.append(EntryPoint(path=path, purpose="Arduino sketch entry point"))
    return entrypoints


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
            is_dataclass = any(
                isinstance(dec, ast.Name) and dec.id == "dataclass" for dec in node.decorator_list
            )
            is_pydantic = any(
                isinstance(base, ast.Name) and base.id == "BaseModel" for base in node.bases
            )
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
    func_re = re.compile(r"^\s*(?!static\b)([\w:<>]+(?:\s+[\w:<>]+)*)\s+(\w+)\s*\(([^;]*?)\)\s*(?:const)?\s*\{", re.MULTILINE)
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
        abs_path = os.path.join(ROOT, path)
        text = read_file(abs_path)
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
    manual_notes: str,
) -> str:
    lines = []
    lines.append(f"# {project_name} Reference")
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
    lines.append("## Notes (Manual)")
    if manual_notes:
        lines.append(manual_notes)
    else:
        lines.append("")
    lines.append("")
    return "\n".join(lines)


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
    pyproject_data = {}
    if "pyproject.toml" in manifests:
        pyproject_data = parse_pyproject(os.path.join(ROOT, "pyproject.toml"))

    entrypoints = find_entrypoints(files)
    overview = summarize_overview(readme_text or "", manifests, language)
    architecture = summarize_architecture(files, entrypoints)

    interfaces, models = collect_interfaces(files, language)
    dependencies = detect_dependencies(manifests, pyproject_data)

    manual_notes = split_manual_notes(read_file(REFERENCE_PATH))

    content = build_reference(
        project_name=project_name,
        overview=overview,
        architecture=architecture,
        entrypoints=entrypoints,
        interfaces=interfaces,
        models=models,
        dependencies=dependencies,
        manual_notes=manual_notes,
    )

    os.makedirs(PLAN_DIR, exist_ok=True)
    with open(REFERENCE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {REFERENCE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
