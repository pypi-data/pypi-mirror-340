"""
Extractor for PERFORM statements in COBOL programs.
"""
import re
from typing import List, Dict, Any

from cobol_parser.extractors.base_extractor import BaseExtractor


def extract_performs(source: str, line_map: List[int]) -> List[Dict[str, Any]]:
    """
    Extract PERFORM statements from COBOL source code.
    
    This function identifies different types of PERFORM statements:
    - Simple procedure calls: PERFORM procedure-name
    - Thru performs: PERFORM procedure-1 THRU procedure-2
    - Inline performs: PERFORM UNTIL condition ... END-PERFORM
    - Times performs: PERFORM procedure-name n TIMES
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        
    Returns:
        List of dictionaries with information about each PERFORM.
    """
    results = []
    
    # For debugging, let's print the source content around where TERMINATION should be
    termination_index = source.find("TERMINATION")
    if termination_index >= 0:
        start_idx = max(0, termination_index - 50)
        end_idx = min(len(source), termination_index + 50)
        print(f"DEBUG: Context around TERMINATION: [{source[start_idx:end_idx]}]")
        print(f"DEBUG: TERMINATION characters: {[ord(c) for c in 'TERMINATION']}")
        print(f"DEBUG: Characters in source: {[ord(c) for c in source[termination_index:termination_index+11]]}")
    
    # Simpler pattern to match basic PERFORM statements
    basic_pattern = re.compile(
        r'PERFORM\s+([A-Z0-9][A-Z0-9\-]+)',
        re.IGNORECASE
    )
    
    for match in basic_pattern.finditer(source):
        procedure_name = match.group(1).strip()
        # Skip inline keywords that might be mistaken for procedure names
        if procedure_name.upper() in ['UNTIL', 'VARYING', 'WITH', 'TEST']:
            continue
            
        # Create a simple result dictionary
        result = {
            'type': 'explicit',
            'procedure': procedure_name,
            'match': match.group(0),
            'line': BaseExtractor.get_line_number(match.start(), source, line_map),
            'groups': {'procedure': procedure_name}
        }
        results.append(result)
    
    # 2. Extract inline PERFORM statements
    inline_pattern = re.compile(
        r'(?:^|\s+)'                              # Start of line or whitespace
        r'PERFORM\s+'                             # PERFORM keyword
        r'(?:(?P<with_test>WITH\s+TEST\s+(?:BEFORE|AFTER))\s+)?'  # Optional WITH TEST
        r'(?:UNTIL\s+(?P<until>[^\.]+))?'        # Optional UNTIL condition
        r'(?:VARYING\s+(?P<varying>[^\.]+))?'    # Optional VARYING clause
        r'(?P<body>.*?)'                         # Body of the PERFORM
        r'END-PERFORM(?:\s*\.)?',                # END-PERFORM with optional period
        re.IGNORECASE | re.DOTALL
    )
    
    # Also look for PERFORM VARYING clauses without the explicit END-PERFORM
    varying_pattern = re.compile(
        r'PERFORM\s+VARYING\s+([^\s]+)\s+FROM\s+',
        re.IGNORECASE
    )
    
    for match in varying_pattern.finditer(source):
        varying_info = match.group(0) + "..."  # Capture part of the VARYING clause
        result = {
            'type': 'inline',
            'varying': varying_info,
            'match': match.group(0),
            'line': BaseExtractor.get_line_number(match.start(), source, line_map),
            'groups': {'varying': varying_info}
        }
        results.append(result)
    
    inline_results = BaseExtractor.find_matches(inline_pattern, source, line_map)
    for result in inline_results:
        result['type'] = 'inline'
        
        # Get body of the inline PERFORM
        body = result['groups']['body'].strip() if result['groups']['body'] else ""
        result['body'] = body
        
        # Add WITH TEST info if present
        if result['groups']['with_test']:
            result['with_test'] = result['groups']['with_test'].strip()
        
        # Add UNTIL condition if present
        if result['groups']['until']:
            result['until'] = result['groups']['until'].strip()
        
        # Add VARYING info if present
        if result['groups']['varying']:
            result['varying'] = result['groups']['varying'].strip()
        
        results.append(result)
    
    print("DEBUG: Found explicit performs:", [r['procedure'] for r in results if r.get('type') == 'explicit'])
    return results 