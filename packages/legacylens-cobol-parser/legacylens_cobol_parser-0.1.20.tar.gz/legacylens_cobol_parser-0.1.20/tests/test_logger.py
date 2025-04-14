"""
Tests for the COBOL parser logger.
"""
import io
import logging
import sys
from unittest import TestCase, mock

from cobol_parser.logger import CobolLogger


class TestCobolLogger(TestCase):
    """Test cases for the CobolLogger class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a new logger instance for each test
        self.logger = CobolLogger("test_logger")
        # Create a StringIO to capture log output
        self.log_capture = io.StringIO()
        # Create a handler that writes to our StringIO
        self.handler = logging.StreamHandler(self.log_capture)
        # Set the formatter to match the logger's format
        self.handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        # Add the handler to the logger
        self.logger.logger.addHandler(self.handler)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the handler and close the StringIO
        self.logger.logger.removeHandler(self.handler)
        self.log_capture.close()
    
    def test_info_level(self):
        """Test INFO level logging."""
        self.logger.set_level(logging.INFO)
        
        # Log messages at different levels
        self.logger.info("Test info message")
        self.logger.warning("Test warning message")  # Fixed typo in message
        self.logger.debug("Test debug message")
        
        output = self.log_capture.getvalue()
        # INFO and higher levels should be logged, but not DEBUG
        self.assertIn("Test info message", output)
        self.assertIn("Test warning message", output)  # WARNING level is higher than INFO
        self.assertNotIn("Test debug message", output)  # DEBUG level is lower than INFO

    
    def test_debug_level(self):
        """Test DEBUG level logging."""
        self.logger.set_level(logging.DEBUG)
        
        # Log messages at different levels
        self.logger.info("Test info message")
        self.logger.warning("Test warning message")
        self.logger.debug("Test debug message")
        
        output = self.log_capture.getvalue()
        # All messages should be logged
        self.assertIn("Test info message", output)
        self.assertIn("Test warning message", output)
        self.assertIn("Test debug message", output)
    
    def test_log_format(self):
        """Test log message format."""
        self.logger.info("Test message")
        
        output = self.log_capture.getvalue()
        # Check if the output contains all required parts of the format
        self.assertIn("test_logger", output)  # logger name
        self.assertIn("INFO", output)  # level name
        self.assertIn("Test message", output)  # message
        # Check for timestamp format (YYYY-MM-DD HH:MM:SS)
        self.assertRegex(output, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    
    def test_log_level_ordering(self):
        """Test that log levels are properly ordered."""
        # Test INFO level
        self.logger.set_level(logging.INFO)
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.debug("Debug message")
        
        output = self.log_capture.getvalue()
        self.assertIn("Info message", output)
        self.assertIn("Warning message", output)  # WARNING is higher than INFO
        self.assertNotIn("Debug message", output)  # DEBUG is lower than INFO
        
        # Clear the log capture
        self.log_capture.truncate(0)
        self.log_capture.seek(0)
        
        # Test WARNING level
        self.logger.set_level(logging.WARNING)
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.debug("Debug message")
        
        output = self.log_capture.getvalue()
        self.assertNotIn("Info message", output)  # INFO is lower than WARNING
        self.assertIn("Warning message", output)
        self.assertNotIn("Debug message", output)  # DEBUG is lower than WARNING
        
        # Clear the log capture
        self.log_capture.truncate(0)
        self.log_capture.seek(0)
        
        # Test DEBUG level
        self.logger.set_level(logging.DEBUG)
        self.logger.info("Info message")
        self.logger.warning("Warning message")
        self.logger.debug("Debug message")
        
        output = self.log_capture.getvalue()
        self.assertIn("Info message", output)  # INFO is higher than DEBUG
        self.assertIn("Warning message", output)  # WARNING is higher than DEBUG
        self.assertIn("Debug message", output)  # All messages should be visible at DEBUG level