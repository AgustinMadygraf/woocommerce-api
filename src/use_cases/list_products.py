"""
Path: src/use_cases/list_products.py
"""

from src.entities.product import Product

class ListProductsUseCase:
    "Caso de uso para listar productos, devolviendo entidades Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, filters=None):
        "Lista productos con filtros opcionales y los convierte a Product."
        data_list = self.product_gateway.list_products(filters)
        return [Product.from_dict(data) for data in data_list]
