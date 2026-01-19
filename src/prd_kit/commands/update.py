"""Update command implementation."""

from pathlib import Path

from rich.console import Console

from prd_kit.commands.init import (
    PACKAGE_DIR,
    TEMPLATES_DIR,
    detect_shell,
    _make_scripts_executable,
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

    if script is None:
        script = detect_shell()

    console.print(f"  AI Agent: [green]{ai}[/green]")
    console.print(f"  Script type: [green]{script}[/green]")

    # Update files (excluding user data)
    _update_files(target, ai, script)
    
    # Make bash scripts executable
    _make_scripts_executable(target, script)

    console.print("\n[bold green]✓ PRD Kit updated successfully![/bold green]")
    console.print("\n[yellow]Note:[/yellow] Your PRDs and product-constitution.md were preserved")


def _update_files(target: Path, ai: str, script: str) -> None:
    """Update template files, preserving user data."""
    import shutil

    prd_kit_dir = target / ".prd-kit"

    # Files to update (excludes user data like product-constitution.md and PRDs)
    files_to_update = {
        # Templates (structure only, not user constitution)
        "prd-template.md": prd_kit_dir / "templates" / "prd-template.md",
        "deliverable-template.md": prd_kit_dir / "templates" / "deliverable-template.md",
        "research-template.md": prd_kit_dir / "templates" / "research-template.md",
        # Commands
        "commands/constitution.md": prd_kit_dir / "commands" / "constitution.md",
        "commands/discover.md": prd_kit_dir / "commands" / "discover.md",
        "commands/draft.md": prd_kit_dir / "commands" / "draft.md",
        "commands/refine.md": prd_kit_dir / "commands" / "refine.md",
        "commands/decompose.md": prd_kit_dir / "commands" / "decompose.md",
        "commands/generate-deliverables.md": prd_kit_dir / "commands" / "generate-deliverables.md",
        # Validators
        "validators/check-completeness.py": prd_kit_dir / "validators" / "check-completeness.py",
        "validators/check-deliverables.py": prd_kit_dir / "validators" / "check-deliverables.py",
        "validators/generate-implementation-order.py": (
            prd_kit_dir / "validators" / "generate-implementation-order.py"
        ),
    }

    # Scripts based on type
    if script == "sh":
        files_to_update.update({
            "scripts/bash/common.sh": prd_kit_dir / "scripts" / "bash" / "common.sh",
            "scripts/bash/setup-constitution.sh": prd_kit_dir / "scripts" / "bash" / "setup-constitution.sh",
            "scripts/bash/setup-discover.sh": prd_kit_dir / "scripts" / "bash" / "setup-discover.sh",
            "scripts/bash/setup-draft.sh": prd_kit_dir / "scripts" / "bash" / "setup-draft.sh",
            "scripts/bash/setup-refine.sh": prd_kit_dir / "scripts" / "bash" / "setup-refine.sh",
            "scripts/bash/setup-decompose.sh": prd_kit_dir / "scripts" / "bash" / "setup-decompose.sh",
            "scripts/bash/setup-deliverables.sh": prd_kit_dir / "scripts" / "bash" / "setup-deliverables.sh",
        })

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

    console.print(f"\n[green]Updated {updated_count} files, created {created_count} new files[/green]")
