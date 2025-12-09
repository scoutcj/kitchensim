"""
Update knowledge base node - merges user overrides with defaults.
Currently a stub that passes data through.
"""

from state import KitchenSimulatorState
from knowledge_base import KnowledgeBase


def update_kb_node(state: KitchenSimulatorState) -> dict:
    """
    Merge user overrides into knowledge base.
    
    TODO (PR 2 integration): Use KnowledgeBase.update() to merge overrides
    """
    # Stub: Create default knowledge base for now
    kb = KnowledgeBase()
    
    # If we have parsed_data with overrides, apply them (will implement in PR 4)
    if state.get("parsed_data") and state["parsed_data"].get("user_overrides"):
        # TODO: kb.update(state["parsed_data"]["user_overrides"])
        pass
    
    return {
        "knowledge_base": kb
    }

