"""
Path: src/interface_adapters/gateways/product_persistence_gateway.py
"""

from abc import ABC, abstractmethod
from typing import List, Any

class ProductPersistenceGateway(ABC):
    "Interfaz para la persistencia de productos en la base de datos local."
    @abstractmethod
    def list_products(self) -> List[Any]:
        "Devuelve una lista de productos almacenados en la base de datos local."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def update_products_from_sheet(self, values: list) -> dict:
        "Actualiza o inserta productos en la base local a partir de datos de Google Sheets. Devuelve un resumen de la operación."
        pass # pylint: disable=unnecessary-pass
