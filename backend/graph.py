"""
LangGraph workflow for Kitchen Simulator.
"""

from typing import Literal
from langgraph.graph import StateGraph, END
from state import KitchenSimulatorState
from nodes import (
    parse_input_node,
    update_kb_node,
    analyze_recipes_node,
    build_dag_node,
    schedule_node,
    validate_node,
    detect_conflicts_node,
    format_output_node,
)


def create_workflow() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Node flow:
    1. parse_input → extracts structured data
    2. update_kb → merges user overrides
    3. analyze_recipes → parses recipes into tasks
    4. build_dag → creates dependency graph
    5. schedule → allocates resources and creates timeline
    6. validate → checks feasibility
    7. detect_conflicts → finds bottlenecks
    8. format_output → creates readable timeline
    """
    workflow = StateGraph(KitchenSimulatorState)
    
    # Add nodes (using different names to avoid conflicts with state attributes)
    workflow.add_node("parse_input", parse_input_node)
    workflow.add_node("update_kb", update_kb_node)
    workflow.add_node("analyze_recipes", analyze_recipes_node)
    workflow.add_node("build_dag", build_dag_node)
    workflow.add_node("schedule_tasks", schedule_node)  # Renamed to avoid conflict with state.schedule
    workflow.add_node("validate", validate_node)
    workflow.add_node("detect_conflicts", detect_conflicts_node)
    workflow.add_node("format_output", format_output_node)
    
    # Define edges (linear flow for now)
    workflow.set_entry_point("parse_input")
    workflow.add_edge("parse_input", "update_kb")
    workflow.add_edge("update_kb", "analyze_recipes")
    workflow.add_edge("analyze_recipes", "build_dag")
    workflow.add_edge("build_dag", "schedule_tasks")
    workflow.add_edge("schedule_tasks", "validate")
    workflow.add_edge("validate", "detect_conflicts")
    workflow.add_edge("detect_conflicts", "format_output")
    workflow.add_edge("format_output", END)
    
    return workflow.compile()


# Create the compiled workflow instance
workflow = create_workflow()

