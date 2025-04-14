"""
COBOL Parser - A tool to extract information from COBOL programs.
"""

# Direct imports from the package to make the API cleaner
from .parser import CobolParser
from .logger import setup_logger
from .interface import parse_file, parse_string
from .extractors import (
    extract_calls,
    extract_copybooks,
    extract_io_files,
    extract_performs,
    extract_sql_queries,
    expand_copybooks,
    extract_with_copybook_expansion,
    extract_recursive_elements,
)

# Package metadata
__version__ = "0.1.1"
__package_name__ = "legacylens_cobol_parser"

# Define __all__ without extractors initially
__all__ = [
    'CobolParser',
    'setup_logger',
    'parse_file',
    'parse_string',
    'BaseExtractor',
    'extract_calls',
    'extract_copybooks',
    'extract_io_files',
    'extract_performs',
    'extract_sql_queries',
    'expand_copybooks',
    'extract_with_copybook_expansion',
    'extract_recursive_elements'
]
