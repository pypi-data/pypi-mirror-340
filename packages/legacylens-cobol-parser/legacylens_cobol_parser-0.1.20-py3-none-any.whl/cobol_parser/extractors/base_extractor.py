"""
Base extractor module providing common functionality for all extractors.
"""
import re
from typing import List, Dict, Any, Pattern, Match, Tuple


class BaseExtractor:
    """Base class for all COBOL element extractors."""
    
    @staticmethod
    def find_matches(pattern: Pattern, source: str, line_map: List[int]) -> List[Dict[str, Any]]:
        """
        Find all matches for a given regex pattern in the source code.
        
        Args:
            pattern: Compiled regex pattern to search for.
            source: Normalized source code to search in.
            line_map: Mapping of normalized line numbers to original line numbers.
            
        Returns:
            List of dictionaries containing match information.
        """
        results = []
        
        for match in pattern.finditer(source):
            result = BaseExtractor.create_match_result(match, line_map, source)
            results.append(result)
            
        return results
    
    @staticmethod
    def create_match_result(match: Match, line_map: List[int], source: str = None) -> Dict[str, Any]:
        """
        Create a match result dictionary from a regex match object.
        
        Args:
            match: The regex match object.
            line_map: Mapping of normalized line numbers to original line numbers.
            source: Optional normalized source code, used for line number calculation.
                    If not provided, will use match position directly.
            
        Returns:
            Dictionary containing match information.
        """
        start_pos = match.start()
        end_pos = match.end()
        
        # For line calculation, we need the source if not provided
        if source is None:
            # We'll just use the position in the matched text, which might be less accurate
            source_prefix = ''
        else:
            source_prefix = source[:start_pos]
            
        # Find line number from position
        line_idx = source_prefix.count('\n')
        original_line = line_map[line_idx] if line_idx < len(line_map) else -1
        
        # Extract the matched text
        matched_text = match.group(0)
        
        # Create result dictionary
        return {
            'match': matched_text,
            'line': original_line,
            'groups': {name: value for name, value in match.groupdict().items()}
        }
    
    @staticmethod
    def get_line_number(pos: int, source: str, line_map: List[int]) -> int:
        """
        Get the original line number for a position in the normalized source.
        
        Args:
            pos: Position in the normalized source.
            source: Normalized source code.
            line_map: Mapping of normalized line numbers to original line numbers.
            
        Returns:
            Original line number (1-based).
        """
        line_idx = source[:pos].count('\n')
        return line_map[line_idx] if line_idx < len(line_map) else -1 