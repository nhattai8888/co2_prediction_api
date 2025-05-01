"""
Common models and enums used throughout the application.
"""
from enum import Enum
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    """
    Custom ObjectId type for Pydantic models.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserRole(str, Enum):
    """
    User role enum.
    """
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"

class RecommendationType(str, Enum):
    """
    Recommendation type enum.
    """
    USAGE_OPTIMIZATION = "USAGE_OPTIMIZATION"
    DEVICE_SWITCH = "DEVICE_SWITCH"
    GREEN_INITIATIVE = "GREEN_INITIATIVE"

class TimestampMixin(BaseModel):
    """
    Mixin to add timestamps to models.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None 