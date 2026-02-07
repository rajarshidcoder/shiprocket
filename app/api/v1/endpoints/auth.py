"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException
from app.schemas.auth import TokenResponse
from app.services.shiprocket import ShiprocketService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login():
    """
    Get Bearer token from Shiprocket.
    
    This endpoint authenticates with Shiprocket using credentials from environment variables.
    """
    try:
        service = ShiprocketService()
        token = await service.authenticate()
        return TokenResponse(token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
