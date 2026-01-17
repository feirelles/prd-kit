#!/usr/bin/env bash
# PRD Kit - Draft Phase Setup Script

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
RESEARCH_FILE=$(get_research_file "$FEATURE_NAME")

if [[ ! -f "$RESEARCH_FILE" ]]; then
    log_error "Research file not found. Run discovery phase first."
    exit 1
fi

# ============================================================================
# Setup PRD File
# ============================================================================
PRD_FILE=$(get_prd_file "$FEATURE_NAME")
PRD_TEMPLATE="$PRD_KIT_DIR/templates/prd-template.md"

if [[ ! -f "$PRD_FILE" ]]; then
    if [[ -f "$PRD_TEMPLATE" ]]; then
        sed "s/\[FEATURE_NAME\]/$FEATURE_NAME/g; s/\[DATE\]/$(date +%Y-%m-%d)/g" \
            "$PRD_TEMPLATE" > "$PRD_FILE"
    else
        touch "$PRD_FILE"
    fi
fi

# ============================================================================
# Get Constitution
# ============================================================================
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
  "RESEARCH_FILE": "$RESEARCH_FILE",
  "PRD_FILE": "$PRD_FILE",
  "PRD_TEMPLATE": "$PRD_TEMPLATE",
  "CONSTITUTION": "$CONSTITUTION",
  "COMMAND_FILE": "$PRD_KIT_DIR/commands/draft.md",
  "VALIDATOR": "$PRD_KIT_DIR/validators/check-completeness.py",
  "STATUS": "$STATUS"
}
EOF
else
    log_info "Feature: $FEATURE_NAME"
    log_info "Research: $RESEARCH_FILE"
    log_info "PRD file: $PRD_FILE"
    log_info "Status: $STATUS"
    log_success "Draft phase ready"
fi
