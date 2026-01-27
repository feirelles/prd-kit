#!/usr/bin/env python3
"""PRD Kit - Setup for init-feature command.

Handles branch creation and spec directory initialization.
Supports multiple deliverables - creates one branch/directory for all.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .common import (
    Colors,
    PRDKitPaths,
    check_prd_kit_initialized,
    log_error,
    log_info,
    log_success,
)


def get_next_feature_number(paths: PRDKitPaths) -> int:
    """Determine the next feature number from all sources.
    
    Checks:
    - specs/ directory
    - Remote branches (feat/XXX-*)
    - Local branches (feat/XXX-*)
    
    Returns the highest number found + 1.
    """
    highest = 0
    
    # Check specs directory
    specs_dir = paths.project_root / "specs"
    if specs_dir.is_dir():
        for spec in specs_dir.iterdir():
            if spec.is_dir():
                match = re.match(r"^(\d+)-", spec.name)
                if match:
                    num = int(match.group(1))
                    highest = max(highest, num)
    
    # Check git branches
    try:
        result = subprocess.run(
            ["git", "branch", "-a", "--format=%(refname:short)"],
            capture_output=True,
            text=True,
            cwd=paths.project_root,
        )
        if result.returncode == 0:
            for branch in result.stdout.strip().split("\n"):
                # Match feat/001-name or origin/feat/001-name
                match = re.search(r"feat/(\d+)-", branch)
                if match:
                    num = int(match.group(1))
                    highest = max(highest, num)
    except Exception:
        pass  # Git not available
    
    return highest + 1


def slugify(text: str) -> str:
    """Convert text to slug format (lowercase-with-hyphens)."""
    # Remove special characters, replace spaces with hyphens
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def find_deliverable(paths: PRDKitPaths, identifier: str) -> Path | None:
    """Find a deliverable by ID, name, or path.
    
    Args:
        paths: PRDKitPaths instance
        identifier: Can be:
            - Full path to deliverable file
            - Deliverable ID (e.g., "001", "002")
            - Deliverable name
            
    Returns:
        Path to deliverable file, or None if not found.
    """
    # Check if it's a direct path
    if Path(identifier).is_file():
        return Path(identifier)
    
    # Check if it's an absolute path
    abs_path = paths.project_root / identifier
    if abs_path.is_file():
        return abs_path
    
    # Search in all prds/*/deliverables/ directories
    for prd_dir in paths.prds_dir.iterdir():
        if not prd_dir.is_dir():
            continue
        deliverables_dir = prd_dir / "deliverables"
        if not deliverables_dir.is_dir():
            continue
        
        # Try to match by ID
        for f in deliverables_dir.glob("deliverable-*.md"):
            # Match deliverable-001-name.md
            match = re.match(r"deliverable-(\d+)-(.+)\.md", f.name)
            if match:
                file_id = match.group(1)
                if identifier == file_id or identifier == f"0{file_id}" or identifier.zfill(3) == file_id.zfill(3):
                    return f
            
            # Match just the filename
            if identifier.lower() in f.name.lower():
                return f
    
    return None


def list_available_deliverables(paths: PRDKitPaths) -> list[dict]:
    """List all available deliverables."""
    deliverables = []
    
    for prd_dir in paths.prds_dir.iterdir():
        if not prd_dir.is_dir():
            continue
        deliverables_dir = prd_dir / "deliverables"
        if not deliverables_dir.is_dir():
            continue
        
        for f in deliverables_dir.glob("deliverable-*.md"):
            match = re.match(r"deliverable-(\d+)-(.+)\.md", f.name)
            if match:
                deliverables.append({
                    "id": match.group(1),
                    "name": match.group(2),
                    "path": str(f.relative_to(paths.project_root)),
                    "prd": prd_dir.name,
                })
    
    return deliverables


def extract_deliverable_info(deliverable_path: Path) -> dict:
    """Extract name and priority from deliverable file."""
    content = deliverable_path.read_text()
    
    info = {
        "name": "",
        "id": "",
        "priority": "MEDIUM",
        "dependencies": [],
    }
    
    # Extract from filename
    match = re.match(r"deliverable-(\d+)-(.+)\.md", deliverable_path.name)
    if match:
        info["id"] = match.group(1)
        info["name"] = match.group(2)
    
    # Extract from content
    lines = content.split("\n")
    for line in lines[:20]:  # Check first 20 lines
        if line.startswith("# Deliverable:"):
            info["name"] = line.replace("# Deliverable:", "").strip()
        elif "Deliverable ID" in line:
            match = re.search(r"(\d+)", line)
            if match:
                info["id"] = match.group(1)
        elif "Priority" in line:
            if "HIGH" in line.upper():
                info["priority"] = "HIGH"
            elif "LOW" in line.upper():
                info["priority"] = "LOW"
        elif "Dependencies" in line:
            deps = re.findall(r"(\d+)", line)
            info["dependencies"] = deps
    
    return info


def create_branch(paths: PRDKitPaths, branch_name: str) -> bool:
    """Create a new git branch."""
    try:
        result = subprocess.run(
            ["git", "checkout", "-b", branch_name],
            capture_output=True,
            text=True,
            cwd=paths.project_root,
        )
        return result.returncode == 0
    except Exception:
        return False


def generate_combined_name(deliverable_infos: list[dict]) -> str:
    """Generate a combined name from multiple deliverables.
    
    Examples:
        - [auth, email] -> "auth-and-email"
        - [ui, ux, design] -> "ui-ux-design"
    """
    if len(deliverable_infos) == 1:
        return slugify(deliverable_infos[0]["name"])[:30]
    
    # Take first word from each deliverable name
    words = []
    for info in deliverable_infos[:3]:  # Max 3 deliverables in name
        name_parts = info["name"].split("-")
        words.append(name_parts[0])
    
    if len(deliverable_infos) > 3:
        combined = "-".join(words) + "-plus"
    elif len(deliverable_infos) == 2:
        combined = "-and-".join(words)
    else:
        combined = "-".join(words)
    
    return slugify(combined)[:40]


def main():
    parser = argparse.ArgumentParser(
        description="Initialize feature branch and spec directory"
    )
    parser.add_argument(
        "--deliverable",
        nargs="+",  # Accept multiple deliverables
        required=True,
        help="Deliverable ID(s), name(s), or path(s). Multiple deliverables will be combined in one branch.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    
    args = parser.parse_args()
    
    try:
        paths = check_prd_kit_initialized()
        
        # Find all deliverables
        deliverable_paths = []
        not_found = []
        
        for identifier in args.deliverable:
            deliverable_path = find_deliverable(paths, identifier)
            if deliverable_path is None:
                not_found.append(identifier)
            else:
                deliverable_paths.append(deliverable_path)
        
        # Handle not found deliverables
        if not_found:
            available = list_available_deliverables(paths)
            if args.json:
                print(json.dumps({
                    "STATUS": "error",
                    "ERROR": f"Deliverables not found: {', '.join(not_found)}",
                    "AVAILABLE": available,
                }))
            else:
                log_error(f"Deliverables not found: {', '.join(not_found)}")
                log_info("Available deliverables:")
                for d in available:
                    print(f"  - {d['id']}: {d['name']} ({d['path']})")
            sys.exit(1)
        
        # Extract info from all deliverables
        deliverable_infos = []
        for path in deliverable_paths:
            info = extract_deliverable_info(path)
            info["path"] = path
            deliverable_infos.append(info)
        
        # Determine next feature number
        next_num = get_next_feature_number(paths)
        feature_num = str(next_num).zfill(3)
        
        # Generate combined name
        combined_name = generate_combined_name(deliverable_infos)
        
        # Branch and directory names
        branch_name = f"feat/{feature_num}-{combined_name}"
        spec_dir_name = f"{feature_num}-{combined_name}"
        spec_dir = paths.project_root / "specs" / spec_dir_name
        
        # Create specs directory
        spec_dir.mkdir(parents=True, exist_ok=True)
        
        # Create README.md
        deliverable_links = []
        for info in deliverable_infos:
            rel_path = info["path"].relative_to(paths.project_root)
            deliverable_links.append(f"- [{info['path'].name}]({rel_path})")
        
        deliverable_section = "\n".join(deliverable_links)
        
        readme_content = f"""# {combined_name.replace('-', ' ').title()}

**Deliverables**:
{deliverable_section}

**Branch**: {branch_name}
**Status**: Initializing
**Count**: {len(deliverable_infos)} deliverable(s)

## Documents

- [ ] context.md - Project analysis (run @prd-context)
- [ ] plan.md - Technical decisions (run @prd-plan)
- [ ] tasks.md - Implementation tasks (run @prd-tasks)
"""
        (spec_dir / "README.md").write_text(readme_content)
        
        # Copy all deliverable references
        import shutil
        for i, info in enumerate(deliverable_infos):
            if len(deliverable_infos) == 1:
                dest_name = "deliverable.md"
            else:
                dest_name = f"deliverable-{info['id']}.md"
            shutil.copy2(info["path"], spec_dir / dest_name)
        
        # Create branch
        branch_created = create_branch(paths, branch_name)
        
        # Count total user stories
        total_us = 0
        for info in deliverable_infos:
            content = info["path"].read_text()
            total_us += len(re.findall(r"###\s*\[US\d+\]", content))
        
        # Collect all priorities and dependencies
        priorities = set(info["priority"] for info in deliverable_infos)
        all_deps = []
        for info in deliverable_infos:
            all_deps.extend(info["dependencies"])
        unique_deps = sorted(set(all_deps))
        
        # Build result
        result = {
            "STATUS": "success",
            "FEATURE_NUMBER": feature_num,
            "FEATURE_NAME": spec_dir_name,
            "BRANCH_NAME": branch_name,
            "BRANCH_CREATED": branch_created,
            "SPEC_DIR": str(spec_dir.relative_to(paths.project_root)),
            "DELIVERABLES": [
                {
                    "id": info["id"],
                    "name": info["name"],
                    "priority": info["priority"],
                    "path": str(info["path"].relative_to(paths.project_root)),
                }
                for info in deliverable_infos
            ],
            "COMBINED": {
                "count": len(deliverable_infos),
                "total_user_stories": total_us,
                "priorities": sorted(priorities),
                "dependencies": unique_deps if unique_deps else ["None"],
            },
            "FILES_CREATED": [
                "README.md",
            ] + [
                f"deliverable-{info['id']}.md" if len(deliverable_infos) > 1 else "deliverable.md"
                for info in deliverable_infos
            ],
        }
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print()
            if len(deliverable_infos) == 1:
                log_success(f"Feature initialized: {spec_dir_name}")
            else:
                log_success(f"Feature initialized ({len(deliverable_infos)} deliverables combined): {spec_dir_name}")
            print()
            print(f"  📁 Directory: specs/{spec_dir_name}/")
            print(f"  🌿 Branch: {branch_name} {'(created)' if branch_created else '(failed to create)'}")
            print()
            print("  📄 Files created:")
            print("     - README.md (status tracker)")
            if len(deliverable_infos) == 1:
                print("     - deliverable.md")
            else:
                for info in deliverable_infos:
                    print(f"     - deliverable-{info['id']}.md ({info['name']})")
            print()
            print("  📋 Summary:")
            print(f"     - {total_us} total user stories")
            print(f"     - Priorities: {', '.join(sorted(priorities))}")
            print(f"     - Dependencies: {', '.join(unique_deps) if unique_deps else 'None'}")
            print()
            print("  ➡️  Next step: Run @prd-context to analyze the project")
            print()
        
        return 0
        
    except SystemExit:
        raise
    except Exception as e:
        if args.json:
            print(json.dumps({
                "STATUS": "error",
                "ERROR": str(e),
            }))
        else:
            log_error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
