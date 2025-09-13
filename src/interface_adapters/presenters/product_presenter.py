"""
Path: src/interface_adapters/presenters/product_presenter.py
"""

import json
from src.shared.logger import logger

class ProductPresenter:
    "Clase para presentar la información del producto."
    @staticmethod
    def show_product_list(products):
        " Muestra una lista de productos."
        if not products:
            print("No hay productos para mostrar.")
            return
        for p in products:
            print(f"   - [{p['id']}] {p['name']} | SKU: {p.get('sku') or '-'} | Precio: {p.get('regular_price') or '-'}")

    @staticmethod
    def show_product_detail(product):
        " Muestra detalles de un solo producto."
        if not product:
            print("Producto no encontrado.")
            return
        logger.info(json.dumps(product, indent=2, ensure_ascii=False))

    @staticmethod
    def show_message(message):
        " Muestra un mensaje informativo."
        print(message)

    @staticmethod
    def show_error(message):
        " Muestra un mensaje de error."
        logger.error(message)
