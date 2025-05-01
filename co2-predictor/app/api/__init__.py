from fastapi import APIRouter

from .endpoints import auth, users, calculator, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(calculator.router)
api_router.include_router(admin.router) 