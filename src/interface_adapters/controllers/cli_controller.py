"""
Path: src/interface_adapters/controllers/cli_controller.py
"""

import os

from src.interface_adapters.presenters.input_validator import is_valid_float, is_valid_int
from src.interface_adapters.presenters.pagination_presenter import PaginationPresenter

class CLIController:
    """Controlador CLI centralizado para la interacción con el usuario."""
    def __init__(self, list_products_uc, get_product_by_id_uc, create_product_uc, update_product_uc, presenter, list_sheet_values_uc=None):
        self.list_products_uc = list_products_uc
        self.get_product_by_id_uc = get_product_by_id_uc
        self.create_product_uc = create_product_uc
        self.update_product_uc = update_product_uc
        self.presenter = presenter
        self.list_sheet_values_uc = list_sheet_values_uc

    def run(self):
        """Bucle principal de interacción CLI con menú de opciones mejorado."""
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 40)
                print("        MENÚ PRINCIPAL")
                print("=" * 40)
                print("1. Listar productos")
                print("2. Buscar producto por ID")
                print("3. Actualizar producto por ID")
                print("4. Mostrar datos de Google Sheets")
                print("0. Salir")
                print("-" * 40)
                opcion = input("Seleccione una opción (0-4): ").strip()
                if opcion not in {"0", "1", "2", "3", "4"}:
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
                def format_item(p, idx):
                    return f"{idx}. {p.name} | SKU: {p.sku} | Precio: {p.regular_price} | Stock: {p.stock_quantity} | Estado: {p.status}"
                PaginationPresenter.show_paginated_list(page_items, page, PAGE_SIZE, total, format_item, title="PRODUCTOS")
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
            nuevo_precio = input(f"Nuevo precio (actual: {prod.regular_price}): ").strip()
            if nuevo_precio:
                if is_valid_float(nuevo_precio):
                    prod.regular_price = nuevo_precio
                else:
                    self.presenter.show_error("El precio debe ser un número válido.")
                    input("Presione Enter para continuar...")
                    return
            nueva_cantidad = input(f"Nueva cantidad en stock (actual: {prod.stock_quantity}): ").strip()
            if nueva_cantidad:
                if is_valid_int(nueva_cantidad):
                    prod.stock_quantity = int(nueva_cantidad)
                else:
                    self.presenter.show_error("La cantidad debe ser un número entero.")
                    input("Presione Enter para continuar...")
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
                start = page * PAGE_SIZE
                end = start + PAGE_SIZE
                page_items = filtered[start:end]
                def format_row(row, idx):
                    return f"{idx} | " + " | ".join(str(cell) for cell in row)
                PaginationPresenter.show_paginated_list(page_items, page, PAGE_SIZE, total, format_row, title="DATOS DE GOOGLE SHEETS")
                PaginationPresenter.show_navigation_help()
                cmd = input("Comando [n/p/f/q]: ").strip().lower()
                if cmd == 'n' and end < total:
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
