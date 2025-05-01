"""
Admin endpoints for user, device, and report management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from ...models.user import User
from ...schemas.user import UserCreate, UserResponse, UserUpdate
from ...schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from ...services.user_service import UserService
from ...services.device_service import DeviceService
from ...services.report_service import ReportService
from ...services.ai_service import AIService
from ..deps import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

# User management endpoints
@router.get("/users", response_model=List[UserResponse])
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

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    Create a new user (admin only).
    """
    user = await user_service.create_user(user_data)
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    Update a user (admin only).
    """
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    user_service: UserService = Depends()
):
    """
    Delete a user (admin only).
    """
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Device management endpoints
@router.get("/devices", response_model=List[DeviceResponse])
async def get_all_devices(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    device_service: DeviceService = Depends()
):
    """
    Get all devices (admin only).
    """
    devices = await device_service.get_devices(skip, limit)
    return devices

@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device_data: DeviceCreate,
    current_user: User = Depends(get_current_admin_user),
    device_service: DeviceService = Depends()
):
    """
    Create a new device (admin only).
    """
    device = await device_service.create_device(device_data)
    return device

@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: str,
    device_data: DeviceUpdate,
    current_user: User = Depends(get_current_admin_user),
    device_service: DeviceService = Depends()
):
    """
    Update a device (admin only).
    """
    updated_device = await device_service.update_device(device_id, device_data)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device

@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    current_user: User = Depends(get_current_admin_user),
    device_service: DeviceService = Depends()
):
    """
    Delete a device (admin only).
    """
    success = await device_service.delete_device(device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Report endpoints
@router.post("/reports/export")
async def export_report(
    format: str = "excel",
    report_type: str = "calculations",
    current_user: User = Depends(get_current_admin_user),
    report_service: ReportService = Depends()
):
    """
    Export data as a report in the specified format (admin only).
    """
    if format not in ["excel", "csv", "pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported format")
    
    if report_type not in ["calculations", "users", "devices", "predictions"]:
        raise HTTPException(status_code=400, detail="Unsupported report type")
    
    report = await report_service.generate_report(format, report_type)
    
    # Return appropriate file response based on format
    content_type = "application/vnd.ms-excel"
    if format == "csv":
        content_type = "text/csv"
    elif format == "pdf":
        content_type = "application/pdf"
    
    return Response(
        content=report,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename=report.{format}"}
    )

# AI model management
@router.post("/ai/train", status_code=status.HTTP_202_ACCEPTED)
async def trigger_model_training(
    current_user: User = Depends(get_current_admin_user),
    ai_service: AIService = Depends()
):
    """
    Trigger training of the AI model with latest data (admin only).
    """
    await ai_service.train_model()
    return {"message": "Model training initiated successfully"} 