"""
Path: src/use_cases/update_product.py
"""

from src.entities.product import Product

class UpdateProductUseCase:
    "Caso de uso para actualizar un producto usando la entidad Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product: Product):
        "Actualiza un producto usando la entidad Product."
        data = product.to_dict()
        product_id = product.product_id  # <-- corregido aquí
        return self.product_gateway.update_product(product_id, data)
