"""
Test for complex SQL and DB2 patterns in COBOL programs.
"""
import pytest

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.sql_extractor import extract_sql_queries

def test_complex_sql_patterns():
    """Test extraction of complex SQL statements including joins, subqueries, and special DB2 syntax."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. SQLTEST.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-VARIABLES.
          05  WS-CUSTOMER-ID             PIC X(10).
          05  WS-ORDER-ID                PIC X(8).
          05  WS-DATE                    PIC X(10).
          05  WS-STATUS                  PIC X(1).
          05  WS-AMOUNT                  PIC S9(9)V99 COMP-3.
          
      EXEC SQL INCLUDE SQLCA END-EXEC.
      
      PROCEDURE DIVISION.
          MOVE '1000000001' TO WS-CUSTOMER-ID
          MOVE '20230101' TO WS-DATE
          
          EXEC SQL
              SELECT O.ORDER_ID, O.ORDER_DATE, O.TOTAL_AMOUNT
              INTO :WS-ORDER-ID, :WS-DATE, :WS-AMOUNT
              FROM ORDERS O
              WHERE O.CUSTOMER_ID = :WS-CUSTOMER-ID
              AND O.ORDER_DATE = (
                  SELECT MAX(ORDER_DATE)
                  FROM ORDERS
                  WHERE CUSTOMER_ID = :WS-CUSTOMER-ID
              )
          END-EXEC
          
          EVALUATE SQLCODE
              WHEN 0
                  PERFORM PROCESS-ORDER
              WHEN 100
                  DISPLAY "No orders found"
              WHEN OTHER
                  DISPLAY "SQL Error: " SQLCODE
          END-EVALUATE
          
          COPY SQL-OPERATIONS-COPYBOOK.
          
          STOP RUN.
          
      PROCESS-ORDER.
          DISPLAY "Order found: " WS-ORDER-ID
          DISPLAY "Order date: " WS-DATE
          DISPLAY "Order amount: " WS-AMOUNT.
    """
    
    sql_operations = """
      * Complex SQL operations
      
      * Update with join
      EXEC SQL
          UPDATE ORDER_ITEMS OI
          SET OI.STATUS = 'S'
          FROM ORDER_ITEMS OI
          JOIN ORDERS O ON OI.ORDER_ID = O.ORDER_ID
          WHERE O.CUSTOMER_ID = :WS-CUSTOMER-ID
          AND O.ORDER_DATE >= :WS-DATE
      END-EXEC.
      
      * Insert with select
      EXEC SQL
          INSERT INTO ORDER_HISTORY
          (ORDER_ID, CUSTOMER_ID, ORDER_DATE, AMOUNT, PROCESS_DATE)
          SELECT ORDER_ID, CUSTOMER_ID, ORDER_DATE, TOTAL_AMOUNT, CURRENT DATE
          FROM ORDERS
          WHERE CUSTOMER_ID = :WS-CUSTOMER-ID
      END-EXEC.
      
      * Delete with exists subquery
      EXEC SQL
          DELETE FROM TEMP_ORDERS TO
          WHERE EXISTS (
              SELECT 1 
              FROM ORDERS O
              WHERE O.ORDER_ID = TO.ORDER_ID
              AND O.PROCESS_STATUS = 'C'
          )
      END-EXEC.
      
      * Complex query with GROUP BY, HAVING, and ORDER BY
      EXEC SQL
          SELECT CUSTOMER_ID, 
                 COUNT(*) AS ORDER_COUNT,
                 SUM(TOTAL_AMOUNT) AS TOTAL_SPENT
          INTO :WS-CUSTOMER-ID, :SQL-COUNT, :WS-AMOUNT
          FROM ORDERS
          WHERE ORDER_DATE BETWEEN :WS-DATE - 1 YEAR AND :WS-DATE
          GROUP BY CUSTOMER_ID
          HAVING COUNT(*) > 5
          ORDER BY SUM(TOTAL_AMOUNT) DESC
          FETCH FIRST 10 ROWS ONLY
      END-EXEC.
      
      * DB2-specific syntax with WITH clause (common table expression)
      EXEC SQL
          WITH RECENT_ORDERS AS (
              SELECT CUSTOMER_ID, ORDER_ID, ORDER_DATE, TOTAL_AMOUNT
              FROM ORDERS
              WHERE ORDER_DATE >= :WS-DATE - 90 DAYS
          )
          SELECT COUNT(*), SUM(TOTAL_AMOUNT)
          INTO :SQL-COUNT, :WS-AMOUNT
          FROM RECENT_ORDERS
          WHERE CUSTOMER_ID = :WS-CUSTOMER-ID
      END-EXEC.
    """
    
    def copybook_resolver(name):
        if name == "SQL-OPERATIONS-COPYBOOK":
            return sql_operations
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Extract SQL statements
    sql_results = extract_sql_queries(expanded_source, line_map)
    
    # Verify that we have multiple SQL statements
    assert len(sql_results) >= 6  # Main + 5 from copybook
    
    # Check SQL operations
    operations = [r['operation'] for r in sql_results]
    assert "SELECT" in operations
    assert "UPDATE" in operations
    assert "INSERT" in operations
    assert "DELETE" in operations
    
    # Check for tables
    tables = []
    for result in sql_results:
        if 'tables' in result:
            tables.extend(result['tables'])
    
    # Verify we found the main tables
    assert "ORDERS" in tables
    assert "ORDER_ITEMS" in tables
    assert "ORDER_HISTORY" in tables
    assert "TEMP_ORDERS" in tables
    
    # Check for complex SQL features
    found_subquery = False
    found_join = False
    found_group_by = False
    found_with_clause = False
    
    for result in sql_results:
        sql_query = result.get('sql_query', '')
        
        # Check for JOIN syntax
        if " JOIN " in sql_query:
            found_join = True
            
        # Check for subquery
        if "SELECT" in sql_query and "(" in sql_query and "SELECT" in sql_query.split("(")[1]:
            found_subquery = True
            
        # Check for GROUP BY
        if "GROUP BY" in sql_query:
            found_group_by = True
            
        # Check for WITH clause
        if "WITH " in sql_query and " AS (" in sql_query:
            found_with_clause = True
    
    # Assert we found complex SQL features
    assert found_subquery, "Should find subqueries"
    assert found_join, "Should find JOIN operations"
    assert found_group_by, "Should find GROUP BY clauses"
    assert found_with_clause, "Should find WITH clauses"


def test_dynamic_sql():
    """Test extraction of dynamic SQL in COBOL programs."""
    main_program = """
      IDENTIFICATION DIVISION.
      PROGRAM-ID. DYNSQL.
      
      DATA DIVISION.
      WORKING-STORAGE SECTION.
      01  WS-VARIABLES.
          05  WS-TABLE-NAME              PIC X(30) VALUE 'CUSTOMERS'.
          05  WS-COLUMN-NAMES            PIC X(50) VALUE 'CUSTOMER_ID, NAME, STATUS'.
          05  WS-WHERE-CLAUSE            PIC X(50) VALUE 'STATUS = ''A'''.
          05  WS-SQL-STATEMENT           PIC X(200).
          
      EXEC SQL INCLUDE SQLCA END-EXEC.
      
      PROCEDURE DIVISION.
          * Build dynamic SQL statement
          STRING 'SELECT ' DELIMITED BY SIZE
                 WS-COLUMN-NAMES DELIMITED BY SPACE
                 ' FROM ' DELIMITED BY SIZE
                 WS-TABLE-NAME DELIMITED BY SPACE
                 ' WHERE ' DELIMITED BY SIZE
                 WS-WHERE-CLAUSE DELIMITED BY SIZE
                 INTO WS-SQL-STATEMENT
          END-STRING
          
          DISPLAY "Executing: " WS-SQL-STATEMENT
          
          EXEC SQL
              PREPARE STMT1 FROM :WS-SQL-STATEMENT
          END-EXEC
          
          EXEC SQL
              DECLARE C1 CURSOR FOR STMT1
          END-EXEC
          
          EXEC SQL
              OPEN C1
          END-EXEC
          
          PERFORM PROCESS-CURSOR
          
          EXEC SQL
              CLOSE C1
          END-EXEC
          
          COPY DYNAMIC-SQL-COPYBOOK.
          
          STOP RUN.
          
      PROCESS-CURSOR.
          DISPLAY "Processing cursor".
    """
    
    dynamic_sql = """
      * More dynamic SQL operations
      
      * Execute immediate with parameter markers
      MOVE 'UPDATE CUSTOMERS SET STATUS = ? WHERE CUSTOMER_ID = ?' TO WS-SQL-STATEMENT
      
      EXEC SQL
          EXECUTE IMMEDIATE :WS-SQL-STATEMENT
          USING 'I', :WS-CUSTOMER-ID
      END-EXEC.
      
      * Dynamic INSERT
      MOVE 'INSERT INTO AUDIT_LOG(USER_ID, ACTION, TABLE_NAME, ACTION_DATE) VALUES(?, ?, ?, CURRENT TIMESTAMP)' 
           TO WS-SQL-STATEMENT
      
      EXEC SQL
          PREPARE STMT2 FROM :WS-SQL-STATEMENT
      END-EXEC
      
      EXEC SQL
          EXECUTE STMT2 USING 'SYSTEM', 'UPDATE', :WS-TABLE-NAME
      END-EXEC.
      
      * Dynamic CREATE TABLE
      MOVE 'CREATE TABLE TEMP_' TO WS-SQL-STATEMENT
      STRING WS-SQL-STATEMENT DELIMITED BY SIZE
             WS-TABLE-NAME DELIMITED BY SPACE
             ' AS SELECT * FROM ' DELIMITED BY SIZE
             WS-TABLE-NAME DELIMITED BY SPACE
             ' WITH NO DATA' DELIMITED BY SIZE
             INTO WS-SQL-STATEMENT
      END-STRING
      
      EXEC SQL
          EXECUTE IMMEDIATE :WS-SQL-STATEMENT
      END-EXEC.
    """
    
    def copybook_resolver(name):
        if name == "DYNAMIC-SQL-COPYBOOK":
            return dynamic_sql
        return None
    
    line_map = list(range(1, 200))
    
    # Expand source
    expanded_source = expand_copybooks(main_program, copybook_resolver)
    
    # Extract SQL statements
    sql_results = extract_sql_queries(expanded_source, line_map)
    
    # Check for PREPARE/EXECUTE statements
    prepare_statements = [r for r in sql_results if 'PREPARE' in r.get('sql_query', '')]
    execute_statements = [r for r in sql_results if 'EXECUTE' in r.get('sql_query', '')]
    
    assert len(prepare_statements) >= 2  # At least 2 PREPARE statements
    assert len(execute_statements) >= 2  # At least 2 EXECUTE statements
    
    # Check for cursor operations
    cursor_operations = []
    for result in sql_results:
        sql_query = result.get('sql_query', '')
        if 'DECLARE' in sql_query and 'CURSOR' in sql_query:
            cursor_operations.append('DECLARE')
        elif 'OPEN' in sql_query:
            cursor_operations.append('OPEN')
        elif 'CLOSE' in sql_query:
            cursor_operations.append('CLOSE')
    
    # Complete set of cursor operations
    assert 'DECLARE' in cursor_operations
    assert 'OPEN' in cursor_operations
    assert 'CLOSE' in cursor_operations 