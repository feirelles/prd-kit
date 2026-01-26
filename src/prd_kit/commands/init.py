"""Init command implementation."""

import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console

console = Console()

# Paths relative to the package
PACKAGE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = PACKAGE_DIR / "templates"

# PRD Kit ASCII Art
PRD_KIT_BANNER = """
[bold cyan]
██████╗ ██████╗ ██████╗     ██╗  ██╗██╗████████╗
██╔══██╗██╔══██╗██╔══██╗    ██║ ██╔╝██║╚══██╔══╝
██████╔╝██████╔╝██║  ██║    █████╔╝ ██║   ██║   
██╔═══╝ ██╔══██╗██║  ██║    ██╔═██╗ ██║   ██║   
██║     ██║  ██║██████╔╝    ██║  ██╗██║   ██║   
╚═╝     ╚═╝  ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝   ╚═╝   
[/bold cyan]
[dim]  Product Requirements Document Generation with AI[/dim]
"""


def init_command(
    path: str,
    ai: str,
    script: str | None,
    force: bool,
    no_git: bool,
) -> None:
    """Initialize a new PRD Kit project."""
    target = Path(path).resolve()

    # Print banner
    console.print(PRD_KIT_BANNER)

    # Validate AI option
    supported_ai = ["copilot", "claude"]
    if ai not in supported_ai:
        console.print(f"[red]Error:[/red] Unsupported AI agent: {ai}")
        console.print(f"Supported agents: {', '.join(supported_ai)}")
        raise SystemExit(1)

    # Script type is now always Python (cross-platform)
    # The --script option is kept for backward compatibility but ignored
    if script is not None:
        console.print(f"[yellow]Note:[/yellow] --script option is deprecated. Python scripts are now used for cross-platform support.")

    # Check if directory exists and is not empty
    if target.exists():
        contents = list(target.iterdir())
        # Filter out hidden files for emptiness check
        visible_contents = [c for c in contents if not c.name.startswith(".")]
        if visible_contents:
            if not force:
                # Prompt user for confirmation
                console.print(f"\n[yellow]Warning:[/yellow] Current directory is not empty ({len(visible_contents)} items)")
                console.print("Template files will be merged with existing content and may overwrite existing files")
                
                if not typer.confirm("Do you want to continue?", default=False):
                    console.print("[dim]Initialization cancelled[/dim]")
                    raise SystemExit(0)
    else:
        target.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold blue]Initializing PRD Kit[/bold blue] in {target}")
    console.print(f"  AI Agent: [green]{ai}[/green]")
    console.print(f"  Scripts: [green]Python (cross-platform)[/green]")

    # Create directory structure
    _create_directory_structure(target, ai)

    # Initialize git if requested
    if not no_git:
        _init_git(target)

    console.print("\n[bold green]✓ PRD Kit initialized successfully![/bold green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Edit [cyan].prd-kit/memory/product-constitution.md[/cyan] with your product principles")
    console.print("  2. Start a new PRD with [cyan]@prd-discover[/cyan] in your AI assistant")


def _create_directory_structure(target: Path, ai: str) -> None:
    """Create the PRD Kit directory structure."""
    # .prd-kit structure
    prd_kit_dir = target / ".prd-kit"

    dirs_to_create = [
        prd_kit_dir / "memory",
        prd_kit_dir / "templates",
        prd_kit_dir / "commands",
        prd_kit_dir / "validators",
        prd_kit_dir / "scripts" / "prd_scripts",
        target / "prds",
    ]

    # AI-specific directories
    if ai == "copilot":
        dirs_to_create.append(target / ".github" / "agents")
    elif ai == "claude":
        dirs_to_create.append(target / ".claude" / "commands")

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        console.print(f"  Created: [dim]{dir_path.relative_to(target)}[/dim]")

    # Copy template files
    _copy_templates(target, ai)


def _copy_templates(target: Path, ai: str) -> None:
    """Copy template files to the target directory."""
    prd_kit_dir = target / ".prd-kit"

    # Template mappings: source -> destination
    template_files = {
        # Memory
        "memory/product-constitution.md": prd_kit_dir / "memory" / "product-constitution.md",
        "tech-constitution.md": prd_kit_dir / "templates" / "tech-constitution.md",
        # Templates
        "prd-template.md": prd_kit_dir / "templates" / "prd-template.md",
        "deliverable-template.md": prd_kit_dir / "templates" / "deliverable-template.md",
        "research-template.md": prd_kit_dir / "templates" / "research-template.md",
        "context-template.md": prd_kit_dir / "templates" / "context-template.md",
        "plan-template.md": prd_kit_dir / "templates" / "plan-template.md",
        "tasks-template.md": prd_kit_dir / "templates" / "tasks-template.md",
        # Commands - Phase 1 (Client-facing)
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
    }

    # Python scripts (cross-platform)
    script_templates = {
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

    # Agent files based on AI type
    agent_templates = {
        "copilot": {
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
        },
        "claude": {
            "agents/claude/CLAUDE.md": target / "CLAUDE.md",
        },
    }

    # Copy all template files
    all_templates = {
        **template_files,
        **script_templates,
        **agent_templates.get(ai, {}),
    }

    for src_name, dest_path in all_templates.items():
        src_path = TEMPLATES_DIR / src_name
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            console.print(f"  Copied: [dim]{dest_path.relative_to(target)}[/dim]")
        else:
            # Create placeholder if template doesn't exist yet
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(f"# TODO: Template content for {src_name}\n")
            console.print(f"  Created placeholder: [yellow]{dest_path.relative_to(target)}[/yellow]")

    # Create AGENTS.md
    agents_md = target / "AGENTS.md"
    agents_content = _generate_agents_md(ai)
    agents_md.write_text(agents_content)
    console.print(f"  Created: [dim]AGENTS.md[/dim]")

    # Create .gitkeep in prds/
    (target / "prds" / ".gitkeep").touch()

    # Create README.md
    readme = target / "README.md"
    if not readme.exists():
        readme.write_text(_generate_readme())
        console.print(f"  Created: [dim]README.md[/dim]")


def _generate_agents_md(ai: str) -> str:
    """Generate AGENTS.md content."""
    return f"""# PRD Kit Agents

This project uses PRD Kit for Product Requirements Document generation.

## Available Agents

| Agent | Description |
|-------|-------------|
| `@prd-constitution` | Set up product principles, personas, and constraints (run first!) |
| `@prd-discover` | Start discovery phase - interview to understand the product idea |
| `@prd-draft` | Generate PRD draft from research notes |
| `@prd-refine` | Refine and validate PRD against constitution |
| `@prd-decompose` | Decompose PRD into technical deliverables |
| `@prd-deliverables` | Generate deliverable files for Spec Kit |

## Workflow

1. **Constitution**: `@prd-constitution` - Define product principles (one-time setup)
2. **Discovery**: `@prd-discover` - Describe your product idea
3. **Draft**: `@prd-draft` - Generate initial PRD
4. **Refine**: `@prd-refine` - Validate and improve PRD
5. **Decompose**: `@prd-decompose` - Break into deliverables
6. **Generate**: `@prd-deliverables` - Create deliverable files

## Configuration

- AI Agent: **{ai}**
- Constitution: `.prd-kit/memory/product-constitution.md`
- Templates: `.prd-kit/templates/`
- Commands: `.prd-kit/commands/`

## Handoff to Spec Kit

After generating deliverables, use each `deliverable-XXX.md` file to initialize
a spec in Spec Kit:

```bash
specify init specs/[deliverable-name]
# When asked "What should I build?", provide the deliverable file content
```
"""


def _generate_readme() -> str:
    """Generate README.md content."""
    return """# PRD Kit Project

This project uses [PRD Kit](https://github.com/feirelles/prd-kit) for Product Requirements Document generation with AI agents.

## Getting Started

1. Edit `.prd-kit/memory/product-constitution.md` with your product principles
2. Start a new PRD by invoking `@prd-discover` in your AI assistant
3. Follow the workflow: Discover → Draft → Refine → Decompose → Deliverables

## Directory Structure

```
.prd-kit/
├── memory/
│   └── product-constitution.md   # Your product principles
├── templates/                     # Document templates
├── commands/                      # Agent command definitions
├── validators/                    # Validation scripts
└── scripts/
    └── prd_scripts/              # Python setup scripts (cross-platform)

prds/
└── [feature-name]/
    ├── research.md               # Discovery notes
    ├── PRD.md                    # Product Requirements Document
    └── deliverables/
        ├── deliverables-map.json
        └── deliverable-XXX.md    # Technical deliverables
```

## Documentation

See [AGENTS.md](AGENTS.md) for available AI agents and workflow details.
"""


def _init_git(target: Path) -> None:
    """Initialize a git repository if not already initialized."""
    git_dir = target / ".git"
    if git_dir.exists():
        console.print("  [dim]Git repository already exists[/dim]")
        return

    try:
        subprocess.run(
            ["git", "init"],
            cwd=target,
            check=True,
            capture_output=True,
        )
        console.print("  [green]Initialized git repository[/green]")

        # Create .gitignore
        gitignore = target / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                """# PRD Kit
*.pyc
__pycache__/
.env
.venv/
*.egg-info/
dist/
build/
"""
            )
            console.print("  Created: [dim].gitignore[/dim]")

    except FileNotFoundError:
        console.print("  [yellow]Warning: git not found, skipping repository init[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"  [yellow]Warning: git init failed: {e}[/yellow]")
