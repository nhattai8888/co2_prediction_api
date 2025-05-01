"""
CO2 calculation and prediction endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ...models.user import User
from ...schemas.calculation import CalculationCreate, CalculationResponse
from ...schemas.device import DeviceResponse
from ...schemas.prediction import PredictionRequest, PredictionResponse
from ...schemas.recommendation import RecommendationResponse
from ...services.calculation_service import CalculationService
from ...services.device_service import DeviceService
from ...services.ai_service import AIService
from ...services.recommendation_service import RecommendationService
from ..deps import get_current_active_user

router = APIRouter(prefix="/calculator", tags=["calculator"])

@router.post("/calculations", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
async def create_calculation(
    calculation_data: CalculationCreate,
    current_user: User = Depends(get_current_active_user),
    calculation_service: CalculationService = Depends()
):
    """
    Create a new CO2 calculation for a device.
    """
    calculation = await calculation_service.create_calculation(
        user_id=str(current_user.id),
        calculation_data=calculation_data
    )
    return calculation

@router.get("/calculations", response_model=List[CalculationResponse])
async def get_user_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    calculation_service: CalculationService = Depends()
):
    """
    Get all calculations for the current user.
    """
    calculations = await calculation_service.get_user_calculations(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit
    )
    return calculations

@router.get("/devices", response_model=List[DeviceResponse])
async def get_user_devices(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    device_service: DeviceService = Depends()
):
    """
    Get all devices for the current user.
    """
    devices = await device_service.get_user_devices(
        user_id=str(current_user.id),
        skip=skip,
        limit=limit
    )
    return devices

@router.post("/predict", response_model=PredictionResponse)
async def predict_emissions(
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends()
):
    """
    Predict future CO2 emissions based on current usage patterns.
    """
    prediction = await ai_service.predict_emissions(
        user_id=str(current_user.id),
        prediction_request=prediction_request
    )
    return prediction

@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    current_user: User = Depends(get_current_active_user),
    recommendation_service: RecommendationService = Depends()
):
    """
    Get CO2 reduction recommendations based on user's devices and patterns.
    """
    recommendations = await recommendation_service.generate_recommendations(
        user_id=str(current_user.id)
    )
    return recommendations 