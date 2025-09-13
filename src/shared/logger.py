"""
Path: src/shared/logger.py
"""

import logging

logging.basicConfig(
	level=logging.DEBUG,  # Cambia INFO por DEBUG
	format='[%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("woocommerce-api")
