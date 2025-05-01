"""
User models.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

from .common import PyObjectId, UserRole, TimestampMixin

class User(TimestampMixin):
    """
    User model representing both clients and admins.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    password_hash: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    is_admin: bool = False
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "role": "CLIENT",
                "is_active": True,
                "is_admin": False
            }
        } 