"""
Extractor for embedded SQL statements in COBOL programs.
"""
import re
from typing import List, Dict, Any

from cobol_parser.extractors.base_extractor import BaseExtractor


def extract_sql_queries(source: str, line_map: List[int]) -> List[Dict[str, Any]]:
    """
    Extract embedded SQL statements from COBOL source code.
    
    This function identifies:
    - EXEC SQL / END-EXEC blocks
    - Various SQL operations (SELECT, INSERT, UPDATE, DELETE)
    - Table names and operations
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        
    Returns:
        List of dictionaries with information about each SQL query.
    """
    # Pattern for EXEC SQL blocks
    sql_pattern = re.compile(
        r'EXEC\s+SQL\s+'                      # EXEC SQL
        r'(?P<query>.*?)'                     # Query content (non-greedy)
        r'(?:END-EXEC|END-EXEC\.)',           # END-EXEC or END-EXEC.
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all SQL blocks
    results = BaseExtractor.find_matches(sql_pattern, source, line_map)
    
    # Process SQL statements further
    for result in results:
        query = result['groups']['query'].strip()
        result['sql_query'] = query
        
        # Determine SQL operation type
        if re.search(r'^\s*SELECT', query, re.IGNORECASE):
            result['operation'] = 'SELECT'
            # Try to extract table names
            from_match = re.search(r'FROM\s+(?P<tables>(?:[A-Za-z0-9_\-]+(?:\.[A-Za-z0-9_\-]+)*(?:\s*,\s*|\s+JOIN\s+)?)+)', query, re.IGNORECASE)
            if from_match:
                tables_str = from_match.group('tables').strip()
                # Handle commas and joins, preserving qualified names
                tables = [t.strip() for t in re.split(r'\s*,\s*|\s+JOIN\s+', tables_str) if t.strip()]
                # Clean up any remaining whitespace or trailing dots
                tables = [re.sub(r'\.+$', '', t.strip()) for t in tables]
                result['tables'] = tables
            
        elif re.search(r'^\s*INSERT', query, re.IGNORECASE):
            result['operation'] = 'INSERT'
            # Try to extract table name
            into_match = re.search(r'INTO\s+(?P<table>[A-Za-z0-9_\-]+)', query, re.IGNORECASE)
            if into_match:
                table_name = into_match.group('table').strip()
                result['table'] = table_name
                # Also store in tables list for consistency
                result['tables'] = [table_name]
            
        elif re.search(r'^\s*UPDATE', query, re.IGNORECASE):
            result['operation'] = 'UPDATE'
            # Try to extract table name - improved to handle aliases
            update_match = re.search(r'UPDATE\s+(?P<table>[A-Za-z0-9_\-]+)(?:\s+[A-Za-z0-9_\-]+)?', query, re.IGNORECASE)
            if update_match:
                table_name = update_match.group('table').strip()
                result['table'] = table_name
                # Also store in tables list for consistency
                result['tables'] = [table_name]
                
            # Look for FROM clause that might contain additional tables (common in UPDATE with JOIN)
            from_match = re.search(r'FROM\s+(?P<tables>(?:[A-Za-z0-9_\-]+(?:\s+[A-Za-z0-9_\-]+)?(?:\s*,\s*|\s+JOIN\s+)?)+)', query, re.IGNORECASE)
            if from_match:
                tables_str = from_match.group('tables').strip()
                tables = [t.strip().split()[0] for t in re.split(r'\s*,\s*|\s+JOIN\s+', tables_str) if t.strip()]
                result['tables'] = tables
            
        elif re.search(r'^\s*DELETE', query, re.IGNORECASE):
            result['operation'] = 'DELETE'
            # Try to extract table name
            from_match = re.search(r'FROM\s+(?P<table>[A-Za-z0-9_\-]+)', query, re.IGNORECASE)
            if from_match:
                table_name = from_match.group('table').strip()
                result['table'] = table_name
                # Also store in tables list for consistency
                result['tables'] = [table_name]
                
        elif re.search(r'^\s*CREATE', query, re.IGNORECASE):
            result['operation'] = 'CREATE'
            
        elif re.search(r'^\s*ALTER', query, re.IGNORECASE):
            result['operation'] = 'ALTER'
            
        elif re.search(r'^\s*DROP', query, re.IGNORECASE):
            result['operation'] = 'DROP'
            
        elif re.search(r'^\s*DECLARE', query, re.IGNORECASE):
            result['operation'] = 'DECLARE'
            
        elif re.search(r'^\s*FETCH', query, re.IGNORECASE):
            result['operation'] = 'FETCH'
            
        elif re.search(r'^\s*OPEN', query, re.IGNORECASE):
            result['operation'] = 'OPEN'
            
        elif re.search(r'^\s*CLOSE', query, re.IGNORECASE):
            result['operation'] = 'CLOSE'
            
        else:
            result['operation'] = 'UNKNOWN'
    
    return results 