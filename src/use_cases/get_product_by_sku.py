class GetProductBySkuUseCase:
    def __init__(self, product_gateway):
        self.product_gateway = product_gateway

    def execute(self, sku):
        return self.product_gateway.get_product_by_sku(sku)
