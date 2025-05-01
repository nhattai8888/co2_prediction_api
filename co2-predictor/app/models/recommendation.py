"""
Recommendation models.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from .common import PyObjectId, RecommendationType, TimestampMixin

class Recommendation(TimestampMixin):
    """
    Recommendation model for CO2 reduction suggestions.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: RecommendationType
    title: str
    description: str
    potential_reduction: float  # Potential CO2 reduction in kg
    related_device_type: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "type": "DEVICE_SWITCH",
                "title": "Consider Energy-Efficient Refrigerator",
                "description": "Switching to an energy-efficient refrigerator could reduce your CO2 emissions.",
                "potential_reduction": 120.0,
                "related_device_type": "Refrigeration",
                "details": {
                    "current_device_id": "60d5ec9af3eaf3d4e2c0e5a2",
                    "suggested_device_id": "60d5ec9af3eaf3d4e2c0e5a3",
                    "payback_period_months": 36
                }
            }
        } 