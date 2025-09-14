"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
import traceback
from flask import Flask, jsonify, send_from_directory

from src.infrastructure.pymysql.product_persistence_gateway_impl import ProductPersistenceGatewayImpl
from src.infrastructure.woocommerce.gateway_impl import WooCommerceProductGateway
from src.use_cases.update_local_products_from_woocommerce import UpdateLocalProductsFromWooCommerceUseCase
from src.infrastructure.google_sheets.sheets_gateway import GoogleSheetsGateway
from src.use_cases.list_sheet_values import ListSheetValuesUseCase
from src.use_cases.update_local_products_from_sheets import UpdateLocalProductsFromSheetsUseCase
from src.shared.config import GOOGLE_CREDS_PATH, SPREADSHEET_ID, WORKSHEET_NAME

# Get the project root directory (3 levels up from the current file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
static_folder = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_folder)

@app.route('/api/update-from-woocommerce', methods=['POST'])
def update_from_woocommerce():
    """Endpoint para actualizar la base de datos local desde WooCommerce."""
    try:
        woocommerce_gateway = WooCommerceProductGateway()
        persistence_gateway = ProductPersistenceGatewayImpl()
        use_case = UpdateLocalProductsFromWooCommerceUseCase(woocommerce_gateway, persistence_gateway)
        result = use_case.execute()
        return jsonify({"success": True, "message": "Actualización desde WooCommerce completada.", "result": result})
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        print("[ERROR] /api/update-from-woocommerce:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/sheet-values')
def api_sheet_values():
    "Endpoint que devuelve los valores de productos desde MySQL para la tabla."
    try:
        mysql_gateway = ProductPersistenceGatewayImpl()
        productos = mysql_gateway.list_google_sheet_products()
        # Opcional: transformar a formato de tabla si es necesario
        if not productos:
            return jsonify([])
        # Encabezados
        headers = ["id_google_sheets", "formato", "color", "stock_quantity"]
        data = [headers]
        for prod in productos:
            data.append([
                prod.get("id_google_sheets"),
                prod.get("formato"),
                prod.get("color"),
                prod.get("stock_quantity"),
            ])
        return jsonify(data)
    except (AttributeError, KeyError, TypeError) as e:
        print("[ERROR] /api/sheet-values: Error al procesar los datos:", e)
        traceback.print_exc()
        return jsonify({"error": "Error al procesar los datos de la base de datos MySQL. Contacta al administrador."}), 500

@app.route('/api/update-from-sheets', methods=['POST'])
def update_from_sheets():
    """Endpoint para actualizar la base de datos local desde Google Sheets."""
    try:
        # Instanciar gateway de Google Sheets
        sheets_gateway = GoogleSheetsGateway(GOOGLE_CREDS_PATH)
        # Caso de uso para obtener valores de la hoja
        list_sheet_values_uc = ListSheetValuesUseCase(sheets_gateway, SPREADSHEET_ID, WORKSHEET_NAME)
        # Obtener los valores crudos de la hoja
        values = list_sheet_values_uc.execute()
        # Instanciar gateway de persistencia local
        persistence_gateway = ProductPersistenceGatewayImpl()
        # Caso de uso para actualizar productos locales
        update_local_products_from_sheets_uc = UpdateLocalProductsFromSheetsUseCase(persistence_gateway)
        # Actualizar productos locales desde los valores de Sheets
        result = update_local_products_from_sheets_uc.execute(values)
        return jsonify({"success": True, "message": "Actualización desde Google Sheets completada.", "result": result})
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        print("[ERROR] /api/update-from-sheets:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/woocommerce-products')
def api_woocommerce_products():
    "Endpoint que devuelve los productos WooCommerce almacenados en MySQL."
    try:
        mysql_gateway = ProductPersistenceGatewayImpl()
        productos = mysql_gateway.list_products()
        if not productos:
            return jsonify([])
        # Encabezados
        headers = ["id", "name", "sku", "regular_price", "stock_quantity", "status", "type"]
        data = [headers]
        for prod in productos:
            data.append([
                prod.get("id"),
                prod.get("name"),
                prod.get("sku"),
                prod.get("regular_price"),
                prod.get("stock_quantity"),
                prod.get("status"),
                prod.get("type"),
            ])
        return jsonify(data)
    except (AttributeError, KeyError, TypeError) as e:
        print("[ERROR] /api/woocommerce-products: Error al procesar los datos:", e)
        traceback.print_exc()
        return jsonify({"error": "Error al procesar los datos de la base de datos MySQL. Contacta al administrador."}), 500

@app.route('/')
def index():
    "Sirve el archivo index.html desde el directorio static."
    return send_from_directory(app.static_folder, 'index.html')
