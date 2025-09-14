"""
Caso de uso: Actualizar productos locales desde WooCommerce
"""
from src.infrastructure.woocommerce.woocommerce_product_adapter import WooCommerceProductAdapter

class UpdateLocalProductsFromWooCommerceUseCase:
    " Use case para actualizar productos locales desde WooCommerce. "
    def __init__(self, woocommerce_gateway, persistence_gateway):
        self.woocommerce_gateway = woocommerce_gateway
        self.persistence_gateway = persistence_gateway

    def execute(self):
        "Ejecuta el caso de uso para actualizar productos locales desde WooCommerce."
        # Obtener productos desde WooCommerce
        productos = self.woocommerce_gateway.list_products({"status": "any", "per_page": 100})
        # Transformar al formato esperado por la tabla local
        productos_transformados = WooCommerceProductAdapter.transform(productos)
        # Actualizar tabla local
        resultado = self.persistence_gateway.update_products_from_woocommerce(productos_transformados)
        return resultado
