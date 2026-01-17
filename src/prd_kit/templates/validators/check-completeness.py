#!/usr/bin/env python3
"""
PRD Kit - Completeness Validator

Validates that PRD and research documents have all required sections
and no remaining [NEEDS_DETAIL] tags.

Usage:
    python check-completeness.py <file_path>
    python check-completeness.py prds/feature-name/PRD.md
"""

import re
import sys
import json
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    """Result of a validation check."""
    passed: bool
    issues: list[str]
    warnings: list[str]
    needs_detail_tags: list[str]
    missing_sections: list[str]


# Required sections for each document type
REQUIRED_SECTIONS = {
    "research.md": [
        "Initial Idea",
        "Discovery Questions",
        "Problem Space",
        "User Understanding", 
        "Solution Space",
        "Success Criteria",
        "Constitution Alignment",
    ],
    "PRD.md": [
        "Problem Statement",
        "Solution Overview",
        "User Stories",
        "Non-Functional Requirements",
        "Success Metrics",
        "Risks & Mitigations",
    ],
}


def find_needs_detail_tags(content: str) -> list[str]:
    """Find all [NEEDS_DETAIL: xxx] tags in content."""
    pattern = r'\[NEEDS_DETAIL:\s*([^\]]+)\]'
    matches = re.findall(pattern, content)
    return [m.strip() for m in matches]


def find_present_sections(content: str) -> set[str]:
    """Find all markdown headers (## and ###) in content."""
    pattern = r'^#{2,3}\s+(.+)$'
    matches = re.findall(pattern, content, re.MULTILINE)
    return set(m.strip() for m in matches)


def check_section_present(content: str, section_name: str) -> bool:
    """Check if a section (by header) is present in content."""
    # Check for exact match or partial match in headers
    present_sections = find_present_sections(content)
    
    # Exact match
    if section_name in present_sections:
        return True
    
    # Partial match (section name is substring)
    for section in present_sections:
        if section_name.lower() in section.lower():
            return True
    
    return False


def validate_user_stories(content: str) -> list[str]:
    """Validate user story format."""
    issues = []
    
    # Find user story sections
    story_pattern = r'###\s+\[US\d+\]'
    stories = re.findall(story_pattern, content)
    
    if not stories:
        issues.append("No user stories found (expected format: ### [US1] Title)")
        return issues
    
    # Check for required parts in each story
    as_a_pattern = r'\*\*As a\*\*'
    i_want_pattern = r'\*\*I want to\*\*'
    so_that_pattern = r'\*\*So that\*\*'
    gherkin_pattern = r'```gherkin'
    
    if not re.search(as_a_pattern, content):
        issues.append("User stories missing 'As a' format")
    if not re.search(i_want_pattern, content):
        issues.append("User stories missing 'I want to' format")
    if not re.search(so_that_pattern, content):
        issues.append("User stories missing 'So that' format")
    if not re.search(gherkin_pattern, content):
        issues.append("User stories missing Gherkin acceptance criteria")
    
    return issues


def validate_file(file_path: Path) -> ValidationResult:
    """Validate a PRD or research file."""
    issues = []
    warnings = []
    missing_sections = []
    
    if not file_path.exists():
        return ValidationResult(
            passed=False,
            issues=[f"File not found: {file_path}"],
            warnings=[],
            needs_detail_tags=[],
            missing_sections=[],
        )
    
    content = file_path.read_text()
    file_name = file_path.name
    
    # Find NEEDS_DETAIL tags
    needs_detail = find_needs_detail_tags(content)
    if needs_detail:
        issues.append(f"Found {len(needs_detail)} [NEEDS_DETAIL] tags")
    
    # Check required sections based on file type
    required = REQUIRED_SECTIONS.get(file_name, [])
    for section in required:
        if not check_section_present(content, section):
            missing_sections.append(section)
    
    if missing_sections:
        issues.append(f"Missing {len(missing_sections)} required sections")
    
    # Additional validation for PRD files
    if file_name == "PRD.md":
        story_issues = validate_user_stories(content)
        issues.extend(story_issues)
        
        # Check for placeholder values
        placeholder_pattern = r'\[(?:PLACEHOLDER|TODO|TBD|XXX)[^\]]*\]'
        placeholders = re.findall(placeholder_pattern, content, re.IGNORECASE)
        if placeholders:
            warnings.append(f"Found {len(placeholders)} placeholder markers")
    
    # Check for empty sections (header followed by another header or end)
    empty_section_pattern = r'^(#{2,3}\s+.+)\n\s*\n(#{2,3}\s+|$)'
    empty_sections = re.findall(empty_section_pattern, content, re.MULTILINE)
    if empty_sections:
        warnings.append(f"Found {len(empty_sections)} potentially empty sections")
    
    passed = len(issues) == 0 and len(needs_detail) == 0 and len(missing_sections) == 0
    
    return ValidationResult(
        passed=passed,
        issues=issues,
        warnings=warnings,
        needs_detail_tags=needs_detail,
        missing_sections=missing_sections,
    )


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python check-completeness.py <file_path>", file=sys.stderr)
        return 1
    
    file_path = Path(sys.argv[1])
    result = validate_file(file_path)
    
    # Output as JSON for easy parsing by agents
    output = {
        "file": str(file_path),
        "passed": result.passed,
        "issues": result.issues,
        "warnings": result.warnings,
        "needs_detail_tags": result.needs_detail_tags,
        "missing_sections": result.missing_sections,
    }
    
    print(json.dumps(output, indent=2))
    
    # Also print human-readable summary
    print("\n" + "=" * 50, file=sys.stderr)
    if result.passed:
        print("✅ VALIDATION PASSED", file=sys.stderr)
    else:
        print("❌ VALIDATION FAILED", file=sys.stderr)
        
        if result.needs_detail_tags:
            print(f"\n[NEEDS_DETAIL] tags ({len(result.needs_detail_tags)}):", file=sys.stderr)
            for tag in result.needs_detail_tags:
                print(f"  - {tag}", file=sys.stderr)
        
        if result.missing_sections:
            print(f"\nMissing sections ({len(result.missing_sections)}):", file=sys.stderr)
            for section in result.missing_sections:
                print(f"  - {section}", file=sys.stderr)
        
        if result.issues:
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
