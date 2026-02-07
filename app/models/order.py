"""Order database model."""

from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Order(Base):
    """Order model for storing Shiprocket orders."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    shiprocket_order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Order details
    order_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pickup_location: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Billing information
    billing_customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    billing_city: Mapped[str] = mapped_column(String(100), nullable=False)
    billing_pincode: Mapped[str] = mapped_column(String(10), nullable=False)
    billing_state: Mapped[str] = mapped_column(String(100), nullable=False)
    billing_country: Mapped[str] = mapped_column(String(100), nullable=False)
    billing_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    billing_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    billing_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Order items (stored as JSON)
    order_items: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Payment and shipping
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    length: Mapped[float | None] = mapped_column(Float, nullable=True)
    breadth: Mapped[float | None] = mapped_column(Float, nullable=True)
    height: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default="created")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shipments: Mapped[list["Shipment"]] = relationship("Shipment", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_id='{self.order_id}', status='{self.status}')>"
