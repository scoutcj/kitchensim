"""
Pydantic models for kitchen resources and staff.
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from enum import Enum


class BurnerType(str, Enum):
    """Types of burners/stoves."""
    GAS = "gas"
    ELECTRIC = "electric"
    INDUCTION = "induction"


class ChefRole(str, Enum):
    """Chef roles."""
    PREP = "prep"
    COOK = "cook"
    GENERAL = "general"
    SERVER = "server"


class SkillLevel(str, Enum):
    """Chef skill levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class EnergyLevel(str, Enum):
    """Chef energy/tiredness levels."""
    FRESH = "fresh"
    TIRED = "tired"
    EXHAUSTED = "exhausted"


class Oven(BaseModel):
    """Oven resource model."""
    id: str = Field(..., description="Unique identifier for the oven")
    capacity: int = Field(..., ge=1, description="How many dishes can fit simultaneously")
    max_temp: int = Field(default=500, ge=200, le=1000, description="Maximum temperature in Fahrenheit")


class Burner(BaseModel):
    """Individual burner resource model."""
    id: str = Field(..., description="Unique identifier for the burner")
    type: BurnerType = Field(default=BurnerType.GAS, description="Type of burner (gas, electric, induction)")


class Microwave(BaseModel):
    """Microwave resource model."""
    id: str = Field(..., description="Unique identifier for the microwave")
    wattage: int = Field(default=1000, ge=500, le=2000, description="Microwave wattage")


class Chef(BaseModel):
    """Chef/staff member model."""
    id: str = Field(..., description="Unique identifier for the chef")
    role: ChefRole = Field(..., description="Role of the chef")
    skill_level: SkillLevel = Field(default=SkillLevel.INTERMEDIATE, description="Skill level")
    energy_level: EnergyLevel = Field(default=EnergyLevel.FRESH, description="Current energy/tiredness level")
    
    def get_task_multiplier(self, task_type: str) -> float:
        """
        Returns time multiplier based on task type and chef state.
        
        Task types: "prep", "cook", "passive", "plate"
        - Prep tasks (chopping, peeling) are more affected by energy level
        - Cooking tasks are more affected by skill level
        - Passive tasks (boiling, waiting) are barely affected
        """
        base = 1.0
        
        # Energy level affects prep tasks significantly
        if task_type == "prep":
            if self.energy_level == EnergyLevel.TIRED:
                base *= 1.3
            elif self.energy_level == EnergyLevel.EXHAUSTED:
                base *= 1.6
        
        # Skill level affects cooking tasks
        if task_type == "cook":
            if self.skill_level == SkillLevel.BEGINNER:
                base *= 1.2
            elif self.skill_level == SkillLevel.EXPERT:
                base *= 0.9  # Experts are faster
        
        # Energy also affects cooking, but less than prep
        if task_type == "cook":
            if self.energy_level == EnergyLevel.TIRED:
                base *= 1.15
            elif self.energy_level == EnergyLevel.EXHAUSTED:
                base *= 1.3
        
        # Passive tasks (boiling, waiting) barely affected
        if task_type == "passive":
            if self.energy_level == EnergyLevel.EXHAUSTED:
                base *= 1.1  # Minimal impact
            else:
                base *= 1.0
        
        # Plating is affected by both skill and energy
        if task_type == "plate":
            if self.skill_level == SkillLevel.BEGINNER:
                base *= 1.15
            if self.energy_level == EnergyLevel.TIRED:
                base *= 1.2
            elif self.energy_level == EnergyLevel.EXHAUSTED:
                base *= 1.4
        
        return base


class Kitchen(BaseModel):
    """Complete kitchen model for a session."""
    ovens: List[Oven] = Field(default_factory=list, description="List of ovens")
    burners: List[Burner] = Field(default_factory=list, description="List of burners")
    microwaves: List[Microwave] = Field(default_factory=list, description="List of microwaves")
    chefs: List[Chef] = Field(default_factory=list, description="List of chefs/staff")
    
    def get_oven(self, oven_id: str) -> Optional[Oven]:
        """Get oven by ID."""
        return next((o for o in self.ovens if o.id == oven_id), None)
    
    def get_burner(self, burner_id: str) -> Optional[Burner]:
        """Get burner by ID."""
        return next((b for b in self.burners if b.id == burner_id), None)
    
    def get_microwave(self, microwave_id: str) -> Optional[Microwave]:
        """Get microwave by ID."""
        return next((m for m in self.microwaves if m.id == microwave_id), None)
    
    def get_chef(self, chef_id: str) -> Optional[Chef]:
        """Get chef by ID."""
        return next((c for c in self.chefs if c.id == chef_id), None)
    
    def get_available_ovens(self) -> List[Oven]:
        """Get all available ovens."""
        return self.ovens
    
    def get_available_burners(self) -> List[Burner]:
        """Get all available burners."""
        return self.burners
    
    def get_available_microwaves(self) -> List[Microwave]:
        """Get all available microwaves."""
        return self.microwaves
    
    def get_chefs_by_role(self, role: ChefRole) -> List[Chef]:
        """Get all chefs with a specific role."""
        return [c for c in self.chefs if c.role == role]

