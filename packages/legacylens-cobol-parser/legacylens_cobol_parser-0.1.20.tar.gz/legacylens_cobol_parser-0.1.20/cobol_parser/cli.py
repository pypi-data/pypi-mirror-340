"""
Command-line interface for the LegacyLens COBOL parser.
"""
import argparse
import json
import logging
import sys
from typing import Dict, Any, List, Optional

from .parser import CobolParser
from .logger import setup_logger


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='LegacyLens COBOL Parser - Extract information from COBOL programs'
    )
    
    parser.add_argument(
        'file',
        help='Path to the COBOL file to parse'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'text'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--extract', '-e',
        choices=['all', 'calls', 'io_files', 'performs', 'sql_queries', 'copybooks'],
        default='all',
        help='Information to extract (default: all)'
    )
    
    parser.add_argument(
        '--ignore-case', '-i',
        action='store_true',
        default=True,
        help='Ignore case when parsing (default: true)'
    )
    
    parser.add_argument(
        '--log-level', '-l',
        choices=['info', 'warning', 'debug'],
        default='info',
        help='Logging level (default: info)'
    )
    
    return parser.parse_args()


def format_text_output(data: Dict[str, Any]) -> str:
    """Format the extraction results as text."""
    output = []
    
    # Helper function to format a list of results
    def format_section(title: str, results: List[Dict[str, Any]]) -> None:
        output.append(f"\n{title} ({len(results)} found)")
        output.append("=" * (len(title) + 10))
        
        for i, result in enumerate(results, 1):
            output.append(f"\n{i}. Line {result.get('line', 'Unknown')}:")
            
            # Format based on section type
            if title == "CALLS":
                output.append(f"   Program: {result.get('program_name', 'Unknown')}")
                if result.get('parameters'):
                    output.append(f"   Parameters: {', '.join(result.get('parameters', []))}")
            
            elif title == "FILE I/O":
                output.append(f"   Operation: {result.get('operation', 'Unknown')}")
                if result.get('file_name'):
                    output.append(f"   File: {result.get('file_name')}")
                if result.get('files'):
                    output.append(f"   Files: {', '.join(result.get('files', []))}")
                if result.get('mode'):
                    output.append(f"   Mode: {result.get('mode')}")
            
            elif title == "PERFORMS":
                output.append(f"   Type: {result.get('type', 'Unknown')}")
                if result.get('procedure'):
                    output.append(f"   Procedure: {result.get('procedure')}")
                if result.get('thru'):
                    output.append(f"   THRU: {result.get('thru')}")
                if result.get('times'):
                    output.append(f"   TIMES: {result.get('times')}")
            
            elif title == "SQL QUERIES":
                output.append(f"   Operation: {result.get('operation', 'Unknown')}")
                if result.get('table'):
                    output.append(f"   Table: {result.get('table')}")
                if result.get('tables'):
                    output.append(f"   Tables: {', '.join(result.get('tables', []))}")
                output.append(f"   Query: {result.get('sql_query', '')[:80]}...")
            
            elif title == "COPYBOOKS":
                output.append(f"   Copybook: {result.get('copybook_name', 'Unknown')}")
                if result.get('library'):
                    output.append(f"   Library: {result.get('library')}")
                if result.get('replacements'):
                    output.append("   Replacements:")
                    for rep in result.get('replacements', []):
                        output.append(f"     {rep.get('from')} -> {rep.get('to')}")
    
    # Format each section in the data
    if 'calls' in data:
        format_section("CALLS", data['calls'])
    
    if 'io_files' in data:
        format_section("FILE I/O", data['io_files'])
    
    if 'performs' in data:
        format_section("PERFORMS", data['performs'])
    
    if 'sql_queries' in data:
        format_section("SQL QUERIES", data['sql_queries'])
    
    if 'copybooks' in data:
        format_section("COPYBOOKS", data['copybooks'])
    
    return "\n".join(output)


def main() -> None:
    """Main entry point for the command-line interface."""
    args = parse_arguments()
    
    # Set log level based on command line argument
    logger = setup_logger(level=args.log_level)
    
    # Create parser
    parser = CobolParser(ignore_case=args.ignore_case)
    
    try:
        # Load source from file
        parser.load_from_file(args.file)
        
        # Extract requested information
        if args.extract == 'all':
            results = parser.extract_all()
        elif args.extract == 'calls':
            results = {'calls': parser.extract_calls()}
        elif args.extract == 'io_files':
            results = {'io_files': parser.extract_io_files()}
        elif args.extract == 'performs':
            results = {'performs': parser.extract_performs()}
        elif args.extract == 'sql_queries':
            results = {'sql_queries': parser.extract_sql_queries()}
        elif args.extract == 'copybooks':
            results = {'copybooks': parser.extract_copybooks()}
        else:
            results = parser.extract_all()
        
        # Format the output
        if args.format == 'json':
            output = json.dumps(results, indent=2)
        else:  # text format
            output = format_text_output(results)
        
        # Write to file or stdout
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)
            
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()