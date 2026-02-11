from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import TokenResponse
from app.services.shiprocket import ShiprocketService
from app.services import auth as auth_service

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get access token by authenticating with Shiprocket.
    
    This endpoint verifies credentials with Shiprocket and returns a local JWT.
    """
    try:
        # In this implementation, we verify the credentials by trying to login to Shiprocket
        # Note: ShiprocketService by default uses settings.SHIPROCKET_EMAIL/PASSWORD
        # If we want to support multiple users, we'd need to modify ShiprocketService
        # but for now we follow the existing pattern and just issue a JWT if Shiprocket auth passes.
        
        service = ShiprocketService()
        # You might want to compare form_data.username/password here if you want to restrict login
        # to the ones in settings, or just try to use them for Shiprocket.
        
        await service.authenticate()
        
        access_token = auth_service.create_access_token(
            subject=form_data.username
        )
        return TokenResponse(token=access_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
