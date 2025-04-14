"""
Integration tests to verify all packages are correctly imported and work together.
"""
import os
import pytest
import importlib
import inspect
import sys
from typing import Any, List, Dict

# Test the top-level package imports
def test_top_level_imports():
    """Test that all top-level modules can be imported."""
    from cobol_parser import CobolParser, setup_logger, parse_file, parse_string
    
    # Verify objects are of the correct type
    assert inspect.isclass(CobolParser)
    assert callable(setup_logger)
    assert callable(parse_file)
    assert callable(parse_string)


def test_parser_module_imports():
    """Test imports from the parser module."""
    from cobol_parser.parser import CobolParser
    
    # Verify the class has the expected methods
    assert hasattr(CobolParser, 'load_from_file')
    assert hasattr(CobolParser, 'load_from_string')
    assert hasattr(CobolParser, 'extract_all')
    assert hasattr(CobolParser, 'extract_calls')
    assert hasattr(CobolParser, 'extract_io_files')
    assert hasattr(CobolParser, 'extract_performs')
    assert hasattr(CobolParser, 'extract_sql_queries')
    assert hasattr(CobolParser, 'extract_copybooks')


def test_logger_module_imports():
    """Test imports from the logger module."""
    from cobol_parser.logger import setup_logger, CobolLogger, get_log_level
    
    # Verify the functions and classes exist
    assert callable(setup_logger)
    assert inspect.isclass(CobolLogger)
    assert callable(get_log_level)


def test_interface_module_imports():
    """Test imports from the interface module."""
    from cobol_parser.interface import parse_file, parse_string
    
    # Verify that functions exist
    assert callable(parse_file)
    assert callable(parse_string)


def test_extractor_imports():
    """Test imports from extractors module."""
    # Test the __init__.py exports
    from cobol_parser.extractors import (
        BaseExtractor, 
        extract_calls,
        extract_copybooks,
        extract_io_files,
        extract_performs,
        extract_sql_queries,
        expand_copybooks,
        extract_with_copybook_expansion,
        extract_recursive_elements
    )
    
    # Verify each extractor function
    assert callable(extract_calls)
    assert callable(extract_copybooks)
    assert callable(extract_io_files)
    assert callable(extract_performs)
    assert callable(extract_sql_queries)
    assert callable(expand_copybooks)
    assert callable(extract_with_copybook_expansion)
    assert callable(extract_recursive_elements)
    assert inspect.isclass(BaseExtractor)

    # Import each extractor module directly
    from cobol_parser.extractors import base_extractor
    from cobol_parser.extractors import call_extractor
    from cobol_parser.extractors import copybook_extractor
    from cobol_parser.extractors import io_extractor
    from cobol_parser.extractors import perform_extractor
    from cobol_parser.extractors import sql_extractor
    from cobol_parser.extractors import utils


def test_extractor_implementations():
    """Test that each extractor implementation has required functions."""
    from cobol_parser.extractors import call_extractor
    from cobol_parser.extractors import copybook_extractor
    from cobol_parser.extractors import io_extractor
    from cobol_parser.extractors import perform_extractor
    from cobol_parser.extractors import sql_extractor
    
    # Verify each module has its main extraction function
    assert hasattr(call_extractor, 'extract_calls')
    assert hasattr(copybook_extractor, 'extract_copybooks')
    assert hasattr(io_extractor, 'extract_io_files')
    assert hasattr(perform_extractor, 'extract_performs')
    assert hasattr(sql_extractor, 'extract_sql_queries')


def test_cli_imports():
    """Test imports from CLI module."""
    from cobol_parser import cli
    
    # Verify that the main CLI functions exist
    assert hasattr(cli, 'main')
    assert hasattr(cli, 'parse_arguments')


def test_integrated_functionality():
    """Test that the main components work together properly."""
    from cobol_parser import CobolParser
    
    # Create a simple COBOL source
    source = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
           DISPLAY "Hello, World".
           CALL "TESTPROG" USING WS-VARIABLE.
           PERFORM TEST-PARA UNTIL DONE = 'Y'.
           STOP RUN.
       TEST-PARA.
           DISPLAY "Test paragraph".
    """
    
    # Create a parser and load the source
    parser = CobolParser()
    parser.load_from_string(source)
    
    # Extract all information
    results = parser.extract_all()
    
    # Verify that all extraction types are present
    assert "calls" in results
    assert "io_files" in results
    assert "performs" in results
    assert "sql_queries" in results
    assert "copybooks" in results
    
    # Verify the call was extracted correctly
    calls = results["calls"]
    assert len(calls) == 1
    assert calls[0]["program_name"] == "TESTPROG"
    
    # Verify the perform was extracted correctly
    performs = results["performs"]
    assert len(performs) >= 1
    # Find the explicit PERFORM
    explicit_performs = [p for p in performs if p.get("type") == "explicit"]
    assert len(explicit_performs) == 1
    assert explicit_performs[0]["procedure"] == "TEST-PARA"


def test_interface_functionality():
    """Test that the simplified interface functions work properly."""
    from cobol_parser import parse_string
    
    # Create a simple COBOL source
    source = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
           DISPLAY "Hello, World".
           CALL "TESTPROG" USING WS-VARIABLE.
           STOP RUN.
    """
    
    # Use the parse_string function to process the source
    results = parse_string(source)
    
    # Verify that all extraction types are present
    assert "calls" in results
    assert "io_files" in results
    assert "performs" in results
    assert "sql_queries" in results
    assert "copybooks" in results
    
    # Test with specific extraction types
    calls_only = parse_string(source, extract_types=["calls"])
    assert "calls" in calls_only
    assert "io_files" not in calls_only
    assert "performs" not in calls_only
    
    # Verify the call was extracted correctly
    calls = results["calls"]
    assert len(calls) == 1
    assert calls[0]["program_name"] == "TESTPROG"


if __name__ == "__main__":
    # Allow this test module to be run directly
    pytest.main(["-xvs", __file__])