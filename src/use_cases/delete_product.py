"""
Path: src/use_cases/delete_product.py
"""

class DeleteProductUseCase:
    " Caso de uso para eliminar un producto."
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product_id, force=True):
        " Elimina un producto por su ID."
        return self.product_gateway.delete_product(product_id, force=force)
