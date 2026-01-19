#!/usr/bin/env python3
"""PRD Kit - Draft Phase Setup Script."""

import argparse
import json
import sys
from datetime import date
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
    parser = argparse.ArgumentParser(description="PRD Kit Draft Setup")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    feature_name = parsed.feature
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    # Validate prerequisites
    feature_dir = paths.get_feature_dir(feature_name)
    research_file = paths.get_research_file(feature_name)
    
    if not research_file.is_file():
        log_error("Research file not found. Run discovery phase first.")
        sys.exit(1)
    
    # Setup PRD file
    prd_file = paths.get_prd_file(feature_name)
    prd_template = paths.templates_dir / "prd-template.md"
    
    if not prd_file.is_file():
        if prd_template.is_file():
            content = prd_template.read_text()
            content = content.replace("[FEATURE_NAME]", feature_name)
            content = content.replace("[DATE]", date.today().isoformat())
            prd_file.write_text(content)
        else:
            prd_file.touch()
    
    # Get constitution
    constitution = paths.constitution_file
    constitution_str = str(constitution) if constitution.is_file() else ""
    
    # Get status
    status = get_feature_status(paths, feature_name)
    
    # Paths for output
    command_file = paths.commands_dir / "draft.md"
    validator = paths.validators_dir / "check-completeness.py"
    
    # Output
    if parsed.json:
        output = {
            "FEATURE_NAME": feature_name,
            "FEATURE_DIR": str(feature_dir),
            "RESEARCH_FILE": str(research_file),
            "PRD_FILE": str(prd_file),
            "PRD_TEMPLATE": str(prd_template),
            "CONSTITUTION": constitution_str,
            "COMMAND_FILE": str(command_file),
            "VALIDATOR": str(validator),
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Feature: {feature_name}")
        log_info(f"Research: {research_file}")
        log_info(f"PRD file: {prd_file}")
        log_info(f"Status: {status}")
        log_success("Draft phase ready")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
