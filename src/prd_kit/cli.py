"""PRD Kit CLI - Main entry point."""

import typer
from rich.console import Console

from prd_kit.commands.init import init_command
from prd_kit.commands.update import update_command
from prd_kit.commands.version import version_command

app = typer.Typer(
    name="prd",
    help="PRD Kit - Product Requirements Document generation with AI agents",
    no_args_is_help=True,
)

console = Console()


@app.command("init")
def init(
    path: str = typer.Argument(
        ".",
        help="Path to initialize the PRD Kit project. Use '.' for current directory.",
    ),
    ai: str = typer.Option(
        "copilot",
        "--ai",
        "-a",
        help="AI agent to configure: copilot, claude",
    ),
    script: str = typer.Option(
        None,
        "--script",
        "-s",
        help="Script type: sh (bash) or ps (powershell). Auto-detected if not specified.",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Initialize in current directory (same as path='.')",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force initialization in non-empty directory",
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip git repository initialization",
    ),
) -> None:
    """Initialize a new PRD Kit project."""
    target_path = "." if here else path
    init_command(
        path=target_path,
        ai=ai,
        script=script,
        force=force,
        no_git=no_git,
    )


@app.command("update")
def update(
    ai: str = typer.Option(
        None,
        "--ai",
        "-a",
        help="AI agent to update: copilot, claude. Auto-detected if not specified.",
    ),
    script: str = typer.Option(
        None,
        "--script",
        "-s",
        help="Script type: sh (bash) or ps (powershell). Auto-detected if not specified.",
    ),
) -> None:
    """Update PRD Kit templates and agents in current project."""
    update_command(ai=ai, script=script)


@app.command("
@app.command("version")
def version() -> None:
    """Show PRD Kit version."""
    version_command()


if __name__ == "__main__":
    app()
