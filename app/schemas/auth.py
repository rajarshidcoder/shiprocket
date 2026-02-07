"""Authentication Pydantic schemas."""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Schema for token response."""
    
    token: str = Field(..., description="Bearer token for authentication")
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
