"""
End-to-end tests for PR 2: Knowledge Base System

Test that:
1. Can load defaults
2. Can update kitchen configuration
3. Can query values
"""

import pytest
from knowledge_base import KnowledgeBase, Kitchen, Oven, Burner, Microwave, Chef


def test_load_defaults():
    """Test that we can load default kitchen configurations."""
    # Test loading each kitchen type
    kb_home = KnowledgeBase(kitchen_type="home")
    kitchen = kb_home.get_kitchen()
    
    assert len(kitchen.ovens) == 1
    assert len(kitchen.burners) == 4
    assert len(kitchen.microwaves) == 1
    assert len(kitchen.chefs) == 1
    
    # Test small restaurant
    kb_restaurant = KnowledgeBase(kitchen_type="small_restaurant")
    kitchen = kb_restaurant.get_kitchen()
    
    assert len(kitchen.ovens) == 2
    assert len(kitchen.burners) == 6
    assert len(kitchen.microwaves) == 2
    assert len(kitchen.chefs) == 2
    
    # Test commercial
    kb_commercial = KnowledgeBase(kitchen_type="commercial")
    kitchen = kb_commercial.get_kitchen()
    
    assert len(kitchen.ovens) == 4
    assert len(kitchen.burners) == 8
    assert len(kitchen.microwaves) == 5
    assert len(kitchen.chefs) == 5


def test_update_kitchen():
    """Test that we can update kitchen configuration."""
    kb = KnowledgeBase(kitchen_type="home")
    
    # Update existing oven
    kitchen = kb.update({
        "ovens": [{"id": "oven_1", "capacity": 4}]
    })
    
    oven = kitchen.get_oven("oven_1")
    assert oven is not None
    assert oven.capacity == 4
    
    # Add new oven
    kitchen = kb.update({
        "add_oven": {"id": "oven_2", "capacity": 3, "max_temp": 550}
    })
    
    assert len(kitchen.ovens) == 2
    oven_2 = kitchen.get_oven("oven_2")
    assert oven_2 is not None
    assert oven_2.capacity == 3
    assert oven_2.max_temp == 550


def test_query_values():
    """Test that we can query kitchen values."""
    kb = KnowledgeBase(kitchen_type="small_restaurant")
    kitchen = kb.get_kitchen()
    
    # Query oven
    oven = kitchen.get_oven("oven_1")
    assert oven is not None
    assert oven.capacity > 0
    assert oven.max_temp > 0
    
    # Query burner
    burner = kitchen.get_burner("burner_1")
    assert burner is not None
    
    # Query microwave
    microwave = kitchen.get_microwave("microwave_1")
    assert microwave is not None
    assert microwave.wattage > 0
    
    # Query chef
    chef = kitchen.get_chef("chef_1")
    assert chef is not None
    assert chef.role in ["prep", "cook", "general", "server"]


def test_chef_multipliers():
    """Test task-selective multipliers."""
    kb = KnowledgeBase(kitchen_type="home")
    kitchen = kb.get_kitchen()
    chef = kitchen.chefs[0]
    
    # Test that multipliers vary by task type
    prep_multiplier = chef.get_task_multiplier("prep")
    passive_multiplier = chef.get_task_multiplier("passive")
    
    # Prep should have higher multiplier when tired
    chef.energy_level = "tired"
    tired_prep_multiplier = chef.get_task_multiplier("prep")
    tired_passive_multiplier = chef.get_task_multiplier("passive")
    
    assert tired_prep_multiplier > prep_multiplier
    assert tired_passive_multiplier < tired_prep_multiplier  # Passive less affected


def test_reset_to_defaults():
    """Test resetting kitchen to defaults."""
    kb = KnowledgeBase(kitchen_type="home")
    
    # Make some changes
    kb.update({"ovens": [{"id": "oven_1", "capacity": 10}]})
    assert kb.get_kitchen().get_oven("oven_1").capacity == 10
    
    # Reset
    kitchen = kb.reset_to_defaults("home")
    assert kitchen.get_oven("oven_1").capacity != 10  # Back to default

