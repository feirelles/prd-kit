#!/usr/bin/env python3
"""PRD Kit - Discovery Phase Setup Script."""

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
    parser = argparse.ArgumentParser(description="PRD Kit Discovery Setup")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    feature_name = parsed.feature
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    # Setup feature directory
    feature_dir = paths.get_feature_dir(feature_name)
    feature_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup research file
    research_file = paths.get_research_file(feature_name)
    research_template = paths.templates_dir / "research-template.md"
    
    if not research_file.is_file():
        if research_template.is_file():
            # Copy and replace placeholders
            content = research_template.read_text()
            content = content.replace("[FEATURE_NAME]", feature_name)
            content = content.replace("[DATE]", date.today().isoformat())
            research_file.write_text(content)
        else:
            research_file.touch()
    
    # Get constitution path
    constitution = paths.constitution_file
    constitution_str = str(constitution) if constitution.is_file() else ""
    
    # Get status
    status = get_feature_status(paths, feature_name)
    
    # Paths for output
    command_file = paths.commands_dir / "discover.md"
    validator = paths.validators_dir / "check-completeness.py"
    
    # Output
    if parsed.json:
        output = {
            "FEATURE_NAME": feature_name,
            "FEATURE_DIR": str(feature_dir),
            "RESEARCH_FILE": str(research_file),
            "CONSTITUTION": constitution_str,
            "RESEARCH_TEMPLATE": str(research_template),
            "COMMAND_FILE": str(command_file),
            "VALIDATOR": str(validator),
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Feature: {feature_name}")
        log_info(f"Directory: {feature_dir}")
        log_info(f"Research file: {research_file}")
        log_info(f"Constitution: {constitution_str or '(not found)'}")
        log_info(f"Status: {status}")
        log_success("Discovery phase ready")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
