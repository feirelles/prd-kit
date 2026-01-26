#!/usr/bin/env python3
"""PRD Kit - Setup for init-feature command.

Handles branch creation and spec directory initialization.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

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


def main():
    parser = argparse.ArgumentParser(
        description="Initialize feature branch and spec directory"
    )
    parser.add_argument(
        "--deliverable",
        required=True,
        help="Deliverable ID, name, or path",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    
    args = parser.parse_args()
    
    try:
        paths = check_prd_kit_initialized()
        
        # Find the deliverable
        deliverable_path = find_deliverable(paths, args.deliverable)
        
        if deliverable_path is None:
            available = list_available_deliverables(paths)
            if args.json:
                print(json.dumps({
                    "STATUS": "error",
                    "ERROR": f"Deliverable not found: {args.deliverable}",
                    "AVAILABLE": available,
                }))
            else:
                log_error(f"Deliverable not found: {args.deliverable}")
                log_info("Available deliverables:")
                for d in available:
                    print(f"  - {d['id']}: {d['name']} ({d['path']})")
            sys.exit(1)
        
        # Extract deliverable info
        info = extract_deliverable_info(deliverable_path)
        
        # Determine next feature number
        next_num = get_next_feature_number(paths)
        feature_num = str(next_num).zfill(3)
        
        # Create short name
        short_name = slugify(info["name"])[:30]  # Limit length
        
        # Branch and directory names
        branch_name = f"feat/{feature_num}-{short_name}"
        spec_dir_name = f"{feature_num}-{short_name}"
        spec_dir = paths.project_root / "specs" / spec_dir_name
        
        # Create specs directory
        spec_dir.mkdir(parents=True, exist_ok=True)
        
        # Create README.md
        readme_content = f"""# {info['name']}

**Deliverable**: [{deliverable_path.name}]({deliverable_path.relative_to(paths.project_root)})
**Branch**: {branch_name}
**Status**: Initializing

## Documents

- [ ] context.md - Project analysis (run @prd-context)
- [ ] plan.md - Technical decisions (run @prd-plan)
- [ ] tasks.md - Implementation tasks (run @prd-tasks)
"""
        (spec_dir / "README.md").write_text(readme_content)
        
        # Copy deliverable reference
        import shutil
        shutil.copy2(deliverable_path, spec_dir / "deliverable.md")
        
        # Create branch
        branch_created = create_branch(paths, branch_name)
        
        # Count user stories in deliverable
        content = deliverable_path.read_text()
        us_count = len(re.findall(r"###\s*\[US\d+\]", content))
        
        result = {
            "STATUS": "success",
            "FEATURE_NUMBER": feature_num,
            "FEATURE_NAME": spec_dir_name,
            "BRANCH_NAME": branch_name,
            "BRANCH_CREATED": branch_created,
            "SPEC_DIR": str(spec_dir.relative_to(paths.project_root)),
            "DELIVERABLE": {
                "name": info["name"],
                "id": info["id"],
                "priority": info["priority"],
                "dependencies": info["dependencies"],
                "user_stories": us_count,
            },
            "FILES_CREATED": [
                "README.md",
                "deliverable.md",
            ],
        }
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print()
            log_success(f"Feature initialized: {spec_dir_name}")
            print()
            print(f"  📁 Directory: specs/{spec_dir_name}/")
            print(f"  🌿 Branch: {branch_name} {'(created)' if branch_created else '(failed to create)'}")
            print()
            print("  📄 Files created:")
            print("     - README.md (status tracker)")
            print("     - deliverable.md (copy from PRD deliverables)")
            print()
            print("  📋 Deliverable summary:")
            print(f"     - {us_count} user stories")
            print(f"     - Priority: {info['priority']}")
            deps = info['dependencies'] if info['dependencies'] else ['None']
            print(f"     - Dependencies: {', '.join(deps)}")
            print()
            print("  ➡️  Next step: Run @prd-context to analyze the project")
            print()
        
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
        sys.exit(1)


if __name__ == "__main__":
    main()
