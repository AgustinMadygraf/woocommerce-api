"""
Path: src/interface_adapters/gateways/base_gateway.py
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseProductGateway(ABC):
    "Interfaz base para gateways de productos."
    @abstractmethod
    def get_product_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        "Obtener un producto por su SKU."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def list_products(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        "Listar productos con filtros opcionales."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        "Crear un nuevo producto."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def update_product(self, product_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        "Actualizar un producto existente."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        "Eliminar un producto."
        pass # pylint: disable=unnecessary-pass
