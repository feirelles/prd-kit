#!/usr/bin/env python3
"""PRD Kit - Generate Deliverables Phase Setup Script."""

import argparse
import json
import sys
from pathlib import Path

from .common import (
    PRDKitPaths,
    check_prd_kit_initialized,
    get_feature_status,
    log_error,
    log_info,
    log_success,
)


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PRD Kit Generate Deliverables Setup")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    feature_name = parsed.feature
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    # Validate prerequisites
    feature_dir = paths.get_feature_dir(feature_name)
    prd_file = paths.get_prd_file(feature_name)
    deliverables_dir = paths.get_deliverables_dir(feature_name)
    deliverables_map = paths.get_deliverables_map(feature_name)
    
    if not deliverables_map.is_file():
        log_error("Deliverables map not found. Run decompose phase first.")
        sys.exit(1)
    
    # Get template
    deliverable_template = paths.templates_dir / "deliverable-template.md"
    
    # Get status
    status = get_feature_status(paths, feature_name)
    
    # List existing deliverables
    existing_deliverables = []
    if deliverables_dir.is_dir():
        existing_deliverables = [f.name for f in deliverables_dir.glob("deliverable-*.md")]
    
    existing_deliverables_str = ",".join(existing_deliverables)
    
    # Paths for output
    command_file = paths.commands_dir / "generate-deliverables.md"
    validator = paths.validators_dir / "check-deliverables.py"
    
    # Output
    if parsed.json:
        output = {
            "FEATURE_NAME": feature_name,
            "FEATURE_DIR": str(feature_dir),
            "PRD_FILE": str(prd_file),
            "DELIVERABLES_DIR": str(deliverables_dir),
            "DELIVERABLES_MAP": str(deliverables_map),
            "DELIVERABLE_TEMPLATE": str(deliverable_template),
            "EXISTING_DELIVERABLES": existing_deliverables_str,
            "COMMAND_FILE": str(command_file),
            "VALIDATOR": str(validator),
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Feature: {feature_name}")
        log_info(f"PRD file: {prd_file}")
        log_info(f"Deliverables map: {deliverables_map}")
        log_info(f"Existing deliverables: {existing_deliverables_str or '(none)'}")
        log_info(f"Status: {status}")
        log_success("Generate deliverables phase ready")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
