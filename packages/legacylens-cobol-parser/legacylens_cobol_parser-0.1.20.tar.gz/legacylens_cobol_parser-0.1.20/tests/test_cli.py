"""
Test module for the COBOL parser CLI.
"""
import os
import json
import pytest
import tempfile
import sys
from unittest.mock import patch

from cobol_parser.cli import parse_arguments, format_text_output, main


def test_parse_arguments():
    """Test argument parsing."""
    with patch('sys.argv', ['cobol-parser', 'file.cbl']):
        args = parse_arguments()
        assert args.file == 'file.cbl'
        assert args.output is None
        assert args.format == 'json'
        assert args.extract == 'all'
        assert args.ignore_case is True

    with patch('sys.argv', [
        'cobol-parser', 'file.cbl',
        '--output', 'output.json',
        '--format', 'text',
        '--extract', 'calls'
    ]):
        args = parse_arguments()
        assert args.file == 'file.cbl'
        assert args.output == 'output.json'
        assert args.format == 'text'
        assert args.extract == 'calls'


def test_format_text_output():
    """Test formatting of text output."""
    # Create sample data
    data = {
        'calls': [
            {
                'line': 10,
                'match': 'CALL "TEST-PROGRAM" USING PARAM1 PARAM2',
                'program_name': 'TEST-PROGRAM',
                'parameters': ['PARAM1', 'PARAM2'],
                'groups': {'program': 'TEST-PROGRAM', 'using': 'USING PARAM1 PARAM2'}
            }
        ],
        'io_files': [
            {
                'line': 20,
                'match': 'OPEN INPUT FILE1',
                'operation': 'OPEN',
                'mode': 'INPUT',
                'files': ['FILE1'],
                'groups': {'mode': 'INPUT', 'files': ' FILE1'}
            }
        ],
        'performs': [
            {
                'line': 30,
                'match': 'PERFORM PROC1',
                'type': 'explicit',
                'procedure': 'PROC1',
                'groups': {'procedure': 'PROC1'}
            }
        ],
        'sql_queries': [
            {
                'line': 40,
                'match': 'EXEC SQL SELECT * FROM TABLE1 END-EXEC',
                'operation': 'SELECT',
                'sql_query': 'SELECT * FROM TABLE1',
                'tables': ['TABLE1'],
                'groups': {'query': 'SELECT * FROM TABLE1'}
            }
        ],
        'copybooks': [
            {
                'line': 50,
                'match': 'COPY COPYBOOK1.',
                'copybook_name': 'COPYBOOK1',
                'groups': {'copybook': 'COPYBOOK1'}
            }
        ]
    }
    
    # Format the data
    output = format_text_output(data)
    
    # Check that all sections are included
    assert "CALLS (1 found)" in output
    assert "FILE I/O (1 found)" in output
    assert "PERFORMS (1 found)" in output
    assert "SQL QUERIES (1 found)" in output
    assert "COPYBOOKS (1 found)" in output
    
    # Check specific content
    assert "Program: TEST-PROGRAM" in output
    assert "Parameters: PARAM1, PARAM2" in output
    assert "Operation: OPEN" in output
    assert "Mode: INPUT" in output
    assert "Type: explicit" in output
    assert "Procedure: PROC1" in output
    assert "Operation: SELECT" in output
    assert "Tables: TABLE1" in output
    assert "Copybook: COPYBOOK1" in output


@pytest.mark.parametrize('format_type', ['json', 'text'])
def test_main_with_output_file(format_type):
    """Test main function with output to file."""
    # Sample COBOL file path
    sample_file = os.path.join(os.path.dirname(__file__), 'sample.cbl')
    
    # Create a temporary output file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        output_file = temp_file.name
    
    try:
        # Run with arguments
        with patch('sys.argv', [
            'cobol-parser',
            sample_file,
            '--output', output_file,
            '--format', format_type
        ]):
            main()
        
        # Check that the output file was created and has content
        assert os.path.exists(output_file)
        with open(output_file, 'r') as f:
            content = f.read()
            assert content
        
        # If JSON format, check that it's valid JSON
        if format_type == 'json':
            try:
                data = json.loads(content)
                assert isinstance(data, dict)
                assert "calls" in data
                assert "io_files" in data
                assert "performs" in data
                assert "sql_queries" in data
                assert "copybooks" in data
            except json.JSONDecodeError:
                pytest.fail("Output is not valid JSON")
    finally:
        # Clean up the temporary file
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_main_with_error():
    """Test main function with an error condition."""
    # Non-existent file
    non_existent_file = 'does_not_exist.cbl'
    
    # Redirect stderr to capture the error message
    with patch('sys.stderr') as mock_stderr, \
         patch('sys.argv', ['cobol-parser', non_existent_file]), \
         patch('sys.exit') as mock_exit:
        
        main()
        
        # Check that sys.exit was called with a non-zero exit code
        mock_exit.assert_called_once()
        args, kwargs = mock_exit.call_args
        assert args[0] != 0
        
        # Check that an error message was written to stderr
        mock_stderr.write.assert_called()
        args, kwargs = mock_stderr.write.call_args
        assert "Error:" in args[0] 