from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TarotCard:
    """Represents a tarot card with its properties."""
    image_path: str
    name: str
    meaning: str
    key: str


@dataclass
class CardReading:
    """Represents a complete tarot card reading."""
    cards: List[TarotCard]
    random_image: str
    prophecy: str
