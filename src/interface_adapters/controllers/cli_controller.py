"""
Path: src/interface_adapters/controllers/cli_controller.py
"""


class CLIController:
    """Controlador CLI centralizado para la interacción con el usuario."""
    def __init__(self, list_products_uc, get_product_by_sku_uc, create_product_uc, update_product_uc, presenter, test_sku="DEMO-0001"):
        self.list_products_uc = list_products_uc
        self.get_product_by_sku_uc = get_product_by_sku_uc
        self.create_product_uc = create_product_uc
        self.update_product_uc = update_product_uc
        self.presenter = presenter
        self.test_sku = test_sku

    def run(self):
        """Bucle principal de interacción CLI con menú de opciones."""
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Listar productos")
            print("2. Buscar producto por SKU")
            print("3. Actualizar producto por SKU")
            print("4. Salir")
            opcion = input("Seleccione una opción (1-4): ").strip()
            if opcion not in {"1", "2", "3", "4"}:
                self.presenter.show_message("Opción no válida. Intente de nuevo.")
                continue
            if opcion == "1":
                per_page_input = input("¿Cuántos productos listar? (default 5): ").strip()
                if per_page_input and not per_page_input.isdigit():
                    self.presenter.show_error("Debe ingresar un número válido para la cantidad de productos.")
                    continue
                per_page = int(per_page_input) if per_page_input else 5
                try:
                    productos = self.list_products_uc.execute({"per_page": per_page, "page": 1, "status": "any"})
                    if not productos:
                        self.presenter.show_message("No se encontraron productos.")
                    else:
                        self.presenter.show_product_list(productos)
                except ValueError as e:
                    self.presenter.show_error(f"Error de valor al listar productos: {e}")
                except (TypeError, KeyError) as e:
                    self.presenter.show_error(f"Error inesperado al listar productos: {e}")
            elif opcion == "2":
                sku = input("Ingrese el SKU del producto a buscar: ").strip()
                if not sku:
                    self.presenter.show_error("Debe ingresar un SKU válido.")
                    continue
                try:
                    prod = self.get_product_by_sku_uc.execute(sku)
                    if prod:
                        self.presenter.show_product_detail(prod)
                    else:
                        self.presenter.show_message("Producto no encontrado.")
                except ValueError as e:
                    self.presenter.show_error(f"Error de valor al buscar producto: {e}")
                except (TypeError, KeyError) as e:
                    self.presenter.show_error(f"Error inesperado al buscar producto: {e}")
            elif opcion == "3":
                try:
                    prod = self.get_product_by_sku_uc.execute(sku)
                    if not prod:
                        self.presenter.show_message("Producto no encontrado.")
                        continue
                    print("Deje vacío para mantener el valor actual.")
                    nuevo_precio = input(f"Nuevo precio (actual: {prod.regular_price}): ").strip()
                    if nuevo_precio:
                        try:
                            float(nuevo_precio)
                            prod.regular_price = nuevo_precio
                        except ValueError:
                            self.presenter.show_error("El precio debe ser un número válido.")
                            continue
                    nueva_cantidad = input(f"Nueva cantidad en stock (actual: {prod.stock_quantity}): ").strip()
                    if nueva_cantidad:
                        if nueva_cantidad.isdigit():
                            prod.stock_quantity = int(nueva_cantidad)
                        else:
                            self.presenter.show_error("La cantidad debe ser un número entero.")
                            continue
                    self.update_product_uc.execute(prod)
                    self.presenter.show_message("Producto actualizado correctamente.")
                except ValueError as e:
                    self.presenter.show_error(f"Error de valor al actualizar producto: {e}")
                except (TypeError, KeyError) as e:
                    self.presenter.show_error(f"Error inesperado al actualizar producto: {e}")
            elif opcion == "4":
                print("Saliendo del sistema. ¡Hasta luego!")
                break
