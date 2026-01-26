#!/usr/bin/env python3
"""
PRD Kit - Deliverables Validator

Validates deliverables-map.json and individual deliverable files.
Checks for:
- Valid JSON structure
- No circular dependencies
- All referenced IDs exist
- Required sections in deliverable files

Usage:
    python check-deliverables.py <deliverables_dir_or_map_file>
    python check-deliverables.py prds/feature-name/deliverables/
    python check-deliverables.py prds/feature-name/deliverables/deliverables-map.json
"""

import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    """Result of validation."""
    passed: bool
    issues: list[str]
    warnings: list[str]


REQUIRED_DELIVERABLE_SECTIONS = [
    "Context",
    "User Stories",
    "Acceptance Criteria",
]

RECOMMENDED_DELIVERABLE_SECTIONS = [
    "Out of Scope",  # Lists PRD features planned for other deliverables (prevents premature implementation)
]


def load_deliverables_map(map_path: Path) -> dict | None:
    """Load and parse deliverables-map.json."""
    try:
        with open(map_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        return None
    except FileNotFoundError:
        return None


def check_circular_dependencies(deliverables: list[dict]) -> list[str]:
    """Check for circular dependencies in the deliverables graph."""
    issues = []
    
    # Build adjacency list
    graph: dict[str, list[str]] = {}
    id_set = set()
    
    for d in deliverables:
        d_id = d.get("id", "")
        deps = d.get("dependencies", [])
        graph[d_id] = deps
        id_set.add(d_id)
    
    # Check all referenced dependencies exist
    for d_id, deps in graph.items():
        for dep in deps:
            if dep not in id_set:
                issues.append(f"Deliverable '{d_id}' references non-existent dependency '{dep}'")
    
    # DFS to detect cycles
    visited = set()
    rec_stack = set()
    
    def has_cycle(node: str, path: list[str]) -> bool:
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, path + [neighbor]):
                    return True
            elif neighbor in rec_stack:
                cycle_path = path[path.index(neighbor):] + [neighbor] if neighbor in path else [node, neighbor]
                issues.append(f"Circular dependency detected: {' -> '.join(cycle_path)}")
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            has_cycle(node, [node])
    
    return issues


def validate_deliverable_file(file_path: Path) -> tuple[list[str], list[str]]:
    """Validate a single deliverable file.
    
    Returns:
        Tuple of (issues, warnings)
    """
    issues = []
    warnings = []
    
    if not file_path.exists():
        issues.append(f"Deliverable file not found: {file_path}")
        return issues, warnings
    
    content = file_path.read_text()
    
    # Check required sections
    for section in REQUIRED_DELIVERABLE_SECTIONS:
        pattern = rf'^##\s+{re.escape(section)}'
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            issues.append(f"{file_path.name}: Missing required section '{section}'")
    
    # Check recommended sections
    for section in RECOMMENDED_DELIVERABLE_SECTIONS:
        pattern = rf'^##\s+{re.escape(section)}'
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"{file_path.name}: Missing recommended section '{section}' - should list PRD features planned for other deliverables")
    
    # Check for Source PRD reference
    if "Source PRD" not in content:
        issues.append(f"{file_path.name}: Missing 'Source PRD' reference")
    
    # Check for Deliverable ID
    if "Deliverable ID" not in content:
        issues.append(f"{file_path.name}: Missing 'Deliverable ID'")
    
    # Check for NEEDS_DETAIL tags (shouldn't have any in final deliverables)
    needs_detail = re.findall(r'\[NEEDS_DETAIL:\s*([^\]]+)\]', content)
    if needs_detail:
        issues.append(f"{file_path.name}: Contains {len(needs_detail)} [NEEDS_DETAIL] tags")
    
    return issues, warnings


def validate_deliverables_map(map_data: dict) -> list[str]:
    """Validate the structure of deliverables-map.json."""
    issues = []
    
    # Check required top-level fields
    required_fields = ["source_prd", "deliverables"]
    for field in required_fields:
        if field not in map_data:
            issues.append(f"Missing required field in map: '{field}'")
    
    deliverables = map_data.get("deliverables", [])
    
    if not isinstance(deliverables, list):
        issues.append("'deliverables' must be an array")
        return issues
    
    if len(deliverables) == 0:
        issues.append("No deliverables defined in map")
        return issues
    
    # Check each deliverable entry
    required_deliverable_fields = ["id", "name", "title"]
    ids_seen = set()
    
    for i, d in enumerate(deliverables):
        for field in required_deliverable_fields:
            if field not in d:
                issues.append(f"Deliverable {i}: Missing required field '{field}'")
        
        d_id = d.get("id", "")
        if d_id in ids_seen:
            issues.append(f"Duplicate deliverable ID: '{d_id}'")
        ids_seen.add(d_id)
    
    # Check for circular dependencies
    circular_issues = check_circular_dependencies(deliverables)
    issues.extend(circular_issues)
    
    return issues


def validate_directory(dir_path: Path) -> ValidationResult:
    """Validate all deliverables in a directory."""
    issues = []
    warnings = []
    
    map_path = dir_path / "deliverables-map.json"
    
    if not map_path.exists():
        return ValidationResult(
            passed=False,
            issues=["deliverables-map.json not found"],
            warnings=[],
        )
    
    # Validate map
    map_data = load_deliverables_map(map_path)
    if map_data is None:
        return ValidationResult(
            passed=False,
            issues=["Failed to parse deliverables-map.json"],
            warnings=[],
        )
    
    map_issues = validate_deliverables_map(map_data)
    issues.extend(map_issues)
    
    # Validate each deliverable file
    deliverables = map_data.get("deliverables", [])
    for d in deliverables:
        file_name = d.get("file", "")
        if file_name:
            file_path = dir_path / file_name
            file_issues, file_warnings = validate_deliverable_file(file_path)
            issues.extend(file_issues)
            warnings.extend(file_warnings)
    
    # Check for orphan deliverable files (not in map)
    map_files = {d.get("file", "") for d in deliverables}
    for f in dir_path.glob("deliverable-*.md"):
        if f.name not in map_files:
            warnings.append(f"Orphan deliverable file not in map: {f.name}")
    
    passed = len(issues) == 0
    return ValidationResult(passed=passed, issues=issues, warnings=warnings)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python check-deliverables.py <path>", file=sys.stderr)
        return 1
    
    path = Path(sys.argv[1])
    
    if path.is_dir():
        result = validate_directory(path)
    elif path.name == "deliverables-map.json":
        result = validate_directory(path.parent)
    else:
        # Single file validation
        file_issues, file_warnings = validate_deliverable_file(path)
        result = ValidationResult(
            passed=len(file_issues) == 0,
            issues=file_issues,
            warnings=file_warnings,
        )
    
    # Output as JSON
    output = {
        "path": str(path),
        "passed": result.passed,
        "issues": result.issues,
        "warnings": result.warnings,
    }
    print(json.dumps(output, indent=2))
    
    # Human-readable summary
    print("\n" + "=" * 50, file=sys.stderr)
    if result.passed:
        print("✅ VALIDATION PASSED", file=sys.stderr)
    else:
        print("❌ VALIDATION FAILED", file=sys.stderr)
        print(f"\nIssues ({len(result.issues)}):", file=sys.stderr)
        for issue in result.issues:
            print(f"  - {issue}", file=sys.stderr)
    
    if result.warnings:
        print(f"\nWarnings ({len(result.warnings)}):", file=sys.stderr)
        for warning in result.warnings:
            print(f"  - {warning}", file=sys.stderr)
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
