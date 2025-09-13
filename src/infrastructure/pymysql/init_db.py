"""
Script para inicializar la base de datos MySQL y la tabla 'products' si no existen.
"""

import pymysql
from src.shared.config import MYSQL_CONFIG

from src.shared.logger import logger

def crear_db_y_tabla():
    "Crea la base de datos y la tabla 'products' si no existen."
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

        # 2. Conexión a la base de datos ya existente para crear la tabla
        conn = pymysql.connect(
            **MYSQL_CONFIG,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    sku VARCHAR(100),
                    regular_price DECIMAL(10,2),
                    stock_quantity INT,
                    status VARCHAR(50),
                    type VARCHAR(50)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            logger.info("Tabla 'products' verificada/creada.")
        conn.commit()
        conn.close()
        print("[OK] Base de datos y tabla 'products' listas.")
    except pymysql.MySQLError as e:
        logger.exception("Error al inicializar la base de datos: %s", e)
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
