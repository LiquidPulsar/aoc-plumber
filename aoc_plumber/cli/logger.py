import os
import sys
from loguru import logger

log_level = os.getenv("AOCP_LOG_LEVEL", "INFO").upper()

logger.remove()
logger.add(sys.stderr, level=log_level)
