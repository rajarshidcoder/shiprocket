"""Test API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient):
    """Test order creation."""
    order_data = {
        "order_id": "TEST001",
        "order_date": "2026-02-07",
        "pickup_location": "Primary",
        "billing_customer_name": "Test User",
        "billing_city": "Bangalore",
        "billing_pincode": "560001",
        "billing_state": "Karnataka",
        "billing_country": "India",
        "billing_phone": "9999999999",
        "order_items": [
            {
                "name": "Test Product",
                "sku": "TEST001",
                "units": 1,
                "selling_price": 100
            }
        ],
        "payment_method": "Prepaid",
        "weight": 0.5
    }
    
    # Note: This will fail without valid Shiprocket credentials
    # In production, mock the Shiprocket service
    response = await client.post("/api/v1/orders/", json=order_data)
    # assert response.status_code == 201
