# AppLogger - Comprehensive Logging for Meal Calorie Counter

A robust logging system designed specifically for the meal calorie counter application, providing structured logging, multiple output formats, and specialized logging methods for different types of events.

## Features

- **Multiple Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Dual Output**: Console and file logging with automatic rotation
- **Structured Logging**: Support for contextual data with each log entry
- **Specialized Methods**: Domain-specific logging for HTTP requests, database operations, user actions, etc.
- **Performance Monitoring**: Built-in timing and performance logging
- **Exception Handling**: Comprehensive exception logging with full tracebacks
- **Security Events**: Dedicated logging for security-related events
- **Function Decorators**: Easy function call logging with timing
- **Customizable**: Configurable log levels, formats, and file settings

## Quick Start

### Basic Usage

```python
from app.utils import AppLogger, info, error

# Create a logger instance
logger = AppLogger(name="my_module")

# Basic logging
logger.info("Application started")
logger.error("An error occurred", error_code=500)

# Using convenience functions
info("Simple info message")
error("Simple error message", context="authentication")
```

### Specialized Logging Methods

```python
# HTTP Request logging
logger.log_request("GET", "/api/calories", 200, 0.125, user_id="123")

# Database operation logging
logger.log_database_operation("SELECT", "users", 0.050, user_id="123")

# User action logging
logger.log_user_action("user_123", "login", ip_address="192.168.1.1")

# API call logging
logger.log_api_call("USDA", "/foods/search", True, query="apple")

# Calorie calculation logging
logger.log_calorie_calculation("apple", 95.0, serving_size="1 medium")

# Performance logging
logger.log_performance("database_query", 0.075, query="SELECT * FROM users")

# Security event logging
logger.log_security_event("failed_login", "Invalid credentials", user_id="admin")
```

### Exception Logging

```python
try:
    result = some_operation()
except Exception as e:
    logger.log_exception(
        e,
        "operation_context",
        user_id="123",
        additional_context="relevant info"
    )
```

### Function Decorator

```python
from app.utils import log_function_call

@log_function_call(AppLogger(name="my_module"))
def my_function(param1, param2):
    # Function logic here
    return result
```

## Configuration Options

### Logger Initialization

```python
logger = AppLogger(
    name="custom_logger",           # Logger name
    log_level="DEBUG",              # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_file="custom.log",          # Custom log file path
    max_file_size=5*1024*1024,      # Max file size before rotation (5MB)
    backup_count=3,                 # Number of backup files to keep
    enable_console=True,            # Enable console output
    enable_file=True,               # Enable file output
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Custom format
)
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors that may prevent the program from running

## File Structure

Logs are automatically stored in a `logs/` directory at the project root:

```
meal-calorie-counter/
├── logs/
│   ├── meal_calorie_counter.log
│   ├── meal_calorie_counter.log.1
│   └── meal_calorie_counter.log.2
```

## Log Format

Default log format includes:
- Timestamp
- Logger name
- Log level
- File name and line number
- Function name
- Message
- Context data (if provided)

Example output:
```
2024-01-15 10:30:45,123 | meal_calorie_counter | INFO | main.py:25 | startup | Application started | Context: version=1.0.0
```

## Integration Examples

### In Controllers

```python
from app.utils import AppLogger

logger = AppLogger(name="auth_controller")

class AuthController:
    def login(self, credentials):
        logger.info("Login attempt", user_email=credentials.email)
        
        try:
            # Authentication logic
            logger.log_user_action(credentials.email, "login", ip_address=request.client.host)
        except Exception as e:
            logger.log_exception(e, "login_authentication", user_email=credentials.email)
            raise
```

### In Services

```python
from app.utils import log_function_call, AppLogger

logger = AppLogger(name="calorie_service")

class CalorieService:
    @log_function_call(logger)
    def calculate_calories(self, food_item, quantity):
        logger.log_calorie_calculation(food_item, calories, quantity=quantity)
        return calories
```

### In Middleware

```python
from app.utils import AppLogger

logger = AppLogger(name="request_middleware")

async def log_request_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.log_request(
        request.method,
        str(request.url),
        response.status_code,
        duration,
        user_id=get_user_id(request)
    )
    
    return response
```

## Best Practices

1. **Use Descriptive Names**: Give loggers meaningful names that reflect their purpose
2. **Include Context**: Always include relevant contextual data with log messages
3. **Use Appropriate Levels**: Choose the right log level for each message
4. **Handle Exceptions**: Always log exceptions with full context
5. **Performance Monitoring**: Use performance logging for slow operations
6. **Security Events**: Log all security-related events for audit purposes

## Environment Variables

You can configure logging behavior using environment variables:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Set log file path
export LOG_FILE=/path/to/custom.log

# Disable file logging
export LOG_ENABLE_FILE=false

# Disable console logging
export LOG_ENABLE_CONSOLE=false
```

## Testing

The logger includes comprehensive examples in `logger_example.py`. Run it to see all features in action:

```bash
python -m app.utils.logger_example
```

## Dependencies

The logger uses only Python standard library modules:
- `logging`
- `pathlib`
- `datetime`
- `functools`
- `traceback`

No additional dependencies are required. 