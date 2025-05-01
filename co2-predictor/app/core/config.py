"""
Application configuration settings.
"""
import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """
    Application settings.
    """
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "CO2 Predictor API"
    
    # Security Configuration
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # MongoDB Configuration
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field(default="co2predictor", env="MONGODB_DB_NAME")
    
    # AI Model Configuration
    MODEL_PATH: str = "app/services/ai_models"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings() 