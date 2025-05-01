"""
Calculation schemas for API validation and responses.
"""
from typing import Optional
from pydantic import BaseModel, validator

from .common import IDModelMixin, DateTimeModelMixin
from .device import DeviceResponse

class CalculationBase(BaseModel):
    """
    Base calculation schema.
    """
    device_id: Optional[str] = None
    usage_hours: Optional[float] = None
    calculation_method: Optional[str] = "standard"

class CalculationCreate(CalculationBase):
    """
    Schema for creating a calculation.
    """
    device_id: str
    usage_hours: float
    
    @validator('usage_hours')
    def usage_hours_must_be_positive(cls, v):
        """
        Validate that usage hours are positive.
        """
        if v <= 0:
            raise ValueError('Usage hours must be positive')
        return v

class CalculationResponse(IDModelMixin, DateTimeModelMixin, CalculationBase):
    """
    Schema for calculation response.
    """
    user_id: str
    device_id: str
    usage_hours: float
    calculated_co2_hourly: float
    calculated_co2_monthly: float
    device: Optional[DeviceResponse] = None
    
    class Config:
        orm_mode = True 