#!/usr/bin/env bash
set -euo pipefail

# PP (Project Planning & Implementing) Installer
#
# Installs PP capabilities to the target platform's home directory.
# Supports: cursor, claude, codex
#
# Usage:
#   ./install.sh <platform>            Install PP for a platform
#   ./install.sh <platform> --remove   Remove PP from a platform
#   ./install.sh all                   Install PP for all platforms
#   ./install.sh all --remove          Remove PP from all platforms
#   ./install.sh --help                Show this help

PP_DIR="$(cd "$(dirname "$0")" && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PLATFORMS=(cursor claude codex)

pp_skills=()

# Platform capability matrix
#   skills:   cursor, claude, codex
#   agents:   cursor, claude
#   rules:    cursor only (claude/codex use AGENTS.md instead)

platform_home() {
    echo "${HOME}/.${1}"
}

has_skills()   { return 0; }  # all platforms
has_agents()   { [[ "$1" == "cursor" || "$1" == "claude" ]]; }
has_rules()    { [[ "$1" == "cursor" ]]; }

discover_pp_skills() {
    local skills_root="${PP_DIR}/skills"
    local skill_dir
    pp_skills=()

    while IFS= read -r skill_dir; do
        if [ -f "${skill_dir}/SKILL.md" ]; then
            pp_skills+=("$(basename "${skill_dir}")")
        fi
    done < <(find "${skills_root}" -mindepth 1 -maxdepth 1 -type d -name 'pp-*' | LC_ALL=C sort)

    if [ "${#pp_skills[@]}" -eq 0 ]; then
        echo -e "${RED}Error: No PP skills found under ${skills_root}${NC}"
        exit 1
    fi
}

install_pp() {
    local platform="$1"
    local home
    home="$(platform_home "${platform}")"
    local skills_dir="${home}/skills"
    local agents_dir="${home}/agents"
    local rules_dir="${home}/rules"

    echo -e "${CYAN}[${platform}]${NC} Installing PP to ${home}/"
    echo ""

    # Skills (all platforms)
    mkdir -p "${skills_dir}"
    for skill in "${pp_skills[@]}"; do
        local src="${PP_DIR}/skills/${skill}"
        local dst="${skills_dir}/${skill}"
        if [ -d "${dst}" ]; then
            rm -rf "${dst}"
        fi
        cp -r "${src}" "${dst}"
        echo -e "  ${GREEN}✓${NC} Skill: ${skill}"
    done

    # Subagent (cursor, claude)
    if has_agents "${platform}"; then
        mkdir -p "${agents_dir}"
        cp "${PP_DIR}/agents/pp-researcher.md" "${agents_dir}/pp-researcher.md"
        echo -e "  ${GREEN}✓${NC} Subagent: pp-researcher"
    else
        echo -e "  ${YELLOW}—${NC} Subagent: pp-researcher (not supported on ${platform})"
    fi

    # Rules (cursor only; claude/codex use AGENTS.md per-project)
    if has_rules "${platform}"; then
        mkdir -p "${rules_dir}"
        cp "${PP_DIR}/rules/pp-conventions.mdc" "${rules_dir}/pp-conventions.mdc"
        echo -e "  ${GREEN}✓${NC} Rule: pp-conventions"
    else
        echo -e "  ${YELLOW}—${NC} Rule: pp-conventions (not supported on ${platform}, use AGENTS.md per-project)"
    fi

    echo ""
    echo -e "${GREEN}PP installed for ${platform}.${NC}"
    echo ""
    echo "Available commands in chat:"
    echo "  /pp-init       Scaffold a new project"
    echo "  /pp-plan       Create or revise the project plan"
    echo "  /pp-todo       Add/list future-reference TODO items"
    echo "  /pp-arch-catalog  Generate architecture/code catalog and docs"
    echo "  /pp-pipeline   Validate/summarize pipeline config"
    echo "  /pp-pipeline-edit  Edit pipeline (wizard/summary/print)"
    echo "  /pp-task       Plan the next task"
    echo "  /pp-design-review  Review/gate task design"
    echo "  /pp-implement  Implement the task"
    echo "  /pp-review     Review the implementation"
    echo "  /pp-test       Run minimal test"
    echo "  /pp-done       Complete the task"
    echo "  /pp-next       Orchestrator (step or auto mode)"
    echo "  /pp-status     Show project status"
    echo "  /pp-help       Show workflow guide"
    echo ""
    echo "Get started: type /pp-help in any chat session."
}

remove_pp() {
    local platform="$1"
    local home
    home="$(platform_home "${platform}")"
    local skills_dir="${home}/skills"
    local agents_dir="${home}/agents"
    local rules_dir="${home}/rules"

    echo -e "${CYAN}[${platform}]${NC} Removing PP from ${home}/"
    echo ""

    for skill in "${pp_skills[@]}"; do
        local dst="${skills_dir}/${skill}"
        if [ -d "${dst}" ]; then
            rm -rf "${dst}"
            echo -e "  ${YELLOW}✗${NC} Removed skill: ${skill}"
        fi
    done

    if has_agents "${platform}"; then
        if [ -f "${agents_dir}/pp-researcher.md" ]; then
            rm "${agents_dir}/pp-researcher.md"
            echo -e "  ${YELLOW}✗${NC} Removed subagent: pp-researcher"
        fi
    fi

    if has_rules "${platform}"; then
        if [ -f "${rules_dir}/pp-conventions.mdc" ]; then
            rm "${rules_dir}/pp-conventions.mdc"
            echo -e "  ${YELLOW}✗${NC} Removed rule: pp-conventions"
        fi
    fi

    echo ""
    echo -e "${GREEN}PP removed from ${platform}.${NC}"
}

validate_platform() {
    local p="$1"
    for valid in "${PLATFORMS[@]}"; do
        [[ "${p}" == "${valid}" ]] && return 0
    done
    return 1
}

show_help() {
    echo "PP Installer"
    echo ""
    echo "Usage:"
    echo "  ./install.sh <platform>            Install PP capabilities"
    echo "  ./install.sh <platform> --remove   Remove PP capabilities"
    echo "  ./install.sh all                   Install for all platforms"
    echo "  ./install.sh all --remove          Remove from all platforms"
    echo "  ./install.sh --help                Show this help"
    echo ""
    echo "Platforms: cursor, claude, codex"
    echo ""
    echo "Capability support:"
    echo "  Skills (${#pp_skills[@]}):    cursor, claude, codex"
    echo "  Subagent:       cursor, claude"
    echo "  Rules (.mdc):   cursor"
    echo ""
    echo "Examples:"
    echo "  ./install.sh cursor               Install to ~/.cursor/"
    echo "  ./install.sh claude               Install to ~/.claude/"
    echo "  ./install.sh all                  Install to all platforms"
    echo "  ./install.sh cursor --remove      Uninstall from ~/.cursor/"
}

# --- Main ---

discover_pp_skills

if [[ $# -eq 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    show_help
    exit 0
fi

target="${1}"
action="${2:-install}"

if [[ "${target}" == "all" ]]; then
    for p in "${PLATFORMS[@]}"; do
        if [[ "${action}" == "--remove" || "${action}" == "-r" ]]; then
            remove_pp "${p}"
        else
            install_pp "${p}"
        fi
        echo ""
    done
elif validate_platform "${target}"; then
    if [[ "${action}" == "--remove" || "${action}" == "-r" ]]; then
        remove_pp "${target}"
    else
        install_pp "${target}"
    fi
else
    echo -e "${RED}Error: Unknown platform '${target}'${NC}"
    echo "Valid platforms: cursor, claude, codex, all"
    exit 1
fi
