"""
Path: src/infrastructure/pymysql/product_persistence_gateway_impl.py
"""

from typing import List, Any
import pymysql

from src.shared.config import MYSQL_CONFIG
from src.shared.logger import logger
from src.interface_adapters.gateways.product_persistence_gateway import ProductPersistenceGateway
from src.infrastructure.google_sheets.sheet_product_adapter import SheetProductAdapter

class ProductPersistenceGatewayImpl(ProductPersistenceGateway):
    """Implementación de ProductPersistenceGateway usando PyMySQL para MySQL."""
    def __init__(self, host=None, user=None, password=None, db=None, port=None):
        self.connection_params = MYSQL_CONFIG.copy()
        # Permitir sobreescribir parámetros si se pasan al constructor
        if host is not None:
            self.connection_params['host'] = host
        if user is not None:
            self.connection_params['user'] = user
        if password is not None:
            self.connection_params['password'] = password
        if db is not None:
            self.connection_params['database'] = db
        if port is not None:
            self.connection_params['port'] = port
        self.connection_params['cursorclass'] = pymysql.cursors.DictCursor

    def list_products(self) -> List[Any]:
        logger.debug("Intentando conectar a MySQL para listar productos de WooCommerce: %s", self.connection_params)
        try:
            with pymysql.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name, sku, regular_price, stock_quantity, status, type FROM products_woocommerce")
                    productos = cursor.fetchall()
                    logger.info("Productos WooCommerce recuperados: %d", len(productos))
                    return productos
        except pymysql.err.OperationalError as e:
            logger.error("Error operacional al conectar a MySQL: %s", e)
            raise
        except Exception as e:
            logger.exception("Error inesperado al listar productos: %s", e)
            raise
            
    def list_google_sheet_products(self) -> List[Any]:
        logger.debug("Intentando conectar a MySQL para listar productos de Google Sheets: %s", self.connection_params)
        try:
            with pymysql.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id_google_sheets, formato, color, stock_quantity FROM products_google_sheets")
                    productos = cursor.fetchall()
                    logger.info("Productos Google Sheets recuperados: %d", len(productos))
                    return productos
        except pymysql.err.OperationalError as e:
            logger.error("Error operacional al conectar a MySQL: %s", e)
            raise
        except Exception as e:
            logger.exception("Error inesperado al listar productos de Google Sheets: %s", e)
            raise

    def update_products_from_sheet(self, values: list) -> dict:
        logger.debug("Iniciando actualización de productos desde Google Sheets a MySQL.")
        updated, inserted, errores = 0, 0, []
        try:
            if not values or len(values) < 2:
                logger.warning("No hay datos suficientes para actualizar.")
                return {"actualizados": 0, "insertados": 0, "errores": ["No hay datos suficientes."]}

            # Transformar los datos crudos de la hoja al formato estándar
            transformed_values = SheetProductAdapter.transform(values)
            if not transformed_values or len(transformed_values) < 2:
                logger.warning("No hay datos transformados suficientes para actualizar.")
                return {"actualizados": 0, "insertados": 0, "errores": ["No hay datos transformados suficientes."]}

            headers = transformed_values[0]
            data_rows = transformed_values[1:]
            
            # Adaptar los nombres de columnas para la nueva estructura

            # Ajuste: aceptar directamente los encabezados entregados por el adaptador
            required_cols = ["formato", "color", "gramaje", "stock_quantity"]
            missing = [col for col in required_cols if col not in headers]
            if missing:
                msg = f"Faltan columnas requeridas tras la transformación: {missing}. Encabezados encontrados: {headers}"
                logger.error(msg)
                return {"actualizados": 0, "insertados": 0, "errores": [msg]}

            # Mapear índices de columnas
            col_idx = {col: headers.index(col) for col in required_cols}
            with pymysql.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # Limpiamos la tabla antes de insertar nuevos datos
                    cursor.execute("TRUNCATE TABLE products_google_sheets")
                    logger.info("Tabla products_google_sheets limpiada para nuevos datos")
                    
                    for row in data_rows:
                        if len(row) < len(headers):
                            logger.warning("Fila incompleta ignorada: %s", row)
                            continue
                            
                        try:
                            # Mapeamos los datos según la nueva estructura
                            formato = row[col_idx["formato"]]
                            color = row[col_idx["color"]]
                            gramaje = row[col_idx["gramaje"]]
                            stock_quantity = row[col_idx["stock_quantity"]]
                            cursor.execute("""
                                INSERT INTO products_google_sheets (formato, color, gramaje, stock_quantity)
                                VALUES (%s, %s, %s, %s)
                            """, (formato, color, gramaje, stock_quantity))
                            inserted += 1
                            logger.debug("Producto de Google Sheets insertado: formato=%s, color=%s, gramaje=%s", formato, color, gramaje)
                        except (pymysql.MySQLError, ValueError) as row_e:
                            logger.error("Error al procesar fila %s: %s", row, row_e)
                            errores.append(f"Error en fila: {row}: {str(row_e)}")
                    conn.commit()
            logger.info("Actualización completada. Filas insertadas: %d", inserted)
            return {"actualizados": updated, "insertados": inserted, "errores": errores}
        except pymysql.err.OperationalError as e:
            logger.error("Error operacional al conectar o actualizar en MySQL: %s", e)
            errores.append(f"Error operacional: {str(e)}")
        except (pymysql.MySQLError, ValueError) as e:
            logger.exception("Error inesperado al actualizar productos desde Sheets: %s", e)
            errores.append(str(e))
        return {"actualizados": updated, "insertados": inserted, "errores": errores}
