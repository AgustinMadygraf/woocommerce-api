"""
Transforma los datos de productos desde WooCommerce a un formato estándar para MySQL.
Ubicación: src/interface_adapters/presenter/woocommerce_product_adapter.py
"""

class WooCommerceProductAdapter:
    """Transforma los datos de productos desde WooCommerce a un formato estándar para MySQL."""
    @staticmethod
    def transform(raw_products: list) -> list:
        """
        Transforma la lista de productos de WooCommerce al formato de la tabla products_woocommerce.
        Devuelve una lista donde la primera fila son los encabezados.
        """
        header = ["id", "name", "sku", "regular_price", "stock_quantity", "status", "type"]
        transformed = [header]
        for p in raw_products:
            row = [
                p.get("id"),
                p.get("name", ""),
                p.get("sku", ""),
                p.get("regular_price", "0.00"),
                p.get("stock_quantity", 0),
                p.get("status", ""),
                p.get("type", "")
            ]
            transformed.append(row)
        return transformed
