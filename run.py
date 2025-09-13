"""
Path: run.py
"""

from src.infrastructure.woocommerce.gateway_impl import WooCommerceProductGateway
from src.interface_adapters.presenters.product_presenter import ProductPresenter
from src.interface_adapters.controllers.cli_controller import CLIController
from src.use_cases.list_products import ListProductsUseCase
from src.use_cases.get_product_by_id import GetProductByIdUseCase
from src.use_cases.create_product import CreateProductUseCase
from src.use_cases.update_product import UpdateProductUseCase

TEST_SKU = "DEMO-0001"

if __name__ == "__main__":
    gateway = WooCommerceProductGateway()
    list_products = ListProductsUseCase(gateway)
    get_product_by_id = GetProductByIdUseCase(gateway)
    create_product = CreateProductUseCase(gateway)
    update_product = UpdateProductUseCase(gateway)
    Presenter = ProductPresenter
    controller = CLIController(
        list_products_uc=list_products,
        get_product_by_id_uc=get_product_by_id,
        create_product_uc=create_product,
        update_product_uc=update_product,
        presenter=Presenter,
        test_sku=TEST_SKU
    )
    controller.run()
