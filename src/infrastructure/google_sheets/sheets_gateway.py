"""
Path: src/infrastructure/google_sheets/sheets_gateway.py
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from src.shared.logger import logger

class GoogleSheetsGateway:
    "Gateway para interactuar con Google Sheets."
    def __init__(self, creds_json_path):
        logger.debug("Ruta de credenciales recibida: %s", creds_json_path)
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        logger.debug("Scope usado para Google Sheets: %s", scope)
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
        service_email = getattr(creds, 'service_account_email', None)
        logger.debug("Credenciales cargadas: %s", service_email if service_email else str(creds))
        if service_email:
            logger.warning("Asegúrate de compartir el spreadsheet con este email de servicio: %s", service_email)
        self.client = gspread.authorize(creds)
        logger.debug("Cliente gspread autorizado correctamente.")

    def get_sheet_values(self, spreadsheet_id, worksheet_name):
        " Obtiene todos los valores de una hoja específica."
        try:
            logger.info("Intentando abrir spreadsheet con ID: %s", spreadsheet_id)
            logger.debug("Usando cliente gspread: %s", self.client)
            sheet = self.client.open_by_key(spreadsheet_id)
            logger.debug("Spreadsheet abierto correctamente: %s", sheet)
            worksheet = sheet.worksheet(worksheet_name)
            logger.info("Accediendo a la hoja: %s", worksheet_name)
            logger.debug("Worksheet obtenido: %s", worksheet)
            values = worksheet.get_all_values()
            logger.info("Valores obtenidos correctamente, filas: %d", len(values))
            logger.debug("Primeras filas: %s", values[:2] if values else "[]")
            return values
        except PermissionError as e:
            logger.error("Permiso denegado al acceder a Google Sheets: %s", e)
            logger.error("Tipo de excepción: %s", type(e))
            logger.warning("Verifica que la API de Google Sheets esté habilitada y las credenciales sean correctas.")
            logger.debug("Traceback completo:", exc_info=True)
            return []
        except (gspread.SpreadsheetNotFound, gspread.WorksheetNotFound) as e:
            logger.warning("No se encontró el spreadsheet o worksheet: %s", e)
            logger.debug("Spreadsheet ID: %s, Worksheet Name: %s", spreadsheet_id, worksheet_name)
            return []
        except (gspread.exceptions.APIError, gspread.exceptions.GSpreadException, OSError, ValueError) as e:
            logger.error("Error al obtener datos de Google Sheets: %s", e)
            logger.error("Tipo de excepción: %s", type(e))
            logger.debug("Traceback completo:", exc_info=True)
            return []
        except RuntimeError as e:
            logger.error("Error de tiempo de ejecución inesperado: %s", e)
            logger.error("Tipo de excepción: %s", type(e))
            logger.debug("Traceback completo:", exc_info=True)
            return []
