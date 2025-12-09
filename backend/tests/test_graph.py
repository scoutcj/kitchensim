"""
Test LangGraph workflow with mock data.
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from graph import workflow
from state import KitchenSimulatorState


def test_workflow_with_mock_data():
    """Test that workflow runs and data flows through all nodes."""
    # Create mock initial state
    initial_state: KitchenSimulatorState = {
        "user_input": "Dinner for 4 people. Make pasta with sauce."
    }
    
    # Run workflow
    result = workflow.invoke(initial_state)
    
    # Verify all nodes executed and state was updated
    assert "user_input" in result
    assert result["user_input"] == "Dinner for 4 people. Make pasta with sauce."
    
    # Verify parsed_data was created (even if stub)
    assert "parsed_data" in result
    
    # Verify knowledge_base was created
    assert "knowledge_base" in result
    
    # Verify recipes was created (even if empty)
    assert "recipes" in result
    
    # Verify tasks was created (even if empty)
    assert "tasks" in result
    
    # Verify schedule was created (even if empty)
    assert "schedule" in result
    
    # Verify validation was created
    assert "validation" in result
    
    # Verify conflicts was created (even if empty)
    assert "conflicts" in result
    
    # Verify output was created
    assert "output" in result
    assert result["output"] == "Timeline will be generated here..."
    
    print("✅ All nodes executed successfully!")
    print(f"Final state keys: {list(result.keys())}")


def test_workflow_data_flow():
    """Test that data flows correctly through nodes."""
    initial_state: KitchenSimulatorState = {
        "user_input": "Test input"
    }
    
    result = workflow.invoke(initial_state)
    
    # Verify data was passed through
    assert result["user_input"] == "Test input"
    assert result["parsed_data"] is not None
    assert result["knowledge_base"] is not None
    
    print("✅ Data flows through all nodes correctly!")


if __name__ == "__main__":
    test_workflow_with_mock_data()
    test_workflow_data_flow()
    print("\n✅ All tests passed!")

