"""
Prediction models.
"""
from typing import Dict, Optional
from pydantic import BaseModel, Field

from .common import PyObjectId, TimestampMixin

class Prediction(TimestampMixin):
    """
    Prediction model representing AI/ML predictions of CO2 emissions.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    device_id: Optional[PyObjectId] = None
    input_features: Dict[str, float]
    predicted_co2: float  # in kg CO2
    prediction_period: str = "monthly"  # monthly, yearly, etc.
    mae: Optional[float] = None  # Mean Absolute Error of the prediction
    rmse: Optional[float] = None  # Root Mean Square Error of the prediction
    model_version: str = "1.0"
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "60d5ec9af3eaf3d4e2c0e5a1",
                "device_id": "60d5ec9af3eaf3d4e2c0e5a2",
                "input_features": {
                    "power_consumption": 150.0,
                    "usage_hours": 8.0,
                    "emission_factor": 0.5
                },
                "predicted_co2": 22.5,
                "prediction_period": "monthly",
                "mae": 1.2,
                "rmse": 1.8,
                "model_version": "1.0"
            }
        } 