#!/usr/bin/env bash
# PRD Kit - Generate Deliverables Phase Setup Script

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
DELIVERABLES_DIR=$(get_deliverables_dir "$FEATURE_NAME")
DELIVERABLES_MAP=$(get_deliverables_map "$FEATURE_NAME")

if [[ ! -f "$DELIVERABLES_MAP" ]]; then
    log_error "Deliverables map not found. Run decompose phase first."
    exit 1
fi

# ============================================================================
# Get Template
# ============================================================================
DELIVERABLE_TEMPLATE="$PRD_KIT_DIR/templates/deliverable-template.md"

STATUS=$(get_feature_status "$FEATURE_NAME")

# ============================================================================
# List existing deliverables
# ============================================================================
EXISTING_DELIVERABLES=""
if [[ -d "$DELIVERABLES_DIR" ]]; then
    # Use find instead of ls to avoid exit code 2 when no files match (set -e)
    EXISTING_DELIVERABLES=$(find "$DELIVERABLES_DIR" -maxdepth 1 -name 'deliverable-*.md' -printf '%f\n' 2>/dev/null | tr '\n' ',' | sed 's/,$//' || true)
fi

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
  "DELIVERABLE_TEMPLATE": "$DELIVERABLE_TEMPLATE",
  "EXISTING_DELIVERABLES": "$EXISTING_DELIVERABLES",
  "COMMAND_FILE": "$PRD_KIT_DIR/commands/generate-deliverables.md",
  "VALIDATOR": "$PRD_KIT_DIR/validators/check-deliverables.py",
  "STATUS": "$STATUS"
}
EOF
else
    log_info "Feature: $FEATURE_NAME"
    log_info "PRD file: $PRD_FILE"
    log_info "Deliverables map: $DELIVERABLES_MAP"
    log_info "Existing deliverables: ${EXISTING_DELIVERABLES:-"(none)"}"
    log_info "Status: $STATUS"
    log_success "Generate deliverables phase ready"
fi
