"""
API endpoint for running the kitchen simulator workflow.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from graph import workflow
from state import KitchenSimulatorState

router = APIRouter(prefix="/api/simulate", tags=["simulate"])


class SimulateRequest(BaseModel):
    """Request model for simulation."""
    input: str


class SimulateResponse(BaseModel):
    """Response model for simulation."""
    user_input: str
    parsed_data: dict
    knowledge_base: dict
    recipes: list
    tasks: dict
    schedule: dict
    validation: dict
    conflicts: list
    output: str


@router.post("", response_model=SimulateResponse)
async def simulate(request: SimulateRequest):
    """
    Run the kitchen simulator workflow.
    
    This is PR 3 - workflow skeleton with stub nodes.
    All nodes execute but return placeholder data.
    """
    try:
        # Create initial state
        initial_state: KitchenSimulatorState = {
            "user_input": request.input
        }
        
        # Run workflow
        result = workflow.invoke(initial_state)
        
        # Convert KnowledgeBase to dict for JSON response
        kb_dict = {}
        if result.get("knowledge_base"):
            kb = result["knowledge_base"]
            kb_dict = {
                "kitchen_type": kb.kitchen_type,
                "ovens": [oven.model_dump() for oven in kb.kitchen.ovens],
                "burners": [burner.model_dump() for burner in kb.kitchen.burners],
                "microwaves": [m.model_dump() for m in kb.kitchen.microwaves],
                "chefs": [chef.model_dump() for chef in kb.kitchen.chefs],
            }
        
        return SimulateResponse(
            user_input=result.get("user_input", ""),
            parsed_data=result.get("parsed_data", {}),
            knowledge_base=kb_dict,
            recipes=result.get("recipes", []),
            tasks=result.get("tasks", {}),
            schedule=result.get("schedule", {}),
            validation=result.get("validation", {}),
            conflicts=result.get("conflicts", []),
            output=result.get("output", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow error: {str(e)}")


