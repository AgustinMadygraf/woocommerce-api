class CreateProductUseCase:
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, data):
        return self.product_gateway.create_product(data)
