"""
MongoDB database connection setup.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any

from ..core.config import settings

class Database:
    """
    Database class for MongoDB connection.
    """
    client: AsyncIOMotorClient = None
    db = None
    
    @classmethod
    async def connect_db(cls):
        """
        Connect to MongoDB.
        """
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
        print(f"Connected to MongoDB at {settings.MONGODB_URL}")
    
    @classmethod
    async def close_db(cls):
        """
        Close MongoDB connection.
        """
        if cls.client:
            cls.client.close()
            print("Closed MongoDB connection")
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """
        Get MongoDB collection.
        """
        if not cls.db:
            raise RuntimeError("Database not connected. Call connect_db first.")
        
        return cls.db[collection_name]
    
# Collections
USERS_COLLECTION = "users"
DEVICES_COLLECTION = "devices"
CALCULATIONS_COLLECTION = "calculations"
PREDICTIONS_COLLECTION = "predictions"
RECOMMENDATIONS_COLLECTION = "recommendations" 