"""Order endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.db.session import get_db
from app.models.order import Order
from app.models.shipment import Shipment
from app.schemas.order import OrderCreate, OrderResponse
from app.services.shiprocket import ShiprocketService

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new order and submit to Shiprocket."""
    try:
        result = await db.execute(
            select(Order).where(Order.order_id == order_data.order_id)
        )
        existing_order = result.scalar_one_or_none()
        
        if existing_order:
            raise HTTPException(status_code=400, detail="Order ID already exists")
        
        order = Order(
            order_id=order_data.order_id,
            order_date=order_data.order_date,
            pickup_location=order_data.pickup_location,
            billing_customer_name=order_data.billing_customer_name,
            billing_city=order_data.billing_city,
            billing_pincode=order_data.billing_pincode,
            billing_state=order_data.billing_state,
            billing_country=order_data.billing_country,
            billing_phone=order_data.billing_phone,
            billing_email=order_data.billing_email,
            billing_address=order_data.billing_address,
            order_items=[item.model_dump() for item in order_data.order_items],
            payment_method=order_data.payment_method,
            weight=order_data.weight,
            length=order_data.length,
            breadth=order_data.breadth,
            height=order_data.height,
            status="created"
        )
        
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
        try:
            service = ShiprocketService()
            shiprocket_response = await service.create_order(order_data.model_dump())
            
            order.shiprocket_order_id = shiprocket_response.get("order_id")
            order.status = "submitted"
            
            shipment_id = shiprocket_response.get("shipment_id")
            if shipment_id:
                shipment = Shipment(
                    order_id=order.id,
                    shiprocket_shipment_id=shipment_id,
                    status="created"
                )
                db.add(shipment)
            
            await db.commit()
            await db.refresh(order)
            
        except Exception as e:
            logger.error(f"Failed to submit order to Shiprocket: {e}")
            order.status = "failed"
            await db.commit()
            raise HTTPException(status_code=500, detail=f"Failed to submit to Shiprocket: {str(e)}")
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Order creation failed: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all orders."""
    result = await db.execute(
        select(Order).offset(skip).limit(limit).order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get order by ID."""
    result = await db.execute(
        select(Order).where(Order.order_id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order
