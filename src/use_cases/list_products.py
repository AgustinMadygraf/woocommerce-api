class ListProductsUseCase:
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, filters=None):
        return self.product_gateway.list_products(filters)
