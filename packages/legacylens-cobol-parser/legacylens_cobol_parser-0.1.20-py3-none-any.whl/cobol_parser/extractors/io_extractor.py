"""
Extractor for file I/O operations in COBOL programs.
"""
import re
from typing import List, Dict, Any

from cobol_parser.extractors.base_extractor import BaseExtractor


def extract_io_files(source: str, line_map: List[int]) -> List[Dict[str, Any]]:
    """
    Extract file I/O operations from COBOL source code.
    
    This function identifies:
    - SELECT statements in the FILE-CONTROL section
    - OPEN/CLOSE statements
    - READ/WRITE/REWRITE statements
    
    Note: SQL statements (EXEC SQL blocks) are NOT included in these results,
    even if they contain similar operations like OPEN, CLOSE, etc.
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        
    Returns:
        List of dictionaries with information about each file I/O operation.
    """
    results = []
    
    # First, identify all EXEC SQL blocks to exclude them
    sql_pattern = re.compile(
        r'EXEC\s+SQL\s+'                      # EXEC SQL
        r'(?P<query>.*?)'                     # Query content (non-greedy)
        r'(?:END-EXEC|END-EXEC\.)',           # END-EXEC or END-EXEC.
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all SQL blocks and create a list of spans to exclude
    sql_spans = []
    for match in re.finditer(sql_pattern, source):
        sql_spans.append((match.start(), match.end()))
    
    # Helper function to check if a match is within any SQL block
    def is_in_sql_block(match_start, match_end):
        for sql_start, sql_end in sql_spans:
            if match_start >= sql_start and match_end <= sql_end:
                return True
        return False
    
    # Helper function to check if a match is a valid COBOL file operation 
    # (not an SQL operation even if outside a full SQL block)
    def is_sql_operation(text):
        # Check if text contains END-EXEC or other SQL indicators
        return "END-EXEC" in text.upper() or "ORDER_CURSOR" in text.upper()
    
    # 1. Extract SELECT statements (file declarations)
    select_pattern = re.compile(
        r'SELECT\s+(?P<file_name>\S+)'           # SELECT file-name
        r'(?:\s+ASSIGN\s+TO\s+(?P<assign>[^\.\,]+))?',  # ASSIGN TO clause
        re.IGNORECASE
    )
    
    # Only include SELECT statements that are not within SQL blocks
    for match in re.finditer(select_pattern, source):
        if not is_in_sql_block(match.start(), match.end()):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'SELECT'
            
            # Clean up assign value if present
            if result['groups']['assign']:
                assign = result['groups']['assign'].strip()
                # Remove quotes if present
                if (assign.startswith('"') and assign.endswith('"')) or \
                   (assign.startswith("'") and assign.endswith("'")):
                    assign = assign[1:-1]
                result['assign_to'] = assign
            
            results.append(result)
    
    # 2. Extract OPEN statements
    open_pattern = re.compile(
        r'OPEN\s+(?P<mode>INPUT|OUTPUT|I-O|EXTEND)'  # OPEN mode
        r'(?P<files>(?:\s+[A-Za-z0-9\-_]+)+)'        # File names (one or more valid COBOL identifiers)
        r'(?:[\.\,]|$|\s+(?:IF|PERFORM|CALL))',      # End with period, comma, end of string, or start of a new statement
        re.IGNORECASE
    )
    
    # Only include OPEN statements that are not within SQL blocks
    for match in re.finditer(open_pattern, source):
        if not is_in_sql_block(match.start(), match.end()) and not is_sql_operation(match.group(0)):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'OPEN'
            mode = result['groups']['mode']
            
            # Process file names - only consider valid COBOL identifiers
            files_str = result['groups']['files'].strip()
            files = [f.strip() for f in re.split(r'\s+', files_str) if f.strip() and re.match(r'^[A-Za-z0-9\-_]+$', f.strip(), re.IGNORECASE)]
            result['files'] = files
            result['mode'] = mode
            
            results.append(result)
    
    # 4. Extract READ statements
    read_pattern = re.compile(
        r'READ\s+(?P<file>[A-Za-z0-9\-_]+)'         # READ file-name (must be valid COBOL identifier)
        r'(?:\s+(?:NEXT|PREVIOUS))?'                # Optional NEXT or PREVIOUS
        r'(?:\s+(?:INTO\s+(?P<into>[A-Za-z0-9\-_]+)))?'  # Optional INTO clause
        r'(?:\s+(?:KEY\s+IS\s+(?P<key>[^\.\,\n]+)))?'  # Optional KEY clause
        r'(?:[\.\,]|$|\s+(?:AT|END|NOT|IF|PERFORM|CALL))',  # Statement terminators or next keywords
        re.IGNORECASE
    )
    
    # Only include READ statements that are not within SQL blocks
    for match in re.finditer(read_pattern, source):
        if not is_in_sql_block(match.start(), match.end()):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'READ'
            
            # Add file name to make consistent with other operations
            result['files'] = [result['groups']['file']]
            
            # Add INTO target if present
            if result['groups']['into']:
                result['into'] = result['groups']['into'].strip()
            
            # Add KEY if present
            if result['groups']['key']:
                result['key'] = result['groups']['key'].strip()
            
            results.append(result)
            
    # Special case for processing CLOSE statements with multiple files
    # This can handle both single-line and multi-line patterns like:
    # CLOSE FILE1 FILE2. 
    # and 
    # CLOSE FILE1
    # CLOSE FILE2.
    def extract_close_files(text):
        # First, check if it's a multi-line close with "CLOSE" on each line
        if "\nCLOSE " in text.upper():
            # Split by CLOSE and process each part
            parts = re.split(r'(?i)CLOSE\s+', text)
            # First part is empty, skip it
            parts = [p.strip() for p in parts[1:] if p.strip()]
            
            all_files = []
            for part in parts:
                # Clean up the part to remove anything after periods, commas, or keywords
                part = re.sub(r'(?i)[\.\,].*$', '', part)
                part = re.sub(r'(?i)\s+(?:CALL|IF|PERFORM|DISPLAY).*$', '', part)
                
                # Extract valid file names from each CLOSE statement
                files = [f.strip() for f in re.split(r'\s+', part) 
                        if f.strip() and re.match(r'^[A-Za-z0-9\-_]+$', f.strip(), re.IGNORECASE)
                        and f.upper() != 'CLOSE']  # Exclude 'CLOSE' keyword
                all_files.extend(files)
            return all_files
        else:
            # Single CLOSE statement with multiple files
            # Extract the part after "CLOSE "
            file_text = re.sub(r'(?i)^CLOSE\s+', '', text).strip()
            
            # Clean up the text to remove anything after periods, commas, or keywords
            file_text = re.sub(r'(?i)[\.\,].*$', '', file_text)
            file_text = re.sub(r'(?i)\s+(?:CALL|IF|PERFORM|DISPLAY).*$', '', file_text)
            
            # Split by whitespace and filter valid identifiers
            return [f.strip() for f in re.split(r'\s+', file_text) 
                    if f.strip() and re.match(r'^[A-Za-z0-9\-_]+$', f.strip(), re.IGNORECASE)
                    and f.upper() != 'CLOSE']  # Exclude 'CLOSE' keyword
    
    # Helper function to check if an entry is a duplicate
    def is_duplicate(new_entry, existing_entries):
        """Check if an entry is a duplicate of an existing one."""
        for entry in existing_entries:
            if (entry['operation'] == new_entry['operation'] and
                entry['line'] == new_entry['line']):
                # For CLOSE operations, compare file lists
                if entry['operation'] == 'CLOSE' and 'files' in entry and 'files' in new_entry:
                    # If the file lists are identical or one contains the other, it's a duplicate
                    if (set(entry['files']) == set(new_entry['files']) or
                        set(entry['files']).issubset(set(new_entry['files'])) or
                        set(new_entry['files']).issubset(set(entry['files']))):
                        return True
                else:
                    # For other operations, same line = duplicate
                    return True
        return False
    
    # First, let's look for multi-line patterns - match two or more consecutive CLOSE statements
    multiline_close_pattern = re.compile(
        r'CLOSE\s+[A-Za-z0-9\-_]+\s*[\n\r]+\s*(?:CLOSE\s+[A-Za-z0-9\-_]+\s*[\n\r]+\s*)*CLOSE\s+[A-Za-z0-9\-_]+',
        re.IGNORECASE
    )
    
    # Keep track of positions that we've already processed to avoid duplicates
    processed_close_positions = set()
    
    for match in re.finditer(multiline_close_pattern, source):
        if not is_in_sql_block(match.start(), match.end()) and not is_sql_operation(match.group(0)):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'CLOSE'
            
            # Use the specialized function to extract file names
            result['files'] = extract_close_files(match.group(0))
            
            # Only add if not a duplicate
            if not is_duplicate(result, results):
                # Remember that we've processed this span
                processed_close_positions.add((match.start(), match.end()))
                results.append(result)
            
    # Now, look for single-line CLOSE statements
    close_pattern = re.compile(
        r'CLOSE'                                    # CLOSE keyword
        r'(?P<files>(?:\s+[A-Za-z0-9\-_]+)+)'      # File names (one or more valid COBOL identifiers)  
        r'(?:[\.\,]|$|\s+(?:IF|PERFORM|CALL|DISPLAY))',  # End with period, comma, end of string, or start of a new statement
        re.IGNORECASE
    )
    
    # Only include CLOSE statements that are not within SQL blocks or SQL operations
    for match in re.finditer(close_pattern, source):
        if not is_in_sql_block(match.start(), match.end()) and not is_sql_operation(match.group(0)):
            # Skip if this CLOSE is part of a multiline pattern we already processed
            overlapping = False
            for start, end in processed_close_positions:
                if (match.start() >= start and match.end() <= end):
                    overlapping = True
                    break
                    
            if not overlapping:
                result = BaseExtractor.create_match_result(match, line_map, source)
                result['operation'] = 'CLOSE'
                
                # Process file names using the special function
                result['files'] = extract_close_files(match.group(0))
                
                # Only add if not a duplicate
                if not is_duplicate(result, results):
                    results.append(result)
    
    # 5. Extract WRITE statements
    write_pattern = re.compile(
        r'WRITE\s+(?P<record>[A-Za-z0-9\-_]+)'       # WRITE record-name
        r'(?:\s+FROM\s+(?P<from>[A-Za-z0-9\-_]+))?'  # Optional FROM clause
        r'(?:[\.\,]|$)',                             # Statement must end with period, comma, or end of string
        re.IGNORECASE
    )
    
    # Only include WRITE statements that are not within SQL blocks
    for match in re.finditer(write_pattern, source):
        if not is_in_sql_block(match.start(), match.end()):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'WRITE'
            
            # Add FROM source if present
            if result['groups']['from']:
                result['from'] = result['groups']['from'].strip()
            
            results.append(result)
    
    # 6. Extract REWRITE statements
    rewrite_pattern = re.compile(
        r'REWRITE\s+(?P<record>[A-Za-z0-9\-_]+)'      # REWRITE record-name
        r'(?:\s+FROM\s+(?P<from>[A-Za-z0-9\-_]+))?'   # Optional FROM clause
        r'(?:[\.\,]|$)',                              # Statement must end with period, comma, or end of string
        re.IGNORECASE
    )
    
    # Only include REWRITE statements that are not within SQL blocks
    for match in re.finditer(rewrite_pattern, source):
        if not is_in_sql_block(match.start(), match.end()):
            result = BaseExtractor.create_match_result(match, line_map, source)
            result['operation'] = 'REWRITE'
            
            # Add FROM source if present
            if result['groups']['from']:
                result['from'] = result['groups']['from'].strip()
            
            results.append(result)
    
    return results 