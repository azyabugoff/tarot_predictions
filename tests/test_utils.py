import pytest
import logging
from unittest.mock import patch
from utils.logger import setup_logger


class TestLogger:
    """Test cases for logger utility."""
    
    def test_setup_logger_basic(self):
        """Test basic logger setup."""
        logger = setup_logger('test_logger')
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == 'test_logger'
        assert logger.level == logging.INFO
    
    def test_setup_logger_custom_level(self):
        """Test logger setup with custom level."""
        logger = setup_logger('test_logger_custom', level=logging.DEBUG)
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == 'test_logger_custom'
        assert logger.level == logging.DEBUG
    
    def test_setup_logger_has_handlers(self):
        """Test that logger has handlers after setup."""
        logger = setup_logger('test_logger_handlers')
        
        assert len(logger.handlers) > 0
        assert isinstance(logger.handlers[0], logging.StreamHandler)
    
    def test_setup_logger_handler_level(self):
        """Test that handler has correct level."""
        logger = setup_logger('test_logger_handler_level')
        
        handler = logger.handlers[0]
        assert handler.level == logging.INFO
    
    def test_setup_logger_formatter(self):
        """Test that logger has proper formatter."""
        logger = setup_logger('test_logger_formatter')
        
        handler = logger.handlers[0]
        formatter = handler.formatter
        
        assert formatter is not None
        assert isinstance(formatter, logging.Formatter)
        
        # Check formatter format string if it exists
        if formatter._fmt:
            assert '%(asctime)s' in formatter._fmt
            assert '%(name)s' in formatter._fmt
            assert '%(levelname)s' in formatter._fmt
            assert '%(message)s' in formatter._fmt
    
    def test_setup_logger_idempotent(self):
        """Test that calling setup_logger multiple times doesn't add duplicate handlers."""
        logger1 = setup_logger('test_logger_idempotent')
        initial_handler_count = len(logger1.handlers)
        
        logger2 = setup_logger('test_logger_idempotent')
        
        # Should be the same logger instance
        assert logger1 is logger2
        # Should not have added more handlers
        assert len(logger2.handlers) == initial_handler_count
    
    def test_setup_logger_different_names(self):
        """Test that different logger names create different loggers."""
        logger1 = setup_logger('logger_one')
        logger2 = setup_logger('logger_two')
        
        assert logger1 is not logger2
        assert logger1.name == 'logger_one'
        assert logger2.name == 'logger_two'
    
    def test_setup_logger_default_level(self):
        """Test that logger uses INFO level by default."""
        logger = setup_logger('test_logger_default')
        
        assert logger.level == logging.INFO
    
    def test_setup_logger_can_log(self):
        """Test that the logger can actually log messages."""
        logger = setup_logger('test_logger_logging')
        
        # This should not raise any exceptions
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        logger.debug("Test debug message")
        
        # All messages should be logged successfully
        assert True  # If we get here, no exceptions were raised 