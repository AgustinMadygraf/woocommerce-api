class UpdateProductUseCase:
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, product_id, data):
        return self.product_gateway.update_product(product_id, data)
