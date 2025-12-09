"""
Build DAG node - converts recipes into unified dependency graph.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def build_dag_node(state: KitchenSimulatorState) -> dict:
    """
    Build unified dependency graph from all recipe tasks.
    
    TODO (PR 6): Implement TaskDAG builder to:
    - Flatten all tasks from all recipes
    - Build dependency edges
    - Validate no cycles
    """
    # Stub: Return empty DAG for now
    return {
        "tasks": {
            "nodes": [],
            "edges": []
        }
    }

