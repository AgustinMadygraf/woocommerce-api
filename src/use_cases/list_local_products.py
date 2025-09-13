"""
Path: src/use_cases/list_local_products.py
"""

from typing import List, Any
from src.interface_adapters.gateways.product_persistence_gateway import ProductPersistenceGateway

class ListLocalProductsUseCase:
    " Use case para listar productos locales desde la base de datos. "
    def __init__(self, gateway: ProductPersistenceGateway):
        self.gateway = gateway

    def execute(self) -> List[Any]:
        "Ejecuta el caso de uso y devuelve la lista de productos locales."
        return self.gateway.list_products()
