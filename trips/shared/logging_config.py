import logging
from logging.handlers import RotatingFileHandler
import os
from flask import request
from werkzeug.exceptions import HTTPException


class RequestContextFilter(logging.Filter):
    """A filter to add default request context attributes to the log record."""
    def filter(self, record):
        record.method = getattr(record, 'method', '-')
        record.path = getattr(record, 'path', '-')
        record.status = getattr(record, 'status', '-')
        return True

def setup_logger(service_name: str, log_dir: str = "logs"):
    """
    Configures and returns a logger for a specific service.
    
    Args:
        service_name (str): The name of the service (e.g., "trips", "users").
        log_dir (str): The directory where log files will be stored.
    """
    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{service_name}.log")

    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    # Prevent adding handlers multiple times if this function is called more than once
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add the custom filter
    logger.addFilter(RequestContextFilter())

    # Create a rotating file handler for file-based logging
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(method)s %(path)s - %(status)s | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Create a stream handler to also log to the console
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger

def register_logging_handlers(app, logger):
    """
    Registers global error handling and request logging for the Flask app.
    """

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all unhandled exceptions and log them."""
        # Pass through HTTP-related exceptions
        if isinstance(e, HTTPException):
            return e

        # Log the full traceback for any other exception
        logger.error(f"Unhandled Exception: {e}", exc_info=True)
        
        # Return a generic 500 error response
        return {"message": "An internal server error occurred."}, 500

    @app.after_request
    def log_request(response):
        """Log every request after it has been handled."""
        log_message = "Request processed"  # Default message

        if response.is_json:
            try:
                data = response.get_json()
                if isinstance(data, dict):
                    log_message = data.get('message', log_message)
                elif isinstance(data, list):
                    log_message = f"Response contains a list with {len(data)} items"
            except Exception:
                pass

        logger.info(
            log_message,
            extra={
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
            }
        )
        return response
