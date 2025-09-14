"""
Script para inicializar la base de datos MySQL y las tablas 'products_google_sheets' y 'products_woocommerce' si no existen.
"""

import pymysql
from src.shared.config import MYSQL_CONFIG
from src.shared.logger import logger

def crear_db_y_tabla():
    "Crea la base de datos y las tablas si no existen."
    try:
        # 1. Conexión sin base de datos para crearla si no existe
        conn_params = MYSQL_CONFIG.copy()
        conn_params.pop('database', None)  # Eliminar database para la conexión inicial
        conn = pymysql.connect(
            **conn_params,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            logger.info("Base de datos '%s' verificada/creada.", MYSQL_CONFIG['database'])
        conn.close()

        # 2. Conexión a la base de datos ya existente para crear las tablas
        conn = pymysql.connect(
            **MYSQL_CONFIG,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Crear tabla para datos de Google Sheets
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_google_sheets (
                    id_google_sheets INT AUTO_INCREMENT PRIMARY KEY,
                    formato VARCHAR(255),
                    color VARCHAR(100),
                    gramaje VARCHAR(100),
                    stock_quantity INT
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            logger.info("Tabla 'products_google_sheets' verificada/creada.")
            
            # Crear tabla para datos de WooCommerce
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products_woocommerce (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    sku VARCHAR(100),
                    regular_price DECIMAL(10,2),
                    stock_quantity INT,
                    status VARCHAR(50),
                    type VARCHAR(50)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            logger.info("Tabla 'products_woocommerce' verificada/creada.")
            
        conn.commit()
        conn.close()
        print("[OK] Base de datos y tablas 'products_google_sheets' y 'products_woocommerce' listas.")
    except pymysql.MySQLError as e:
        logger.exception("Error al inicializar la base de datos: %s", e)
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
