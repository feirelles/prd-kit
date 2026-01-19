#!/usr/bin/env python3
"""PRD Kit - Common functions and configuration."""

import re
import sys
from pathlib import Path


# ============================================================================
# Color Output (cross-platform)
# ============================================================================
class Colors:
    """ANSI color codes for terminal output."""
    
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color
    
    @classmethod
    def disable(cls):
        """Disable colors for non-TTY output."""
        cls.RED = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.BLUE = ""
        cls.NC = ""


# Disable colors if not a TTY
if not sys.stdout.isatty():
    Colors.disable()


def log_info(message: str) -> None:
    """Log an info message."""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def log_success(message: str) -> None:
    """Log a success message."""
    print(f"{Colors.GREEN}[OK]{Colors.NC} {message}")


def log_warn(message: str) -> None:
    """Log a warning message."""
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {message}")


def log_error(message: str) -> None:
    """Log an error message to stderr."""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)


# ============================================================================
# Path Configuration
# ============================================================================
class PRDKitPaths:
    """Path configuration for PRD Kit project."""
    
    def __init__(self, project_root: Path | None = None):
        """Initialize paths from project root.
        
        Args:
            project_root: The project root directory. If None, searches
                         upward from CWD to find .prd-kit directory.
        """
        if project_root is None:
            project_root = self._find_project_root()
        
        self.project_root = project_root
        self.prd_kit_dir = project_root / ".prd-kit"
        self.prds_dir = project_root / "prds"
        self.memory_dir = self.prd_kit_dir / "memory"
        self.templates_dir = self.prd_kit_dir / "templates"
        self.commands_dir = self.prd_kit_dir / "commands"
        self.validators_dir = self.prd_kit_dir / "validators"
        self.scripts_dir = self.prd_kit_dir / "scripts"
    
    def _find_project_root(self) -> Path:
        """Find project root by looking for .prd-kit directory."""
        current = Path.cwd()
        
        while current != current.parent:
            if (current / ".prd-kit").is_dir():
                return current
            current = current.parent
        
        # Fall back to CWD
        return Path.cwd()
    
    # Feature paths
    def get_feature_dir(self, feature_name: str) -> Path:
        """Get the directory for a feature."""
        return self.prds_dir / feature_name
    
    def get_research_file(self, feature_name: str) -> Path:
        """Get the research file path for a feature."""
        return self.get_feature_dir(feature_name) / "research.md"
    
    def get_prd_file(self, feature_name: str) -> Path:
        """Get the PRD file path for a feature."""
        return self.get_feature_dir(feature_name) / "PRD.md"
    
    def get_deliverables_dir(self, feature_name: str) -> Path:
        """Get the deliverables directory for a feature."""
        return self.get_feature_dir(feature_name) / "deliverables"
    
    def get_deliverables_map(self, feature_name: str) -> Path:
        """Get the deliverables map file path for a feature."""
        return self.get_deliverables_dir(feature_name) / "deliverables-map.json"
    
    # Constitution paths
    @property
    def constitution_file(self) -> Path:
        """Get the product constitution file path."""
        return self.memory_dir / "product-constitution.md"
    
    @property
    def constitution_template(self) -> Path:
        """Get the constitution template file path."""
        return self.templates_dir / "product-constitution.md"
    
    # Spec Kit integration
    @property
    def tech_constitution_file(self) -> Path:
        """Get the technical constitution file path (Spec Kit)."""
        return self.project_root / ".specify" / "memory" / "constitution.md"


# ============================================================================
# Validation Functions
# ============================================================================
def check_prd_kit_initialized(paths: PRDKitPaths | None = None) -> PRDKitPaths:
    """Check if PRD Kit is initialized and return paths.
    
    Args:
        paths: Optional PRDKitPaths instance.
        
    Returns:
        PRDKitPaths instance if initialized.
        
    Raises:
        SystemExit: If PRD Kit is not initialized.
    """
    if paths is None:
        paths = PRDKitPaths()
    
    if not paths.prd_kit_dir.is_dir():
        log_error("PRD Kit not initialized. Run 'prd init' first.")
        sys.exit(1)
    
    return paths


def check_feature_exists(paths: PRDKitPaths, feature_name: str) -> bool:
    """Check if a feature directory exists."""
    return paths.get_feature_dir(feature_name).is_dir()


def check_file_exists(file_path: Path, description: str) -> bool:
    """Check if a file exists and print status."""
    if file_path.is_file():
        print(f"  ✓ {description}")
        return True
    else:
        print(f"  ✗ {description}")
        return False


# ============================================================================
# Feature Status
# ============================================================================
def get_feature_status(paths: PRDKitPaths, feature_name: str) -> str:
    """Get the current status of a feature.
    
    Returns one of:
        - not_started
        - discovery_in_progress
        - discovery_complete
        - drafted
        - approved
        - decomposed
        - deliverables_generated
    """
    feature_dir = paths.get_feature_dir(feature_name)
    
    if not feature_dir.is_dir():
        return "not_started"
    
    research_file = paths.get_research_file(feature_name)
    prd_file = paths.get_prd_file(feature_name)
    deliverables_map = paths.get_deliverables_map(feature_name)
    deliverables_dir = paths.get_deliverables_dir(feature_name)
    
    # Check for deliverable files
    if deliverables_dir.is_dir():
        deliverable_files = list(deliverables_dir.glob("deliverable-*.md"))
        if deliverable_files:
            return "deliverables_generated"
    
    if deliverables_map.is_file():
        return "decomposed"
    
    if prd_file.is_file():
        try:
            content = prd_file.read_text()
            if re.search(r"Status.*Approved", content):
                return "approved"
        except Exception:
            pass
        return "drafted"
    
    if research_file.is_file():
        try:
            content = research_file.read_text()
            if "[NEEDS_DETAIL:" in content:
                return "discovery_in_progress"
        except Exception:
            pass
        return "discovery_complete"
    
    return "not_started"


# ============================================================================
# Template Functions
# ============================================================================
def copy_template(paths: PRDKitPaths, template_name: str, dest_path: Path) -> bool:
    """Copy a template file to destination.
    
    Args:
        paths: PRDKitPaths instance.
        template_name: Name of the template file.
        dest_path: Destination path.
        
    Returns:
        True if successful, False otherwise.
    """
    template_path = paths.templates_dir / template_name
    
    if template_path.is_file():
        import shutil
        shutil.copy2(template_path, dest_path)
        log_success(f"Created: {dest_path}")
        return True
    else:
        log_error(f"Template not found: {template_path}")
        return False


def list_available_docs(paths: PRDKitPaths, feature_name: str) -> list[str]:
    """List available documentation files for a feature."""
    feature_dir = paths.get_feature_dir(feature_name)
    docs = []
    
    if (feature_dir / "research.md").is_file():
        docs.append("research.md")
    
    if (feature_dir / "PRD.md").is_file():
        docs.append("PRD.md")
    
    deliverables_dir = paths.get_deliverables_dir(feature_name)
    
    if (deliverables_dir / "deliverables-map.json").is_file():
        docs.append("deliverables-map.json")
    
    if deliverables_dir.is_dir():
        for f in deliverables_dir.glob("deliverable-*.md"):
            docs.append(f.name)
    
    return docs


if __name__ == "__main__":
    # Quick test
    paths = PRDKitPaths()
    print(f"Project root: {paths.project_root}")
    print(f"PRD Kit dir: {paths.prd_kit_dir}")
    print(f"Initialized: {paths.prd_kit_dir.is_dir()}")
