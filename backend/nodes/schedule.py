"""
Schedule node - creates timeline with resource allocation.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def schedule_node(state: KitchenSimulatorState) -> dict:
    """
    Schedule tasks with resource allocation.
    
    TODO (PR 7): Implement SchedulerAgent to:
    - Topological sort
    - Resource allocation (ovens, chefs, burners)
    - Timeline calculation with buffer times
    """
    # Stub: Return empty schedule for now
    return {
        "schedule": {
            "tasks": [],
            "timeline": {}
        }
    }

