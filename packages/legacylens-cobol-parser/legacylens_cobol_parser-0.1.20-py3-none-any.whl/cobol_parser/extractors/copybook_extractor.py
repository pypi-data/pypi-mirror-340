"""
Extractor for COPYBOOK inclusions in COBOL programs.
"""
import re
from typing import List, Dict, Any

from cobol_parser.extractors.base_extractor import BaseExtractor


def extract_copybooks(source: str, line_map: List[int]) -> List[Dict[str, Any]]:
    """
    Extract COPYBOOK inclusions from COBOL source code.
    
    This function identifies:
    - COPY statements with copybook names
    - REPLACING options if present
    - Library (source) if specified
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        
    Returns:
        List of dictionaries with information about each COPYBOOK inclusion.
    """
    # Pattern for COPY statements
    copy_pattern = re.compile(
        r'COPY\s+'                                 # COPY keyword
        r'(?P<copybook>(?:"[^"]+"|\'[^\']+\'|\S+))' # Copybook name (quoted or not)
        r'(?:\s+(?P<library>IN|OF)\s+(?P<lib_name>\S+))?' # Optional library
        r'(?:\s+REPLACING\s+(?P<replacing>.*?))?'  # Optional REPLACING clause
        r'(?:[\.\,])',                             # Terminator
        re.IGNORECASE | re.DOTALL
    )
    
    # Find all COPY statements
    results = BaseExtractor.find_matches(copy_pattern, source, line_map)
    
    # Process results
    for result in results:
        # Clean up copybook name
        copybook = result['groups']['copybook'].strip()
        if (copybook.startswith('"') and copybook.endswith('"')) or \
           (copybook.startswith("'") and copybook.endswith("'")):
            copybook = copybook[1:-1]
        result['copybook_name'] = copybook
        
        # Process library name if present
        if result['groups']['lib_name']:
            result['library'] = result['groups']['lib_name'].strip()
        
        # Process REPLACING clause if present
        if result['groups']['replacing']:
            replacing_text = result['groups']['replacing'].strip()
            # Basic parsing of REPLACING - could be enhanced for more complex cases
            replacements = []
            
            # Split by "==" to find the pairs
            parts = re.split(r'\s+==\s+', replacing_text)
            for i in range(0, len(parts) - 1, 2):
                if i+1 < len(parts):
                    # Clean up the BY part by removing trailing "=="
                    by_part = parts[i+1]
                    if "==" in by_part:
                        by_part = by_part.split("==")[0].strip()
                    
                    replacement = {
                        "from": parts[i].strip(),
                        "to": by_part.strip()
                    }
                    replacements.append(replacement)
            
            result['replacements'] = replacements
    
    return results 


def expand_copybooks(source: str, copybook_resolver, max_depth: int = 5) -> str:
    """
    Expand copybooks within a COBOL source string by replacing COPY statements with copybook content.
    
    This function recursively replaces COPY statements with their corresponding copybook content
    to create a fully expanded source file for analysis. It supports:
    - Multiple levels of nested copybooks
    - Depth limiting to prevent infinite recursion
    - Copybook lookup via a resolver function
    
    Args:
        source: Normalized COBOL source code with COPY statements.
        copybook_resolver: A function that takes a copybook name and returns its content.
                           Should return None if the copybook is not found.
        max_depth: Maximum depth of copybook nesting to prevent infinite recursion.
                  Default is 5 levels deep.
        
    Returns:
        Expanded COBOL source code with copybooks replaced by their content.
    """
    if max_depth <= 0:
        # Prevent infinite recursion by returning source if max depth reached
        return source
    
    # Pattern for COPY statements similar to the one in extract_copybooks
    copy_pattern = re.compile(
        r'COPY\s+'                                  # COPY keyword
        r'(?P<copybook>(?:"[^"]+"|\'[^\']+\'|\S+))' # Copybook name (quoted or not)
        r'(?:\s+(?P<library>IN|OF)\s+(?P<lib_name>\S+))?' # Optional library
        r'(?:\s+REPLACING\s+(?P<replacing>.*?))?'   # Optional REPLACING clause
        r'(?:[\.\,])',                              # Terminator
        re.IGNORECASE | re.DOTALL
    )
    
    def replace_copybook(match):
        # Extract copybook name
        copybook = match.group('copybook').strip()
        if (copybook.startswith('"') and copybook.endswith('"')) or \
           (copybook.startswith("'") and copybook.endswith("'")):
            copybook = copybook[1:-1]
        
        # Get copybook content from resolver
        content = copybook_resolver(copybook)
        
        if content is None:
            # If copybook not found, keep original COPY statement
            return match.group(0)
        
        # Process REPLACING clause if present
        if match.group('replacing'):
            replacing_text = match.group('replacing').strip()
            
            # Parse the replacing directive to get each pair
            replacement_pairs = []
            # First, find all ==X== BY ==Y== patterns
            replacing_pattern = re.compile(
                r'==(?P<from>[^=]+)==\s+BY\s+==(?P<to>[^=]+)==',
                re.IGNORECASE
            )
            
            for repl_match in replacing_pattern.finditer(replacing_text):
                from_text = repl_match.group('from').strip()
                to_text = repl_match.group('to').strip()
                replacement_pairs.append((from_text, to_text))
            
            # Apply all replacements to the content
            for from_text, to_text in replacement_pairs:
                content = content.replace(from_text, to_text)
        
        # Recursively expand copybooks in the included content
        expanded_content = expand_copybooks(content, copybook_resolver, max_depth - 1)
        return expanded_content
    
    # Apply replacements - we use count=0 to replace all occurrences
    expanded_source = copy_pattern.sub(replace_copybook, source)
    
    return expanded_source


# Update the extract_copybooks function to support expansion
def extract_copybooks_with_expansion(source: str, line_map: List[int], 
                                   copybook_resolver=None, expand: bool = False) -> List[Dict[str, Any]]:
    """
    Extract COPYBOOK inclusions from COBOL source code with optional expansion.
    
    This enhanced version adds support for:
    - Optionally expanding copybooks before extraction
    - Analyzing elements within copybooks
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        copybook_resolver: Function that takes copybook name and returns content.
        expand: If True, expand copybooks before extraction.
        
    Returns:
        List of dictionaries with information about each COPYBOOK inclusion.
    """
    # Expand copybooks if requested
    if expand and copybook_resolver:
        expanded_source = expand_copybooks(source, copybook_resolver)
        # Extract copybooks from the expanded source
        return extract_copybooks(expanded_source, line_map)
    else:
        # Use the original extraction function
        return extract_copybooks(source, line_map) 