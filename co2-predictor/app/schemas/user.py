"""
User schemas for API validation and responses.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, validator

from ..models.common import UserRole
from .common import IDModelMixin, DateTimeModelMixin

class UserBase(BaseModel):
    """
    Base user schema.
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    role: Optional[UserRole] = UserRole.CLIENT

class UserCreate(UserBase):
    """
    Schema for creating a user.
    """
    username: str
    email: EmailStr
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        """
        Validate password strength.
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        # Add more password validations if needed
        return v

class UserUpdate(UserBase):
    """
    Schema for updating a user.
    """
    password: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        """
        Validate password strength.
        """
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        # Add more password validations if needed
        return v

class UserResponse(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Schema for user response.
    """
    # Note: password_hash is not included in the response
    class Config:
        orm_mode = True 