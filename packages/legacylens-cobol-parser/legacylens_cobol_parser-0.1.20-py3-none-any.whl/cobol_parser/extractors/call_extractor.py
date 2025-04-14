"""
Extractor for CALL statements in COBOL programs.
"""
import re
from typing import List, Dict, Any

from cobol_parser.extractors.base_extractor import BaseExtractor


def extract_calls(source: str, line_map: List[int]) -> List[Dict[str, Any]]:
    """
    Extract CALL statements from COBOL source code.
    
    This function identifies different forms of CALL statements:
    - Standard calls: CALL "program-name"
    - Dynamic calls: CALL program-id
    - Calls with USING clause: CALL "program" USING parameters
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        
    Returns:
        List of dictionaries with information about each CALL.
    """
    # Pattern for CALL statements - matches different variations of CALL syntax
    # Group 1: The program name (with or without quotes)
    # Group 2: Optional USING clause (parameters)
    call_pattern = re.compile(
        r'CALL\s+'                                # CALL keyword
        r'(?P<program>(?:"[^"]+"|\'[^\']+\'|\S+))'  # Program name (quoted or not)
        r'(?:\s+(?P<using>USING\s+[^\.\n]+))?'    # Optional USING clause - capture until a period or newline
        r'(?:[\.\n]|$)',                          # End with period, newline or end of string
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all matches
    results = BaseExtractor.find_matches(call_pattern, source, line_map)
    
    # Process results to clean up and extract additional information
    for result in results:
        # Clean up program name by removing quotes if present
        program = result['groups']['program'].strip()
        if (program.startswith('"') and program.endswith('"')) or \
           (program.startswith("'") and program.endswith("'")):
            program = program[1:-1]
        
        result['program_name'] = program
        
        # Process USING clause if present
        if result['groups']['using']:
            using_clause = result['groups']['using'].strip()
            # Remove the USING keyword
            params_str = using_clause.replace('USING', '', 1).strip()
            
            # Check if parameters are comma-separated
            if ',' in params_str:
                # Split parameters by commas
                params = [p.strip() for p in params_str.split(',') if p.strip()]
            else:
                # Handle space-separated parameters more carefully
                words = [w for w in params_str.split() if w.strip()]
                
                # In COBOL, when we have hyphenated identifiers like WS-CUSTOMER-RECORD,
                # we should keep them as a single parameter
                if len(words) == 1 or '-' in params_str:
                    params = [params_str]
                else:
                    params = words
            
            result['parameters'] = params
        else:
            result['parameters'] = []
    
    return results 