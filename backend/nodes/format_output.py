"""
Format output node - creates readable text timeline.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def format_output_node(state: KitchenSimulatorState) -> dict:
    """
    Format schedule into readable text timeline.
    
    TODO (PR 9): Implement formatter to create:
    - Timeline grouped by time
    - Resource assignments
    - Conflict warnings
    - Buffer times and service windows
    """
    # Stub: Return placeholder output for now
    return {
        "output": "Timeline will be generated here..."
    }

