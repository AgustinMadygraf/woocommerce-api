"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
from flask import Flask, jsonify, send_from_directory

from src.shared import config

from src.infrastructure.google_sheets.sheets_gateway import GoogleSheetsGateway
from src.infrastructure.google_sheets.sheet_product_adapter import SheetProductAdapter
from src.use_cases.list_sheet_values import ListSheetValuesUseCase

# Get the project root directory (3 levels up from the current file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
static_folder = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_folder)

@app.route('/api/sheet-values')
def api_sheet_values():
    "Endpoint que devuelve los valores de Google Sheets transformados para la tabla."
    try:
        sheets_gateway = GoogleSheetsGateway(config.GOOGLE_CREDS_PATH)
        use_case = ListSheetValuesUseCase(
            sheets_gateway,
            config.SPREADSHEET_ID,
            config.WORKSHEET_NAME
        )
        raw_values = use_case.execute()
        data = SheetProductAdapter.transform(raw_values)
        return jsonify(data)
    except Exception as e:
        import traceback
        print("[ERROR] /api/sheet-values:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    "Sirve el archivo index.html desde el directorio static."
    return send_from_directory(app.static_folder, 'index.html')
