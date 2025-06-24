import os
from dotenv import load_dotenv
from typing import Optional
from exceptions import ConfigurationError

load_dotenv()


class Config:
    """Configuration class to handle all application settings."""
    
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
    CARDS_FOLDER: str = 'static/cards'
    RANDOM_IMAGES_FOLDER: str = 'static/random_images'
    DEBUG: bool = True
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.HF_TOKEN:
            raise ConfigurationError("HF_TOKEN environment variable is required")
        
        if not os.path.exists(cls.CARDS_FOLDER):
            raise ConfigurationError(f"Cards folder '{cls.CARDS_FOLDER}' does not exist")
        
        if not os.path.exists(cls.RANDOM_IMAGES_FOLDER):
            raise ConfigurationError(f"Random images folder '{cls.RANDOM_IMAGES_FOLDER}' does not exist") 