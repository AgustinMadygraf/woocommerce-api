"""
Validador de entradas para la CLI y otros adaptadores.
"""

def is_valid_int(value: str) -> bool:
    """Valida si el valor es un entero válido."""
    return value.isdigit()

def is_valid_float(value: str) -> bool:
    """Valida si el valor es un float válido."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_non_empty(value: str) -> bool:
    """Valida que el valor no esté vacío."""
    return bool(value and value.strip())
