# Quick Start Guide

## Prerequisites
- Docker and Docker Compose installed
- Shiprocket account with API credentials

## Setup Steps

### 1. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Shiprocket credentials
# Required fields:
# - SHIPROCKET_EMAIL
# - SHIPROCKET_PASSWORD
```

### 2. Start the Application
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

### 3. Run Database Migrations
```bash
# Create initial migration
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

### 4. Verify Installation
Visit http://localhost:8000/docs to see the API documentation.

## Quick Test

### 1. Get Authentication Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login
```

### 2. Check Serviceability
```bash
curl "http://localhost:8000/api/v1/shipments/serviceability?pickup_postcode=700001&delivery_postcode=560001&weight=0.5&cod=0"
```

### 3. Create an Order
```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
-H "Content-Type: application/json" \
-d '{
  "order_id": "ORD001",
  "order_date": "2026-02-07",
  "pickup_location": "Primary",
  "billing_customer_name": "Test Customer",
  "billing_city": "Bangalore",
  "billing_pincode": "560001",
  "billing_state": "Karnataka",
  "billing_country": "India",
  "billing_phone": "9999999999",
  "order_items": [{
    "name": "Test Product",
    "sku": "TEST001",
    "units": 1,
    "selling_price": 299
  }],
  "payment_method": "Prepaid",
  "weight": 0.3
}'
```

## Common Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Access backend shell
docker-compose exec backend /bin/bash

# Run tests
docker-compose exec backend pytest
```

## Troubleshooting

### Database Connection Issues
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Migration Issues
```bash
# Reset migrations (⚠️ deletes all data)
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

### View Application Logs
```bash
docker-compose logs -f backend
```

## Production Deployment

For production, use:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

Make sure to:
1. Change SECRET_KEY in .env
2. Use strong database passwords
3. Configure proper CORS origins
4. Set DEBUG=False
5. Use HTTPS with SSL certificates
