"""
Path: src/use_cases/create_product.py
"""

from src.entities.product import Product

class CreateProductUseCase:
    "Caso de uso para crear un producto usando la entidad Product."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product: Product):
        "Crea un nuevo producto usando la entidad Product."
        data = product.to_dict()
        return self.product_gateway.create_product(data)
