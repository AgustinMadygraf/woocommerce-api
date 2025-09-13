"""
Path: src/entities/product.py
"""

from typing import Optional

class Product:
    "Entidad que representa un producto."
    def __init__(self, product_id: Optional[int] = None, name: str = '', sku: str = '', regular_price: str = '', stock_quantity: Optional[int] = None, status: str = '', type_: str = 'simple'):
        self.product_id = product_id
        self.name = name
        self.sku = sku
        self.regular_price = regular_price
        self.stock_quantity = stock_quantity
        self.status = status
        self.type = type_

    @classmethod
    def from_dict(cls, data: dict):
        "Crea una instancia de Product a partir de un diccionario."
        return cls(
            product_id=data.get('id'),
            name=data.get('name', ''),
            sku=data.get('sku', ''),
            regular_price=data.get('regular_price', ''),
            stock_quantity=data.get('stock_quantity'),
            status=data.get('status', ''),
            type_=data.get('type', 'simple')
        )

    def to_dict(self):
        "Convierte la instancia de Product a un diccionario."
        return {
            'id': self.product_id,
            'name': self.name,
            'sku': self.sku,
            'regular_price': self.regular_price,
            'stock_quantity': self.stock_quantity,
            'status': self.status,
            'type': self.type
        }
