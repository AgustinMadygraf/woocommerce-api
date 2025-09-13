"""
Path: src/use_cases/list_products.py
"""

class ListProductsUseCase:
    "Caso de uso para listar productos, devolviendo entidades Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, params=None):
        "Lista productos con parámetros opcionales y los devuelve como entidades Product."
        return self.product_gateway.list_products(params)
