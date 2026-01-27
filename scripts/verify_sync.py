#!/usr/bin/env python3
"""Verify that init.py and update.py are in sync with actual template files."""

from pathlib import Path
import sys

# Project root
ROOT = Path(__file__).parent.parent

# Actual files in templates
TEMPLATES_DIR = ROOT / "src" / "prd_kit" / "templates"

def get_actual_files():
    """Get all files that should be managed."""
    files = {
        "templates": [],
        "commands": [],
        "validators": [],
        "scripts": [],
        "agents_copilot": [],
    }
    
    # Templates (*.md in root, excluding memory/)
    for f in TEMPLATES_DIR.glob("*.md"):
        if f.name != "product-constitution.md":  # User data
            files["templates"].append(f.name)
    
    # Commands
    for f in (TEMPLATES_DIR / "commands").glob("*.md"):
        files["commands"].append(f"commands/{f.name}")
    
    # Validators
    for f in (TEMPLATES_DIR / "validators").glob("*.py"):
        files["validators"].append(f"validators/{f.name}")
    
    # Scripts
    for f in (TEMPLATES_DIR / "scripts" / "prd_scripts").glob("*.py"):
        files["scripts"].append(f"scripts/prd_scripts/{f.name}")
    
    # Copilot agents
    for f in (TEMPLATES_DIR / "agents" / "copilot").glob("*.agent.md"):
        files["agents_copilot"].append(f"agents/copilot/{f.name}")
    
    return files

def extract_from_python(file_path, dict_name):
    """Extract file paths from Python dictionary."""
    content = file_path.read_text()
    
    # Find the dictionary
    in_dict = False
    files = []
    
    for line in content.split("\n"):
        if f"{dict_name} = {{" in line or f"{dict_name}.update({{" in line:
            in_dict = True
            continue
        
        if in_dict:
            if line.strip() == "}":
                in_dict = False
                continue
            
            # Extract file path from line like: "path/file.md": ...
            if '":' in line:
                key = line.split('"')[1]
                # Skip user data files
                if key != "memory/product-constitution.md" and not key.startswith("."):
                    files.append(key)
    
    return set(files)

def main():
    """Check sync between actual files and init.py/update.py."""
    actual = get_actual_files()
    
    # Extract from init.py
    init_py = ROOT / "src" / "prd_kit" / "commands" / "init.py"
    init_templates = extract_from_python(init_py, "template_files")
    init_scripts = extract_from_python(init_py, "script_templates")
    init_agents = extract_from_python(init_py, "agent_templates")
    
    # Extract from update.py
    update_py = ROOT / "src" / "prd_kit" / "commands" / "update.py"
    update_files = extract_from_python(update_py, "files_to_update")
    
    # Check sync
    errors = []
    
    # Check templates
    actual_all = set(actual["templates"] + actual["commands"] + actual["validators"])
    if actual_all != init_templates:
        missing_init = actual_all - init_templates
        extra_init = init_templates - actual_all
        if missing_init:
            errors.append(f"init.py template_files MISSING: {missing_init}")
        if extra_init:
            errors.append(f"init.py template_files EXTRA: {extra_init}")
    
    # Check scripts
    actual_scripts = set(actual["scripts"])
    if actual_scripts != init_scripts:
        missing_init = actual_scripts - init_scripts
        extra_init = init_scripts - actual_scripts
        if missing_init:
            errors.append(f"init.py script_templates MISSING: {missing_init}")
        if extra_init:
            errors.append(f"init.py script_templates EXTRA: {extra_init}")
    
    # Check update.py has all managed files
    expected_in_update = actual_all | actual_scripts
    if not expected_in_update.issubset(update_files):
        missing = expected_in_update - update_files
        errors.append(f"update.py files_to_update MISSING: {missing}")
    
    # Report
    if errors:
        print("❌ SYNC ERRORS FOUND:\n")
        for error in errors:
            print(f"  • {error}")
        print("\n⚠️  Please update init.py and/or update.py to match actual template files.")
        return 1
    else:
        print("✅ All files are in sync!")
        print(f"\n📊 Summary:")
        print(f"  • Templates: {len(actual['templates'])}")
        print(f"  • Commands: {len(actual['commands'])}")
        print(f"  • Validators: {len(actual['validators'])}")
        print(f"  • Scripts: {len(actual['scripts'])}")
        print(f"  • Copilot Agents: {len(actual['agents_copilot'])}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
