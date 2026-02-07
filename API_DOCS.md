# API Documentation

Complete API reference for the Shiprocket Integration Service.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All Shiprocket API calls require authentication. First, obtain a token:

### Login
```http
POST /auth/login
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## Orders API

### Create Order

Create a new order and submit to Shiprocket.

```http
POST /orders/
```

**Request Body:**
```json
{
  "order_id": "ORD123",
  "order_date": "2026-02-07",
  "pickup_location": "Primary",
  "billing_customer_name": "Rajarshi",
  "billing_city": "Bangalore",
  "billing_pincode": "560001",
  "billing_state": "Karnataka",
  "billing_country": "India",
  "billing_phone": "9999999999",
  "billing_email": "customer@example.com",
  "billing_address": "123 Main St",
  "order_items": [
    {
      "name": "USB Cable",
      "sku": "USB001",
      "units": 1,
      "selling_price": 299,
      "discount": 0,
      "tax": 0,
      "hsn": 8544
    }
  ],
  "payment_method": "Prepaid",
  "weight": 0.3,
  "length": 10,
  "breadth": 5,
  "height": 2
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "order_id": "ORD123",
  "shiprocket_order_id": 456789,
  "status": "submitted",
  "created_at": "2026-02-07T10:30:00",
  "updated_at": "2026-02-07T10:30:00"
}
```

### List Orders

Get all orders with pagination.

```http
GET /orders/?skip=0&limit=100
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "order_id": "ORD123",
    "shiprocket_order_id": 456789,
    "status": "submitted",
    "created_at": "2026-02-07T10:30:00",
    "updated_at": "2026-02-07T10:30:00"
  }
]
```

### Get Order

Get a specific order by ID.

```http
GET /orders/{order_id}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "order_id": "ORD123",
  "shiprocket_order_id": 456789,
  "status": "submitted",
  "created_at": "2026-02-07T10:30:00",
  "updated_at": "2026-02-07T10:30:00"
}
```

---

## Shipments API

### Check Serviceability

Check if delivery is available for given PIN codes.

```http
GET /shipments/serviceability?pickup_postcode=700001&delivery_postcode=560001&weight=0.5&cod=0
```

**Query Parameters:**
- `pickup_postcode` (required): 6-digit pickup PIN code
- `delivery_postcode` (required): 6-digit delivery PIN code
- `weight` (required): Package weight in kg
- `cod` (optional): Cash on delivery (0 or 1), default: 0

**Response:** `200 OK`
```json
[
  {
    "courier_company_id": 12,
    "courier_name": "Delhivery",
    "rate": 52.0,
    "estimated_delivery_days": 4,
    "cod": 0,
    "pickup_availability": "Available"
  }
]
```

### Assign AWB

Assign Air Waybill number to a shipment.

```http
POST /shipments/assign-awb
```

**Request Body:**
```json
{
  "shipment_id": 987654,
  "courier_id": 12
}
```

**Response:** `200 OK`
```json
{
  "message": "AWB assigned successfully",
  "awb_code": "SR123456789"
}
```

### Generate Label

Generate shipping label for shipments.

```http
POST /shipments/generate-label
```

**Request Body:**
```json
{
  "shipment_id": [987654]
}
```

**Response:** `200 OK`
```json
{
  "message": "Label generated successfully",
  "label_url": "https://shiprocket.in/label.pdf"
}
```

### Schedule Pickup

Schedule pickup for shipments.

```http
POST /shipments/schedule-pickup
```

**Request Body:**
```json
{
  "shipment_id": [987654],
  "pickup_date": "2026-02-08"
}
```

**Response:** `200 OK`
```json
{
  "message": "Pickup scheduled successfully",
  "response": {
    "pickup_scheduled": true
  }
}
```

### Track Shipment

Track shipment by AWB code.

```http
GET /shipments/track/{awb_code}
```

**Response:** `200 OK`
```json
{
  "awb_code": "SR123456789",
  "current_status": "In Transit",
  "tracking_history": [
    {
      "status": "Picked Up",
      "location": "Bangalore",
      "date": "2026-02-07 10:30:00"
    },
    {
      "status": "In Transit",
      "location": "Mumbai Hub",
      "date": "2026-02-07 18:45:00"
    }
  ]
}
```

### List Shipments

Get all shipments with pagination.

```http
GET /shipments/?skip=0&limit=100
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "order_id": 1,
    "shiprocket_shipment_id": 987654,
    "awb_code": "SR123456789",
    "courier_name": "Delhivery",
    "status": "in_transit",
    "current_status": "In Transit",
    "label_url": "https://shiprocket.in/label.pdf",
    "pickup_scheduled": true,
    "created_at": "2026-02-07T10:30:00",
    "updated_at": "2026-02-07T18:45:00"
  }
]
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Order ID already exists"
}
```

### 404 Not Found
```json
{
  "detail": "Order not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "billing_pincode"],
      "msg": "ensure this value has at least 6 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to submit to Shiprocket: Connection timeout"
}
```

---

## Data Models

### OrderItem
```typescript
{
  name: string;           // Product name
  sku: string;            // Product SKU
  units: number;          // Quantity (> 0)
  selling_price: number;  // Price per unit (> 0)
  discount?: number;      // Discount amount (>= 0)
  tax?: number;           // Tax amount (>= 0)
  hsn?: number;           // HSN code
}
```

### Order
```typescript
{
  id: number;
  order_id: string;
  shiprocket_order_id?: number;
  status: string;
  created_at: datetime;
  updated_at: datetime;
}
```

### Shipment
```typescript
{
  id: number;
  order_id: number;
  shiprocket_shipment_id?: number;
  awb_code?: string;
  courier_name?: string;
  status: string;
  current_status?: string;
  label_url?: string;
  pickup_scheduled: boolean;
  created_at: datetime;
  updated_at: datetime;
}
```

---

## Status Values

### Order Status
- `created` - Order created locally
- `submitted` - Submitted to Shiprocket
- `failed` - Submission failed

### Shipment Status
- `created` - Shipment created
- `awb_assigned` - AWB assigned
- `label_generated` - Label generated
- `pickup_scheduled` - Pickup scheduled
- `in_transit` - In transit
- `delivered` - Delivered

---

## Rate Limits

Currently no rate limits are enforced on the API. However, Shiprocket API has its own rate limits:
- Authentication: 10 requests/minute
- Other endpoints: 100 requests/minute

---

## Interactive Documentation

Visit these URLs when the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
