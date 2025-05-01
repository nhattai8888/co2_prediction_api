"""
Device models.
"""
from typing import Optional
from pydantic import BaseModel, Field

from .common import PyObjectId, TimestampMixin

class Device(TimestampMixin):
    """
    Device model representing electrical devices with power consumption data.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    type: str
    description: Optional[str] = None
    power_consumption: float  # in Watts
    default_emission_factor: float  # in kg CO2/kWh
    average_usage_hours: Optional[float] = None  # typical usage hours per day
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "name": "Standard Refrigerator",
                "type": "Refrigeration",
                "description": "Average household refrigerator",
                "power_consumption": 150.0,
                "default_emission_factor": 0.5,
                "average_usage_hours": 24.0
            }
        } 