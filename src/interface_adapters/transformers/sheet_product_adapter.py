class SheetProductAdapter:
    @staticmethod
    def transform(raw_values: list) -> list:
        """
        Transforma la estructura de la hoja actual al formato estándar requerido:
        [id, name, sku, regular_price, stock_quantity, status, type]
        Asume que los datos relevantes empiezan en la fila 4 (índice 3) y que las columnas son:
        0: (vacío o índice), 1: (vacío), 2: name, 3: sku/color, 4: peso, 5: referencia/stock, 6: programa, 7: verificado
        """
        transformed = []
        header = ["id", "name", "sku", "regular_price", "stock_quantity", "status", "type"]
        transformed.append(header)
        for row in raw_values[3:]:
            if len(row) < 6 or not row[2]:
                continue
            # Generar un id único (puede ser la referencia o un hash de name+sku)
            id_value = str(row[5]) if row[5] else f"{row[2]}-{row[3]}"
            name = str(row[2])
            sku = str(row[3])
            regular_price = "0"  # No hay precio en la hoja, se pone 0 por defecto
            stock_quantity = str(row[5]) if row[5] else "0"
            status = "publish"
            type_ = "simple"
            transformed.append([
                id_value, name, sku, regular_price, stock_quantity, status, type_
            ])
        return transformed
