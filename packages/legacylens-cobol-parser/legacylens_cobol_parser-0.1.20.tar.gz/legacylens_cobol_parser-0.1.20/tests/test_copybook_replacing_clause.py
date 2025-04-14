"""
Test for COPY statements with REPLACING clause.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.utils import extract_with_copybook_expansion

def test_copybook_replacing_clause():
    """Test extraction with COPY REPLACING clause which can modify copybook content."""
    # Main program with a COPY REPLACING statement
    main_source = """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. REPLACINGTEST.
        
        PROCEDURE DIVISION.
            COPY TEMPLATE-COPYBOOK REPLACING
                ==TEMPLATE-NAME== BY ==CUSTOMER-FILE==
                ==TEMPLATE-FUNC== BY ==PROCESS-CUSTOMER==.
            STOP RUN.
    """
    
    # Copybook with placeholders for replacement
    template_copybook = """
        * This is a template copybook with placeholders
        OPEN INPUT TEMPLATE-NAME
        READ TEMPLATE-NAME
            AT END SET EOF TO TRUE
        END-READ
        
        TEMPLATE-FUNC.
            CALL "TEMPLATE-NAME-MODULE" USING WS-VAR
            EXEC SQL SELECT * FROM TEMPLATE_NAME END-EXEC
    """
    
    # Create a copybook resolver that applies the REPLACING
    def copybook_resolver(name):
        if name == "TEMPLATE-COPYBOOK":
            return template_copybook
        return None
    
    # Create a simple line map
    line_map = list(range(1, 100))
    
    # First expand the source manually
    expanded_source = expand_copybooks(main_source, copybook_resolver)
    
    # Verify that replacements were properly applied by checking the expanded source
    assert "CUSTOMER-FILE" in expanded_source
    assert "PROCESS-CUSTOMER" in expanded_source
    assert "TEMPLATE-NAME" not in expanded_source
    assert "TEMPLATE-FUNC" not in expanded_source 