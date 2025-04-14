"""
Tests for verifying module dependencies and import relationships.
"""
import os
import sys
import inspect
import importlib
import pytest
from types import ModuleType


def get_module_dependencies(module_name: str, already_checked=None) -> set:
    """
    Recursively get all dependencies for a module.
    
    Args:
        module_name: The name of the module to check
        already_checked: Set of modules already checked (for recursion)
        
    Returns:
        Set of all module dependencies
    """
    if already_checked is None:
        already_checked = set()
    
    if module_name in already_checked:
        return set()
    
    already_checked.add(module_name)
    
    try:
        # Import the module
        module = importlib.import_module(module_name)
        
        # Get the module's dependencies
        dependencies = set()
        for name, obj in inspect.getmembers(module):
            if inspect.ismodule(obj) and obj.__name__ != module_name:
                if obj.__name__.startswith('cobol_parser'):
                    dependencies.add(obj.__name__)
                    # Recursively get dependencies of this dependency
                    sub_deps = get_module_dependencies(obj.__name__, already_checked)
                    dependencies.update(sub_deps)
        
        return dependencies
    
    except (ImportError, AttributeError) as e:
        print(f"Error importing {module_name}: {e}")
        return set()


def test_no_circular_dependencies():
    """Test that there are no circular dependencies in the package."""
    all_modules = [
        'cobol_parser',
        'cobol_parser.parser',
        'cobol_parser.logger',
        'cobol_parser.interface',
        'cobol_parser.cli',
        'cobol_parser.extractors',
        'cobol_parser.extractors.base_extractor',
        'cobol_parser.extractors.call_extractor',
        'cobol_parser.extractors.copybook_extractor',
        'cobol_parser.extractors.io_extractor',
        'cobol_parser.extractors.perform_extractor',
        'cobol_parser.extractors.sql_extractor',
        'cobol_parser.extractors.utils',
    ]
    
    # Check each module for circular dependencies
    for module_name in all_modules:
        print(f"Checking dependencies for {module_name}")
        dependencies = get_module_dependencies(module_name)
        
        # A module should not import itself through any chain of dependencies
        assert module_name not in dependencies, f"Circular dependency detected in {module_name}"
        
        # Print dependencies for inspection
        print(f"  Dependencies: {dependencies}")


def test_expected_import_structure():
    """Test that the import structure matches the expected architecture."""
    # Load the modules
    base = importlib.import_module('cobol_parser')
    parser = importlib.import_module('cobol_parser.parser')
    logger = importlib.import_module('cobol_parser.logger')
    interface = importlib.import_module('cobol_parser.interface')
    extractors = importlib.import_module('cobol_parser.extractors')
    
    # Check that the parser imports the logger but not the other way around
    assert hasattr(parser, 'logger')
    
    # Check that interface imports CobolParser from parser module
    assert hasattr(interface, 'CobolParser')
    # Check that interface imports setup_logger from logger module
    assert hasattr(interface, 'setup_logger')
    
    # Check the extractors package structure
    assert hasattr(extractors, 'BaseExtractor')
    assert hasattr(extractors, 'extract_calls')
    assert hasattr(extractors, 'extract_copybooks')
    assert hasattr(extractors, 'extract_io_files')
    assert hasattr(extractors, 'extract_performs')
    assert hasattr(extractors, 'extract_sql_queries')


def test_import_from_parser():
    """Test that the parser can correctly import all extractors."""
    from cobol_parser.parser import CobolParser
    parser = CobolParser()
    
    # Create a simple test to force importing each extractor
    source = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
       MAIN-LOGIC.
           DISPLAY "Hello".
           STOP RUN.
    """
    
    parser.load_from_string(source)
    
    # Test each extraction method which will import the relevant extractors
    calls = parser.extract_calls()
    io_files = parser.extract_io_files()
    performs = parser.extract_performs()
    sql_queries = parser.extract_sql_queries()
    copybooks = parser.extract_copybooks()
    
    # All these should return lists (maybe empty for this simple source)
    assert isinstance(calls, list)
    assert isinstance(io_files, list)
    assert isinstance(performs, list)
    assert isinstance(sql_queries, list)
    assert isinstance(copybooks, list)


def test_all_extractors_via_utils():
    """Test that all extractors can be used through the utils module."""
    from cobol_parser.extractors.utils import extract_with_copybook_expansion
    
    # Create a simple test source
    source = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
           DISPLAY "Hello, World".
           CALL "SUBPROGRAM".
           PERFORM PROCESS-PARA.
       PROCESS-PARA.
           COPY TESTCOPY.
    """
    
    # Mock line map
    line_map = list(range(1, 100))
    
    # Mock copybook resolver
    def mock_resolver(name):
        if name == "TESTCOPY":
            return """
           DISPLAY "In copybook".
           CALL "COPYBOOK-SUBPROGRAM".
            """
        return None
    
    # Use the utility function to extract everything
    results = extract_with_copybook_expansion(
        source, 
        line_map,
        mock_resolver,
        expand_copybooks_flag=True
    )
    
    # Check that all extraction types are present
    assert "copybooks" in results
    assert "calls" in results
    assert "io" in results
    assert "performs" in results
    assert "sql" in results
    
    # When expand_copybooks_flag is True, copybook statements are replaced 
    # with their content before extraction, so we won't find copybooks in the result
    # Instead, we should check that calls from the expanded copybook were detected
    calls = results["calls"]
    copybook_call_found = any(call["program_name"] == "COPYBOOK-SUBPROGRAM" for call in calls)
    assert copybook_call_found, "Call from expanded copybook not found"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])