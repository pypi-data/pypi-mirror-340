"""
Test module to validate the separation of SQL and COBOL IO operations.
"""
import pytest
from typing import Dict, Any, List

from cobol_parser.extractors.io_extractor import extract_io_files
from cobol_parser.extractors.sql_extractor import extract_sql_queries


@pytest.fixture
def mixed_io_sql_source():
    """Sample COBOL source code with both COBOL IO and SQL operations."""
    return """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. IOSQLTEST.
        
        ENVIRONMENT DIVISION.
        INPUT-OUTPUT SECTION.
        FILE-CONTROL.
            SELECT CUSTOMER-FILE ASSIGN TO "CUSTOMER.DAT"
                ORGANIZATION IS INDEXED
                ACCESS MODE IS DYNAMIC
                RECORD KEY IS CUSTOMER-ID.
                
            SELECT REPORT-FILE ASSIGN TO "REPORT.DAT"
                ORGANIZATION IS SEQUENTIAL.
                
        DATA DIVISION.
        FILE SECTION.
        FD  CUSTOMER-FILE.
        01  CUSTOMER-RECORD.
            05  CUSTOMER-ID       PIC X(6).
            05  CUSTOMER-NAME     PIC X(30).
            
        FD  REPORT-FILE.
        01  REPORT-RECORD        PIC X(132).
        
        WORKING-STORAGE SECTION.
        01  WS-VARIABLES.
            05  WS-COUNT           PIC 9(4)  VALUE ZEROS.
            05  WS-CUSTOMER-ID     PIC X(6)  VALUE SPACES.
            05  WS-EOF-FLAG        PIC X     VALUE 'N'.
                88  END-OF-FILE              VALUE 'Y'.
                
        EXEC SQL INCLUDE SQLCA END-EXEC.
        
        PROCEDURE DIVISION.
        MAIN-PROCEDURE.
            PERFORM INITIALIZATION
            PERFORM PROCESS-RECORDS UNTIL END-OF-FILE
            PERFORM TERMINATION
            STOP RUN.
            
        INITIALIZATION.
            DISPLAY "INITIALIZING..."
            MOVE ZERO TO WS-COUNT
            OPEN INPUT CUSTOMER-FILE
            IF WS-CUSTOMER-ID = SPACES
                DISPLAY "Invalid customer ID"
            END-IF
            OPEN OUTPUT REPORT-FILE.
            
        PROCESS-RECORDS.
            READ CUSTOMER-FILE
                AT END
                    MOVE 'Y' TO WS-EOF-FLAG
                NOT AT END
                    PERFORM PROCESS-CUSTOMER
            END-READ.
            
        PROCESS-CUSTOMER.
            MOVE CUSTOMER-ID TO WS-CUSTOMER-ID
            
            EXEC SQL
                SELECT COUNT(*) 
                INTO :WS-COUNT
                FROM ORDERS
                WHERE CUSTOMER_ID = :WS-CUSTOMER-ID
            END-EXEC
            
            IF SQLCODE = 0 AND WS-COUNT > 0
                PERFORM PROCESS-ORDERS
            END-IF
            
            WRITE REPORT-RECORD FROM CUSTOMER-RECORD.
            
        PROCESS-ORDERS.
            EXEC SQL
                DECLARE ORDER_CURSOR CURSOR FOR
                SELECT ORDER_ID, ORDER_DATE, ORDER_AMOUNT
                FROM ORDERS
                WHERE CUSTOMER_ID = :WS-CUSTOMER-ID
                ORDER BY ORDER_DATE DESC
            END-EXEC
            
            EXEC SQL
                OPEN ORDER_CURSOR
            END-EXEC
            
            PERFORM UNTIL SQLCODE NOT = 0
                EXEC SQL
                    FETCH ORDER_CURSOR INTO
                        :WS-ORDER-ID,
                        :WS-ORDER-DATE,
                        :WS-ORDER-AMOUNT
                END-EXEC
                
                IF SQLCODE = 0
                    WRITE REPORT-RECORD FROM ORDER-DETAIL
                END-IF
            END-PERFORM
            
            EXEC SQL
                CLOSE ORDER_CURSOR
            END-EXEC.
            
        TERMINATION.
            CLOSE CUSTOMER-FILE
            CLOSE REPORT-FILE
            DISPLAY "Processing complete.".
    """


def test_separation_of_io_and_sql_operations(mixed_io_sql_source):
    """Test that SQL and COBOL IO operations are properly separated."""
    # Create line map (just use sequential numbers for this test)
    line_map = list(range(1, 150))
    
    # Extract IO operations
    io_results = extract_io_files(mixed_io_sql_source, line_map)
    
    # Extract SQL operations
    sql_results = extract_sql_queries(mixed_io_sql_source, line_map)
    
    # Verify IO operations
    io_operations = [(r['operation'], r.get('files', [])) for r in io_results]
    
    # Check that we have the expected IO operations
    # 2 SELECT statements from FILE-CONTROL
    select_statements = [op for op, _ in io_operations if op == 'SELECT']
    assert len(select_statements) == 2, "Should find 2 SELECT statements"
    
    # 2 OPEN statements (INPUT CUSTOMER-FILE and OUTPUT REPORT-FILE)
    open_statements = [(op, files) for op, files in io_operations if op == 'OPEN']
    assert len(open_statements) == 2, "Should find 2 OPEN statements"
    
    # Verify OPEN files and modes
    for _, files in open_statements:
        assert any(f == 'CUSTOMER-FILE' for f in files) or any(f == 'REPORT-FILE' for f in files), \
               "OPEN statements should reference CUSTOMER-FILE or REPORT-FILE"
    
    # Check for READ operation
    read_operations = [op for op, _ in io_operations if op == 'READ']
    assert len(read_operations) == 1, "Should find 1 READ statement"
    
    # Check for WRITE operation
    write_operations = [op for op, _ in io_operations if op == 'WRITE']
    assert len(write_operations) >= 1, "Should find at least 1 WRITE statement"
    
    # 2 CLOSE statements (potentially on one line: "CLOSE CUSTOMER-FILE CLOSE REPORT-FILE")
    close_files = []
    for op, files in io_operations:
        if op == 'CLOSE':
            close_files.extend(files)
    
    assert 'CUSTOMER-FILE' in close_files, "CLOSE statements should include CUSTOMER-FILE"
    assert 'REPORT-FILE' in close_files, "CLOSE statements should include REPORT-FILE"
    
    # Verify SQL operations don't include COBOL IO operations
    for sql_result in sql_results:
        # Check that EXEC SQL OPEN/CLOSE doesn't appear in IO results
        if 'ORDER_CURSOR' in sql_result.get('sql_query', ''):
            operation = sql_result.get('operation', '')
            
            # Find any IO operation with the same line number
            matching_io = [r for r in io_results if r.get('line') == sql_result.get('line')]
            
            # There should be no IO operation at the same line as an SQL cursor operation
            assert len(matching_io) == 0, f"SQL {operation} should not be included in IO operations"


def test_multiline_close_statements():
    """Test handling of multi-line CLOSE statements."""
    source = """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. MULTICLOSE.
        
        DATA DIVISION.
        WORKING-STORAGE SECTION.
        01  WS-EOF-FLAG        PIC X     VALUE 'N'.
            
        PROCEDURE DIVISION.
            PERFORM INITIALIZATION
            PERFORM PROCESS-DATA
            PERFORM TERMINATION
            STOP RUN.
            
        INITIALIZATION.
            OPEN INPUT CUSTOMER-FILE
            OPEN INPUT ORDER-FILE
            OPEN OUTPUT REPORT-FILE.
            
        PROCESS-DATA.
            DISPLAY "Processing data".
            
        TERMINATION.
            CLOSE CUSTOMER-FILE
            CLOSE ORDER-FILE
            CLOSE REPORT-FILE
            DISPLAY "Processing complete.".
    """
    
    # Create line map
    line_map = list(range(1, 50))
    
    # Extract IO operations
    io_results = extract_io_files(source, line_map)
    
    # Check for CLOSE operations
    close_operations = [(r['operation'], r.get('files', [])) for r in io_results if r['operation'] == 'CLOSE']
    
    # We should find either one or three CLOSE operations depending on whether 
    # they're treated as separate statements or merged
    close_files = []
    for _, files in close_operations:
        close_files.extend(files)
    
    # Verify all three files are included
    assert 'CUSTOMER-FILE' in close_files, "CLOSE statements should include CUSTOMER-FILE"
    assert 'ORDER-FILE' in close_files, "CLOSE statements should include ORDER-FILE" 
    assert 'REPORT-FILE' in close_files, "CLOSE statements should include REPORT-FILE"


def test_no_sql_identifiers_in_io_results():
    """Test that SQL identifiers like ORDER_CURSOR are not included in IO results."""
    source = """
        IDENTIFICATION DIVISION.
        PROGRAM-ID. SQLCURSORTEST.
        
        DATA DIVISION.
        WORKING-STORAGE SECTION.
        01  WS-VARIABLES.
            05  WS-COUNT           PIC 9(4) VALUE ZEROS.
            
        PROCEDURE DIVISION.
            OPEN INPUT CUSTOMER-FILE
            
            EXEC SQL
                OPEN ORDER_CURSOR
            END-EXEC
            
            CLOSE CUSTOMER-FILE
            
            EXEC SQL
                CLOSE ORDER_CURSOR
            END-EXEC
            
            STOP RUN.
    """
    
    # Create line map
    line_map = list(range(1, 50))
    
    # Extract IO operations
    io_results = extract_io_files(source, line_map)
    
    # Check all IO operations
    for result in io_results:
        # No SQL identifiers should be present in any IO operation
        if 'files' in result:
            for file_name in result['files']:
                assert 'ORDER_CURSOR' not in file_name, "SQL cursor name should not appear in IO file names"
        
        # Check match text doesn't contain SQL keywords
        assert 'END-EXEC' not in result.get('match', ''), "SQL statements should not be in IO results" 