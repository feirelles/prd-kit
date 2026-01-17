#!/usr/bin/env bash
# PRD Kit - Discovery Phase Setup Script

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
            echo "Usage: $0 --feature <name> [--json]"
            exit 1
            ;;
    esac
done

# ============================================================================
# Validation
# ============================================================================
if [[ -z "$FEATURE_NAME" ]]; then
    log_error "Feature name is required."
    echo "Usage: $0 --feature <name> [--json]"
    exit 1
fi

check_prd_kit_initialized

# ============================================================================
# Setup Feature Directory
# ============================================================================
FEATURE_DIR=$(get_feature_dir "$FEATURE_NAME")
mkdir -p "$FEATURE_DIR"

# ============================================================================
# Copy Research Template
# ============================================================================
RESEARCH_FILE=$(get_research_file "$FEATURE_NAME")
RESEARCH_TEMPLATE="$PRD_KIT_DIR/templates/research-template.md"

if [[ ! -f "$RESEARCH_FILE" ]]; then
    if [[ -f "$RESEARCH_TEMPLATE" ]]; then
        # Copy and replace placeholders
        sed "s/\[FEATURE_NAME\]/$FEATURE_NAME/g; s/\[DATE\]/$(date +%Y-%m-%d)/g" \
            "$RESEARCH_TEMPLATE" > "$RESEARCH_FILE"
    else
        touch "$RESEARCH_FILE"
    fi
fi

# ============================================================================
# Get Constitution Path
# ============================================================================
CONSTITUTION="$PRD_KIT_DIR/memory/product-constitution.md"
if [[ ! -f "$CONSTITUTION" ]]; then
    CONSTITUTION=""
fi

# ============================================================================
# Get Status
# ============================================================================
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
  "CONSTITUTION": "$CONSTITUTION",
  "RESEARCH_TEMPLATE": "$RESEARCH_TEMPLATE",
  "COMMAND_FILE": "$PRD_KIT_DIR/commands/discover.md",
  "VALIDATOR": "$PRD_KIT_DIR/validators/check-completeness.py",
  "STATUS": "$STATUS"
}
EOF
else
    log_info "Feature: $FEATURE_NAME"
    log_info "Directory: $FEATURE_DIR"
    log_info "Research file: $RESEARCH_FILE"
    log_info "Constitution: ${CONSTITUTION:-"(not found)"}"
    log_info "Status: $STATUS"
    log_success "Discovery phase ready"
fi
