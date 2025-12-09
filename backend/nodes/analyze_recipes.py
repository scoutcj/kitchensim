"""
Analyze recipes node - parses recipes into tasks.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def analyze_recipes_node(state: KitchenSimulatorState) -> dict:
    """
    Analyze recipes and extract tasks with timing, dependencies, resources.
    
    TODO (PR 5): Implement RecipeAgent to extract:
    - Task breakdown (explicit + implicit steps)
    - Duration estimates (from recipe instructions)
    - Dependencies (what must happen before)
    - Resource needs (oven, burner, chef, etc.)
    """
    # Stub: Return empty recipes list for now
    return {
        "recipes": []
    }

