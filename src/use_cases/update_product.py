"""
Path: src/use_cases/update_product.py
"""

class UpdateProductUseCase:
    " Caso de uso para actualizar un producto."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product_id, data):
        " Actualiza un producto por su ID con los datos proporcionados."
        return self.product_gateway.update_product(product_id, data)
