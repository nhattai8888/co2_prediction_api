"""
User management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...models.user import User
from ...schemas.user import UserCreate, UserResponse, UserUpdate
from ...services.user_service import UserService
from ..deps import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends()
):
    """
    Create a new user.
    """
    user = await user_service.create_user(user_data)
    return user

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get information about the current authenticated user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends()
):
    """
    Update the current authenticated user.
    """
    updated_user = await user_service.update_user(str(current_user.id), user_data)
    return updated_user

@router.get("", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    Get all users (admin only).
    """
    users = await user_service.get_users(skip, limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    Get user by ID (admin only).
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 