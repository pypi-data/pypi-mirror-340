"""
COBOL Parser - A tool to extract information from COBOL programs.
"""

# Direct imports from the package to make the API cleaner
from .parser import CobolParser
from .logger import setup_logger
from .interface import parse_file, parse_string

# Package metadata
__version__ = "0.1.0"
__package_name__ = "legacylens_cobol_parser"

__all__ = [
    'CobolParser',
    'setup_logger',
    'parse_file',
    'parse_string'
]