"""
Detect conflicts node - finds bottlenecks and risks.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def detect_conflicts_node(state: KitchenSimulatorState) -> dict:
    """
    Detect conflicts, bottlenecks, and risks.
    
    TODO (PR 8): Implement ConflictAgent to find:
    - Overlapping resource usage
    - Insufficient resources
    - Tasks that can't finish in time
    - Critical path bottlenecks
    """
    # Stub: Return empty conflicts list for now
    return {
        "conflicts": []
    }

