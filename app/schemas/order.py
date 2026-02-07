"""Order Pydantic schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class OrderItem(BaseModel):
    """Order item schema."""
    
    name: str = Field(..., description="Product name")
    sku: str = Field(..., description="Product SKU")
    units: int = Field(..., gt=0, description="Number of units")
    selling_price: float = Field(..., gt=0, description="Selling price per unit")
    discount: Optional[float] = Field(0, ge=0, description="Discount amount")
    tax: Optional[float] = Field(0, ge=0, description="Tax amount")
    hsn: Optional[int] = Field(None, description="HSN code")


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    
    order_id: str = Field(..., description="Unique order ID")
    order_date: str = Field(..., description="Order date in YYYY-MM-DD format")
    pickup_location: str = Field(default="Primary", description="Pickup location name")
    
    # Billing information
    billing_customer_name: str = Field(..., min_length=1, max_length=255)
    billing_city: str = Field(..., min_length=1, max_length=100)
    billing_pincode: str = Field(..., min_length=6, max_length=6)
    billing_state: str = Field(..., min_length=1, max_length=100)
    billing_country: str = Field(default="India", max_length=100)
    billing_phone: str = Field(..., min_length=10, max_length=10)
    billing_email: Optional[str] = Field(None, max_length=255)
    billing_address: Optional[str] = Field(None, max_length=500)
    billing_address_2: Optional[str] = Field(None, max_length=500)
    
    # Shipping information (optional, defaults to billing)
    shipping_is_billing: bool = Field(default=True)
    shipping_customer_name: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_pincode: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_country: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_email: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_address_2: Optional[str] = None
    
    # Order items
    order_items: List[OrderItem] = Field(..., min_length=1)
    
    # Payment and shipping
    payment_method: str = Field(..., description="Payment method: Prepaid or COD")
    sub_total: Optional[float] = Field(None, ge=0)
    length: Optional[float] = Field(None, gt=0, description="Package length in cm")
    breadth: Optional[float] = Field(None, gt=0, description="Package breadth in cm")
    height: Optional[float] = Field(None, gt=0, description="Package height in cm")
    weight: float = Field(..., gt=0, description="Package weight in kg")
    
    @validator("payment_method")
    def validate_payment_method(cls, v):
        """Validate payment method."""
        if v not in ["Prepaid", "COD"]:
            raise ValueError("Payment method must be 'Prepaid' or 'COD'")
        return v
    
    @validator("order_date")
    def validate_order_date(cls, v):
        """Validate order date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Order date must be in YYYY-MM-DD format")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD123",
                "order_date": "2026-02-07",
                "pickup_location": "Primary",
                "billing_customer_name": "Rajarshi",
                "billing_city": "Bangalore",
                "billing_pincode": "560001",
                "billing_state": "Karnataka",
                "billing_country": "India",
                "billing_phone": "9999999999",
                "order_items": [
                    {
                        "name": "USB Cable",
                        "sku": "USB001",
                        "units": 1,
                        "selling_price": 299
                    }
                ],
                "payment_method": "Prepaid",
                "weight": 0.3
            }
        }


class OrderResponse(BaseModel):
    """Schema for order response."""
    
    id: int
    order_id: str
    shiprocket_order_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
