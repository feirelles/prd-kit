#!/usr/bin/env python3
"""PRD Kit - Tasks Phase Setup Script.

Sets up environment for task list generation.
"""

import argparse
import json
import sys
from pathlib import Path

from .common import (
    PRDKitPaths,
    check_prd_kit_initialized,
    log_error,
    log_info,
    log_success,
)


def find_spec_dir(paths: PRDKitPaths, identifier: str) -> Path | None:
    """Find spec directory by identifier.
    
    Args:
        paths: PRDKitPaths instance
        identifier: Can be:
            - Full path to spec directory
            - Spec number (e.g., "001", "01", "1")
            - Spec name (e.g., "bulk-email")
            
    Returns:
        Path to spec directory, or None if not found.
    """
    specs_dir = paths.project_root / "specs"
    
    if not specs_dir.is_dir():
        return None
    
    # Check if it's a direct path
    direct_path = Path(identifier)
    if direct_path.is_dir() and direct_path.parent == specs_dir:
        return direct_path
    
    # Check relative to specs/
    rel_path = specs_dir / identifier
    if rel_path.is_dir():
        return rel_path
    
    # Search by number or name
    for spec in specs_dir.iterdir():
        if not spec.is_dir():
            continue
        
        # Match by number prefix
        if spec.name.startswith(identifier.zfill(3) + "-"):
            return spec
        
        # Match by name suffix
        if spec.name.endswith(f"-{identifier}"):
            return spec
        
        # Match partial name
        if identifier.lower() in spec.name.lower():
            return spec
    
    return None


def main(args: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PRD Kit Tasks Setup")
    parser.add_argument("--spec", required=True, help="Spec directory identifier")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parsed = parser.parse_args(args)
    
    # Check initialization
    paths = check_prd_kit_initialized()
    
    # Find spec directory
    spec_dir = find_spec_dir(paths, parsed.spec)
    
    if spec_dir is None:
        if parsed.json:
            print(json.dumps({
                "ERROR": f"Spec directory not found: {parsed.spec}",
                "SPECS_AVAILABLE": [
                    d.name for d in (paths.project_root / "specs").iterdir()
                    if d.is_dir()
                ] if (paths.project_root / "specs").is_dir() else [],
            }, indent=2))
        else:
            log_error(f"Spec directory not found: {parsed.spec}")
        return 1
    
    # Get paths
    deliverable_file = spec_dir / "deliverable.md"
    context_file = spec_dir / "context.md"
    plan_file = spec_dir / "plan.md"
    tasks_file = spec_dir / "tasks.md"
    tech_constitution = paths.memory_dir / "tech-constitution.md"
    tasks_template = paths.templates_dir / "tasks-template.md"
    command_file = paths.commands_dir / "tasks.md"
    
    # Check files exist
    has_deliverable = deliverable_file.is_file()
    has_context = context_file.is_file()
    has_plan = plan_file.is_file()
    has_tasks = tasks_file.is_file()
    has_tech_constitution = tech_constitution.is_file()
    
    # Determine status
    if not has_plan:
        status = "missing_plan"
    elif has_tasks:
        status = "tasks_exist"
    else:
        status = "ready"
    
    # Output
    if parsed.json:
        output = {
            "SPEC_DIR": str(spec_dir),
            "SPEC_NAME": spec_dir.name,
            "DELIVERABLE_FILE": str(deliverable_file),
            "CONTEXT_FILE": str(context_file),
            "PLAN_FILE": str(plan_file),
            "TASKS_FILE": str(tasks_file),
            "TECH_CONSTITUTION": str(tech_constitution) if has_tech_constitution else "",
            "TASKS_TEMPLATE": str(tasks_template),
            "COMMAND_FILE": str(command_file),
            "HAS_DELIVERABLE": has_deliverable,
            "HAS_CONTEXT": has_context,
            "HAS_PLAN": has_plan,
            "HAS_TASKS": has_tasks,
            "STATUS": status,
        }
        print(json.dumps(output, indent=2))
    else:
        log_info(f"Spec: {spec_dir.name}")
        log_info(f"Directory: {spec_dir}")
        log_info(f"Deliverable: {'✓' if has_deliverable else '✗'}")
        log_info(f"Context: {'✓' if has_context else '✗'}")
        log_info(f"Plan: {'✓' if has_plan else '✗'}")
        log_info(f"Tasks: {'exists' if has_tasks else 'to be created'}")
        log_info(f"Tech Constitution: {'✓' if has_tech_constitution else '✗'}")
        
        if has_plan:
            log_success("Tasks phase ready")
        else:
            log_error("Missing plan.md - run @prd-plan first")
    
    return 0 if has_plan else 1


if __name__ == "__main__":
    sys.exit(main())
