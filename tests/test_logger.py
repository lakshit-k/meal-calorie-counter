"""
Example usage of the AppLogger class for the meal calorie counter application.
This file demonstrates various logging features and patterns.
"""

from app.utils.logger import AppLogger, log_function_call, info, error, debug


# Example 1: Basic logger usage
def basic_logging_example():
    """Demonstrate basic logging functionality."""
    logger = AppLogger(name="basic_example")
    
    logger.info("Application started")
    logger.debug("Debug information", user_id="123", action="login")
    logger.warning("Warning message", context="authentication")
    logger.error("Error occurred", error_code=500, endpoint="/api/users")
    logger.critical("Critical system failure", component="database")


# Example 2: Specialized logging methods
def specialized_logging_example():
    """Demonstrate specialized logging methods."""
    logger = AppLogger(name="specialized_example")
    
    # Log HTTP requests
    logger.log_request("GET", "/api/calories", 200, 0.125, user_id="123")
    logger.log_request("POST", "/api/users", 400, 0.250, error="Invalid data")
    
    # Log database operations
    logger.log_database_operation("SELECT", "users", 0.050, user_id="123")
    logger.log_database_operation("INSERT", "calories", 0.075, food_item="apple")
    
    # Log user actions
    logger.log_user_action("user_123", "login", ip_address="192.168.1.1")
    logger.log_user_action("user_456", "search_food", query="chicken breast")
    
    # Log API calls
    logger.log_api_call("USDA", "/foods/search", True, query="apple")
    logger.log_api_call("USDA", "/foods/123", False, error="Not found")
    
    # Log calorie calculations
    logger.log_calorie_calculation("apple", 95.0, serving_size="1 medium")
    logger.log_calorie_calculation("chicken breast", 165.0, serving_size="100g")


# Example 3: Exception logging
def exception_logging_example():
    """Demonstrate exception logging."""
    logger = AppLogger(name="exception_example")
    
    try:
        # Simulate an error
        result = 10 / 0
    except Exception as e:
        logger.log_exception(
            e,
            "division_operation",
            dividend=10,
            divisor=0,
            user_id="123"
        )


# Example 4: Performance logging
def performance_logging_example():
    """Demonstrate performance logging."""
    logger = AppLogger(name="performance_example")
    
    import time
    
    # Simulate a slow operation
    start_time = time.time()
    time.sleep(0.1)  # Simulate work
    duration = time.time() - start_time
    
    logger.log_performance(
        "database_query",
        duration,
        query="SELECT * FROM users",
        rows_returned=100
    )


# Example 5: Security event logging
def security_logging_example():
    """Demonstrate security event logging."""
    logger = AppLogger(name="security_example")
    
    logger.log_security_event(
        "failed_login",
        "Invalid credentials for user admin",
        user_id="admin",
        ip_address="192.168.1.100",
        attempt_count=3
    )
    
    logger.log_security_event(
        "suspicious_activity",
        "Multiple failed login attempts",
        ip_address="192.168.1.100",
        time_window="5 minutes"
    )


# Example 6: Using the decorator
@log_function_call(AppLogger(name="decorator_example"))
def example_function(param1: str, param2: int) -> str:
    """Example function with logging decorator."""
    import time
    time.sleep(0.05)  # Simulate work
    return f"Result: {param1} + {param2}"


# Example 7: Using convenience functions
def convenience_functions_example():
    """Demonstrate convenience functions."""
    logger = AppLogger(name="basic_example")
    logger.info("Using convenience function for info logging")
    logger.debug("Debug message with context", context="convenience_example")
    logger.warning("Warning message", severity="medium")
    logger.error("Error message", error_type="validation")
    logger.critical("Critical message", system="database")


# Example 8: Custom logger configuration
def custom_logger_example():
    """Demonstrate custom logger configuration."""
    # Create logger with custom settings
    custom_logger = AppLogger(
        name="custom_example",
        log_level="DEBUG",
        log_file="../custom_app.log",
        max_file_size=5 * 1024 * 1024,  # 5MB
        backup_count=3,
        enable_console=True,
        enable_file=True,
        format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    custom_logger.info("Custom logger configured")
    custom_logger.debug("Debug message from custom logger")


if __name__ == "__main__":
    # Run all examples
    print("Running logger examples...")
    
    basic_logging_example()
    specialized_logging_example()
    exception_logging_example()
    performance_logging_example()
    security_logging_example()
    example_function("test", 42)
    convenience_functions_example()
    custom_logger_example()
    
    print("All examples completed!") 