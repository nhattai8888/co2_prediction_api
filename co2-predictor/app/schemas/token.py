"""
Token schemas for authentication.
"""
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    Token schema for access token response.
    """
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """
    Token payload schema for JWT.
    """
    sub: Optional[str] = None  # Subject (user ID)
    exp: Optional[int] = None  # Expiry timestamp 