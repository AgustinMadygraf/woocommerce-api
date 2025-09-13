"""
Path: run.py
"""

import json
from src.shared.logger import logger
from src.interface_adapters.gateways.woocommerce_gateway import WooCommerceGateway

# SKU fijo para pruebas (idempotente)
TEST_SKU = "DEMO-0001"

def pretty(obj):
    """Print JSON bonito."""
    logger.info(json.dumps(obj, indent=2, ensure_ascii=False))

def main():
    """Flujo mínimo de prueba: listar, crear, actualizar, borrar usando WooCommerceGateway."""
    gateway = WooCommerceGateway()
    print("1) Listando hasta 5 productos existentes (si hay):")
    productos = gateway.list_products({"per_page": 5, "page": 1})
    for p in productos:
        print(f"   - [{p['id']}] {p['name']} | SKU: {p.get('sku') or '-'} | Precio: {p.get('regular_price') or '-'}")

    # 2) Buscar o crear producto de prueba
    print("\n2) Buscando producto de prueba por SKU…")
    prod = gateway.get_product_by_sku(TEST_SKU)
    if prod:
        logger.info("   Ya existe: ID %s – %s", prod['id'], prod['name'])
    else:
        logger.info("   No existe. Creando producto de prueba…")
        payload = {
            "name": "Producto de prueba (borrar)",
            "type": "simple",
            "regular_price": "9.99",
            "sku": TEST_SKU,
            "manage_stock": True,
            "stock_quantity": 10,
            "status": "draft"  # mantenerlo en borrador para no mostrarlo en la tienda
        }
        prod = gateway.create_product(payload)

    # 3) Actualizar precio
    print("\n3) Actualizando precio a 12.99…")
    prod = gateway.update_product(prod['id'], {"regular_price": "12.99"})
    logger.info("   Producto actualizado:")
    pretty({"id": prod["id"], "name": prod["name"], "price": prod["regular_price"], "sku": prod["sku"]})
