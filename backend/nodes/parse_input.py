"""
Parse input node - extracts structured data from natural language.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState


def parse_input_node(state: KitchenSimulatorState) -> dict:
    """
    Parse user input into structured data.
    
    TODO (PR 4): Implement ParserAgent to extract:
    - Event details (date, time, guest count, event type)
    - Recipe text/menu items
    - Constraints (staff, equipment)
    - User knowledge base overrides
    """
    # Stub: Just pass through for now
    return {
        "parsed_data": {
            "event_details": {"guest_count": 0},
            "recipes_text": [],
            "constraints": {},
            "user_overrides": {}
        }
    }

