"""
Path: src/interface_adapters/controllers/cli_controller.py
"""

from src.interface_adapters.presenters.input_validator import is_valid_float, is_valid_int
from src.interface_adapters.presenters.pagination_presenter import PaginationPresenter
from src.interface_adapters.presenters.cli_style import cyan, green, yellow, red

class CLIController:
    """Controlador CLI centralizado para la interacción con el usuario."""
    def __init__(self, list_products_uc, get_product_by_id_uc, create_product_uc, update_product_uc, presenter, list_sheet_values_uc=None, list_local_products_uc=None, update_local_products_from_sheets_uc=None):
        self.list_products_uc = list_products_uc
        self.get_product_by_id_uc = get_product_by_id_uc
        self.create_product_uc = create_product_uc
        self.update_product_uc = update_product_uc
        self.presenter = presenter
        self.list_sheet_values_uc = list_sheet_values_uc
        self.list_local_products_uc = list_local_products_uc
        self.update_local_products_from_sheets_uc = update_local_products_from_sheets_uc

    def run(self):
        """Bucle principal de interacción CLI con menú de opciones mejorado."""
        try:
            while True:
                #os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 40)
                print("        MENÚ PRINCIPAL")
                print("=" * 40)
                print("1. Listar productos de WooCommerce")
                print("2. Buscar producto por ID de WooCommerce")
                print("3. Actualizar producto por ID de WooCommerce")
                print("4. Mostrar datos de Google Sheets")
                print("5. Visualizar productos locales (MySQL)")
                print("6. Actualizar productos locales desde Google Sheets (MySQL)")
                print("0. Salir")
                print("-" * 40)
                opcion = input("Seleccione una opción (0-6): ").strip()
                if opcion not in {"0", "1", "2", "3", "4", "5", "6"}:
                    self.presenter.show_message("\n[!] Opción no válida. Intente de nuevo.")
                    input("Presione Enter para continuar...")
                    continue
                if opcion == "1":
                    self._listar_productos()
                elif opcion == "2":
                    self._buscar_producto_por_id()
                elif opcion == "3":
                    self._actualizar_producto_por_id()
                elif opcion == "4":
                    self._mostrar_datos_google_sheets()
                elif opcion == "5":
                    self._visualizar_productos_locales()
                elif opcion == "6":
                    self._actualizar_productos_locales_desde_sheets()
                elif opcion == "0":
                    self.presenter.show_message("\nSaliendo del sistema. ¡Hasta luego!")
                    break
        except KeyboardInterrupt:
            self.presenter.show_message("\n\n[!] Interrupción detectada. Saliendo del sistema. ¡Hasta luego!")
            return

    def _listar_productos(self):
        PAGE_SIZE = 5
        page = 0
        filtro_nombre = None
        while True:
            try:
                productos = self.list_products_uc.execute({"status": "any"})
                if filtro_nombre:
                    productos = [p for p in productos if filtro_nombre.lower() in p.name.lower()]
                total = len(productos)
                if total == 0:
                    PaginationPresenter.show_no_results()
                    break
                start = page * PAGE_SIZE
                end = start + PAGE_SIZE
                page_items = productos[start:end]
                headers = [cyan("#"), cyan("Nombre"), cyan("SKU"), cyan("Precio"), cyan("Stock"), cyan("Estado")]
                def format_item(p, idx):
                    estado = green(p.status) if str(p.status).lower() == 'publish' else yellow(p.status)
                    stock = red(p.stock_quantity) if isinstance(p.stock_quantity, int) and p.stock_quantity <= 0 else p.stock_quantity
                    return [str(idx), p.name, p.sku, p.regular_price, stock, estado]
                PaginationPresenter.show_paginated_list(page_items, page, PAGE_SIZE, total, format_item, title="PRODUCTOS", headers=headers)
                PaginationPresenter.show_navigation_help()
                cmd = input("Comando [n/p/f/q]: ").strip().lower()
                if cmd == 'n' and end < total:
                    page += 1
                elif cmd == 'p' and page > 0:
                    page -= 1
                elif cmd == 'f':
                    filtro_nombre = input("Filtrar por nombre (dejar vacío para quitar filtro): ").strip() or None
                    page = 0
                elif cmd == 'q':
                    break
                else:
                    print("Comando no reconocido o fuera de rango.")
            except ValueError as e:
                self.presenter.show_error(f"Error de valor al listar productos: {e}")
                break
            except (TypeError, KeyError) as e:
                self.presenter.show_error(f"Error inesperado al listar productos: {e}")
                break

    def _buscar_producto_por_id(self):
        id_input = input("Ingrese el ID del producto a buscar: ").strip()
        if not is_valid_int(id_input):
            self.presenter.show_error("Debe ingresar un ID válido.")
            input("Presione Enter para continuar...")
            return
        product_id = int(id_input)
        try:
            prod = self.get_product_by_id_uc.execute(product_id)
            if prod:
                self.presenter.show_product_detail(prod)
            else:
                self.presenter.show_message("Producto no encontrado.")
        except ValueError as e:
            self.presenter.show_error(f"Error de valor al buscar producto: {e}")
        except (TypeError, KeyError) as e:
            self.presenter.show_error(f"Error inesperado al buscar producto: {e}")
        input("Presione Enter para volver al menú...")

    def _actualizar_producto_por_id(self):
        id_input = input("Ingrese el ID del producto a actualizar: ").strip()
        if not is_valid_int(id_input):
            self.presenter.show_error("Debe ingresar un ID válido.")
            input("Presione Enter para continuar...")
            return
        product_id = int(id_input)
        try:
            prod = self.get_product_by_id_uc.execute(product_id)
            if not prod:
                self.presenter.show_message("Producto no encontrado.")
                input("Presione Enter para continuar...")
                return
            self.presenter.show_message("Deje vacío para mantener el valor actual.")
            precio_actual = prod.regular_price if prod.regular_price not in (None, "") else "No definido"
            nuevo_precio = input(f"Nuevo precio (actual: {precio_actual}): ").strip()
            if nuevo_precio.lower() == 'q':
                self.presenter.show_message("Actualización cancelada por el usuario.")
                input("Presione Enter para volver al menú...")
                return
            if nuevo_precio:
                if is_valid_float(nuevo_precio):
                    prod.regular_price = nuevo_precio
                else:
                    self.presenter.show_error("El precio debe ser un número válido.")
                    input("Presione Enter para continuar...")
                    return
            nueva_cantidad = input(f"Nueva cantidad en stock (actual: {prod.stock_quantity}): ").strip()
            if nueva_cantidad.lower() == 'q':
                self.presenter.show_message("Actualización cancelada por el usuario.")
                input("Presione Enter para volver al menú...")
                return
            if nueva_cantidad:
                if is_valid_int(nueva_cantidad):
                    prod.stock_quantity = int(nueva_cantidad)
                else:
                    self.presenter.show_error("La cantidad debe ser un número entero.")
                    input("Presione Enter para continuar...")
                    return
            # Confirmación antes de actualizar
            print("\nResumen de cambios a aplicar:")
            print(f"ID: {prod.product_id} | Nombre: {prod.name} | Precio: {prod.regular_price} | Stock: {prod.stock_quantity}")
            confirm = input("¿Confirma que desea actualizar este producto? (s/N): ").strip().lower()
            if confirm != 's':
                self.presenter.show_message("Actualización cancelada por el usuario.")
                input("Presione Enter para volver al menú...")
                return
            self.update_product_uc.execute(prod)
            self.presenter.show_message("Producto actualizado correctamente.")
        except ValueError as e:
            self.presenter.show_error(f"Error de valor al actualizar producto: {e}")
        except (TypeError, KeyError) as e:
            self.presenter.show_error(f"Error inesperado al actualizar producto: {e}")
        input("Presione Enter para volver al menú...")

    def _mostrar_datos_google_sheets(self):
        PAGE_SIZE = 10
        page = 0
        filtro = None
        while True:
            try:
                values = self.list_sheet_values_uc.execute()
                if not values or len(values) == 0:
                    PaginationPresenter.show_no_results()
                    break
                # Filtrar por texto en cualquier celda
                filtered = values
                if filtro:
                    filtered = [row for row in values if any(filtro.lower() in str(cell).lower() for cell in row)]
                total = len(filtered)
                if total == 0:
                    PaginationPresenter.show_no_results()
                    break
                # Detectar si la primera fila es encabezado
                headers = None
                data_rows = filtered
                if filtered and all(cell and isinstance(cell, str) for cell in filtered[0]):
                    headers = [cyan(str(cell)) for cell in filtered[0]]
                    data_rows = filtered[1:]
                start = page * PAGE_SIZE
                end = start + PAGE_SIZE
                page_items = data_rows[start:end]
                def format_row(row, _idx):
                    return [str(cell) for cell in row]
                PaginationPresenter.show_paginated_list(page_items, page, PAGE_SIZE, len(data_rows), format_row, title="DATOS DE GOOGLE SHEETS", headers=headers)
                PaginationPresenter.show_navigation_help()
                cmd = input("Comando [n/p/f/q]: ").strip().lower()
                if cmd == 'n' and end < len(data_rows):
                    page += 1
                elif cmd == 'p' and page > 0:
                    page -= 1
                elif cmd == 'f':
                    filtro = input("Filtrar por texto (dejar vacío para quitar filtro): ").strip() or None
                    page = 0
                elif cmd == 'q':
                    break
                else:
                    print("Comando no reconocido o fuera de rango.")
            except (ValueError, TypeError, KeyError) as e:
                self.presenter.show_error(f"Error al obtener datos de Google Sheets: {e}")
                break

    def _visualizar_productos_locales(self):
        """Muestra los productos almacenados en la base de datos local (MySQL)."""
        try:
            productos = self.list_local_products_uc.execute()
            if not productos:
                self.presenter.show_message("No hay productos en la base de datos local.")
            else:
                self.presenter.show_message("Productos en base local:")
                for prod in productos:
                    self.presenter.show_message(
                        f"ID: {prod['id']}, Nombre: {prod['name']}, SKU: {prod['sku']}, Precio: {prod['regular_price']}, Stock: {prod['stock_quantity']}, Estado: {prod['status']}, Tipo: {prod['type']}"
                    )
        except (ValueError, TypeError, KeyError) as e:
            self.presenter.show_message(f"Error al acceder a la base local: {e}")
        except RuntimeError as e:
            self.presenter.show_message(f"Error inesperado al acceder a la base local: {e}")

    def _actualizar_productos_locales_desde_sheets(self):
        """Actualiza la base de datos local (MySQL) con los datos de Google Sheets."""
        try:
            values = self.list_sheet_values_uc.execute()
            if not values or len(values) < 2:
                self.presenter.show_message("No hay datos suficientes en Google Sheets para actualizar la base local.")
                return

            # Depuración: mostrar primeras filas y encabezados
            self.presenter.show_message(f"[DEBUG] Filas obtenidas de Sheets: {len(values)}")
            self.presenter.show_message(f"[DEBUG] Encabezados: {values[0]}")
            self.presenter.show_message(f"[DEBUG] Primeras filas de datos: {values[1:3]}")

            # Llamar al caso de uso de actualización
            if self.update_local_products_from_sheets_uc is None:
                self.presenter.show_error("Caso de uso para actualizar productos locales no está configurado.")
                return

            resultado = self.update_local_products_from_sheets_uc.execute(values)
            if resultado.get("errores"):
                self.presenter.show_error(f"Errores durante la actualización: {resultado['errores']}")
            self.presenter.show_message(f"Productos actualizados: {resultado.get('actualizados', 0)} | insertados: {resultado.get('insertados', 0)}")
        except (ValueError, TypeError, KeyError) as e:
            self.presenter.show_message(f"Error al actualizar la base local: {e}")
        except RuntimeError as e:
            self.presenter.show_message(f"Error inesperado al actualizar la base local: {e}")
        except Exception as e:
            # Depuración extra para errores no previstos
            import traceback
            self.presenter.show_error(f"Error crítico: {e}\n{traceback.format_exc()}")
