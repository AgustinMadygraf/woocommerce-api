"""
Path: src/interface_adapters/gateways/woocommerce_gateway.py
"""

from woocommerce import API
import requests

from src.entities.product import Product
from src.shared.config import URL, CK, CS
from src.shared.logger import logger

class WooCommerceGateway:
    "Puerta de enlace para interactuar con la API de WooCommerce."
    def __init__(self):
        self.wcapi = API(
            url=URL,
            consumer_key=CK,
            consumer_secret=CS,
            version="wc/v3"
        )

    def list_products(self, params=None):
        "Listar productos con parámetros opcionales. Devuelve lista de entidades Product."
        try:
            response = self.wcapi.get("products", params=params or {})
            response.raise_for_status()
            data = response.json()
            return [Product.from_dict(d) for d in data]
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al listar productos: %s", e)
            return []

    def get_product_by_sku(self, sku):
        "Buscar producto por SKU. Devuelve entidad Product o None."
        try:
            response = self.wcapi.get("products", params={"sku": sku})
            response.raise_for_status()
            products = response.json()
            return Product.from_dict(products[0]) if products else None
        except (requests.exceptions.RequestException, ValueError, IndexError) as e:
            logger.error("Error al buscar producto por SKU: %s", e)
            return None

    def create_product(self, data):
        "Crear un producto nuevo. Devuelve entidad Product."
        try:
            response = self.wcapi.post("products", data)
            response.raise_for_status()
            return Product.from_dict(response.json())
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al crear producto: %s", e)
            return None

    def update_product(self, product_id, data):
        "Actualizar un producto existente. Devuelve entidad Product."
        try:
            response = self.wcapi.put(f"products/{product_id}", data)
            response.raise_for_status()
            return Product.from_dict(response.json())
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al actualizar producto: %s", e)
            return None

    def delete_product(self, product_id, force=True):
        "Eliminar un producto por ID."
        try:
            response = self.wcapi.delete(f"products/{product_id}", params={"force": force})
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error("Error al eliminar producto: %s", e)
            return None
