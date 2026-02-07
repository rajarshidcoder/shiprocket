"""Shipment endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.db.session import get_db
from app.models.shipment import Shipment
from app.schemas.shipment import (
    ShipmentResponse,
    CourierServiceability,
    AWBAssignRequest,
    LabelGenerateRequest,
    PickupScheduleRequest,
    TrackingResponse
)
from app.services.shiprocket import ShiprocketService

router = APIRouter()


@router.get("/serviceability", response_model=List[CourierServiceability])
async def check_serviceability(
    pickup_postcode: str = Query(..., min_length=6, max_length=6),
    delivery_postcode: str = Query(..., min_length=6, max_length=6),
    weight: float = Query(..., gt=0),
    cod: int = Query(0, ge=0, le=1)
):
    """Check courier serviceability."""
    try:
        service = ShiprocketService()
        couriers = await service.check_serviceability(
            pickup_postcode=pickup_postcode,
            delivery_postcode=delivery_postcode,
            weight=weight,
            cod=cod
        )
        return couriers
    except Exception as e:
        logger.error(f"Serviceability check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assign-awb")
async def assign_awb(
    request: AWBAssignRequest,
    db: AsyncSession = Depends(get_db)
):
    """Assign AWB to shipment."""
    try:
        result = await db.execute(
            select(Shipment).where(Shipment.shiprocket_shipment_id == request.shipment_id)
        )
        shipment = result.scalar_one_or_none()
        
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        service = ShiprocketService()
        awb_response = await service.assign_awb(request.shipment_id, request.courier_id)
        
        shipment.awb_code = awb_response.get("response", {}).get("data", {}).get("awb_code")
        shipment.courier_id = awb_response.get("response", {}).get("data", {}).get("courier_company_id")
        shipment.courier_name = awb_response.get("response", {}).get("data", {}).get("courier_name")
        shipment.status = "awb_assigned"
        
        await db.commit()
        await db.refresh(shipment)
        
        return {"message": "AWB assigned successfully", "awb_code": shipment.awb_code}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AWB assignment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-label")
async def generate_label(
    request: LabelGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate shipping label."""
    try:
        service = ShiprocketService()
        label_response = await service.generate_label(request.shipment_id)
        
        label_url = label_response.get("label_url")
        
        for shipment_id in request.shipment_id:
            result = await db.execute(
                select(Shipment).where(Shipment.shiprocket_shipment_id == shipment_id)
            )
            shipment = result.scalar_one_or_none()
            
            if shipment:
                shipment.label_url = label_url
                shipment.status = "label_generated"
        
        await db.commit()
        
        return {"message": "Label generated successfully", "label_url": label_url}
        
    except Exception as e:
        logger.error(f"Label generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule-pickup")
async def schedule_pickup(
    request: PickupScheduleRequest,
    db: AsyncSession = Depends(get_db)
):
    """Schedule pickup for shipments."""
    try:
        service = ShiprocketService()
        pickup_response = await service.schedule_pickup(request.shipment_id)
        
        for shipment_id in request.shipment_id:
            result = await db.execute(
                select(Shipment).where(Shipment.shiprocket_shipment_id == shipment_id)
            )
            shipment = result.scalar_one_or_none()
            
            if shipment:
                shipment.pickup_scheduled = True
                shipment.status = "pickup_scheduled"
        
        await db.commit()
        
        return {"message": "Pickup scheduled successfully", "response": pickup_response}
        
    except Exception as e:
        logger.error(f"Pickup scheduling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/track/{awb_code}", response_model=TrackingResponse)
async def track_shipment(
    awb_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Track shipment by AWB code."""
    try:
        service = ShiprocketService()
        tracking_data = await service.track_shipment(awb_code)
        
        result = await db.execute(
            select(Shipment).where(Shipment.awb_code == awb_code)
        )
        shipment = result.scalar_one_or_none()
        
        if shipment:
            shipment.current_status = tracking_data.get("tracking_data", {}).get("shipment_status")
            shipment.tracking_history = tracking_data.get("tracking_data", {}).get("shipment_track")
            await db.commit()
        
        return TrackingResponse(
            awb_code=awb_code,
            current_status=tracking_data.get("tracking_data", {}).get("shipment_status", "Unknown"),
            tracking_history=tracking_data.get("tracking_data", {}).get("shipment_track", [])
        )
        
    except Exception as e:
        logger.error(f"Tracking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ShipmentResponse])
async def list_shipments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all shipments."""
    result = await db.execute(
        select(Shipment).offset(skip).limit(limit).order_by(Shipment.created_at.desc())
    )
    shipments = result.scalars().all()
    return shipments
