from datetime import datetime, timezone

def get_current_datetime():
    """
    Returns the current UTC datetime as a timezone-aware object.
    """
    return datetime.now(timezone.utc)

# Logger imports
from .logger import (
    AppLogger,
    log_function_call,
    debug,
    info,
    warning,
    error,
    critical,
    default_logger
)

__all__ = [
    'get_current_datetime',
    'AppLogger',
    'log_function_call',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'default_logger'
]
