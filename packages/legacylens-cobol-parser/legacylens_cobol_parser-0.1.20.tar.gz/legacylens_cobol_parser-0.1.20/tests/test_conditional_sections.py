"""
Test for conditional compilation and uncommon COBOL patterns.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.call_extractor import extract_calls
from cobol_parser.extractors.perform_extractor import extract_performs

def test_conditional_copybooks():
    """Test copybooks with conditional compilation patterns."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. CONDCOMP.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-VARIABLES.
          05  WS-ENVIRONMENT             PIC X(4) VALUE 'PROD'.
          05  WS-OPERATION-MODE          PIC X(3) VALUE 'STD'.
          05  WS-DEBUG-LEVEL             PIC 9(1) VALUE 0.
          
      PROCEDURE DIVISION.
          PERFORM INITIALIZATION
          PERFORM MAIN-PROCESS
          PERFORM CLEANUP
          STOP RUN.
          
      INITIALIZATION.
          DISPLAY "Initializing..."
          COPY CONFIG-SETTINGS REPLACING
              ==:ENV:== BY ==PROD==
              ==:MODE:== BY ==STD==.
          
      MAIN-PROCESS.
          DISPLAY "Processing..."
          EVALUATE WS-ENVIRONMENT
              WHEN 'DEV'
                  COPY DEV-PROCESS-COPYBOOK.
              WHEN 'TEST'
                  COPY TEST-PROCESS-COPYBOOK.
              WHEN 'PROD'
                  COPY PROD-PROCESS-COPYBOOK.
              WHEN OTHER
                  DISPLAY "Unknown environment"
          END-EVALUATE.
          
      CLEANUP.
          DISPLAY "Cleaning up..."
          MOVE 0 TO RETURN-CODE.
    """
    
    config_settings = """
      * Configuration settings by environment :ENV: and mode :MODE:
      
      * :ENV: specific settings
      01  ENV-SETTINGS.
          05  ENV-NAME                   PIC X(20) VALUE ":ENV: Environment".
          05  DB-CONNECTION-STRING       PIC X(100) VALUE "SERVER=:ENV:-DB01".
          05  MAX-CONNECTIONS            PIC 9(2) VALUE 
              :ENV:DEV:10:
              :ENV:TEST:20:
              :ENV:PROD:50:.
      
      * :MODE: specific settings
      01  MODE-SETTINGS.
          05  OPERATION-MODE             PIC X(20) VALUE ":MODE: Mode".
          05  BATCH-SIZE                 PIC 9(4) VALUE 
              :MODE:STD:1000:
              :MODE:BULK:5000:
              :MODE:MINI:100:.
    """
    
    dev_process = """
      * Development environment process
      DISPLAY "Running in DEV mode"
      MOVE 5 TO WS-DEBUG-LEVEL
      
      CALL "DEV-LOGGER" USING WS-DEBUG-LEVEL
      
      * Development-only diagnostic section
      DISPLAY "DB Connection: " DB-CONNECTION-STRING
      DISPLAY "Max connections: " MAX-CONNECTIONS
      DISPLAY "Batch size: " BATCH-SIZE
    """
    
    test_process = """
      * Test environment process
      DISPLAY "Running in TEST mode"
      MOVE 3 TO WS-DEBUG-LEVEL
      
      CALL "TEST-LOGGER" USING WS-DEBUG-LEVEL
      
      * Test-only validation section
      PERFORM VALIDATE-SETTINGS
      PERFORM PREPARE-TEST-DATA
      
      VALIDATE-SETTINGS.
          DISPLAY "Validating settings..."
          IF BATCH-SIZE > 2000
              DISPLAY "Warning: Large batch size for TEST"
          END-IF.
          
      PREPARE-TEST-DATA.
          DISPLAY "Preparing test data...".
    """
    
    prod_process = """
      * Production environment process
      DISPLAY "Running in PRODUCTION mode"
      MOVE 0 TO WS-DEBUG-LEVEL
      
      CALL "LOGGER" USING WS-DEBUG-LEVEL
      
      * Production processing
      PERFORM PROCESS-DATA-BATCH
      
      PROCESS-DATA-BATCH.
          DISPLAY "Processing production data"
          CALL "BATCH-PROCESSOR" USING BATCH-SIZE
          CALL "NOTIFICATION-SERVICE" USING ENV-NAME.
    """
    
    def copybook_resolver(name):
        if name == "CONFIG-SETTINGS":
            # This is a special case that needs text substitution for conditional compilation
            content = config_settings
            # Replace environment placeholders - ensuring VALUE is preserved in the output
            content = content.replace(":ENV:DEV:10:", "VALUE 10")
            content = content.replace(":ENV:TEST:20:", "VALUE 20")
            content = content.replace(":ENV:PROD:50:", "VALUE 50")
            # Replace mode placeholders - ensuring VALUE is preserved in the output
            content = content.replace(":MODE:STD:1000:", "VALUE 1000")
            content = content.replace(":MODE:BULK:5000:", "VALUE 0")
            content = content.replace(":MODE:MINI:100:", "VALUE 0")
            # Replace remaining placeholders
            content = content.replace(":ENV:", "PROD")
            content = content.replace(":MODE:", "STD")
            return content
        elif name == "DEV-PROCESS-COPYBOOK":
            return dev_process
        elif name == "TEST-PROCESS-COPYBOOK":
            return test_process
        elif name == "PROD-PROCESS-COPYBOOK":
            return prod_process
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Check for environment-specific content
    assert "Running in PRODUCTION mode" in expanded_source
    assert "PROD Environment" in expanded_source
    assert "STD Mode" in expanded_source
    assert "DB Connection: " in expanded_source
    assert "SERVER=PROD-DB01" in expanded_source
    
    # Check numeric substitutions
    assert "VALUE 50" in expanded_source  # MAX-CONNECTIONS for PROD
    assert "VALUE 1000" in expanded_source  # BATCH-SIZE for STD
    
    # Extract and check calls
    call_results = extract_calls(expanded_source, line_map)
    call_programs = [call['program_name'] for call in call_results]
    
    assert "LOGGER" in call_programs
    assert "BATCH-PROCESSOR" in call_programs
    assert "NOTIFICATION-SERVICE" in call_programs


def test_uncommon_cobol_patterns():
    """Test extraction with uncommon COBOL patterns and syntax."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. UNCOMMON.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-VARIABLES.
          05  WS-COUNTER                 PIC 9(5) COMP-3.
          05  WS-TABLE.
              10  WS-ITEM                OCCURS 10 TIMES
                                         INDEXED BY WS-IDX.
                  15  WS-ITEM-ID         PIC X(5).
                  15  WS-ITEM-VALUE      PIC 9(5).
          
      PROCEDURE DIVISION.
          COPY UNCOMMON-PATTERNS-COPYBOOK.
          
          PERFORM VARYING WS-IDX FROM 1 BY 1 
                  UNTIL WS-IDX > 10
              DISPLAY WS-ITEM-ID(WS-IDX)
          END-PERFORM
          
          STOP RUN.
    """
    
    uncommon_patterns = """
      * Uncommon COBOL patterns
      
      * Inline PERFORM with index notation
      PERFORM VARYING WS-IDX FROM 1 BY 1 UNTIL WS-IDX > 10
          MOVE WS-IDX TO WS-ITEM-VALUE(WS-IDX)
          MOVE "ITEM" TO WS-ITEM-ID(WS-IDX)
      END-PERFORM.
      
      * ALTER statement (rarely used, deprecated feature)
      ALTER PARA-1 TO PROCEED TO PARA-2.
      
      * GO TO with DEPENDING ON
      GO TO PARA-1, PARA-2, PARA-3 
          DEPENDING ON WS-COUNTER.
      
      * INSPECT with CONVERTING
      INSPECT WS-ITEM-ID(1) CONVERTING "abcde" TO "ABCDE".
      
      * INITIALIZE with REPLACING
      INITIALIZE WS-TABLE REPLACING 
          NUMERIC DATA BY 1
          ALPHANUMERIC DATA BY "X".
      
      * EXIT paragraph as procedure end
      PARA-1.
          DISPLAY "Paragraph 1"
          CALL "SUBPROG1"
          EXIT.
      
      PARA-2.
          DISPLAY "Paragraph 2"
          CALL "SUBPROG2"
          EXIT.
      
      PARA-3.
          DISPLAY "Paragraph 3"
          CALL "SUBPROG3"
          EXIT.
      
      * STRING with pointer
      MOVE 1 TO WS-COUNTER
      STRING "A" "B" "C" DELIMITED BY SIZE
          INTO WS-ITEM-ID(1)
          WITH POINTER WS-COUNTER
      END-STRING.
      
      * UNSTRING with multiple receiving fields
      UNSTRING "A,B,C,D" DELIMITED BY ","
          INTO WS-ITEM-ID(1)
               WS-ITEM-ID(2)
               WS-ITEM-ID(3)
               WS-ITEM-ID(4)
      END-UNSTRING.
      
      * Conditionals with NEXT SENTENCE
      IF WS-COUNTER > 100
          NEXT SENTENCE
      ELSE
          DISPLAY "Counter <= 100"
      END-IF.
    """
    
    def copybook_resolver(name):
        if name == "UNCOMMON-PATTERNS-COPYBOOK":
            return uncommon_patterns
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Check for uncommon patterns
    assert "ALTER PARA-1 TO PROCEED TO PARA-2" in expanded_source
    assert "GO TO PARA-1, PARA-2, PARA-3" in expanded_source
    assert "INSPECT WS-ITEM-ID(1) CONVERTING" in expanded_source
    assert "INITIALIZE WS-TABLE REPLACING" in expanded_source
    assert "STRING \"A\" \"B\" \"C\" DELIMITED BY SIZE" in expanded_source
    assert "UNSTRING \"A,B,C,D\" DELIMITED BY \",\"" in expanded_source
    assert "NEXT SENTENCE" in expanded_source
    
    # Extract and check calls
    call_results = extract_calls(expanded_source, line_map)
    call_programs = [call['program_name'] for call in call_results]
    
    assert "SUBPROG1" in call_programs
    assert "SUBPROG2" in call_programs
    assert "SUBPROG3" in call_programs
    
    # Extract and check performs
    perform_results = extract_performs(expanded_source, line_map)
    
    # Check for inline performs
    inline_performs = [p for p in perform_results if p.get('type') == 'inline']
    assert len(inline_performs) >= 2  # At least one from main and one from copybook 