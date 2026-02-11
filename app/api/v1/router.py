from fastapi import APIRouter, Depends
from app.api.v1.endpoints import orders, shipments, auth
from app.api.deps import get_current_user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(
    orders.router, 
    prefix="/orders", 
    tags=["Orders"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(
    shipments.router, 
    prefix="/shipments", 
    tags=["Shipments"],
    dependencies=[Depends(get_current_user)]
)
