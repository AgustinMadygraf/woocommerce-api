"""
Path: src/use_cases/delete_product.py
"""

from src.entities.product import Product

class DeleteProductUseCase:
    "Caso de uso para eliminar un producto usando la entidad Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product: Product, force=True):
        "Elimina un producto usando la entidad Product."
        return self.product_gateway.delete_product(product.id, force=force)
