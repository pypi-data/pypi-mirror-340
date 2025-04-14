"""
Centralized logging module for the COBOL parser.
"""
import logging
import sys
from typing import Optional, Union

# Create a default logger instance
logger = None

def get_log_level(level_name: str) -> int:
    """
    Convert a log level name to the corresponding integer value.

    Args:
        level_name: The name of the log level ('info', 'warning', 'debug')

    Returns:
        The integer value of the log level
    """
    levels = {
        'info': logging.INFO,
        'warning': logging.WARNING,
        'debug': logging.DEBUG
    }
    return levels.get(level_name.lower(), logging.INFO)

def setup_logger(name: str = "cobol_parser", level: Union[int, str] = logging.INFO) -> logging.Logger:
    """
    Set up the logger with the specified name and level.
    
    Args:
        name: Name of the logger
        level: Logging level (INFO, WARNING, DEBUG) or string ('info', 'warning', 'debug')
        
    Returns:
        The configured logger instance
    """
    global logger
    
    # Convert string level to int if needed
    if isinstance(level, str):
        level = get_log_level(level)
    
    logger = CobolLogger(name=name, level=level)
    return logger.logger

class CobolLogger:
    """
    Custom logger for the COBOL parser with standard levels:
    - INFO: Standard information
    - WARNING: Warning information
    - DEBUG: Debugging information
    """
    
    def __init__(self, name: str = "cobol_parser", level: int = logging.INFO):
        """
        Initialize the logger.
        
        Args:
            name: Name of the logger
            level: Initial logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Remove any existing handlers to avoid duplicate output
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def set_level(self, level: Union[int, str]) -> None:
        """
        Set the logging level.
        
        Args:
            level: One of logging.INFO, logging.WARNING, logging.DEBUG, 
                  or a string ('info', 'warning', 'debug')
        """
        if isinstance(level, str):
            level = get_log_level(level)
        self.logger.setLevel(level)
    
    def info(self, msg: str, *args, **kwargs) -> None:
        """Log an info message."""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs) -> None:
        """Log a warning message."""
        self.logger.warning(msg, *args, **kwargs)
    
    def debug(self, msg: str, *args, **kwargs) -> None:
        """Log a debug message."""
        self.logger.debug(msg, *args, **kwargs)

# Initialize the default logger
setup_logger()