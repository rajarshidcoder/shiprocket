"""Shipment database model."""

from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Shipment(Base):
    """Shipment model for storing Shiprocket shipments."""

    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Shiprocket IDs
    shiprocket_shipment_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    awb_code: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    
    # Courier details
    courier_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    courier_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Pricing
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    estimated_delivery_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Status and tracking
    status: Mapped[str] = mapped_column(String(50), default="created")
    current_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tracking_history: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    
    # Labels and documents
    label_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    invoice_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    manifest_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Pickup
    pickup_scheduled: Mapped[bool] = mapped_column(default=False)
    pickup_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="shipments")

    def __repr__(self) -> str:
        return f"<Shipment(id={self.id}, awb_code='{self.awb_code}', status='{self.status}')>"
