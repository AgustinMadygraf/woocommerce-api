"""
Path: src/infrastructure/google_sheets/sheet_product_adapter.py
"""

class SheetProductAdapter:
    "Transforma los datos de productos desde Google Sheets a un formato estándar."
    @staticmethod
    def transform(raw_values: list) -> list:
        " Transforma los datos de productos desde Google Sheets a un formato estándar."
        transformed = []
        # Usamos los nuevos nombres de columnas para Google Sheets
        header = ["formato", "color", "gramaje", "stock_quantity"]
        transformed.append(header)
        for row in raw_values[3:]:
            if len(row) < 7 or not row[2]:
                continue
            formato = str(row[2])
            color = str(row[3])
            gramaje = str(row[4]) if len(row) > 4 else ""
            stock_quantity = str(row[5]) if len(row) > 5 and row[5] else "0"
            transformed.append([
                formato, color, gramaje, stock_quantity
            ])
        return transformed
