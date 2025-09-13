"""
Caso de uso: Obtener producto por ID
Ubicación: src/use_cases/get_product_by_id.py
"""

from typing import Optional
from src.entities.product import Product
from src.interface_adapters.gateways.base_gateway import BaseProductGateway

class GetProductByIdUseCase:
    def __init__(self, gateway: BaseProductGateway):
        self.gateway = gateway

    def execute(self, product_id: int) -> Optional[Product]:
        data = self.gateway.get_product_by_id(product_id)
        if data:
            return Product.from_dict(data)
        return None
