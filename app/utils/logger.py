import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json
from functools import wraps
import traceback


class AppLogger:
    """
    A comprehensive logger class for the meal calorie counter application.
    Supports multiple log levels, file and console output, and structured logging.
    """
    
    def __init__(
        self,
        name: str = "meal_calorie_counter",
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        enable_console: bool = True,
        enable_file: bool = True,
        format_string: Optional[str] = None
    ):
        """
        Initialize the logger with specified configuration.
        
        Args:
            name: Logger name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (if None, uses default location)
            max_file_size: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            enable_console: Whether to log to console
            enable_file: Whether to log to file
            format_string: Custom format string for log messages
        """
        self.name = name
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Set up formatter
        if format_string is None:
            format_string = (
                "%(asctime)s | %(name)s | %(levelname)s | "
                "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
            )
        self.formatter = logging.Formatter(format_string)
        
        # Set up handlers
        if enable_console:
            self._setup_console_handler()
        
        if enable_file:
            self._setup_file_handler(log_file, max_file_size, backup_count)
    
    def _setup_console_handler(self):
        """Set up console logging handler."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self, log_file: Optional[str], max_file_size: int, backup_count: int):
        """Set up file logging handler with rotation."""
        if log_file is None:
            # Create logs directory in project root
            logs_dir = Path(__file__).parent.parent.parent / "logs"
            logs_dir.mkdir(exist_ok=True)
            log_file = logs_dir / f"{self.name}.log"
        
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use RotatingFileHandler for log rotation
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional structured data."""
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional structured data."""
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional structured data."""
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message with optional structured data."""
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message with optional structured data."""
        self._log_with_context(logging.CRITICAL, message, **kwargs)
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        """Log message with optional structured context data."""
        if kwargs:
            # Add structured data to message
            context_str = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            full_message = f"{message} | Context: {context_str}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_request(self, method: str, url: str, status_code: int, response_time: float, **kwargs):
        """Log HTTP request details."""
        self.info(
            f"HTTP {method} {url} - Status: {status_code} - Time: {response_time:.3f}s",
            method=method,
            url=url,
            status_code=status_code,
            response_time=response_time,
            **kwargs
        )
    
    def log_database_operation(self, operation: str, table: str, duration: float, **kwargs):
        """Log database operation details."""
        self.info(
            f"DB {operation} on {table} - Duration: {duration:.3f}s",
            operation=operation,
            table=table,
            duration=duration,
            **kwargs
        )
    
    def log_user_action(self, user_id: str, action: str, **kwargs):
        """Log user actions."""
        self.info(
            f"User {user_id} performed {action}",
            user_id=user_id,
            action=action,
            **kwargs
        )
    
    def log_exception(self, exception: Exception, context: str = "", **kwargs):
        """Log exception with full traceback."""
        error_msg = f"Exception in {context}: {str(exception)}"
        self.error(
            error_msg,
            exception_type=type(exception).__name__,
            exception_message=str(exception),
            traceback=traceback.format_exc(),
            **kwargs
        )
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics."""
        self.info(
            f"Performance: {operation} took {duration:.3f}s",
            operation=operation,
            duration=duration,
            **kwargs
        )
    
    def log_security_event(self, event_type: str, details: str, **kwargs):
        """Log security-related events."""
        self.warning(
            f"Security Event: {event_type} - {details}",
            event_type=event_type,
            details=details,
            **kwargs
        )
    
    def log_api_call(self, service: str, endpoint: str, success: bool, **kwargs):
        """Log external API calls."""
        status = "SUCCESS" if success else "FAILED"
        self.info(
            f"API Call: {service} {endpoint} - {status}",
            service=service,
            endpoint=endpoint,
            success=success,
            **kwargs
        )
    
    def log_calorie_calculation(self, food_item: str, calories: float, **kwargs):
        """Log calorie calculation events."""
        self.info(
            f"Calorie calculation: {food_item} = {calories} calories",
            food_item=food_item,
            calories=calories,
            **kwargs
        )
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logging.Logger instance."""
        return self.logger
    
    def set_level(self, level: str):
        """Set the logging level."""
        self.log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(self.log_level)
        for handler in self.logger.handlers:
            handler.setLevel(self.log_level)


def log_function_call(logger: AppLogger):
    """
    Decorator to log function calls with timing and parameters.
    
    Usage:
        @log_function_call(logger)
        def my_function(param1, param2):
            return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            
            # Log function entry
            logger.debug(
                f"Entering function {func.__name__}",
                function=func.__name__,
                args=str(args),
                kwargs=str(kwargs)
            )
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log successful completion
                logger.debug(
                    f"Function {func.__name__} completed successfully",
                    function=func.__name__,
                    duration=duration,
                    result_type=type(result).__name__
                )
                
                return result
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                
                # Log exception
                logger.log_exception(
                    e,
                    f"Function {func.__name__}",
                    function=func.__name__,
                    duration=duration,
                    args=str(args),
                    kwargs=str(kwargs)
                )
                raise
        
        return wrapper
    return decorator


# Default logger instance
default_logger = AppLogger()

# Convenience functions using default logger
def debug(message: str, **kwargs):
    """Log debug message using default logger."""
    default_logger.debug(message, **kwargs)

def info(message: str, **kwargs):
    """Log info message using default logger."""
    default_logger.info(message, **kwargs)

def warning(message: str, **kwargs):
    """Log warning message using default logger."""
    default_logger.warning(message, **kwargs)

def error(message: str, **kwargs):
    """Log error message using default logger."""
    default_logger.error(message, **kwargs)

def critical(message: str, **kwargs):
    """Log critical message using default logger."""
    default_logger.critical(message, **kwargs) 