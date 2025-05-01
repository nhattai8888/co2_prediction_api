"""
Base repository class for MongoDB.
"""
from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from bson import ObjectId

from ...models.common import PyObjectId
from ..database import Database

T = TypeVar('T')

class BaseMongoDBRepository(Generic[T]):
    """
    Base MongoDB repository class with common CRUD operations.
    """
    
    def __init__(self, collection_name: str, model_class: Type[T]):
        self.collection_name = collection_name
        self.model_class = model_class
        
    @property
    def collection(self):
        """
        Get MongoDB collection.
        """
        return Database.get_collection(self.collection_name)
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """
        Get document by ID.
        """
        if not ObjectId.is_valid(id):
            return None
            
        document = await self.collection.find_one({"_id": ObjectId(id)})
        if document:
            return self.model_class(**document)
        return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        Get all documents with pagination.
        """
        cursor = self.collection.find().skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.model_class(**doc) for doc in documents]
    
    async def find_one(self, query: Dict[str, Any]) -> Optional[T]:
        """
        Find one document by query.
        """
        document = await self.collection.find_one(query)
        if document:
            return self.model_class(**document)
        return None
    
    async def find_many(self, query: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[T]:
        """
        Find many documents by query.
        """
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.model_class(**doc) for doc in documents]
    
    async def create(self, data: Dict[str, Any]) -> T:
        """
        Create a document.
        """
        result = await self.collection.insert_one(data)
        document = await self.collection.find_one({"_id": result.inserted_id})
        return self.model_class(**document)
    
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[T]:
        """
        Update a document.
        """
        if not ObjectId.is_valid(id):
            return None
            
        document = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data},
            return_document=True
        )
        
        if document:
            return self.model_class(**document)
        return None
    
    async def delete(self, id: str) -> bool:
        """
        Delete a document.
        """
        if not ObjectId.is_valid(id):
            return False
            
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0 