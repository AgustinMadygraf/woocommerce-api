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
