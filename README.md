# Shiprocket API Integration

Production-ready Shiprocket API integration service built with FastAPI, PostgreSQL, Redis, Docker, Alembic, and Pydantic.

## 🚀 Features

- **Complete Shiprocket API Integration**: All 7 core endpoints implemented
  - Authentication
  - Serviceability Check
  - Order Creation
  - AWB Assignment
  - Label Generation
  - Pickup Scheduling
  - Shipment Tracking

- **Modern Tech Stack**:
  - FastAPI with async/await
  - SQLAlchemy 2.0 with async support
  - Pydantic v2 for validation
  - Alembic for database migrations
  - PostgreSQL for data persistence
  - Redis for caching
  - Docker & Docker Compose

- **Production Ready**:
  - Professional folder structure
  - Health checks
  - CORS configuration
  - Logging with Loguru
  - Connection pooling
  - Error handling
  - API documentation (Swagger/ReDoc)

## 📁 Project Structure

```
shiprocket/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── orders.py
│   │       │   └── shipments.py
│   │       └── router.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── order.py
│   │   └── shipment.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── order.py
│   │   └── shipment.py
│   ├── services/
│   │   └── shiprocket.py
│   ├── config.py
│   └── main.py
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Setup

### 1. Clone and Configure

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your Shiprocket credentials
# SHIPROCKET_EMAIL=your_email@company.com
# SHIPROCKET_PASSWORD=your_password
```

### 2. Run with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

### 3. Run Database Migrations

```bash
# Create initial migration
docker-compose exec backend alembic revision --autogenerate -m "Initial migration"

# Apply migrations
docker-compose exec backend alembic upgrade head
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔑 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Get Shiprocket bearer token

### Orders
- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/` - List all orders
- `GET /api/v1/orders/{order_id}` - Get specific order

### Shipments
- `GET /api/v1/shipments/serviceability` - Check courier serviceability
- `POST /api/v1/shipments/assign-awb` - Assign AWB to shipment
- `POST /api/v1/shipments/generate-label` - Generate shipping label
- `POST /api/v1/shipments/schedule-pickup` - Schedule pickup
- `GET /api/v1/shipments/track/{awb_code}` - Track shipment
- `GET /api/v1/shipments/` - List all shipments

## 📝 Example Usage

### Create Order

```bash
curl -X POST http://localhost:8000/api/v1/orders/ \
-H "Content-Type: application/json" \
-d '{
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
}'
```

## 🔧 Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🐳 Docker Commands

```bash
# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Remove volumes (⚠️ deletes data)
docker-compose down -v

# Rebuild
docker-compose up --build
```

## 🧪 Testing

```bash
# Run tests
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov=app
```

## 📦 Environment Variables

See `.env.example` for all available configuration options.

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Use strong database passwords
- Keep Shiprocket credentials secure
- Enable HTTPS in production
- Configure CORS origins appropriately

## 📄 License

MIT License
