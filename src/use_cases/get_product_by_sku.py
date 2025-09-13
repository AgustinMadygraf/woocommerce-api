"""
Path: src/use_cases/get_product_by_sku.py
"""

class GetProductBySkuUseCase:
    "Caso de uso para obtener un producto por su SKU, devolviendo una entidad Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, sku):
        "Obtiene un producto por su SKU y lo devuelve como Product o None."
        return self.product_gateway.get_product_by_sku(sku)
