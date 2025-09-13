"""
Path: src/interface_adapters/presenters/pagination_presenter.py
"""

from src.interface_adapters.presenters.cli_style import cyan, format_table
class PaginationPresenter:
    """Presenta datos paginados y ayuda a navegar entre páginas en CLI."""
    @staticmethod
    def show_paginated_list(items, page, page_size, total_items, item_formatter=None, title="LISTA DE DATOS", headers=None):
        "Muestra una lista paginada de ítems en formato tabla con encabezados y colores."
        total_pages = (total_items + page_size - 1) // page_size
        print(cyan(f"\n=== {title} (Página {page+1} de {total_pages}) ==="))
        start = page * page_size
        end = min(start + page_size, total_items)
        table_rows = []
        for idx, item in enumerate(items, start=start+1):
            if item_formatter:
                row = item_formatter(item, idx)
                if isinstance(row, (list, tuple)):
                    table_rows.append([str(cell) for cell in row])
                else:
                    table_rows.append([str(row)])
            else:
                table_rows.append([f"{idx}. {item}"])
        if headers:
            print(format_table(table_rows, headers=headers))
        else:
            print(format_table(table_rows))
        print(cyan(f"=== Mostrando {start+1}-{end} de {total_items} ===\n"))

    @staticmethod
    def show_navigation_help():
        "Muestra instrucciones de navegación para paginación."
        print("[n] Siguiente página | [p] Página anterior | [f] Filtrar | [q] Salir paginación")

    @staticmethod
    def show_no_results():
        "Muestra un mensaje cuando no hay resultados para mostrar."
        print("No hay resultados para mostrar.")
