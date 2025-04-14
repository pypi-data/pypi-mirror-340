"""
Test for COBOL continuation lines and DATA DIVISION copybooks.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.call_extractor import extract_calls
from cobol_parser.extractors.sql_extractor import extract_sql_queries

def test_continuation_lines():
    """Test parsing of COBOL code with continuation lines (hyphen in column 7)."""
    # COBOL code with continuation lines - note the intentional spacing to simulate column 7
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. CONTTEST.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
       01  WS-LONG-FIELD                 PIC X(100) VALUE
      -    "THIS IS A VERY LONG VALUE THAT CONTINUES ON THE NEXT LINE
      -    "AND EVEN CONTINUES FOR MULTIPLE LINES
      -    "UNTIL IT FINALLY ENDS HERE".
      
      PROCEDURE DIVISION.
          EXEC SQL 
              SELECT * 
      -          FROM CUSTOMER 
      -          WHERE CUSTOMER_ID = :WS-ID
      -            AND STATUS = 'ACTIVE'
               END-EXEC.
               
          CALL "SOME-MODULE" 
      -        USING WS-LONG-FIELD
      -              WS-ANOTHER-FIELD
                     .
                     
          COPY CONTINUATION-COPYBOOK.
          
          STOP RUN.
    """
    
    # Copybook with continuation lines
    continuation_copybook = """
       01  COPY-FIELDS.
           05  COPY-ID                  PIC X(10).
           05  COPY-LONG-DESC           PIC X(200) VALUE
      -        "THIS IS A LONG DESCRIPTION IN THE COPYBOOK
      -        "THAT ALSO CONTINUES ACROSS LINES
      -        "FOR DEMONSTRATION PURPOSES".
           
       EXEC SQL
           INSERT INTO AUDIT_LOG
      -        (LOG_ID, LOG_TIME, LOG_DESC)
           VALUES
      -        (:COPY-ID, CURRENT TIMESTAMP, :COPY-LONG-DESC)
       END-EXEC.
    """
    
    # Create a resolver
    def copybook_resolver(name):
        if name == "CONTINUATION-COPYBOOK":
            return continuation_copybook
        return None
    
    # Create a simple line map
    line_map = list(range(1, 100))
    
    # Test expansion
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Verify copybook was expanded
    assert "COPY-FIELDS" in expanded_source
    assert "COPY-LONG-DESC" in expanded_source
    
    # Extract and check SQL statements
    sql_results = extract_sql_queries(expanded_source, line_map)
    assert len(sql_results) >= 2  # Should find both the main program SQL and copybook SQL
    
    # Verify we have both SQL operations (SELECT and INSERT)
    sql_operations = [sql['operation'] for sql in sql_results]
    assert "SELECT" in sql_operations
    assert "INSERT" in sql_operations
    
    # Verify tables
    tables = []
    for result in sql_results:
        if 'tables' in result:
            tables.extend(result['tables'])
    assert "CUSTOMER" in tables
    assert "AUDIT_LOG" in tables


def test_data_division_copybooks():
    """Test copybooks in the DATA DIVISION with complex data structures."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. DATADIV.
      
      ENVIRONMENT DIVISION.
      INPUT-OUTPUT SECTION.
      FILE-CONTROL.
          SELECT CUSTOMER-FILE ASSIGN TO CUSTFILE
          ORGANIZATION IS INDEXED
          ACCESS IS RANDOM
          RECORD KEY IS CUST-ID.
      
      DATA DIVISION.
      FILE SECTION.
      FD  CUSTOMER-FILE
          LABEL RECORDS ARE STANDARD.
      COPY CUSTOMER-RECORD.
      
      WORKING-STORAGE SECTION.
      COPY CONSTANTS-COPYBOOK.
      COPY VARIABLES-COPYBOOK.
      
      01  WS-CUSTOMER-RECORD         PIC X(500).
      
      PROCEDURE DIVISION.
          OPEN INPUT CUSTOMER-FILE
          
          MOVE CUSTOMER-ID-CONSTANT TO CUST-ID
          
          READ CUSTOMER-FILE
              INVALID KEY
                  DISPLAY "Customer not found"
              NOT INVALID KEY
                  PERFORM PROCESS-CUSTOMER
          END-READ
          
          CLOSE CUSTOMER-FILE
          STOP RUN.
      
      PROCESS-CUSTOMER.
          DISPLAY "Customer found: " CUST-NAME
          CALL "CUSTOMER-PROCESSOR" USING WS-CUSTOMER-RECORD
          EXEC SQL
              UPDATE CUSTOMER_TABLE
              SET LAST_ACCESS = CURRENT DATE
              WHERE CUST_ID = :CUST-ID
          END-EXEC.
    """
    
    customer_record = """
      01  CUSTOMER-RECORD.
          05  CUST-ID                    PIC X(10).
          05  CUST-NAME                  PIC X(50).
          05  CUST-ADDRESS.
              10  CUST-STREET            PIC X(50).
              10  CUST-CITY              PIC X(30).
              10  CUST-STATE             PIC X(2).
              10  CUST-ZIP               PIC X(10).
          05  CUST-CONTACT.
              10  CUST-PHONE             PIC X(15).
              10  CUST-EMAIL             PIC X(100).
          05  CUST-ACCOUNT-INFO.
              10  CUST-ACCT-NUM          PIC X(20).
              10  CUST-ACCT-TYPE         PIC X(2).
              10  CUST-ACCT-BALANCE      PIC S9(9)V99 COMP-3.
              10  CUST-ACCT-OPEN-DATE    PIC X(10).
          05  CUST-NOTES                 PIC X(500).
    """
    
    constants_copybook = """
      01  CONSTANTS.
          05  CUSTOMER-ID-CONSTANT       PIC X(10) VALUE "CUST001234".
          05  MAX-RECORDS                PIC 9(5)  VALUE 10000.
          05  COMPANY-NAME               PIC X(30) VALUE "ACME CORPORATION".
          05  COPYRIGHT-NOTICE           PIC X(50) VALUE "COPYRIGHT (C) 2023 ACME CORPORATION".
    """
    
    variables_copybook = """
      01  PROGRAM-VARIABLES.
          05  WS-EOF-FLAG                PIC X     VALUE 'N'.
              88  END-OF-FILE                       VALUE 'Y'.
              88  MORE-RECORDS                      VALUE 'N'.
          05  WS-COUNT                   PIC 9(5)  VALUE ZERO.
          05  WS-TOTAL-BALANCE           PIC S9(9)V99 COMP-3 VALUE ZERO.
    """
    
    def copybook_resolver(name):
        if name == "CUSTOMER-RECORD":
            return customer_record
        elif name == "CONSTANTS-COPYBOOK":
            return constants_copybook
        elif name == "VARIABLES-COPYBOOK":
            return variables_copybook
        return None
    
    line_map = list(range(1, 200))
    
    # Expand the source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Print for debugging
    print("\nExpanded source contains CUSTOMER-RECORD:", "CUSTOMER-RECORD" in expanded_source)
    print("Expanded source contains CUSTOMER-RECORD uppercase:", "CUSTOMER-RECORD" in expanded_source.upper())
    
    # Verify all copybooks were included
    assert "CUSTOMER-RECORD" in expanded_source
    assert "CONSTANTS" in expanded_source
    assert "PROGRAM-VARIABLES" in expanded_source
    
    # Check for specific complex data structures
    assert "CUST-ADDRESS" in expanded_source
    assert "CUST-ACCOUNT-INFO" in expanded_source
    
    # Extract calls
    call_results = extract_calls(expanded_source, line_map)
    print("\nCall results:", call_results)
    
    assert len(call_results) == 1
    assert call_results[0]['program_name'] == "CUSTOMER-PROCESSOR"
    assert "WS-CUSTOMER-RECORD" in str(call_results[0]['parameters'])
    
    # Extract SQL
    sql_results = extract_sql_queries(expanded_source, line_map)
    assert len(sql_results) == 1
    assert sql_results[0]['operation'] == "UPDATE"
    assert "CUSTOMER_TABLE" in sql_results[0]['tables'] 