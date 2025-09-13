"""
Script para inicializar la base de datos MySQL y la tabla 'products' si no existen.
"""
import pymysql
from src.shared import config
from src.shared.logger import logger

def crear_db_y_tabla():
    "Crea la base de datos y la tabla 'products' si no existen."
    try:
        # Conexión sin base de datos para crearla si no existe
        conn = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            port=config.MYSQL_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            logger.info("Base de datos '%s' verificada/creada.", config.MYSQL_DATABASE)
        conn.select_db(config.MYSQL_DATABASE)
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
