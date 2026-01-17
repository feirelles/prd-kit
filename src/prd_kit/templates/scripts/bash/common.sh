#!/usr/bin/env bash
# PRD Kit - Common functions and configuration
# Source this file from other scripts: source "$(dirname "$0")/common.sh"

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRD_KIT_DIR="$PROJECT_ROOT/.prd-kit"
PRDS_DIR="$PROJECT_ROOT/prds"

# ============================================================================
# Color Output
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# ============================================================================
# Validation Functions
# ============================================================================
check_prd_kit_initialized() {
    if [[ ! -d "$PRD_KIT_DIR" ]]; then
        log_error "PRD Kit not initialized. Run 'prd init' first."
        exit 1
    fi
}

check_feature_exists() {
    local feature_name="$1"
    local feature_dir="$PRDS_DIR/$feature_name"
    
    if [[ ! -d "$feature_dir" ]]; then
        return 1
    fi
    return 0
}

check_file_exists() {
    local file_path="$1"
    local description="$2"
    
    if [[ -f "$file_path" ]]; then
        echo "  ✓ $description"
        return 0
    else
        echo "  ✗ $description"
        return 1
    fi
}

# ============================================================================
# Path Functions
# ============================================================================
get_feature_dir() {
    local feature_name="$1"
    echo "$PRDS_DIR/$feature_name"
}

get_research_file() {
    local feature_name="$1"
    echo "$(get_feature_dir "$feature_name")/research.md"
}

get_prd_file() {
    local feature_name="$1"
    echo "$(get_feature_dir "$feature_name")/PRD.md"
}

get_deliverables_dir() {
    local feature_name="$1"
    echo "$(get_feature_dir "$feature_name")/deliverables"
}

get_deliverables_map() {
    local feature_name="$1"
    echo "$(get_deliverables_dir "$feature_name")/deliverables-map.json"
}

# ============================================================================
# Template Functions
# ============================================================================
copy_template() {
    local template_name="$1"
    local dest_path="$2"
    local template_path="$PRD_KIT_DIR/templates/$template_name"
    
    if [[ -f "$template_path" ]]; then
        cp "$template_path" "$dest_path"
        log_success "Created: $dest_path"
    else
        log_error "Template not found: $template_path"
        return 1
    fi
}

# ============================================================================
# JSON Output
# ============================================================================
output_json() {
    local -n data=$1  # nameref to associative array
    local json="{"
    local first=true
    
    for key in "${!data[@]}"; do
        if [[ "$first" == true ]]; then
            first=false
        else
            json+=","
        fi
        json+="\"$key\":\"${data[$key]}\""
    done
    
    json+="}"
    echo "$json"
}

# ============================================================================
# Feature Status
# ============================================================================
get_feature_status() {
    local feature_name="$1"
    local feature_dir=$(get_feature_dir "$feature_name")
    
    if [[ ! -d "$feature_dir" ]]; then
        echo "not_started"
        return
    fi
    
    local research_file=$(get_research_file "$feature_name")
    local prd_file=$(get_prd_file "$feature_name")
    local deliverables_map=$(get_deliverables_map "$feature_name")
    local deliverables_dir=$(get_deliverables_dir "$feature_name")
    
    # Check for deliverable files (excluding map and README)
    if [[ -d "$deliverables_dir" ]] && ls "$deliverables_dir"/deliverable-*.md &>/dev/null; then
        echo "deliverables_generated"
    elif [[ -f "$deliverables_map" ]]; then
        echo "decomposed"
    elif [[ -f "$prd_file" ]]; then
        # Check if PRD is approved (contains "Status: Approved")
        if grep -q "Status.*Approved" "$prd_file" 2>/dev/null; then
            echo "approved"
        else
            echo "drafted"
        fi
    elif [[ -f "$research_file" ]]; then
        # Check if research has NEEDS_DETAIL tags
        if grep -q "\[NEEDS_DETAIL:" "$research_file" 2>/dev/null; then
            echo "discovery_in_progress"
        else
            echo "discovery_complete"
        fi
    else
        echo "not_started"
    fi
}

# ============================================================================
# Available Docs Check
# ============================================================================
list_available_docs() {
    local feature_name="$1"
    local feature_dir=$(get_feature_dir "$feature_name")
    local docs=()
    
    [[ -f "$feature_dir/research.md" ]] && docs+=("research.md")
    [[ -f "$feature_dir/PRD.md" ]] && docs+=("PRD.md")
    [[ -f "$feature_dir/deliverables/deliverables-map.json" ]] && docs+=("deliverables-map.json")
    
    # List deliverable files
    if [[ -d "$feature_dir/deliverables" ]]; then
        for f in "$feature_dir/deliverables"/deliverable-*.md; do
            [[ -f "$f" ]] && docs+=("$(basename "$f")")
        done
    fi
    
    printf '%s\n' "${docs[@]}"
}
