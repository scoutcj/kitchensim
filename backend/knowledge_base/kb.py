"""
Knowledge Base system for managing kitchen configurations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from .models import Kitchen, Oven, Burner, Microwave, Chef, BurnerType, ChefRole, SkillLevel, EnergyLevel


class KnowledgeBase:
    """
    Manages kitchen knowledge base - loads defaults and merges user overrides.
    
    Session-scoped: Each simulation gets a Kitchen instance.
    Structure supports future database persistence.
    """
    
    def __init__(self, kitchen_type: str = "small_restaurant"):
        """
        Initialize knowledge base with a kitchen type.
        
        Args:
            kitchen_type: One of "home", "small_restaurant", "commercial"
        """
        self.defaults_path = Path(__file__).parent / "defaults.json"
        self.defaults = self._load_defaults()
        self.kitchen_type = kitchen_type
        self.kitchen = self._create_kitchen_from_type(kitchen_type)
    
    def _load_defaults(self) -> Dict[str, Any]:
        """Load default kitchen configurations from JSON."""
        with open(self.defaults_path, 'r') as f:
            return json.load(f)
    
    def _create_kitchen_from_type(self, kitchen_type: str) -> Kitchen:
        """Create a Kitchen instance from a kitchen type."""
        if kitchen_type not in self.defaults["kitchen_types"]:
            # Fallback to default
            kitchen_type = self.defaults["default_kitchen_type"]
        
        kitchen_data = self.defaults["kitchen_types"][kitchen_type]
        
        # Parse ovens
        ovens = [Oven(**oven_data) for oven_data in kitchen_data["ovens"]]
        
        # Parse burners
        burners = [Burner(**burner_data) for burner_data in kitchen_data["burners"]]
        
        # Parse microwaves
        microwaves = [Microwave(**microwave_data) for microwave_data in kitchen_data["microwaves"]]
        
        # Parse chefs
        chefs = [Chef(**chef_data) for chef_data in kitchen_data["chefs"]]
        
        return Kitchen(
            ovens=ovens,
            burners=burners,
            microwaves=microwaves,
            chefs=chefs
        )
    
    def update(self, overrides: Dict[str, Any]) -> Kitchen:
        """
        Merge user overrides into the kitchen configuration.
        
        Args:
            overrides: Dictionary with user-specified changes, e.g.:
                {
                    "ovens": [{"id": "oven_1", "capacity": 4}],
                    "chefs": [{"id": "chef_1", "energy_level": "tired"}],
                    "add_oven": {"id": "oven_3", "capacity": 3, "max_temp": 550}
                }
        
        Returns:
            Updated Kitchen instance
        """
        # Update existing ovens
        if "ovens" in overrides:
            for oven_update in overrides["ovens"]:
                oven_id = oven_update.get("id")
                if oven_id:
                    existing_oven = self.kitchen.get_oven(oven_id)
                    if existing_oven:
                        # Update existing oven
                        for key, value in oven_update.items():
                            if key != "id" and hasattr(existing_oven, key):
                                setattr(existing_oven, key, value)
                    else:
                        # Add new oven
                        self.kitchen.ovens.append(Oven(**oven_update))
        
        # Add new oven
        if "add_oven" in overrides:
            self.kitchen.ovens.append(Oven(**overrides["add_oven"]))
        
        # Update existing burners
        if "burners" in overrides:
            for burner_update in overrides["burners"]:
                burner_id = burner_update.get("id")
                if burner_id:
                    existing_burner = self.kitchen.get_burner(burner_id)
                    if existing_burner:
                        for key, value in burner_update.items():
                            if key != "id" and hasattr(existing_burner, key):
                                setattr(existing_burner, key, value)
                    else:
                        self.kitchen.burners.append(Burner(**burner_update))
        
        # Add new burner
        if "add_burner" in overrides:
            self.kitchen.burners.append(Burner(**overrides["add_burner"]))
        
        # Update existing microwaves
        if "microwaves" in overrides:
            for microwave_update in overrides["microwaves"]:
                microwave_id = microwave_update.get("id")
                if microwave_id:
                    existing_microwave = self.kitchen.get_microwave(microwave_id)
                    if existing_microwave:
                        for key, value in microwave_update.items():
                            if key != "id" and hasattr(existing_microwave, key):
                                setattr(existing_microwave, key, value)
                    else:
                        self.kitchen.microwaves.append(Microwave(**microwave_update))
        
        # Add new microwave
        if "add_microwave" in overrides:
            self.kitchen.microwaves.append(Microwave(**overrides["add_microwave"]))
        
        # Update existing chefs
        if "chefs" in overrides:
            for chef_update in overrides["chefs"]:
                chef_id = chef_update.get("id")
                if chef_id:
                    existing_chef = self.kitchen.get_chef(chef_id)
                    if existing_chef:
                        for key, value in chef_update.items():
                            if key != "id" and hasattr(existing_chef, key):
                                setattr(existing_chef, key, value)
                    else:
                        self.kitchen.chefs.append(Chef(**chef_update))
        
        # Add new chef
        if "add_chef" in overrides:
            self.kitchen.chefs.append(Chef(**overrides["add_chef"]))
        
        return self.kitchen
    
    def get_kitchen(self) -> Kitchen:
        """Get the current kitchen instance."""
        return self.kitchen
    
    def reset_to_defaults(self, kitchen_type: Optional[str] = None):
        """Reset kitchen to default configuration."""
        if kitchen_type is None:
            kitchen_type = self.kitchen_type
        self.kitchen = self._create_kitchen_from_type(kitchen_type)
        return self.kitchen

