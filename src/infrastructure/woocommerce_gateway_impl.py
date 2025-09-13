"""
Implementación concreta del gateway WooCommerce para productos.
Ubicación: src/infrastructure/woocommerce_gateway_impl.py
"""

from typing import Any, Dict, List, Optional
from woocommerce import API
import requests

from src.shared.config import URL, CK, CS
from src.shared.logger import logger

from src.entities.gateways.base_product_gateway import BaseProductGateway

class WooCommerceProductGateway(BaseProductGateway):
    "Implementación concreta del gateway de productos usando WooCommerce API."
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtener un producto por su ID usando la API de WooCommerce."""
        try:
            response = self.wcapi.get(f"products/{product_id}")
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al buscar producto por ID: %s", e)
            return None
    def __init__(self):
        self.wcapi = API(
            url=URL,
            consumer_key=CK,
            consumer_secret=CS,
            version="wc/v3"
        )

    def list_products(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            response = self.wcapi.get("products", params=filters or {})
            response.raise_for_status()
            data = response.json()
            return data
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al listar productos: %s", e)
            return []

    def get_product_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.wcapi.get("products", params={"sku": sku})
            response.raise_for_status()
            products = response.json()
            return products[0] if products else None
        except (requests.exceptions.RequestException, ValueError, IndexError) as e:
            logger.error("Error al buscar producto por SKU: %s", e)
            return None

    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.wcapi.post("products", data)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al crear producto: %s", e)
            return {}

    def update_product(self, product_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.wcapi.put(f"products/{product_id}", data)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al actualizar producto: %s", e)
            return {}

    def delete_product(self, product_id: int) -> bool:
        try:
            response = self.wcapi.delete(f"products/{product_id}", params={"force": True})
            response.raise_for_status()
            return True
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al eliminar producto: %s", e)
            return False
