"""
User repository for database operations.
"""
from typing import List, Optional
from datetime import datetime

from ...models.user import User
from ..database import USERS_COLLECTION
from .base import BaseMongoDBRepository

class UserRepository(BaseMongoDBRepository[User]):
    """
    User repository for database operations.
    """
    
    def __init__(self):
        super().__init__(USERS_COLLECTION, User)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        """
        return await self.find_one({"username": username})
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        return await self.find_one({"email": email})
    
    async def create_user(self, user_data: dict) -> User:
        """
        Create a new user.
        """
        return await self.create(user_data)
    
    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        """
        Update a user.
        """
        user_data["updated_at"] = datetime.utcnow()
        return await self.update(user_id, user_data)
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.
        """
        return await self.delete(user_id)
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        """
        return await self.get_all(skip, limit) 