"""
Device repository for database operations.
"""
from typing import List, Optional
from datetime import datetime

from ...models.device import Device
from ..database import DEVICES_COLLECTION
from .base import BaseMongoDBRepository

class DeviceRepository(BaseMongoDBRepository[Device]):
    """
    Device repository for database operations.
    """
    
    def __init__(self):
        super().__init__(DEVICES_COLLECTION, Device)
    
    async def get_by_name(self, name: str) -> Optional[Device]:
        """
        Get device by name.
        """
        return await self.find_one({"name": name})
    
    async def get_by_type(self, device_type: str, skip: int = 0, limit: int = 100) -> List[Device]:
        """
        Get devices by type.
        """
        return await self.find_many({"type": device_type}, skip, limit)
    
    async def create_device(self, device_data: dict) -> Device:
        """
        Create a new device.
        """
        return await self.create(device_data)
    
    async def update_device(self, device_id: str, device_data: dict) -> Optional[Device]:
        """
        Update a device.
        """
        device_data["updated_at"] = datetime.utcnow()
        return await self.update(device_id, device_data)
    
    async def delete_device(self, device_id: str) -> bool:
        """
        Delete a device.
        """
        return await self.delete(device_id)
    
    async def get_devices(self, skip: int = 0, limit: int = 100) -> List[Device]:
        """
        Get all devices with pagination.
        """
        return await self.get_all(skip, limit) 