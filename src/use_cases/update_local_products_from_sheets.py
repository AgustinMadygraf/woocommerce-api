"""
Path: src/use_cases/update_local_products_from_sheets.py
"""

from typing import List
from src.interface_adapters.gateways.product_persistence_gateway import ProductPersistenceGateway

class UpdateLocalProductsFromSheetsUseCase:
    " Use case para actualizar productos locales desde datos de Google Sheets. "
    def __init__(self, gateway: ProductPersistenceGateway):
        self.gateway = gateway

    def execute(self, values: List[list]) -> dict:
        "Ejecuta el caso de uso para actualizar productos locales desde los valores proporcionados de Google Sheets."
        return self.gateway.update_products_from_sheet(values)
