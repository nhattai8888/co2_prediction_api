"""
Prediction schemas for AI predictions.
"""
from typing import Dict, Optional, List
from pydantic import BaseModel

from .common import IDModelMixin, DateTimeModelMixin

class PredictionFeatures(BaseModel):
    """
    Features for CO2 prediction.
    """
    device_id: str
    future_usage_hours: float
    prediction_period: Optional[str] = "monthly"

class PredictionRequest(BaseModel):
    """
    Schema for prediction request.
    """
    features: List[PredictionFeatures]
    include_historical: Optional[bool] = False

class PredictionResult(BaseModel):
    """
    Individual prediction result.
    """
    device_id: str
    predicted_co2: float
    confidence: Optional[float] = None
    
class PredictionResponse(BaseModel):
    """
    Schema for prediction response.
    """
    predictions: List[PredictionResult]
    model_version: str
    total_predicted_co2: float
    prediction_period: str
    mae: Optional[float] = None  # Mean Absolute Error
    rmse: Optional[float] = None  # Root Mean Square Error 