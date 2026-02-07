"""API v1 router."""

from fastapi import APIRouter
from app.api.v1.endpoints import orders, shipments, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["Shipments"])
