"""
Path: src/infrastructure/google_sheets/sheets_gateway.py
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsGateway:
    "Gateway para interactuar con Google Sheets."
    def __init__(self, creds_json_path):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
        self.client = gspread.authorize(creds)

    def get_sheet_values(self, spreadsheet_id, worksheet_name):
        " Obtiene todos los valores de una hoja específica."
        sheet = self.client.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        return worksheet.get_all_values()
