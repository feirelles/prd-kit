#!/usr/bin/env python3
"""PRD Kit - Constitution Setup Script."""

import argparse
import json
import re
import sys
from pathlib import Path

from .common import (
    PRDKitPaths,
    check_prd_kit_initialized,
    log_info,
    log_success,
    log_warn,
)


def check_constitution_completeness(constitution_path: Path) -> tuple[int, int, str]:
    """Check constitution completeness.
    
    Returns:
        Tuple of (placeholder_count, filled_count, status)
    """
    placeholder_count = 0
    filled_count = 0
    status = "incomplete"
    
    if not constitution_path.is_file():
        return placeholder_count, filled_count, status
    
    try:
        content = constitution_path.read_text()
        
        # Count placeholders (anything in [BRACKETS] that looks like a placeholder)
        placeholders = re.findall(r'\[[A-Z][A-Z_0-9]+\]', content)
        placeholder_count = len(placeholders)
        
        # Check for key sections being filled
        if re.search(r'^### I\.', content, re.MULTILINE) and \
           '[PRINCIPLE_1_NAME]' not in content:
            filled_count += 1
        
        if re.search(r'^### Vision', content, re.MULTILINE) and \
           '[VISION_STATEMENT]' not in content:
            filled_count += 1
        
        if re.search(r'^### Primary Persona', content, re.MULTILINE) and \
           '[PERSONA_1_NAME]' not in content:
            filled_count += 1
        
        if placeholder_count == 0:
            status = "complete"
        elif filled_count > 0:
            status = "partial"
            
    except Exception:
        pass
    
    return placeholder_count, filled_count, status


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PRD Kit Constitution Setup")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    constitution = paths.constitution_file
    constitution_template = paths.constitution_template
    command_file = paths.commands_dir / "constitution.md"
    
    # Create constitution from template if it doesn't exist
    if not constitution.is_file() and constitution_template.is_file():
        constitution.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(constitution_template, constitution)
        log_info("Created constitution from template")
    
    # Check completeness
    placeholder_count, filled_count, status = check_constitution_completeness(constitution)
    
    # Output
    if parsed.json:
        output = {
            "CONSTITUTION": str(constitution),
            "CONSTITUTION_TEMPLATE": str(constitution_template),
            "COMMAND_FILE": str(command_file),
            "PLACEHOLDER_COUNT": placeholder_count,
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Constitution file: {constitution}")
        log_info(f"Placeholders remaining: {placeholder_count}")
        log_info(f"Status: {status}")
        
        if status == "complete":
            log_success("Constitution is complete")
        elif status == "partial":
            log_warn("Constitution is partially filled")
        else:
            log_warn("Constitution needs to be filled")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
