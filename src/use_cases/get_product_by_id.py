"""
Path: src/use_cases/get_product_by_id.py
"""

from typing import Optional

from src.entities.product import Product
from src.interface_adapters.gateways.base_product_gateway import BaseProductGateway

class GetProductByIdUseCase:
    " Caso de uso para obtener un producto por su ID, devolviendo una entidad Product."
    def __init__(self, gateway: BaseProductGateway):
        self.gateway = gateway

    def execute(self, product_id: int) -> Optional[Product]:
        "Obtiene un producto por su ID y lo devuelve como una entidad Product."
        data = self.gateway.get_product_by_id(product_id)
        if data:
            return Product.from_dict(data)
        return None
