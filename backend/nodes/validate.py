"""
Validate node - checks if schedule makes sense.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def validate_node(state: KitchenSimulatorState) -> dict:
    """
    Validate schedule and answer user questions.
    
    TODO (PR 8): Implement LLM validation to:
    - Check if schedule makes sense
    - Answer feasibility questions
    - Provide suggestions
    """
    # Stub: Return default validation for now
    return {
        "validation": {
            "feasible": True,
            "risk_level": "low",
            "answers": {},
            "suggestions": []
        }
    }

