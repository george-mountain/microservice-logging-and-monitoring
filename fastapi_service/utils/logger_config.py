from loguru import logger
import os

os.makedirs("app_logs", exist_ok=True)

# Configure the logger
logger.add(
    "app_logs/app.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
    enqueue=True,
    rotation="500 MB",
)

# Export logger instance for shared use
app_logger = logger
