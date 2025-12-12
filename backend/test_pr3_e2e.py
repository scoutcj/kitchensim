#!/usr/bin/env python3
"""
End-to-end test script for PR 3: LangGraph State & Skeleton

Run this to test the workflow with real input.
Usage: python test_pr3_e2e.py
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from graph import workflow
from state import KitchenSimulatorState
import json


def test_workflow_e2e(user_input: str):
    """Test workflow end-to-end with user input."""
    print(f"\n{'='*60}")
    print("🧪 Testing PR 3: LangGraph Workflow (Stub Nodes)")
    print(f"{'='*60}\n")
    
    print(f"📥 Input: {user_input}\n")
    
    # Create initial state
    initial_state: KitchenSimulatorState = {
        "user_input": user_input
    }
    
    # Run workflow
    print("🔄 Running workflow through all 8 nodes...\n")
    result = workflow.invoke(initial_state)
    
    # Display results
    print("📊 Workflow Results:")
    print("-" * 60)
    
    print(f"\n1️⃣  Parsed Data:")
    print(json.dumps(result.get("parsed_data", {}), indent=2))
    
    print(f"\n2️⃣  Knowledge Base:")
    if result.get("knowledge_base"):
        kb = result["knowledge_base"]
        print(f"   Kitchen Type: {kb.kitchen_type}")
        print(f"   Ovens: {len(kb.kitchen.ovens)}")
        print(f"   Burners: {len(kb.kitchen.burners)}")
        print(f"   Microwaves: {len(kb.kitchen.microwaves)}")
        print(f"   Chefs: {len(kb.kitchen.chefs)}")
    
    print(f"\n3️⃣  Recipes:")
    print(json.dumps(result.get("recipes", []), indent=2))
    
    print(f"\n4️⃣  Tasks (DAG):")
    print(json.dumps(result.get("tasks", {}), indent=2))
    
    print(f"\n5️⃣  Schedule:")
    print(json.dumps(result.get("schedule", {}), indent=2))
    
    print(f"\n6️⃣  Validation:")
    print(json.dumps(result.get("validation", {}), indent=2))
    
    print(f"\n7️⃣  Conflicts:")
    print(json.dumps(result.get("conflicts", []), indent=2))
    
    print(f"\n8️⃣  Output:")
    print(result.get("output", ""))
    
    print(f"\n{'='*60}")
    print("✅ Workflow completed! All 8 nodes executed.")
    print(f"{'='*60}\n")
    
    return result


if __name__ == "__main__":
    # Test with sample input
    test_input = "Dinner for 4 people. Make pasta with sauce and garlic bread."
    
    if len(sys.argv) > 1:
        test_input = " ".join(sys.argv[1:])
    
    test_workflow_e2e(test_input)


