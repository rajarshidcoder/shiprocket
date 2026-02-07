"""Shipment Pydantic schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class CourierServiceability(BaseModel):
    """Courier serviceability response schema."""
    
    courier_company_id: int
    courier_name: str
    rate: float
    estimated_delivery_days: int
    cod: int
    pickup_availability: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "courier_company_id": 12,
                "courier_name": "Delhivery",
                "rate": 52.0,
                "estimated_delivery_days": 4,
                "cod": 0
            }
        }


class ShipmentResponse(BaseModel):
    """Schema for shipment response."""
    
    id: int
    order_id: int
    shiprocket_shipment_id: Optional[int] = None
    awb_code: Optional[str] = None
    courier_name: Optional[str] = None
    status: str
    current_status: Optional[str] = None
    label_url: Optional[str] = None
    pickup_scheduled: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AWBAssignRequest(BaseModel):
    """Schema for AWB assignment request."""
    
    shipment_id: int = Field(..., description="Shiprocket shipment ID")
    courier_id: Optional[int] = Field(None, description="Specific courier ID (optional)")


class LabelGenerateRequest(BaseModel):
    """Schema for label generation request."""
    
    shipment_id: List[int] = Field(..., description="List of shipment IDs")


class PickupScheduleRequest(BaseModel):
    """Schema for pickup scheduling request."""
    
    shipment_id: List[int] = Field(..., description="List of shipment IDs")
    pickup_date: Optional[str] = Field(None, description="Pickup date in YYYY-MM-DD format")


class TrackingResponse(BaseModel):
    """Schema for tracking response."""
    
    awb_code: str
    current_status: str
    shipment_status: Optional[str] = None
    tracking_history: List[Dict[str, Any]] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "awb_code": "SR123456789",
                "current_status": "In Transit",
                "tracking_history": [
                    {
                        "status": "Picked Up",
                        "location": "Bangalore",
                        "date": "2026-02-07 10:30:00"
                    }
                ]
            }
        }
