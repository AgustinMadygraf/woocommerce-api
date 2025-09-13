"""
Path: src/shared/config.py
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env automáticamente
load_dotenv()

URL = os.getenv("URL")
CK = os.getenv("CK")
CS = os.getenv("CS")
GOOGLE_CREDS_PATH = os.getenv("GOOGLE_CREDS_PATH")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

# Credenciales de MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "usuario")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "contraseña")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "woocommerce")
