"""
Path: run.py
"""

import sys
import json
from woocommerce import API
from src.shared.config import URL, CK, CS
from src.shared.logger import logger

# SKU fijo para pruebas (idempotente)
TEST_SKU = "DEMO-0001"

def wc():
    """Cliente WooCommerce REST v3."""
    return API(
        url=URL,
        consumer_key=CK,
        consumer_secret=CS,
        version="wc/v3",
        timeout=30
    )

def ok(resp, expect=200):
    """Chequeo simple de estado y log de errores legibles."""
    if resp.status_code == expect:
        return True
    try:
        body = resp.json()
    except json.decoder.JSONDecodeError:
        body = resp.text
    logger.error("HTTP %s (esperado %s). Respuesta:\n%s", resp.status_code, expect, body)
    return False

def pretty(obj):
    " Print JSON bonito."
    logger.info(json.dumps(obj, indent=2, ensure_ascii=False))

def get_product_by_sku(client, sku):
    """Buscar producto por SKU. Retorna dict o None."""
    r = client.get("products", params={"sku": sku})
    if not ok(r, expect=200):
        sys.exit(1)
    items = r.json()
    return items[0] if items else None

def main():
    "Flujo mínimo de prueba: listar, crear, actualizar, borrar."
    client = wc()

    print("1) Listando hasta 5 productos existentes (si hay):")
    r = client.get("products", params={"per_page": 5, "page": 1})
    if not ok(r, expect=200): sys.exit(1)
    for p in r.json():
        print(f"   - [{p['id']}] {p['name']} | SKU: {p.get('sku') or '-'} | Precio: {p.get('regular_price') or '-'}")

    # 2) Buscar o crear producto de prueba
    print("\n2) Buscando producto de prueba por SKU…")
    prod = get_product_by_sku(client, TEST_SKU)
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
        r = client.post("products", data=payload)
        if not ok(r, expect=201): sys.exit(1)
        prod = r.json()
        logger.info("   Creado: ID %s – %s", prod['id'], prod['name'])

    # 3) Actualizar precio
    print("\n3) Actualizando precio a 12.99…")
    r = client.put(f"products/{prod['id']}", data={"regular_price": "12.99"})
    if not ok(r, expect=200): sys.exit(1)
    prod = r.json()
    logger.info("   Producto actualizado:")
    pretty({"id": prod["id"], "name": prod["name"], "price": prod["regular_price"], "sku": prod["sku"]})

    # 4) Eliminar (force=True para borrado permanente)
    print("\n4) Eliminando producto de prueba…")
    r = client.delete(f"products/{prod['id']}", params={"force": True})
    if not ok(r, expect=200): sys.exit(1)
    logger.info("   Eliminado correctamente.")

    logger.info("\n✔ Flujo mínimo OK.")

if __name__ == "__main__":
    if "xxxx" in CK or "xxxx" in CS or URL.startswith("https://tu-"):
        logger.error("⚠ Configurá URL, CK y CS antes de ejecutar.")
        sys.exit(1)
    main()
