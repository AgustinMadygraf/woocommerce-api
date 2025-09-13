"""
Path: src/infrastructure/pymysql/product_persistence_gateway_impl.py
"""

from typing import List, Any
import pymysql

from src.shared import config
from src.shared.logger import logger

from src.interface_adapters.gateways.product_persistence_gateway import ProductPersistenceGateway
from src.infrastructure.google_sheets.sheet_product_adapter import SheetProductAdapter

class ProductPersistenceGatewayImpl(ProductPersistenceGateway):
    """Implementación de ProductPersistenceGateway usando PyMySQL para MySQL."""
    def __init__(self, host=None, user=None, password=None, db=None, port=None):
        self.connection_params = {
            'host': host or config.MYSQL_HOST,
            'user': user or config.MYSQL_USER,
            'password': password or config.MYSQL_PASSWORD,
            'database': db or config.MYSQL_DATABASE,
            'port': port or config.MYSQL_PORT,
            'cursorclass': pymysql.cursors.DictCursor
        }

    def list_products(self) -> List[Any]:
        logger.debug("Intentando conectar a MySQL para listar productos: %s", self.connection_params)
        try:
            with pymysql.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name, sku, regular_price, stock_quantity, status, type FROM products")
                    productos = cursor.fetchall()
                    logger.info("Productos recuperados: %d", len(productos))
                    return productos
        except pymysql.err.OperationalError as e:
            logger.error("Error operacional al conectar a MySQL: %s", e)
            raise
        except Exception as e:
            logger.exception("Error inesperado al listar productos: %s", e)
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
            required_cols = ["id", "name", "sku", "regular_price", "stock_quantity", "status", "type"]
            col_idx = {col: headers.index(col) for col in required_cols if col in headers}
            missing = [col for col in required_cols if col not in col_idx]
            if missing:
                msg = f"Faltan columnas requeridas tras la transformación: {missing}. Encabezados encontrados: {headers}"
                logger.error(msg)
                return {"actualizados": 0, "insertados": 0, "errores": [msg]}

            with pymysql.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    for row in data_rows:
                        if len(row) < len(headers):
                            logger.warning("Fila incompleta ignorada: %s", row)
                            continue
                        data = {col: row[col_idx[col]] for col in required_cols}
                        try:
                            cursor.execute("SELECT COUNT(*) as count FROM products WHERE id = %s", (data["id"],))
                            existe = cursor.fetchone()["count"]
                            if existe:
                                cursor.execute("""
                                    UPDATE products SET name=%s, sku=%s, regular_price=%s, stock_quantity=%s, status=%s, type=%s WHERE id=%s
                                """, (data["name"], data["sku"], data["regular_price"], data["stock_quantity"], data["status"], data["type"], data["id"]))
                                updated += 1
                                logger.debug("Producto actualizado: %s", data['id'])
                            else:
                                cursor.execute("""
                                    INSERT INTO products (id, name, sku, regular_price, stock_quantity, status, type)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (data["id"], data["name"], data["sku"], data["regular_price"], data["stock_quantity"], data["status"], data["type"]))
                                inserted += 1
                                logger.info("Producto insertado: %s", data['id'])
                        except (pymysql.MySQLError, ValueError) as row_e:
                            logger.error("Error al procesar fila %s: %s", row, row_e)
                    conn.commit()
            logger.info("Actualización completada. Filas actualizadas: %d, insertadas: %d", updated, inserted)
            return {"actualizados": updated, "insertados": inserted, "errores": errores}
        except pymysql.err.OperationalError as e:
            logger.error("Error operacional al conectar o actualizar en MySQL: %s", e)
            raise
        except (pymysql.MySQLError, ValueError) as e:
            logger.exception("Error inesperado al actualizar productos desde Sheets: %s", e)
            errores.append(str(e))
        return {"actualizados": updated, "insertados": inserted, "errores": errores}
