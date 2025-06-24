from exceptions import (
    TarotServiceError,
    InsufficientCardsError,
    AIProphecyError,
    ConfigurationError
)


class TestExceptions:
    """Test cases for custom exceptions."""
    
    def test_tarot_service_error_inheritance(self):
        """Test that TarotServiceError inherits from Exception."""
        error = TarotServiceError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
    
    def test_insufficient_cards_error_inheritance(self):
        """Test that InsufficientCardsError inherits from TarotServiceError."""
        error = InsufficientCardsError("Not enough cards")
        assert isinstance(error, TarotServiceError)
        assert isinstance(error, Exception)
        assert str(error) == "Not enough cards"
    
    def test_ai_prophecy_error_inheritance(self):
        """Test that AIProphecyError inherits from TarotServiceError."""
        error = AIProphecyError("AI failed")
        assert isinstance(error, TarotServiceError)
        assert isinstance(error, Exception)
        assert str(error) == "AI failed"
    
    def test_configuration_error_inheritance(self):
        """Test that ConfigurationError inherits from TarotServiceError."""
        error = ConfigurationError("Config invalid")
        assert isinstance(error, TarotServiceError)
        assert isinstance(error, Exception)
        assert str(error) == "Config invalid"
    
    def test_exception_hierarchy(self):
        """Test that all exceptions can be caught by base TarotServiceError."""
        errors = [
            InsufficientCardsError("Test 1"),
            AIProphecyError("Test 2"),
            ConfigurationError("Test 3")
        ]
        
        for error in errors:
            assert isinstance(error, TarotServiceError)
            assert isinstance(error, Exception) 