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

# Define __all__ without extractors initially
__all__ = [
    'CobolParser',
    'setup_logger',
    'parse_file',
    'parse_string',
]

# Define a lazy module loader for extractors to avoid circular import
class LazyExtractorsLoader:
    def __getattr__(self, name):
        # Only import extractors when an attribute is accessed
        from . import extractors as real_extractors
        return getattr(real_extractors, name)

# Create a lazy loader instance
extractors = LazyExtractorsLoader()

# Add extractors to __all__
__all__.append('extractors')