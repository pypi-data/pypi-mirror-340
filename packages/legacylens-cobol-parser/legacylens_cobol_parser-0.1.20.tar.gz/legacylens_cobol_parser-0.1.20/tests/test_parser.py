"""
Test module for the COBOL parser.
"""
import os
import pytest
from typing import Dict, Any, List

from cobol_parser.parser import CobolParser


# Path to the sample COBOL file
SAMPLE_FILE = os.path.join(os.path.dirname(__file__), 'sample.cbl')


@pytest.fixture
def cobol_parser():
    """Create and return a CobolParser instance with the sample file loaded."""
    parser = CobolParser(ignore_case=True)
    parser.load_from_file(SAMPLE_FILE)
    return parser


def test_parser_initialization():
    """Test that parser initializes correctly."""
    parser = CobolParser()
    assert parser._source_code == ""
    assert parser._normalized_source == ""
    assert parser._line_map == []
    assert parser.ignore_case is True
    
    parser = CobolParser(ignore_case=False)
    assert parser.ignore_case is False


def test_parser_load_from_file(cobol_parser):
    """Test loading COBOL source from file."""
    assert cobol_parser._source_code != ""
    assert cobol_parser._normalized_source != ""
    assert len(cobol_parser._line_map) > 0


def test_parser_load_from_string():
    """Test loading COBOL source from string."""
    source = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TEST.
       PROCEDURE DIVISION.
           DISPLAY "HELLO, WORLD".
           STOP RUN.
    """
    
    parser = CobolParser()
    parser.load_from_string(source)
    
    assert parser._source_code == source
    assert parser._normalized_source != ""
    assert len(parser._line_map) > 0


def test_extract_calls(cobol_parser):
    """Test extraction of CALL statements."""
    calls = cobol_parser.extract_calls()
    
    # Check that calls were extracted
    assert isinstance(calls, list)
    assert len(calls) > 0
    
    # Check specific calls in the sample
    call_programs = [c.get('program_name') for c in calls]
    assert "VALIDATE-CUSTOMER" in call_programs
    assert "FORMAT-ORDER" in call_programs
    assert "HEADER-GENERATOR" in call_programs
    assert "FINALIZE-REPORT" in call_programs
    
    # Check that parameters were extracted for at least one call
    call_with_params = next((c for c in calls if c.get('parameters')), None)
    assert call_with_params is not None
    assert len(call_with_params.get('parameters', [])) > 0


def test_extract_io_files(cobol_parser):
    """Test extraction of file I/O operations."""
    io_files = cobol_parser.extract_io_files()
    
    # Check that file operations were extracted
    assert isinstance(io_files, list)
    assert len(io_files) > 0
    
    # Check for SELECT statements
    selects = [f for f in io_files if f.get('operation') == 'SELECT']
    assert len(selects) >= 2  # We have at least 2 SELECT statements
    
    # Check for specific file names
    file_names = []
    for item in selects:
        if 'file_name' in item.get('groups', {}):
            file_names.append(item['groups']['file_name'])
    
    assert "CUSTOMER-FILE" in file_names
    assert "REPORT-FILE" in file_names
    
    # Check for READ operations
    reads = [f for f in io_files if f.get('operation') == 'READ']
    assert len(reads) > 0
    
    # Check for WRITE operations
    writes = [f for f in io_files if f.get('operation') == 'WRITE']
    assert len(writes) > 0
    
    # Check for OPEN operations
    opens = [f for f in io_files if f.get('operation') == 'OPEN']
    assert len(opens) > 0
    
    # Check for CLOSE operations
    closes = [f for f in io_files if f.get('operation') == 'CLOSE']
    assert len(closes) > 0


def test_extract_performs(cobol_parser):
    """Test extraction of PERFORM statements."""
    performs = cobol_parser.extract_performs()
    
    # Check that performs were extracted
    assert isinstance(performs, list)
    assert len(performs) > 0
    
    # Check for explicit PERFORMs
    explicit_performs = [p for p in performs if p.get('type') == 'explicit']
    assert len(explicit_performs) > 0
    
    # Check for specific procedures
    procedure_names = [p.get('procedure') for p in explicit_performs]
    assert "INITIALIZATION" in procedure_names
    assert "PROCESS-RECORDS" in procedure_names
    assert "TERMINATION" in procedure_names
    
    # Check for inline PERFORMs
    inline_performs = [p for p in performs if p.get('type') == 'inline']
    assert len(inline_performs) > 0


def test_extract_sql_queries(cobol_parser):
    """Test extraction of SQL queries."""
    sql_queries = cobol_parser.extract_sql_queries()
    
    # Check that SQL queries were extracted
    assert isinstance(sql_queries, list)
    assert len(sql_queries) > 0
    
    # Check for different SQL operations
    operation_types = [q.get('operation') for q in sql_queries]
    assert "SELECT" in operation_types
    assert "DECLARE" in operation_types
    assert "OPEN" in operation_types
    assert "FETCH" in operation_types
    assert "CLOSE" in operation_types
    
    # Check table names
    tables = []
    for query in sql_queries:
        if 'table' in query:
            tables.append(query['table'])
        elif 'tables' in query:
            tables.extend(query['tables'])
    
    assert "ORDERS" in tables


def test_extract_copybooks(cobol_parser):
    """Test extraction of COPYBOOK inclusions."""
    copybooks = cobol_parser.extract_copybooks()
    
    # Check that copybooks were extracted
    assert isinstance(copybooks, list)
    assert len(copybooks) > 0
    
    # Check for specific copybooks
    copybook_names = [c.get('copybook_name') for c in copybooks]
    assert "CUSTOMER-DETAILS" in copybook_names
    assert "REPORT-HEADER" in copybook_names
    
    # Check that REPLACING is properly extracted
    replacing_copybook = next((c for c in copybooks if "REPLACING" in c.get('match', "")), None)
    assert replacing_copybook is not None
    assert 'replacements' in replacing_copybook


def test_extract_all(cobol_parser):
    """Test extraction of all elements at once."""
    all_results = cobol_parser.extract_all()
    
    # Check that all sections are present
    assert "calls" in all_results
    assert "io_files" in all_results
    assert "performs" in all_results
    assert "sql_queries" in all_results
    assert "copybooks" in all_results
    
    # Check that each section has content
    assert len(all_results["calls"]) > 0
    assert len(all_results["io_files"]) > 0
    assert len(all_results["performs"]) > 0
    assert len(all_results["sql_queries"]) > 0
    assert len(all_results["copybooks"]) > 0 