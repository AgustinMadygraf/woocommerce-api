"""
Path: src/interface_adapters/presenters/cli_style.py
Utilidades para estilos y formateo de tablas en CLI.
"""

from colorama import Fore, Style, init as colorama_init

try:
    colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


def bold(text):
    "Devuelve el texto en negrita si colorama está disponible."
    if COLORAMA_AVAILABLE:
        return Style.BRIGHT + str(text) + Style.RESET_ALL
    return str(text)

def cyan(text):
    "Devuelve el texto en cian si colorama está disponible."
    if COLORAMA_AVAILABLE:
        return Fore.CYAN + str(text) + Fore.RESET
    return str(text)

def yellow(text):
    "Devuelve el texto en amarillo si colorama está disponible."
    if COLORAMA_AVAILABLE:
        return Fore.YELLOW + str(text) + Fore.RESET
    return str(text)

def green(text):
    "Devuelve el texto en verde si colorama está disponible."
    if COLORAMA_AVAILABLE:
        return Fore.GREEN + str(text) + Fore.RESET
    return str(text)

def red(text):
    "Devuelve el texto en rojo si colorama está disponible."
    if COLORAMA_AVAILABLE:
        return Fore.RED + str(text) + Fore.RESET
    return str(text)

def format_table(rows, headers=None):
    """Devuelve una tabla formateada como string."""
    if not rows:
        return ""
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*(rows + ([headers] if headers else [])))]
    def fmt_row(row):
        return " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
    lines = []
    if headers:
        lines.append(bold(fmt_row(headers)))
        lines.append("-+-".join("-" * w for w in col_widths))
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines)
