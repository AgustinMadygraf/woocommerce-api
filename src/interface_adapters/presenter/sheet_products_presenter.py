"""
Presentador para productos de Google Sheets.
Ubicación: src/interface_adapters/presenter/sheet_products_presenter.py
"""

from typing import List, Any

class SheetProductsPresenter:
    """
    Presentador que ordena la lista de productos por stock_quantity de mayor a menor
    y devuelve el formato esperado por la vista (incluyendo encabezados si corresponde).
    """
    @staticmethod
    def present(products: List[Any]) -> List[Any]:
        if not products or len(products) < 2:
            return products
        header, *rows = products
        # Asegurarse de que 'stock_quantity' esté en el header
        if 'stock_quantity' not in header:
            return products
        idx = header.index('stock_quantity')
        # Ordenar filas por stock_quantity (convertir a int, tratar vacíos como 0)
        sorted_rows = sorted(
            rows,
            key=lambda r: int(r[idx]) if len(r) > idx and str(r[idx]).isdigit() else 0,
            reverse=True
        )
        return [header] + sorted_rows
