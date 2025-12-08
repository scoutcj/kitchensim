"""
API endpoints for knowledge base management.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from knowledge_base import KnowledgeBase

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


class KitchenUpdateRequest(BaseModel):
    """Request model for updating kitchen configuration."""
    overrides: Dict[str, Any]
    kitchen_type: Optional[str] = None


class KitchenResponse(BaseModel):
    """Response model for kitchen configuration."""
    kitchen_type: str
    ovens: list
    burners: list
    microwaves: list
    chefs: list


# Global knowledge base instance (session-scoped in real usage)
_kb: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    """Get or create knowledge base instance."""
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
    return _kb


@router.get("/kitchen", response_model=KitchenResponse)
async def get_kitchen():
    """Get current kitchen configuration."""
    kb = get_knowledge_base()
    kitchen = kb.get_kitchen()
    
    return KitchenResponse(
        kitchen_type=kb.kitchen_type,
        ovens=[oven.model_dump() for oven in kitchen.ovens],
        burners=[burner.model_dump() for burner in kitchen.burners],
        microwaves=[microwave.model_dump() for microwave in kitchen.microwaves],
        chefs=[chef.model_dump() for chef in kitchen.chefs],
    )


@router.post("/kitchen/update", response_model=KitchenResponse)
async def update_kitchen(request: KitchenUpdateRequest):
    """Update kitchen configuration with user overrides."""
    kb = get_knowledge_base()
    
    # Reset to different kitchen type if specified
    if request.kitchen_type and request.kitchen_type != kb.kitchen_type:
        kb.kitchen_type = request.kitchen_type
        kb.reset_to_defaults(request.kitchen_type)
    
    # Apply overrides
    try:
        kitchen = kb.update(request.overrides)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update kitchen: {str(e)}")
    
    return KitchenResponse(
        kitchen_type=kb.kitchen_type,
        ovens=[oven.model_dump() for oven in kitchen.ovens],
        burners=[burner.model_dump() for burner in kitchen.burners],
        microwaves=[microwave.model_dump() for microwave in kitchen.microwaves],
        chefs=[chef.model_dump() for chef in kitchen.chefs],
    )


@router.post("/kitchen/reset")
async def reset_kitchen(kitchen_type: Optional[str] = None):
    """Reset kitchen to default configuration."""
    kb = get_knowledge_base()
    kitchen = kb.reset_to_defaults(kitchen_type)
    
    return KitchenResponse(
        kitchen_type=kb.kitchen_type,
        ovens=[oven.model_dump() for oven in kitchen.ovens],
        burners=[burner.model_dump() for burner in kitchen.burners],
        microwaves=[microwave.model_dump() for microwave in kitchen.microwaves],
        chefs=[chef.model_dump() for chef in kitchen.chefs],
    )

