"""
State model for Kitchen Simulator LangGraph workflow.
"""

from typing import TypedDict, List, Optional, Dict, Any
from knowledge_base import KnowledgeBase, Kitchen


class ParsedData(TypedDict, total=False):
    """Structured data extracted from user input."""
    event_details: Dict[str, Any]  # date, time, guest_count, event_type
    recipes_text: List[str]  # Raw recipe text/menu items
    constraints: Dict[str, Any]  # staff, equipment
    user_overrides: Dict[str, Any]  # User-specified kitchen config changes


class Recipe(TypedDict, total=False):
    """Parsed recipe with tasks."""
    recipe_name: str
    servings: int
    tasks: List[Dict[str, Any]]  # Task breakdown with timing, dependencies, resources


class TaskDAG(TypedDict, total=False):
    """Unified dependency graph of all tasks."""
    nodes: List[Dict[str, Any]]  # All tasks from all recipes
    edges: List[tuple]  # Dependency edges (task_id, task_id)


class Schedule(TypedDict, total=False):
    """Final timeline with resource assignments."""
    tasks: List[Dict[str, Any]]  # Tasks with start/end times, resource assignments
    timeline: Dict[str, Any]  # Timeline structure


class Conflict(TypedDict, total=False):
    """Detected bottleneck or risk."""
    type: str  # "resource_overload", "timing_issue", "insufficient_resources"
    message: str
    severity: str  # "warning", "error"
    task_ids: List[str]


class ValidationResult(TypedDict, total=False):
    """LLM validation result."""
    feasible: bool
    risk_level: str  # "low", "medium", "high"
    answers: Dict[str, str]  # Answers to user questions
    suggestions: List[str]


class KitchenSimulatorState(TypedDict, total=False):
    """
    State schema for LangGraph workflow.
    
    All fields are optional to allow incremental updates.
    """
    user_input: str  # Raw natural language input
    parsed_data: Optional[ParsedData]  # Structured data from parser
    knowledge_base: Optional[KnowledgeBase]  # Static kitchen info (equipment, staff)
    recipes: Optional[List[Recipe]]  # Parsed recipes with tasks
    tasks: Optional[TaskDAG]  # Unified dependency graph
    schedule: Optional[Schedule]  # Final timeline with resource assignments
    conflicts: Optional[List[Conflict]]  # Detected bottlenecks/risks
    validation: Optional[ValidationResult]  # LLM validation + answers
    output: Optional[str]  # Formatted text timeline

