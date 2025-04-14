"""
Test for nested copybooks in COBOL programs.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.call_extractor import extract_calls
from cobol_parser.extractors.sql_extractor import extract_sql_queries


def test_nested_copybooks_expansion():
    """Test the expansion of nested copybooks."""
    # Main program that includes a copybook
    main_program = """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. NESTTEST.
        
        PROCEDURE DIVISION.
            DISPLAY "MAIN PROGRAM"
            COPY FIRST-LEVEL.
            STOP RUN.
    """
    
    # First-level copybook that includes another copybook
    first_level = """
        DISPLAY "FIRST LEVEL COPYBOOK"
        CALL "FIRST-LEVEL-MODULE" USING WS-VAR
        EXEC SQL SELECT * FROM FIRST_LEVEL_TABLE END-EXEC
        COPY SECOND-LEVEL.
    """
    
    # Second-level copybook
    second_level = """
        DISPLAY "SECOND LEVEL COPYBOOK"
        CALL "SECOND-LEVEL-MODULE" USING WS-VAR
        EXEC SQL SELECT * FROM SECOND_LEVEL_TABLE END-EXEC
    """
    
    # Create a resolver function that returns copybook content
    def copybook_resolver(name):
        if name == "FIRST-LEVEL":
            return first_level
        elif name == "SECOND-LEVEL":
            return second_level
        return None
    
    # Create a simple line map
    line_map = list(range(1, 100))
    
    # Test the expansion function
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Verify that the expansion included content from both copybooks
    assert "FIRST LEVEL COPYBOOK" in expanded_source
    assert "SECOND LEVEL COPYBOOK" in expanded_source
    assert "FIRST-LEVEL-MODULE" in expanded_source
    assert "SECOND-LEVEL-MODULE" in expanded_source
    
    # Extract and verify calls
    call_results = extract_calls(expanded_source, line_map)
    assert len(call_results) == 2
    call_names = [call['program_name'] for call in call_results]
    assert "FIRST-LEVEL-MODULE" in call_names
    assert "SECOND-LEVEL-MODULE" in call_names
    
    # Extract and verify SQL statements
    sql_results = extract_sql_queries(expanded_source, line_map)
    assert len(sql_results) == 2
    tables = [table for result in sql_results for table in result.get('tables', [])]
    assert "FIRST_LEVEL_TABLE" in tables
    assert "SECOND_LEVEL_TABLE" in tables


def test_deeply_nested_copybooks():
    """Test the expansion of deeply nested copybooks to make sure recursion works correctly."""
    # Create a chain of nested copybooks to test recursion
    main_program = """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. DEEPNEST.
        
        PROCEDURE DIVISION.
            COPY LEVEL-1.
            STOP RUN.
    """
    
    level_1 = "DISPLAY \"LEVEL 1\"\nCOPY LEVEL-2."
    level_2 = "DISPLAY \"LEVEL 2\"\nCOPY LEVEL-3."
    level_3 = "DISPLAY \"LEVEL 3\"\nCOPY LEVEL-4."
    level_4 = "DISPLAY \"LEVEL 4\"\nCOPY LEVEL-5."
    level_5 = "DISPLAY \"LEVEL 5 (MAX)\""
    
    def copybook_resolver(name):
        lookup = {
            "LEVEL-1": level_1,
            "LEVEL-2": level_2,
            "LEVEL-3": level_3,
            "LEVEL-4": level_4,
            "LEVEL-5": level_5
        }
        return lookup.get(name)
    
    # Test with default max_depth of 5
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Check that all 5 levels were expanded
    assert "LEVEL 1" in expanded_source
    assert "LEVEL 2" in expanded_source
    assert "LEVEL 3" in expanded_source
    assert "LEVEL 4" in expanded_source
    assert "LEVEL 5 (MAX)" in expanded_source
    
    # Test with a lower max_depth to ensure it stops at that level
    limited_expanded_source = expand_copybooks(main_program, copybook_resolver, max_depth=2)
    
    # Check that only the first 2 levels were expanded
    assert "LEVEL 1" in limited_expanded_source
    assert "LEVEL 2" in limited_expanded_source
    # The rest should not be expanded but contain COPY statements
    assert "COPY LEVEL-3" in limited_expanded_source 