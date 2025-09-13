"""
Path: src/use_cases/create_product.py
"""

class CreateProductUseCase:
    " Caso de uso para crear un producto."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, data):
        " Crea un nuevo producto con los datos proporcionados."
        return self.product_gateway.create_product(data)
