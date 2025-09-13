"""
Path: run.py
"""

import os

from src.infrastructure.woocommerce.gateway_impl import WooCommerceProductGateway
from src.interface_adapters.presenters.product_presenter import ProductPresenter
from src.interface_adapters.controllers.cli_controller import CLIController
from src.use_cases.list_products import ListProductsUseCase
from src.use_cases.get_product_by_id import GetProductByIdUseCase
from src.use_cases.create_product import CreateProductUseCase
from src.use_cases.update_product import UpdateProductUseCase
from src.infrastructure.google_sheets.sheets_gateway import GoogleSheetsGateway
from src.use_cases.list_sheet_values import ListSheetValuesUseCase
from src.shared.config import GOOGLE_CREDS_PATH, SPREADSHEET_ID, WORKSHEET_NAME
from src.infrastructure.pymysql.product_persistence_gateway_impl import ProductPersistenceGatewayImpl
from src.use_cases.list_local_products import ListLocalProductsUseCase
from src.use_cases.update_local_products_from_sheets import UpdateLocalProductsFromSheetsUseCase
from src.shared.logger import logger

if __name__ == "__main__":
    if not os.path.isfile(GOOGLE_CREDS_PATH) or os.path.getsize(GOOGLE_CREDS_PATH) == 0:
        print(f"[ERROR] Archivo de credenciales de Google no encontrado o vacío: {GOOGLE_CREDS_PATH}")
        print("Por favor, revisa la variable GOOGLE_CREDS_PATH en tu .env o config.py y asegúrate de que el archivo contiene las credenciales JSON válidas.")
        exit(1)

    gateway = WooCommerceProductGateway()
    list_products = ListProductsUseCase(gateway)
    get_product_by_id = GetProductByIdUseCase(gateway)
    create_product = CreateProductUseCase(gateway)
    update_product = UpdateProductUseCase(gateway)
    Presenter = ProductPresenter
    sheets_gateway = GoogleSheetsGateway(GOOGLE_CREDS_PATH)
    list_sheet_values = ListSheetValuesUseCase(sheets_gateway, SPREADSHEET_ID, WORKSHEET_NAME)
    # Inicializar gateway y casos de uso para productos locales (MySQL)
    mysql_gateway = ProductPersistenceGatewayImpl()
    list_local_products = ListLocalProductsUseCase(mysql_gateway)
    update_local_products_from_sheets = UpdateLocalProductsFromSheetsUseCase(mysql_gateway)
    controller = CLIController(
        list_products_uc=list_products,
        get_product_by_id_uc=get_product_by_id,
        create_product_uc=create_product,
        update_product_uc=update_product,
        presenter=Presenter,
        list_sheet_values_uc=list_sheet_values,
        list_local_products_uc=list_local_products,
        update_local_products_from_sheets_uc=update_local_products_from_sheets
    )
    try:
        controller.run()
    except (KeyboardInterrupt, SystemExit) as e:
        logger.info("Ejecución interrumpida por el usuario o salida del sistema: %s", e)
        print("\n[INFO] Ejecución interrumpida.")
    except Exception as e:
        logger.exception("Error fatal en la ejecución del CLI: %s", e)
        print("\n[ERROR] Ocurrió un error inesperado. Revisa los logs para más detalles.")
