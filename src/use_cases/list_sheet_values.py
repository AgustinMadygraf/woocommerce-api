"""
Path: src/use_cases/list_sheet_values.py
"""

class ListSheetValuesUseCase:
    " Caso de uso para listar valores de una hoja de Google Sheets."
    def __init__(self, sheets_gateway, spreadsheet_id, worksheet_name):
        self.sheets_gateway = sheets_gateway
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name

    def execute(self):
        "Ejecuta el caso de uso para obtener los valores de la hoja."
        return self.sheets_gateway.get_sheet_values(self.spreadsheet_id, self.worksheet_name)
    