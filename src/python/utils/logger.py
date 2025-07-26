"""
JAEGIS Python Logger
Structured logging utility for Python components

@version 2.0.0
@author JAEGIS Development Team
"""

import os
import sys
import logging
import structlog
from datetime import datetime
from pathlib import Path

def setup_logger():
    """Setup structured logging for JAEGIS Python components."""
    
    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Setup file handlers
    file_handler = logging.FileHandler(logs_dir / "jaegis-python.log")
    file_handler.setLevel(logging.INFO)
    
    error_handler = logging.FileHandler(logs_dir / "jaegis-python-error.log")
    error_handler.setLevel(logging.ERROR)
    
    # Add handlers to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    return structlog.get_logger("jaegis.python")

# Initialize logger
logger = setup_logger()