"""
Prediction repository for database operations.
"""
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from ...models.prediction import Prediction
from ..database import PREDICTIONS_COLLECTION
from .base import BaseMongoDBRepository

class PredictionRepository(BaseMongoDBRepository[Prediction]):
    """
    Prediction repository for database operations.
    """
    
    def __init__(self):
        super().__init__(PREDICTIONS_COLLECTION, Prediction)
    
    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """
        Get predictions by user ID.
        """
        if not ObjectId.is_valid(user_id):
            return []
            
        return await self.find_many({"user_id": ObjectId(user_id)}, skip, limit)
    
    async def get_by_device_id(self, device_id: str, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """
        Get predictions by device ID.
        """
        if not ObjectId.is_valid(device_id):
            return []
            
        return await self.find_many({"device_id": ObjectId(device_id)}, skip, limit)
    
    async def get_by_user_and_device(self, user_id: str, device_id: str, skip: int = 0, limit: int = 100) -> List[Prediction]:
        """
        Get predictions by user and device ID.
        """
        if not ObjectId.is_valid(user_id) or not ObjectId.is_valid(device_id):
            return []
            
        query = {
            "user_id": ObjectId(user_id),
            "device_id": ObjectId(device_id)
        }
        
        return await self.find_many(query, skip, limit)
    
    async def create_prediction(self, prediction_data: dict) -> Prediction:
        """
        Create a new prediction.
        """
        # Convert string IDs to ObjectId
        if "user_id" in prediction_data and isinstance(prediction_data["user_id"], str):
            prediction_data["user_id"] = ObjectId(prediction_data["user_id"])
            
        if "device_id" in prediction_data and isinstance(prediction_data["device_id"], str) and prediction_data["device_id"]:
            prediction_data["device_id"] = ObjectId(prediction_data["device_id"])
            
        return await self.create(prediction_data)
    
    async def get_latest_prediction(self, user_id: str, device_id: Optional[str] = None) -> Optional[Prediction]:
        """
        Get latest prediction for a user and optionally a device.
        """
        if not ObjectId.is_valid(user_id):
            return None
            
        query = {"user_id": ObjectId(user_id)}
        
        if device_id and ObjectId.is_valid(device_id):
            query["device_id"] = ObjectId(device_id)
            
        cursor = self.collection.find(query).sort("created_at", -1).limit(1)
        documents = await cursor.to_list(length=1)
        
        if documents:
            return self.model_class(**documents[0])
        return None 