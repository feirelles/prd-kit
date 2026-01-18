#!/usr/bin/env bash
# PRD Kit - Constitution Setup Script

set -euo pipefail
source "$(dirname "$0")/common.sh"

# ============================================================================
# Parse Arguments
# ============================================================================
JSON_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_MODE=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Usage: $0 [--json]"
            exit 1
            ;;
    esac
done

check_prd_kit_initialized

# ============================================================================
# Get Constitution File
# ============================================================================
CONSTITUTION="$PRD_KIT_DIR/memory/product-constitution.md"
CONSTITUTION_TEMPLATE="$PRD_KIT_DIR/templates/product-constitution.md"

# Check if constitution exists, if not copy template
if [[ ! -f "$CONSTITUTION" ]]; then
    if [[ -f "$CONSTITUTION_TEMPLATE" ]]; then
        mkdir -p "$(dirname "$CONSTITUTION")"
        cp "$CONSTITUTION_TEMPLATE" "$CONSTITUTION"
        log_info "Created constitution from template"
    fi
fi

# ============================================================================
# Check Constitution Completeness
# ============================================================================
PLACEHOLDER_COUNT=0
FILLED_COUNT=0
STATUS="incomplete"

if [[ -f "$CONSTITUTION" ]]; then
    # Count placeholders (anything in [BRACKETS] that looks like a placeholder)
    PLACEHOLDER_COUNT=$(grep -cE '\[[A-Z][A-Z_0-9]+\]' "$CONSTITUTION" 2>/dev/null || echo "0")
    
    # Check for key sections being filled
    if grep -q "^### I\." "$CONSTITUTION" && \
       ! grep -q '\[PRINCIPLE_1_NAME\]' "$CONSTITUTION"; then
        FILLED_COUNT=$((FILLED_COUNT + 1))
    fi
    
    if grep -q "^### Vision" "$CONSTITUTION" && \
       ! grep -q '\[VISION_STATEMENT\]' "$CONSTITUTION"; then
        FILLED_COUNT=$((FILLED_COUNT + 1))
    fi
    
    if grep -q "^### Primary Persona" "$CONSTITUTION" && \
       ! grep -q '\[PERSONA_1_NAME\]' "$CONSTITUTION"; then
        FILLED_COUNT=$((FILLED_COUNT + 1))
    fi
    
    if [[ "$PLACEHOLDER_COUNT" -eq 0 ]]; then
        STATUS="complete"
    elif [[ "$FILLED_COUNT" -gt 0 ]]; then
        STATUS="partial"
    fi
fi

# ============================================================================
# Output
# ============================================================================
if $JSON_MODE; then
    cat <<EOF
{
  "CONSTITUTION": "$CONSTITUTION",
  "CONSTITUTION_TEMPLATE": "$CONSTITUTION_TEMPLATE",
  "COMMAND_FILE": "$PRD_KIT_DIR/commands/constitution.md",
  "PLACEHOLDER_COUNT": $PLACEHOLDER_COUNT,
  "STATUS": "$STATUS"
}
EOF
else
    log_info "Constitution file: $CONSTITUTION"
    log_info "Placeholders remaining: $PLACEHOLDER_COUNT"
    log_info "Status: $STATUS"
    
    if [[ "$STATUS" == "complete" ]]; then
        log_success "Constitution is complete"
    elif [[ "$STATUS" == "partial" ]]; then
        log_warn "Constitution is partially filled"
    else
        log_warn "Constitution needs to be filled"
    fi
fi
