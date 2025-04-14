# LegacyLens COBOL Parser

A Python tool to extract specific information from COBOL programs.

## Features

This parser extracts the following information from COBOL source code:

- **CALLS**: Identifies CALL statements and their parameters
- **I/O FILES**: Extracts file operations (SELECT, OPEN, CLOSE, READ, WRITE)
- **PERFORMS**: Identifies PERFORM statements (procedural calls)
- **SQL QUERIES**: Extracts embedded SQL statements
- **COPYBOOKS**: Identifies COPY statements (included files)
- **Support for conditional compilation**
- **Configurable logging** with standard levels (INFO, DEBUG)

## Installation

### From PyPI (Recommended)

```bash
pip install lagacylens_cobol_parser
```

### From Source

```bash
# Clone the repository
git clone https://github.com/sam94dion/cobol-parser.git
cd cobol-parser

# Install in development mode
pip install -e .
```

## Usage

### Quick Start (Simplified Interface)

```python
# Parse a file with default settings
from cobol_parser import parse_file

# Parse a file and extract everything
result = parse_file("path/to/your/cobol/program.cbl")
print(result)

# Parse a file and extract only specific information
result = parse_file(
    "path/to/your/cobol/program.cbl", 
    extract_types=["calls", "sql_queries"]
)
print(result)

# Parse from a string
from cobol_parser import parse_string

cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. EXAMPLE.
       PROCEDURE DIVISION.
           PERFORM PARA-A.
           CALL "SUBPGM" USING WS-VAR.
       PARA-A.
           DISPLAY "Hello, World!".
"""
result = parse_string(cobol_code)
print(result)
```

### As a Python Library (Advanced Usage)

```python
from cobol_parser import CobolParser, setup_logger
import logging

# Configure logging (optional)
setup_logger(level=logging.INFO)  # Options: logging.INFO, logging.DEBUG

# Create a parser instance
parser = CobolParser()

# Load COBOL source from a file
parser.load_from_file("path/to/your/cobol/program.cbl")

# Or load from a string
cobol_code = """
       IDENTIFICATION DIVISION.
       PROGRAM-ID. EXAMPLE.
       PROCEDURE DIVISION.
           PERFORM PARA-A.
           CALL "SUBPGM" USING WS-VAR.
       PARA-A.
           DISPLAY "Hello, World!".
"""
parser.load_from_string(cobol_code)

# Extract all information
result = parser.extract_all()
print(result)

# Or extract specific information
calls = parser.extract_calls()
io_files = parser.extract_io_files()
performs = parser.extract_performs()
sql_queries = parser.extract_sql_queries()
copybooks = parser.extract_copybooks()
```

### Logging Configuration

The parser provides a flexible logging system:

```python
from cobol_parser import setup_logger
import logging

# Configure logging with different levels
setup_logger(level=logging.INFO)    # Show only important information
setup_logger(level=logging.DEBUG)   # Show all debugging information

# You can also configure logging with a custom name
setup_logger(name="my_custom_logger", level=logging.INFO)

# The logger will output messages in the format:
# YYYY-MM-DD HH:MM:SS,mmm - logger_name - LEVEL - message
```

### Command Line Interface

```bash
# Basic usage
lagacylens_cobol_parser path/to/your/cobol/program.cbl

# Specify output file
lagacylens_cobol_parser path/to/your/cobol/program.cbl -o results.json

# Extract specific information
lagacylens_cobol_parser path/to/your/cobol/program.cbl -e calls

# Output as text instead of JSON
lagacylens_cobol_parser path/to/your/cobol/program.cbl -f text

# Set log level
lagacylens_cobol_parser path/to/your/cobol/program.cbl -l info    # Show only INFO messages
lagacylens_cobol_parser path/to/your/cobol/program.cbl -l debug   # Show all debug messages
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Extending the Parser

The parser is designed to be extensible. To add support for extracting additional elements:

1. Create a new extractor in the `cobol_parser/extractors/` directory
2. Add a corresponding method to the `CobolParser` class
3. Update the CLI interface in `cobol_parser/cli.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.