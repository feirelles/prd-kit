#!/usr/bin/env python3
"""PRD Kit - Decompose Phase Setup Script.

This phase ONLY creates deliverables-map.json.
DO NOT create deliverable-XXX.md files - that's the deliverables phase.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from .common import (
    PRDKitPaths,
    check_prd_kit_initialized,
    get_feature_status,
    log_error,
    log_info,
    log_success,
    log_warn,
)


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PRD Kit Decompose Setup")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    feature_name = parsed.feature
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    # Validate prerequisites
    feature_dir = paths.get_feature_dir(feature_name)
    prd_file = paths.get_prd_file(feature_name)
    
    if not prd_file.is_file():
        log_error("PRD file not found. Complete draft and refine phases first.")
        sys.exit(1)
    
    # Check if PRD is approved
    try:
        content = prd_file.read_text()
        if not re.search(r"Status.*Approved", content):
            log_warn("PRD may not be approved yet. Check status before decomposing.")
    except Exception:
        pass
    
    # Setup deliverables directory
    deliverables_dir = paths.get_deliverables_dir(feature_name)
    deliverables_dir.mkdir(parents=True, exist_ok=True)
    
    deliverables_map = paths.get_deliverables_map(feature_name)
    
    # Get tech constitution (if Spec Kit is present)
    tech_constitution = paths.tech_constitution_file
    tech_constitution_str = str(tech_constitution) if tech_constitution.is_file() else ""
    
    # Get product constitution
    constitution = paths.constitution_file
    constitution_str = str(constitution) if constitution.is_file() else ""
    
    # Get status
    status = get_feature_status(paths, feature_name)
    
    # Paths for output
    command_file = paths.commands_dir / "decompose.md"
    validator = paths.validators_dir / "check-deliverables.py"
    
    # Output
    if parsed.json:
        output = {
            "FEATURE_NAME": feature_name,
            "FEATURE_DIR": str(feature_dir),
            "PRD_FILE": str(prd_file),
            "DELIVERABLES_DIR": str(deliverables_dir),
            "DELIVERABLES_MAP": str(deliverables_map),
            "CONSTITUTION": constitution_str,
            "TECH_CONSTITUTION": tech_constitution_str,
            "COMMAND_FILE": str(command_file),
            "VALIDATOR": str(validator),
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Feature: {feature_name}")
        log_info(f"PRD file: {prd_file}")
        log_info(f"Deliverables dir: {deliverables_dir}")
        log_info(f"Tech constitution: {tech_constitution_str or '(not found)'}")
        log_info(f"Status: {status}")
        log_success("Decompose phase ready")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
