"""
Dependency injection functions for FastAPI.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional

from ..core.config import settings
from ..core.security import verify_access_token
from ..db.repositories.user_repo import UserRepository
from ..models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends()
) -> User:
    """
    Get the current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current admin user.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user 