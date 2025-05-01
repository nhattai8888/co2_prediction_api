"""
Calculation models.
"""
from typing import Optional
from pydantic import BaseModel, Field

from .common import PyObjectId, TimestampMixin

class Calculation(TimestampMixin):
    """
    Calculation model representing CO2 emission calculations.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    device_id: PyObjectId
    usage_hours: float
    calculated_co2_hourly: float  # in kg CO2
    calculated_co2_monthly: float  # in kg CO2
    calculation_method: str = "standard"  # could be different methods in the future
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "60d5ec9af3eaf3d4e2c0e5a1",
                "device_id": "60d5ec9af3eaf3d4e2c0e5a2",
                "usage_hours": 8.0,
                "calculated_co2_hourly": 0.6,
                "calculated_co2_monthly": 18.0,
                "calculation_method": "standard"
            }
        } 