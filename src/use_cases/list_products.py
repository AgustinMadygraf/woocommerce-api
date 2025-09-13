"""
Path: src/use_cases/list_products.py
"""

class ListProductsUseCase:
    " Caso de uso para listar productos."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, filters=None):
        " Lista productos con filtros opcionales."
        return self.product_gateway.list_products(filters)
