"""
Device schemas for API validation and responses.
"""
from typing import Optional
from pydantic import BaseModel, validator

from .common import IDModelMixin, DateTimeModelMixin

class DeviceBase(BaseModel):
    """
    Base device schema.
    """
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    power_consumption: Optional[float] = None
    default_emission_factor: Optional[float] = None
    average_usage_hours: Optional[float] = None

class DeviceCreate(DeviceBase):
    """
    Schema for creating a device.
    """
    name: str
    type: str
    power_consumption: float
    default_emission_factor: float
    
    @validator('power_consumption')
    def power_must_be_positive(cls, v):
        """
        Validate that power consumption is positive.
        """
        if v <= 0:
            raise ValueError('Power consumption must be positive')
        return v
    
    @validator('default_emission_factor')
    def emission_factor_must_be_positive(cls, v):
        """
        Validate that emission factor is positive.
        """
        if v <= 0:
            raise ValueError('Emission factor must be positive')
        return v

class DeviceUpdate(DeviceBase):
    """
    Schema for updating a device.
    """
    @validator('power_consumption')
    def power_must_be_positive(cls, v):
        """
        Validate that power consumption is positive.
        """
        if v is not None and v <= 0:
            raise ValueError('Power consumption must be positive')
        return v
    
    @validator('default_emission_factor')
    def emission_factor_must_be_positive(cls, v):
        """
        Validate that emission factor is positive.
        """
        if v is not None and v <= 0:
            raise ValueError('Emission factor must be positive')
        return v

class DeviceResponse(IDModelMixin, DateTimeModelMixin, DeviceBase):
    """
    Schema for device response.
    """
    name: str
    type: str
    power_consumption: float
    default_emission_factor: float
    
    class Config:
        orm_mode = True 