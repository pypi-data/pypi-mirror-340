"""
Core COBOL Parser module
"""
import re
import logging
from typing import List, Dict, Any, Optional, Set

from .logger import logger


class CobolParser:
    """
    A parser for COBOL programs that extracts specific information.
    
    This class provides functionality to parse COBOL source code and
    extract various elements such as CALL statements, file I/O operations,
    PERFORM statements, SQL queries, and COPYBOOK inclusions.
    """
    
    def __init__(self, ignore_case: bool = True, log_level: int = logging.INFO):
        """
        Initialize the COBOL parser.
        
        Args:
            ignore_case: Whether to ignore case when parsing COBOL code.
                         COBOL is traditionally case-insensitive.
            log_level: Logging level to use (default: INFO)
        """
        self.ignore_case = ignore_case
        self._source_code = ""
        self._normalized_source = ""
        self._line_map = []
        
        # Set log level
        logger.set_level(log_level)
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load COBOL source code from a file.
        
        Args:
            file_path: Path to the COBOL source file.
        """
        logger.info(f"Loading COBOL source from file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            self._source_code = f.read()
        self._preprocess_source()
    
    def load_from_string(self, source_code: str) -> None:
        """
        Load COBOL source code from a string.
        
        Args:
            source_code: COBOL source code as a string.
        """
        logger.info("Loading COBOL source from string")
        self._source_code = source_code
        self._preprocess_source()
    
    def _preprocess_source(self) -> None:
        """
        Preprocess the source code for parsing.
        
        This method normalizes the source code by:
        - Removing line numbers in columns 1-6 if present
        - Handling continuation lines
        - Removing comments
        - Normalizing whitespace
        """
        if not self._source_code:
            return
            
        logger.warning("Preprocessing COBOL source code")
        
        # Split into lines and process each line
        lines = self._source_code.splitlines()
        normalized_lines = []
        self._line_map = []
        
        continued_line = ""
        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                continue
                
            # Handle COBOL standard format if line appears to be in fixed format
            if len(line) > 6 and line[6] in ['-', ' ']:
                # Remove columns 1-6 (sequence numbers)
                content = line[7:72] if len(line) > 72 else line[7:]
                
                # Check for continuation line
                if line[6] == '-':
                    continued_line += content.strip()
                    continue
            else:
                content = line
                
            # Process normal line
            if continued_line:
                content = continued_line + " " + content.strip()
                continued_line = ""
                
            # Remove comments (lines starting with * or / or containing comment indicators)
            if content.strip().startswith(('*', '/')):
                continue
                
            comment_pos = content.upper().find('*>')
            if comment_pos >= 0:
                content = content[:comment_pos].rstrip()
                
            # Add to normalized source if not empty
            content = content.strip()
            if content:
                normalized_lines.append(content)
                self._line_map.append(i + 1)  # Store original line number (1-based)
        
        # Join normalized lines
        self._normalized_source = '\n'.join(normalized_lines)
        
        # Convert to uppercase if ignore_case is True
        if self.ignore_case:
            self._normalized_source = self._normalized_source.upper()
        
        logger.debug(f"Preprocessed source code length: {len(self._normalized_source)} characters")
    
    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all supported information from the COBOL source code.
        
        Returns:
            A dictionary containing all extracted information.
        """
        logger.info("Extracting all information from COBOL source")
        return {
            "calls": self.extract_calls(),
            "io_files": self.extract_io_files(),
            "performs": self.extract_performs(),
            "sql_queries": self.extract_sql_queries(),
            "copybooks": self.extract_copybooks()
        }
    
    def extract_calls(self) -> List[Dict[str, Any]]:
        """
        Extract CALL statements from the COBOL source code.
        
        Returns:
            List of dictionaries containing information about each CALL.
        """
        logger.warning("Extracting CALL statements")
        # Implementation will be provided by specific extractor
        from .extractors.call_extractor import extract_calls
        return extract_calls(self._normalized_source, self._line_map)
    
    def extract_io_files(self) -> List[Dict[str, Any]]:
        """
        Extract file I/O operations from the COBOL source code.
        
        Returns:
            List of dictionaries containing information about each file I/O.
        """
        logger.warning("Extracting file I/O operations")
        # Implementation will be provided by specific extractor
        from .extractors.io_extractor import extract_io_files
        return extract_io_files(self._normalized_source, self._line_map)
    
    def extract_performs(self) -> List[Dict[str, Any]]:
        """
        Extract PERFORM statements from the COBOL source code.
        
        Returns:
            List of dictionaries containing information about each PERFORM.
        """
        logger.warning("Extracting PERFORM statements")
        # Implementation will be provided by specific extractor
        from .extractors.perform_extractor import extract_performs
        return extract_performs(self._normalized_source, self._line_map)
    
    def extract_sql_queries(self) -> List[Dict[str, Any]]:
        """
        Extract SQL queries from the COBOL source code.
        
        Returns:
            List of dictionaries containing information about each SQL query.
        """
        logger.warning("Extracting SQL queries")
        # Implementation will be provided by specific extractor
        from .extractors.sql_extractor import extract_sql_queries
        return extract_sql_queries(self._normalized_source, self._line_map)
    
    def extract_copybooks(self) -> List[Dict[str, Any]]:
        """
        Extract COPYBOOK inclusions from the COBOL source code.
        
        Returns:
            List of dictionaries containing information about each COPYBOOK.
        """
        logger.warning("Extracting COPYBOOK inclusions")
        # Implementation will be provided by specific extractor
        from .extractors.copybook_extractor import extract_copybooks
        return extract_copybooks(self._normalized_source, self._line_map)