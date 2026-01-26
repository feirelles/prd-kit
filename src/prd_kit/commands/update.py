"""Update command implementation."""

from pathlib import Path

from rich.console import Console

from prd_kit.commands.init import (
    PACKAGE_DIR,
    TEMPLATES_DIR,
)

console = Console()


def update_command(
    ai: str | None,
    script: str | None,
) -> None:
    """Update PRD Kit templates and agents in an existing project."""
    target = Path.cwd()

    # Check if we're in a PRD Kit project
    prd_kit_dir = target / ".prd-kit"
    if not prd_kit_dir.exists():
        console.print("[red]Error:[/red] Not in a PRD Kit project directory")
        console.print("Run [cyan]prd init[/cyan] first to initialize a project")
        raise SystemExit(1)

    console.print("[bold blue]Updating PRD Kit[/bold blue] in current directory")

    # Detect current configuration if not specified
    if ai is None:
        # Check which AI agent is configured
        if (target / ".github" / "agents").exists():
            ai = "copilot"
        elif (target / "CLAUDE.md").exists():
            ai = "claude"
        else:
            ai = "copilot"  # default

    # Script type is now always Python (cross-platform)
    if script is not None:
        console.print(f"[yellow]Note:[/yellow] --script option is deprecated. Python scripts are now used for cross-platform support.")

    console.print(f"  AI Agent: [green]{ai}[/green]")
    console.print(f"  Scripts: [green]Python (cross-platform)[/green]")

    # Update files (excluding user data)
    _update_files(target, ai)

    console.print("\n[bold green]✓ PRD Kit updated successfully![/bold green]")
    console.print("\n[yellow]Note:[/yellow] Your PRDs and product-constitution.md were preserved")


def _update_files(target: Path, ai: str) -> None:
    """Update template files, preserving user data."""
    import shutil

    prd_kit_dir = target / ".prd-kit"

    # Files to update (excludes user data like product-constitution.md and PRDs)
    files_to_update = {
        # Templates (structure only, not user constitution)
        "prd-template.md": prd_kit_dir / "templates" / "prd-template.md",
        "deliverable-template.md": prd_kit_dir / "templates" / "deliverable-template.md",
        "research-template.md": prd_kit_dir / "templates" / "research-template.md",
        "context-template.md": prd_kit_dir / "templates" / "context-template.md",
        "plan-template.md": prd_kit_dir / "templates" / "plan-template.md",
        "tasks-template.md": prd_kit_dir / "templates" / "tasks-template.md",
        "tech-constitution.md": prd_kit_dir / "templates" / "tech-constitution.md",
        # Commands
        "commands/constitution.md": prd_kit_dir / "commands" / "constitution.md",
        "commands/discover.md": prd_kit_dir / "commands" / "discover.md",
        "commands/draft.md": prd_kit_dir / "commands" / "draft.md",
        "commands/refine.md": prd_kit_dir / "commands" / "refine.md",
        "commands/decompose.md": prd_kit_dir / "commands" / "decompose.md",
        "commands/generate-deliverables.md": prd_kit_dir / "commands" / "generate-deliverables.md",
        # Commands - Phase 2 (Technical)
        "commands/init-feature.md": prd_kit_dir / "commands" / "init-feature.md",
        "commands/context.md": prd_kit_dir / "commands" / "context.md",
        "commands/plan.md": prd_kit_dir / "commands" / "plan.md",
        "commands/tasks.md": prd_kit_dir / "commands" / "tasks.md",
        "commands/tech-constitution.md": prd_kit_dir / "commands" / "tech-constitution.md",
        # Validators
        "validators/check-completeness.py": prd_kit_dir / "validators" / "check-completeness.py",
        "validators/check-deliverables.py": prd_kit_dir / "validators" / "check-deliverables.py",
        "validators/generate-implementation-order.py": (
            prd_kit_dir / "validators" / "generate-implementation-order.py"
        ),
        # Python scripts (cross-platform)
        "scripts/prd_scripts/__init__.py": prd_kit_dir / "scripts" / "prd_scripts" / "__init__.py",
        "scripts/prd_scripts/common.py": prd_kit_dir / "scripts" / "prd_scripts" / "common.py",
        "scripts/prd_scripts/setup_constitution.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_constitution.py",
        "scripts/prd_scripts/setup_discover.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_discover.py",
        "scripts/prd_scripts/setup_draft.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_draft.py",
        "scripts/prd_scripts/setup_refine.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_refine.py",
        "scripts/prd_scripts/setup_decompose.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_decompose.py",
        "scripts/prd_scripts/setup_deliverables.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_deliverables.py",
        "scripts/prd_scripts/setup_init_feature.py": prd_kit_dir / "scripts" / "prd_scripts" / "setup_init_feature.py",
    }

    # Agents based on AI type
    if ai == "copilot":
        files_to_update.update({
            "agents/copilot/prd-constitution.agent.md": (
                target / ".github" / "agents" / "prd-constitution.agent.md"
            ),
            "agents/copilot/prd-discover.agent.md": (
                target / ".github" / "agents" / "prd-discover.agent.md"
            ),
            "agents/copilot/prd-draft.agent.md": (
                target / ".github" / "agents" / "prd-draft.agent.md"
            ),
            "agents/copilot/prd-refine.agent.md": (
                target / ".github" / "agents" / "prd-refine.agent.md"
            ),
            "agents/copilot/prd-decompose.agent.md": (
                target / ".github" / "agents" / "prd-decompose.agent.md"
            ),
            "agents/copilot/prd-deliverables.agent.md": (
                target / ".github" / "agents" / "prd-deliverables.agent.md"
            ),
        })

    # Cleanup: Remove obsolete files
    cleaned_count = 0
    
    # Directories that should only contain managed files
    dirs_to_scan = [
        prd_kit_dir / "templates",
        prd_kit_dir / "commands",
        prd_kit_dir / "validators",
        prd_kit_dir / "scripts" / "prd_scripts",
    ]
    
    if ai == "copilot":
        dirs_to_scan.append(target / ".github" / "agents")
    
    # Create set of expected paths for fast lookup
    expected_paths = set(files_to_update.values())
    
    for dir_path in dirs_to_scan:
        if not dir_path.exists():
            continue
            
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                # Skip partial files or hidden files if needed
                if file_path.name.startswith("."):
                    continue
                
                # If file exists on disk but not in our expected list, delete it
                if file_path not in expected_paths:
                    try:
                        file_path.unlink()
                        console.print(f"  Removed: [red]{file_path.relative_to(target)}[/red]")
                        cleaned_count += 1
                    except Exception as e:
                        console.print(f"  [yellow]Failed to remove {file_path.relative_to(target)}: {e}[/yellow]")

    # Copy files
    updated_count = 0
    created_count = 0
    for src_name, dest_path in files_to_update.items():
        src_path = TEMPLATES_DIR / src_name
        if src_path.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            if dest_path.exists():
                shutil.copy2(src_path, dest_path)
                console.print(f"  Updated: [dim]{dest_path.relative_to(target)}[/dim]")
                updated_count += 1
            else:
                shutil.copy2(src_path, dest_path)
                console.print(f"  Created: [green]{dest_path.relative_to(target)}[/green]")
                created_count += 1

    console.print(f"\n[green]Updated {updated_count} files, created {created_count} new files, removed {cleaned_count} obsolete files[/green]")

    # Migration Check: Tech Constitution
    tech_const_dest = prd_kit_dir / "memory" / "tech-constitution.md"
    tech_const_src = prd_kit_dir / "templates" / "tech-constitution.md"
    
    if not tech_const_dest.exists() and tech_const_src.exists():
        shutil.copy2(tech_const_src, tech_const_dest)
        console.print(f"\n[bold blue]Migration Info:[/bold blue] Created [cyan]{tech_const_dest.relative_to(target)}[/cyan]")
        console.print("Please edit this file to define your technical stack and rules.")
