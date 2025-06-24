class TarotServiceError(Exception):
    """Base exception for tarot service errors."""
    pass


class InsufficientCardsError(TarotServiceError):
    """Raised when there are not enough cards available for drawing."""
    pass


class AIProphecyError(TarotServiceError):
    """Raised when AI prophecy generation fails."""
    pass


class ConfigurationError(TarotServiceError):
    """Raised when configuration is invalid or missing."""
    pass 