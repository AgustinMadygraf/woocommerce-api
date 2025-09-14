"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
import traceback
from flask import Flask, jsonify, send_from_directory

from src.infrastructure.pymysql.product_persistence_gateway_impl import ProductPersistenceGatewayImpl

# Get the project root directory (3 levels up from the current file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
static_folder = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_folder)

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
