#!/usr/bin/env python3
"""
PRD Kit - Implementation Order Generator

Generates a topologically sorted implementation order from deliverables-map.json.
Respects dependencies and identifies what can be parallelized.

Usage:
    python generate-implementation-order.py <deliverables_map_path>
    python generate-implementation-order.py prds/feature-name/deliverables/deliverables-map.json
"""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple


class ImplementationPhase(NamedTuple):
    """A phase of implementation."""
    phase_num: int
    deliverables: list[str]
    parallel: bool


def load_deliverables_map(map_path: Path) -> dict | None:
    """Load deliverables map."""
    try:
        with open(map_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def topological_sort_with_levels(deliverables: list[dict]) -> list[ImplementationPhase]:
    """
    Perform topological sort and group deliverables into phases.
    Deliverables in the same phase can be parallelized.
    """
    # Build graph
    graph: dict[str, list[str]] = {}
    in_degree: dict[str, int] = {}
    id_to_deliverable: dict[str, dict] = {}
    
    for d in deliverables:
        d_id = d.get("id", "")
        deps = d.get("dependencies", [])
        graph[d_id] = []
        in_degree[d_id] = len(deps)
        id_to_deliverable[d_id] = d
    
    # Build reverse edges (for tracking what depends on what)
    for d in deliverables:
        d_id = d.get("id", "")
        for dep in d.get("dependencies", []):
            if dep in graph:
                graph[dep].append(d_id)
    
    # Kahn's algorithm with level tracking
    phases: list[ImplementationPhase] = []
    
    # Start with nodes that have no dependencies
    current_level = [d_id for d_id, degree in in_degree.items() if degree == 0]
    phase_num = 1
    
    while current_level:
        # All items in current_level can be done in parallel
        phases.append(ImplementationPhase(
            phase_num=phase_num,
            deliverables=sorted(current_level),
            parallel=len(current_level) > 1,
        ))
        
        # Find next level
        next_level = []
        for d_id in current_level:
            for dependent in graph[d_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    next_level.append(dependent)
        
        current_level = next_level
        phase_num += 1
    
    # Check for cycles (if not all nodes were processed)
    processed = sum(len(p.deliverables) for p in phases)
    if processed < len(deliverables):
        # There's a cycle - return empty (validation should catch this)
        return []
    
    return phases


def generate_order(map_path: Path) -> dict:
    """Generate implementation order from map."""
    map_data = load_deliverables_map(map_path)
    
    if map_data is None:
        return {
            "success": False,
            "error": "Failed to load deliverables map",
            "phases": [],
        }
    
    deliverables = map_data.get("deliverables", [])
    
    if not deliverables:
        return {
            "success": False,
            "error": "No deliverables found",
            "phases": [],
        }
    
    phases = topological_sort_with_levels(deliverables)
    
    if not phases and deliverables:
        return {
            "success": False,
            "error": "Circular dependencies detected",
            "phases": [],
        }
    
    # Build detailed output
    id_to_deliverable = {d["id"]: d for d in deliverables}
    
    phase_details = []
    for phase in phases:
        phase_info = {
            "phase": phase.phase_num,
            "parallel": phase.parallel,
            "deliverables": [],
        }
        
        for d_id in phase.deliverables:
            d = id_to_deliverable.get(d_id, {})
            phase_info["deliverables"].append({
                "id": d_id,
                "name": d.get("name", ""),
                "title": d.get("title", ""),
                "file": d.get("file", ""),
                "priority": d.get("priority", "medium"),
            })
        
        phase_details.append(phase_info)
    
    return {
        "success": True,
        "source": str(map_path),
        "total_deliverables": len(deliverables),
        "total_phases": len(phases),
        "phases": phase_details,
    }


def format_human_readable(order: dict) -> str:
    """Format order for human reading."""
    if not order.get("success"):
        return f"Error: {order.get('error', 'Unknown error')}"
    
    lines = [
        "=" * 60,
        "IMPLEMENTATION ORDER",
        "=" * 60,
        f"Total Deliverables: {order['total_deliverables']}",
        f"Total Phases: {order['total_phases']}",
        "",
    ]
    
    for phase in order["phases"]:
        parallel_marker = " (can be parallel)" if phase["parallel"] else ""
        lines.append(f"Phase {phase['phase']}{parallel_marker}:")
        
        for d in phase["deliverables"]:
            lines.append(f"  [{d['id']}] {d['title']}")
            lines.append(f"       File: {d['file']}")
            lines.append(f"       Priority: {d['priority']}")
        
        lines.append("")
    
    # Generate commands
    lines.append("=" * 60)
    lines.append("SPEC KIT COMMANDS (in order):")
    lines.append("=" * 60)
    
    for phase in order["phases"]:
        for d in phase["deliverables"]:
            name = d["name"] or d["id"]
            lines.append(f"specify init specs/{name}")
    
    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate-implementation-order.py <map_path>", file=sys.stderr)
        return 1
    
    map_path = Path(sys.argv[1])
    order = generate_order(map_path)
    
    # JSON output
    print(json.dumps(order, indent=2))
    
    # Human-readable output to stderr
    print("\n" + format_human_readable(order), file=sys.stderr)
    
    return 0 if order.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
