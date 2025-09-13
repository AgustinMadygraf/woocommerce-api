"""
Path: src/interface_adapters/controllers/cli_controller.py
"""

from src.shared.logger import logger

from src.entities.product import Product

class CLIController:
    """Controlador CLI centralizado para la interacción con el usuario."""
    def __init__(self, list_products_uc, get_product_by_sku_uc, create_product_uc, update_product_uc, presenter, test_sku="DEMO-0001"):
        self.list_products_uc = list_products_uc
        self.get_product_by_sku_uc = get_product_by_sku_uc
        self.create_product_uc = create_product_uc
        self.update_product_uc = update_product_uc
        self.presenter = presenter
        self.test_sku = test_sku

    def run(self):
        """Flujo principal de interacción CLI."""
        logger.info("Listando hasta 5 productos existentes (si hay)...")
        productos = self.list_products_uc.execute({"per_page": 5, "page": 1, "status": "any"})
        logger.debug("Productos obtenidos: %s", productos)
        self.presenter.show_product_list(productos)

        logger.info("Buscando producto de prueba por SKU…")
        prod = self.get_product_by_sku_uc.execute(self.test_sku)
        logger.debug("Resultado búsqueda SKU %s: %s", self.test_sku, prod)
        if prod:
            self.presenter.show_message(f"   Ya existe: ID {prod.product_id} – {prod.name}")
        else:
            self.presenter.show_message("   No existe. Creando producto de prueba…")
            new_product = Product(
                name="Producto de prueba (borrar)",
                type_="simple",
                regular_price="9.99",
                sku=self.test_sku,
                stock_quantity=10,
                status="draft"
            )
            logger.debug("Creando producto: %s", new_product)
            prod = self.create_product_uc.execute(new_product)
            logger.debug("Producto creado: %s", prod)

        logger.info("Actualizando precio a 12.99…")
        prod.regular_price = "12.99"
        updated = self.update_product_uc.execute(prod)
        logger.debug("Producto actualizado: %s", updated)
        self.presenter.show_message("   Producto actualizado:")
        self.presenter.show_product_detail(updated)
