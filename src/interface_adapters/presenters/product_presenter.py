"""
Path: src/interface_adapters/presenters/product_presenter.py
"""

import json

from src.shared.logger import logger

class ProductPresenter:
    "Clase para presentar la información del producto."
    @staticmethod
    def show_product_list(products):
        """Muestra una lista de productos (solo entidades Product)."""
        try:
            logger.info("Mostrando lista de productos (%d)", len(products) if products else 0)
            if not products:
                logger.warning("No hay productos para mostrar.")
                return
            print("\n=== LISTA DE PRODUCTOS ===")
            for p in products:
                try:
                    logger.debug("Producto: %s", p)
                    print(json.dumps(p.to_dict(), indent=2, ensure_ascii=False))
                except (AttributeError, TypeError) as e:
                    logger.error("Error mostrando producto: %s", e)
            print("=== FIN DE LISTA ===\n")
        except (AttributeError, TypeError) as e:
            logger.error("Error en show_product_list: %s", e)

    @staticmethod
    def show_product_detail(product):
        """Muestra detalles de un solo producto (entidad Product)."""
        try:
            if not product:
                logger.warning("Producto no encontrado para mostrar detalle.")
                return
            logger.info("Mostrando detalle de producto: %s", product.product_id)
            logger.debug("Detalle producto: %s", product)
            logger.info(json.dumps(product.to_dict(), indent=2, ensure_ascii=False))
        except (AttributeError, TypeError, ValueError) as e:
            logger.error("Error en show_product_detail: %s", e)

    @staticmethod
    def show_message(message):
        "Muestra un mensaje informativo."
        try:
            logger.info("Mensaje mostrado: %s", message)
        except (TypeError, ValueError) as e:
            logger.error("Error en show_message: %s", e)

    @staticmethod
    def show_error(message):
        "Muestra un mensaje de error."
        try:
            logger.error("ERROR: %s", message)
        except (TypeError, ValueError) as e:
            logger.critical("Error en show_error: %s", e)

    @staticmethod
    def show_sheet_values(values):
        """Muestra los valores de una hoja de cálculo."""
        if not values:
            print("No hay datos en la hoja.")
            return
        print("\n=== DATOS DE GOOGLE SHEETS ===")
        for row in values:
            print(" | ".join(str(cell) for cell in row))
        print("=== FIN DE DATOS ===\n")
