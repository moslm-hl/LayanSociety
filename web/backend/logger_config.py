#!/usr/bin/env python3
"""
Logging configuration for LAYAN SOCIETY applications.
Provides structured logging with file rotation and different log levels.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


def setup_logger(
    name: str,
    log_file: str = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up a logger with file and optional console handlers.
    
    Args:
        name: Logger name (typically __name__ or module name)
        log_file: Path to log file. If None, uses default naming
        level: Logging level (default: INFO)
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        console_output: Whether to output to console
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    if log_file is None:
        # Generate default log filename
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = f"application_{timestamp}.log"
    
    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def setup_statement_logger(username: str) -> logging.Logger:
    """
    Set up a dedicated logger for financial statements.
    These logs are structured differently and don't rotate like application logs.
    
    Args:
        username: Username for the statement log
    
    Returns:
        Configured logger for statements
    """
    logger_name = f"statement.{username}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Generate statement log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_username = username.lower().replace(" ", "_").replace("-", "_")
    log_file = f"statement_{safe_username}_{timestamp}.log"
    
    # File handler (no rotation for statements - each is a unique document)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Statement formatter - simpler format for document-style logs
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_application_logger(module_name: str = None) -> logging.Logger:
    """
    Get or create an application logger.
    
    Args:
        module_name: Optional module name. If None, uses caller's module.
    
    Returns:
        Logger instance
    """
    if module_name is None:
        import inspect
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals.get('__name__', 'layan_app')
    
    # Check if logger already exists
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        # Set up default logger
        return setup_logger(module_name)
    
    return logger


# Pre-configured loggers for common modules
app_logger = get_application_logger('layan_app')
calc_logger = get_application_logger('calculator')
estimator_logger = get_application_logger('estimator')
