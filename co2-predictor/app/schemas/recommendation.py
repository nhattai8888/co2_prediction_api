"""
Recommendation schemas for CO2 reduction suggestions.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from ..models.common import RecommendationType
from .common import IDModelMixin, DateTimeModelMixin

class RecommendationBase(BaseModel):
    """
    Base recommendation schema.
    """
    type: RecommendationType
    title: str
    description: str
    potential_reduction: float
    related_device_type: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class RecommendationResponse(IDModelMixin, DateTimeModelMixin, RecommendationBase):
    """
    Schema for recommendation response.
    """
    class Config:
        orm_mode = True

class RecommendationRequest(BaseModel):
    """
    Schema for recommendation request.
    """
    user_id: Optional[str] = None
    device_types: Optional[List[str]] = None
    max_recommendations: Optional[int] = 5 