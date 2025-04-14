"""
COBOL extractors module - Contains different extractors for COBOL elements.
"""
# Import from the local package structure
from .base_extractor import BaseExtractor
from .call_extractor import extract_calls
from .copybook_extractor import extract_copybooks, expand_copybooks
from .io_extractor import extract_io_files
from .perform_extractor import extract_performs
from .sql_extractor import extract_sql_queries
from .utils import (
    extract_with_copybook_expansion,
    extract_recursive_elements
)

__all__ = [
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