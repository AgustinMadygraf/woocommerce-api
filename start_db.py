"""
Script de inicialización rápida de la base de datos y tabla principal para el proyecto.
Ejecuta este script antes de iniciar la app si es la primera vez.
"""
from src.infrastructure.pymysql.init_db import crear_db_y_tabla

if __name__ == "__main__":
    crear_db_y_tabla()
