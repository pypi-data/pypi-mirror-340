"""
Test for CICS commands and complex control structures in COBOL.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.call_extractor import extract_calls
from cobol_parser.extractors.perform_extractor import extract_performs

def test_cics_commands():
    """Test extraction with CICS commands in copybooks."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. CICSPROG.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-COMMAREA.
          05  WS-REQUEST-TYPE            PIC X(4).
          05  WS-ACCOUNT-NUM             PIC X(10).
          05  WS-RESPONSE-CODE           PIC 9(2).
          
      PROCEDURE DIVISION.
          COPY CICS-HEADER-COPYBOOK.
          
          EVALUATE WS-REQUEST-TYPE
              WHEN 'INQUIRE'
                  PERFORM INQUIRE-PROCESS
              WHEN 'UPDATE'
                  PERFORM UPDATE-PROCESS
              WHEN OTHER
                  MOVE 99 TO WS-RESPONSE-CODE
          END-EVALUATE.
          
          COPY CICS-FOOTER-COPYBOOK.
          
          GOBACK.
          
      INQUIRE-PROCESS.
          EXEC CICS READ
              DATASET('ACCTFILE')
              INTO(WS-COMMAREA)
              RIDFLD(WS-ACCOUNT-NUM)
              RESP(WS-RESPONSE-CODE)
          END-EXEC.
          
      UPDATE-PROCESS.
          EXEC CICS LINK
              PROGRAM('ACCTUPDT')
              COMMAREA(WS-COMMAREA)
              LENGTH(80)
              RESP(WS-RESPONSE-CODE)
          END-EXEC.
    """
    
    cics_header = """
      * Standard CICS header
      EXEC CICS HANDLE CONDITION
          ERROR(GENERAL-ERROR)
          NOTFND(RECORD-NOT-FOUND)
          MAPFAIL(MAP-FAILURE)
      END-EXEC.
      
      EXEC CICS RECEIVE MAP('ACCTMAP')
          MAPSET('ACCTSET')
          INTO(WS-COMMAREA)
          RESP(WS-RESPONSE-CODE)
      END-EXEC.
    """
    
    cics_footer = """
      * Standard CICS footer
      EVALUATE WS-RESPONSE-CODE
          WHEN 0
              EXEC CICS SEND MAP('ACCTMAP')
                  MAPSET('ACCTSET')
                  FROM(WS-COMMAREA)
                  ERASE
              END-EXEC
          WHEN OTHER
              EXEC CICS SEND TEXT
                  FROM(ERROR-MESSAGE)
                  LENGTH(80)
                  ERASE
              END-EXEC
      END-EVALUATE.
      
      GENERAL-ERROR.
          MOVE 'General Error Occurred' TO ERROR-MESSAGE.
          EXEC CICS RETURN END-EXEC.
          
      RECORD-NOT-FOUND.
          MOVE 'Record Not Found' TO ERROR-MESSAGE.
          EXEC CICS RETURN END-EXEC.
          
      MAP-FAILURE.
          MOVE 'Map Failure' TO ERROR-MESSAGE.
          EXEC CICS RETURN END-EXEC.
    """
    
    def copybook_resolver(name):
        if name == "CICS-HEADER-COPYBOOK":
            return cics_header
        elif name == "CICS-FOOTER-COPYBOOK":
            return cics_footer
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Check for expanded CICS commands
    assert "EXEC CICS HANDLE CONDITION" in expanded_source
    assert "EXEC CICS RECEIVE MAP" in expanded_source
    assert "EXEC CICS SEND MAP" in expanded_source
    assert "EXEC CICS RETURN" in expanded_source
    
    # Check for error handlers
    assert "GENERAL-ERROR" in expanded_source
    assert "RECORD-NOT-FOUND" in expanded_source
    assert "MAP-FAILURE" in expanded_source


def test_complex_control_structures():
    """Test with complex control structures like EVALUATE and nested IFs."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. CONTROLTEST.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-VARIABLES.
          05  WS-CODE                    PIC X(2).
          05  WS-STATUS                  PIC X(1).
          05  WS-AMOUNT                  PIC 9(7)V99.
          05  WS-COUNTER                 PIC 9(5) VALUE ZEROS.
          05  WS-RESULT                  PIC X(20) VALUE SPACES.
          
      PROCEDURE DIVISION.
          PERFORM INITIALIZE-PROCESS
          PERFORM MAIN-PROCESS UNTIL WS-COUNTER > 100
          PERFORM END-PROCESS
          STOP RUN.
          
      INITIALIZE-PROCESS.
          MOVE ZEROS TO WS-COUNTER
          MOVE SPACES TO WS-RESULT
          COPY CONTROL-INIT-COPYBOOK.
          
      MAIN-PROCESS.
          ADD 1 TO WS-COUNTER
          COPY CONTROL-MAIN-COPYBOOK.
          
      END-PROCESS.
          COPY CONTROL-END-COPYBOOK.
    """
    
    control_init = """
      * Complex initialization with EVALUATE
      EVALUATE TRUE
          WHEN WS-CODE = '01'
              MOVE 'ACTIVE' TO WS-RESULT
              PERFORM PROCESS-ACTIVE-ACCOUNT
          WHEN WS-CODE = '02' AND WS-STATUS = 'A'
              MOVE 'PENDING' TO WS-RESULT
          WHEN WS-CODE = '03' OR WS-CODE = '04'
              MOVE 'SUSPENDED' TO WS-RESULT
          WHEN OTHER
              MOVE 'UNKNOWN' TO WS-RESULT
      END-EVALUATE.
      
      PROCESS-ACTIVE-ACCOUNT.
          IF WS-AMOUNT > 1000.00
              CALL "HIGH-BALANCE-ROUTINE" USING WS-AMOUNT
          ELSE
              CALL "STANDARD-ROUTINE" USING WS-AMOUNT
          END-IF.
    """
    
    control_main = """
      * Complex nested IF structure
      IF WS-COUNTER < 50
          IF WS-STATUS = 'A'
              PERFORM PROCESS-A
              IF WS-AMOUNT > 500.00
                  CALL "PROCESS-HIGH" USING WS-AMOUNT
              ELSE
                  CALL "PROCESS-LOW" USING WS-AMOUNT
              END-IF
          ELSE
              PERFORM PROCESS-B
          END-IF
      ELSE
          EVALUATE WS-STATUS
              WHEN 'A'
                  PERFORM PROCESS-A-HIGH
              WHEN 'B'
                  PERFORM PROCESS-B-HIGH
              WHEN 'C'
                  CONTINUE
              WHEN OTHER
                  PERFORM PROCESS-DEFAULT
          END-EVALUATE
      END-IF.
      
      PROCESS-A.
          DISPLAY "Process A".
          
      PROCESS-B.
          DISPLAY "Process B".
          
      PROCESS-A-HIGH.
          DISPLAY "Process A High".
          
      PROCESS-B-HIGH.
          DISPLAY "Process B High".
          
      PROCESS-DEFAULT.
          DISPLAY "Process Default".
    """
    
    control_end = """
      * Combining EVALUATE with nested IF
      EVALUATE WS-CODE
          WHEN '01'
              CALL "FINALIZE-01" USING WS-RESULT
              
          WHEN '02'
              IF WS-STATUS = 'A'
                  IF WS-AMOUNT > 1000.00
                      CALL "FINALIZE-02-HIGH" USING WS-RESULT, WS-AMOUNT
                  ELSE
                      CALL "FINALIZE-02-LOW" USING WS-RESULT, WS-AMOUNT
                  END-IF
              ELSE
                  CALL "FINALIZE-02-OTHER" USING WS-RESULT
              END-IF
              
          WHEN '03' THRU '05'
              CALL "FINALIZE-03-05" USING WS-RESULT
              
          WHEN OTHER
              CALL "FINALIZE-DEFAULT" USING WS-RESULT
      END-EVALUATE.
    """
    
    def copybook_resolver(name):
        if name == "CONTROL-INIT-COPYBOOK":
            return control_init
        elif name == "CONTROL-MAIN-COPYBOOK":
            return control_main
        elif name == "CONTROL-END-COPYBOOK":
            return control_end
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Check for complex control structures
    assert "EVALUATE TRUE" in expanded_source
    assert "EVALUATE WS-STATUS" in expanded_source
    assert "EVALUATE WS-CODE" in expanded_source
    
    # Extract and check PERFORMs
    perform_results = extract_performs(expanded_source, line_map)
    perform_procs = [p.get('procedure') for p in perform_results if p.get('type') == 'explicit']
    
    # Check for performs from main and copybooks
    assert "INITIALIZE-PROCESS" in perform_procs
    assert "MAIN-PROCESS" in perform_procs
    assert "END-PROCESS" in perform_procs
    assert "PROCESS-ACTIVE-ACCOUNT" in perform_procs
    assert "PROCESS-A" in perform_procs
    assert "PROCESS-B" in perform_procs
    
    # Extract and check CALLs
    call_results = extract_calls(expanded_source, line_map)
    call_programs = [call['program_name'] for call in call_results]
    
    # Check for calls from copybooks
    assert "HIGH-BALANCE-ROUTINE" in call_programs
    assert "STANDARD-ROUTINE" in call_programs
    assert "PROCESS-HIGH" in call_programs
    assert "PROCESS-LOW" in call_programs
    assert "FINALIZE-01" in call_programs
    assert "FINALIZE-02-HIGH" in call_programs 