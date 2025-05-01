"""
Calculation repository for database operations.
"""
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from ...models.calculation import Calculation
from ..database import CALCULATIONS_COLLECTION
from .base import BaseMongoDBRepository

class CalculationRepository(BaseMongoDBRepository[Calculation]):
    """
    Calculation repository for database operations.
    """
    
    def __init__(self):
        super().__init__(CALCULATIONS_COLLECTION, Calculation)
    
    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Calculation]:
        """
        Get calculations by user ID.
        """
        if not ObjectId.is_valid(user_id):
            return []
            
        return await self.find_many({"user_id": ObjectId(user_id)}, skip, limit)
    
    async def get_by_device_id(self, device_id: str, skip: int = 0, limit: int = 100) -> List[Calculation]:
        """
        Get calculations by device ID.
        """
        if not ObjectId.is_valid(device_id):
            return []
            
        return await self.find_many({"device_id": ObjectId(device_id)}, skip, limit)
    
    async def get_by_user_and_device(self, user_id: str, device_id: str, skip: int = 0, limit: int = 100) -> List[Calculation]:
        """
        Get calculations by user and device ID.
        """
        if not ObjectId.is_valid(user_id) or not ObjectId.is_valid(device_id):
            return []
            
        query = {
            "user_id": ObjectId(user_id),
            "device_id": ObjectId(device_id)
        }
        
        return await self.find_many(query, skip, limit)
    
    async def create_calculation(self, calculation_data: dict) -> Calculation:
        """
        Create a new calculation.
        """
        # Convert string IDs to ObjectId
        if "user_id" in calculation_data and isinstance(calculation_data["user_id"], str):
            calculation_data["user_id"] = ObjectId(calculation_data["user_id"])
            
        if "device_id" in calculation_data and isinstance(calculation_data["device_id"], str):
            calculation_data["device_id"] = ObjectId(calculation_data["device_id"])
            
        return await self.create(calculation_data)
    
    async def update_calculation(self, calculation_id: str, calculation_data: dict) -> Optional[Calculation]:
        """
        Update a calculation.
        """
        calculation_data["updated_at"] = datetime.utcnow()
        return await self.update(calculation_id, calculation_data)
    
    async def delete_calculation(self, calculation_id: str) -> bool:
        """
        Delete a calculation.
        """
        return await self.delete(calculation_id) 