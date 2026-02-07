"""Shiprocket API service."""

from typing import Optional, Dict, Any, List
import httpx
from loguru import logger
from app.config import settings


class ShiprocketService:
    """Service for interacting with Shiprocket API."""

    def __init__(self):
        self.base_url = settings.SHIPROCKET_BASE_URL
        self.email = settings.SHIPROCKET_EMAIL
        self.password = settings.SHIPROCKET_PASSWORD
        self._token: Optional[str] = None

    async def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token."""
        if not self._token:
            await self.authenticate()
        
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}"
        }

    async def authenticate(self) -> str:
        """
        Authenticate with Shiprocket API.
        
        Returns:
            str: Bearer token
        """
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": self.email,
            "password": self.password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                self._token = data.get("token")
                logger.info("Successfully authenticated with Shiprocket")
                return self._token
            except httpx.HTTPError as e:
                logger.error(f"Authentication failed: {e}")
                raise

    async def check_serviceability(
        self,
        pickup_postcode: str,
        delivery_postcode: str,
        weight: float,
        cod: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Check courier serviceability.
        
        Args:
            pickup_postcode: Pickup PIN code
            delivery_postcode: Delivery PIN code
            weight: Package weight in kg
            cod: Cash on delivery (0 or 1)
            
        Returns:
            List of available couriers
        """
        url = f"{self.base_url}/courier/serviceability"
        params = {
            "pickup_postcode": pickup_postcode,
            "delivery_postcode": delivery_postcode,
            "weight": weight,
            "cod": cod
        }
        
        headers = await self._get_headers()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data.get("data", {}).get("available_courier_companies", [])
            except httpx.HTTPError as e:
                logger.error(f"Serviceability check failed: {e}")
                raise

    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create order in Shiprocket.
        
        Args:
            order_data: Order payload
            
        Returns:
            Order response with order_id and shipment_id
        """
        url = f"{self.base_url}/orders/create/adhoc"
        headers = await self._get_headers()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=order_data, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Order created successfully: {data}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Order creation failed: {e}")
                raise

    async def assign_awb(self, shipment_id: int, courier_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Assign AWB to shipment.
        
        Args:
            shipment_id: Shiprocket shipment ID
            courier_id: Optional specific courier ID
            
        Returns:
            AWB assignment response
        """
        url = f"{self.base_url}/courier/assign/awb"
        headers = await self._get_headers()
        payload = {"shipment_id": shipment_id}
        
        if courier_id:
            payload["courier_id"] = courier_id
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"AWB assigned: {data}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"AWB assignment failed: {e}")
                raise

    async def generate_label(self, shipment_ids: List[int]) -> Dict[str, Any]:
        """
        Generate shipping label.
        
        Args:
            shipment_ids: List of shipment IDs
            
        Returns:
            Label generation response with URL
        """
        url = f"{self.base_url}/courier/generate/label"
        headers = await self._get_headers()
        payload = {"shipment_id": shipment_ids}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Label generated: {data}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Label generation failed: {e}")
                raise

    async def schedule_pickup(self, shipment_ids: List[int]) -> Dict[str, Any]:
        """
        Schedule pickup for shipments.
        
        Args:
            shipment_ids: List of shipment IDs
            
        Returns:
            Pickup scheduling response
        """
        url = f"{self.base_url}/courier/generate/pickup"
        headers = await self._get_headers()
        payload = {"shipment_id": shipment_ids}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Pickup scheduled: {data}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Pickup scheduling failed: {e}")
                raise

    async def track_shipment(self, awb_code: str) -> Dict[str, Any]:
        """
        Track shipment by AWB code.
        
        Args:
            awb_code: AWB tracking code
            
        Returns:
            Tracking information
        """
        url = f"{self.base_url}/courier/track/awb/{awb_code}"
        headers = await self._get_headers()
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Tracking info retrieved for {awb_code}")
                return data
            except httpx.HTTPError as e:
                logger.error(f"Tracking failed: {e}")
                raise
