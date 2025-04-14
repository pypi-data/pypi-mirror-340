"""
Utility functions for COBOL extractors with support for copybook expansion.
"""
from typing import List, Dict, Any, Callable, Optional

from cobol_parser.extractors.copybook_extractor import extract_copybooks, expand_copybooks
from cobol_parser.extractors.call_extractor import extract_calls
from cobol_parser.extractors.io_extractor import extract_io_files
from cobol_parser.extractors.perform_extractor import extract_performs
from cobol_parser.extractors.sql_extractor import extract_sql_queries


def extract_with_copybook_expansion(
    source: str, 
    line_map: List[int],
    copybook_resolver: Optional[Callable[[str], Optional[str]]] = None,
    expand_copybooks_flag: bool = False,
    max_expansion_depth: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract all elements from COBOL source with optional copybook expansion.
    
    This function combines all extractors and supports copybook expansion to find
    nested elements within copybooks.
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        copybook_resolver: Function that takes copybook name and returns content.
                          Should return None if copybook not found.
        expand_copybooks_flag: If True, expand copybooks before extraction.
        max_expansion_depth: Maximum depth for copybook expansion.
        
    Returns:
        Dictionary with extraction results for all element types.
    """
    # Expand copybooks if requested and resolver is available
    expanded_source = source
    if expand_copybooks_flag and copybook_resolver:
        expanded_source = expand_copybooks(source, copybook_resolver, max_expansion_depth)
    
    # Extract all elements from the expanded source
    results = {
        'copybooks': extract_copybooks(expanded_source, line_map),
        'calls': extract_calls(expanded_source, line_map),
        'io': extract_io_files(expanded_source, line_map),
        'performs': extract_performs(expanded_source, line_map),
        'sql': extract_sql_queries(expanded_source, line_map)
    }
    
    return results


def extract_recursive_elements(
    source: str,
    line_map: List[int],
    copybook_resolver: Callable[[str], Optional[str]],
    extractor_func: Callable[[str, List[int]], List[Dict[str, Any]]],
    max_depth: int = 5
) -> List[Dict[str, Any]]:
    """
    Extract elements recursively from COBOL source including copybooks.
    
    This specialized function works with a specific extractor to find elements
    within the main source and in all copybooks recursively.
    
    Args:
        source: Normalized COBOL source code.
        line_map: Mapping of normalized line numbers to original line numbers.
        copybook_resolver: Function that takes copybook name and returns content.
        extractor_func: The specific extractor function to use.
        max_depth: Maximum recursion depth.
        
    Returns:
        List of dictionaries with all found elements.
    """
    # Base case - stop recursion if max depth is reached
    if max_depth <= 0:
        return []
    
    # Extract copybooks from the source
    copybooks = extract_copybooks(source, line_map)
    
    # Extract requested elements from main source
    results = extractor_func(source, line_map)
    
    # For each copybook, resolve its content and extract elements recursively
    for cb in copybooks:
        copybook_name = cb['copybook_name']
        copybook_content = copybook_resolver(copybook_name)
        
        if copybook_content:
            # Extract elements from the copybook content
            copybook_results = extract_recursive_elements(
                copybook_content, 
                line_map,  # Use same line map for simplicity
                copybook_resolver,
                extractor_func,
                max_depth - 1
            )
            
            # Add a source attribute to track which copybook these elements came from
            for result in copybook_results:
                result['source_copybook'] = copybook_name
            
            # Add to overall results
            results.extend(copybook_results)
    
    return results 