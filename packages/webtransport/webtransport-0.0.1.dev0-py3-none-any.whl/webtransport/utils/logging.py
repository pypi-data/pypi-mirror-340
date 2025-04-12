"""
Logging utilities for WebTransport server.
"""

import logging
import sys
from typing import Optional


def configure_logging(
    level: int = logging.INFO, log_format: Optional[str] = None
) -> None:
    """
    Configure logging with reasonable defaults.

    Args:
        level: The logging level
        log_format: Optional custom log format
    """
    if log_format is None:
        log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"

    logging.basicConfig(format=log_format, level=level, stream=sys.stdout)

    # Silence some noisy loggers
    logging.getLogger("asyncio").setLevel(logging.WARNING)
