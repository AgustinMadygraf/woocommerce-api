"""
Path: run.py
"""

from src.interface_adapters.gateways.woocommerce_gateway import WooCommerceGateway
from src.use_cases.list_products import ListProductsUseCase
from src.use_cases.get_product_by_sku import GetProductBySkuUseCase
from src.use_cases.create_product import CreateProductUseCase
from src.use_cases.update_product import UpdateProductUseCase
from src.interface_adapters.presenters.product_presenter import ProductPresenter

# SKU fijo para pruebas (idempotente)
TEST_SKU = "DEMO-0001"



def main():
    """Flujo mínimo de prueba: listar, crear, actualizar, borrar usando WooCommerceGateway."""
    gateway = WooCommerceGateway()
    list_products = ListProductsUseCase(gateway)
    get_product_by_sku = GetProductBySkuUseCase(gateway)
    create_product = CreateProductUseCase(gateway)
    update_product = UpdateProductUseCase(gateway)


    print("1) Listando hasta 5 productos existentes (si hay):")
    productos = list_products.execute({"per_page": 5, "page": 1})
    ProductPresenter.show_product_list(productos)


    # 2) Buscar o crear producto de prueba
    print("\n2) Buscando producto de prueba por SKU…")
    prod = get_product_by_sku.execute(TEST_SKU)
    if prod:
        ProductPresenter.show_message(f"   Ya existe: ID {prod['id']} – {prod['name']}")
    else:
        ProductPresenter.show_message("   No existe. Creando producto de prueba…")
        payload = {
            "name": "Producto de prueba (borrar)",
            "type": "simple",
            "regular_price": "9.99",
            "sku": TEST_SKU,
            "manage_stock": True,
            "stock_quantity": 10,
            "status": "draft"  # mantenerlo en borrador para no mostrarlo en la tienda
        }
        prod = create_product.execute(payload)

    # 3) Actualizar precio
    print("\n3) Actualizando precio a 12.99…")
    prod = update_product.execute(prod['id'], {"regular_price": "12.99"})
    ProductPresenter.show_message("   Producto actualizado:")
    ProductPresenter.show_product_detail({"id": prod["id"], "name": prod["name"], "price": prod["regular_price"], "sku": prod["sku"]})
