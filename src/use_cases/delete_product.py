class DeleteProductUseCase:
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product_id, force=True):
        return self.product_gateway.delete_product(product_id, force=force)
