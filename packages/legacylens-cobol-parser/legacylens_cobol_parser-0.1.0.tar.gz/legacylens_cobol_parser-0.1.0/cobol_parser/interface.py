"""
User-friendly interfaces for the COBOL Parser.
"""

import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

from .parser import CobolParser
from .logger import setup_logger


def parse_file(file_path: Union[str, Path], 
              extract_types: Optional[List[str]] = None,
              log_level: int = logging.INFO) -> Dict[str, Any]:
    """
    Parse a COBOL file and extract the specified information.
    
    Args:
        file_path: Path to the COBOL file
        extract_types: Types of information to extract ('calls', 'io_files', 'performs', 
                      'sql_queries', 'copybooks'), defaults to all
        log_level: Logging level (logging.INFO, logging.DEBUG)
    
    Returns:
        Dictionary with extracted information
    """
    setup_logger(level=log_level)
    parser = CobolParser()
    parser.load_from_file(file_path)
    
    if extract_types is None:
        return parser.extract_all()
    
    result = {}
    if 'calls' in extract_types:
        result['calls'] = parser.extract_calls()
    if 'io_files' in extract_types:
        result['io_files'] = parser.extract_io_files()
    if 'performs' in extract_types:
        result['performs'] = parser.extract_performs()
    if 'sql_queries' in extract_types:
        result['sql_queries'] = parser.extract_sql_queries()
    if 'copybooks' in extract_types:
        result['copybooks'] = parser.extract_copybooks()
    
    return result


def parse_string(cobol_code: str,
                extract_types: Optional[List[str]] = None,
                log_level: int = logging.INFO) -> Dict[str, Any]:
    """
    Parse COBOL code from a string and extract the specified information.
    
    Args:
        cobol_code: String containing COBOL code
        extract_types: Types of information to extract ('calls', 'io_files', 'performs', 
                      'sql_queries', 'copybooks'), defaults to all
        log_level: Logging level (logging.INFO, logging.DEBUG)
    
    Returns:
        Dictionary with extracted information
    """
    setup_logger(level=log_level)
    parser = CobolParser()
    parser.load_from_string(cobol_code)
    
    if extract_types is None:
        return parser.extract_all()
    
    result = {}
    if 'calls' in extract_types:
        result['calls'] = parser.extract_calls()
    if 'io_files' in extract_types:
        result['io_files'] = parser.extract_io_files()
    if 'performs' in extract_types:
        result['performs'] = parser.extract_performs()
    if 'sql_queries' in extract_types:
        result['sql_queries'] = parser.extract_sql_queries()
    if 'copybooks' in extract_types:
        result['copybooks'] = parser.extract_copybooks()
    
    return result