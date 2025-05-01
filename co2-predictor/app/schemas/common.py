"""
Common schemas used throughout the application.
"""
from typing import Optional, Generic, TypeVar, List, Dict, Any
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from datetime import datetime

from ..models.common import UserRole, RecommendationType

T = TypeVar('T')

class DateTimeModelMixin(BaseModel):
    """
    Mixin for created_at and updated_at fields.
    """
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class IDModelMixin(BaseModel):
    """
    Mixin for id field.
    """
    id: Optional[str] = None

class ResponseBase(GenericModel, Generic[T]):
    """
    Base response model.
    """
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None

class PaginatedResponse(GenericModel, Generic[T]):
    """
    Response model for paginated results.
    """
    total: int
    page: int
    size: int
    items: List[T] 