#!/usr/bin/env bash
# PRD Kit - Decompose Phase Setup Script

set -euo pipefail
source "$(dirname "$0")/common.sh"

# ============================================================================
# Parse Arguments
# ============================================================================
FEATURE_NAME=""
JSON_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --feature)
            FEATURE_NAME="$2"
            shift 2
            ;;
        --json)
            JSON_MODE=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$FEATURE_NAME" ]]; then
    log_error "Feature name is required."
    echo "Usage: $0 --feature <name> [--json]"
    exit 1
fi

check_prd_kit_initialized

# ============================================================================
# Validate Prerequisites
# ============================================================================
FEATURE_DIR=$(get_feature_dir "$FEATURE_NAME")
PRD_FILE=$(get_prd_file "$FEATURE_NAME")

if [[ ! -f "$PRD_FILE" ]]; then
    log_error "PRD file not found. Complete draft and refine phases first."
    exit 1
fi

# Check if PRD is approved
if ! grep -q "Status.*Approved" "$PRD_FILE" 2>/dev/null; then
    log_warn "PRD may not be approved yet. Check status before decomposing."
fi

# ============================================================================
# Setup Deliverables Directory
# ============================================================================
DELIVERABLES_DIR=$(get_deliverables_dir "$FEATURE_NAME")
mkdir -p "$DELIVERABLES_DIR"

DELIVERABLES_MAP=$(get_deliverables_map "$FEATURE_NAME")

# ============================================================================
# Get Technical Constitution (if Spec Kit is present)
# ============================================================================
TECH_CONSTITUTION="$PROJECT_ROOT/.specify/memory/constitution.md"
[[ ! -f "$TECH_CONSTITUTION" ]] && TECH_CONSTITUTION=""

CONSTITUTION="$PRD_KIT_DIR/memory/product-constitution.md"
[[ ! -f "$CONSTITUTION" ]] && CONSTITUTION=""

STATUS=$(get_feature_status "$FEATURE_NAME")

# ============================================================================
# Output
# ============================================================================
if $JSON_MODE; then
    cat <<EOF
{
  "FEATURE_NAME": "$FEATURE_NAME",
  "FEATURE_DIR": "$FEATURE_DIR",
  "PRD_FILE": "$PRD_FILE",
  "DELIVERABLES_DIR": "$DELIVERABLES_DIR",
  "DELIVERABLES_MAP": "$DELIVERABLES_MAP",
  "CONSTITUTION": "$CONSTITUTION",
  "TECH_CONSTITUTION": "$TECH_CONSTITUTION",
  "COMMAND_FILE": "$PRD_KIT_DIR/commands/decompose.md",
  "VALIDATOR": "$PRD_KIT_DIR/validators/check-deliverables.py",
  "STATUS": "$STATUS"
}
EOF
else
    log_info "Feature: $FEATURE_NAME"
    log_info "PRD file: $PRD_FILE"
    log_info "Deliverables dir: $DELIVERABLES_DIR"
    log_info "Tech constitution: ${TECH_CONSTITUTION:-"(not found)"}"
    log_info "Status: $STATUS"
    log_success "Decompose phase ready"
fi
