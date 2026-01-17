"""Version command implementation."""

from rich.console import Console

from prd_kit import __version__

console = Console()


def version_command() -> None:
    """Display the current PRD Kit version."""
    console.print(f"[bold blue]PRD Kit[/bold blue] version [green]{__version__}[/green]")
