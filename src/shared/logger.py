"""
Path: src/shared/logger.py
"""

import logging

logging.basicConfig(
	level=logging.INFO,
	format='[%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("woocommerce-api")
