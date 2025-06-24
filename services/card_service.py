import os
import random
from typing import List, Optional
from models import TarotCard
from meanings import CARD_MEANINGS
from config import Config
from exceptions import InsufficientCardsError
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CardService:
    """Service responsible for managing tarot card operations."""
    
    def __init__(self):
        self.cards_folder = Config.CARDS_FOLDER
        logger.info(f"CardService initialized with cards folder: {self.cards_folder}")
    
    def get_available_cards(self) -> List[str]:
        """Get list of available card image files."""
        if not os.path.exists(self.cards_folder):
            logger.warning(f"Cards folder does not exist: {self.cards_folder}")
            return []
        
        card_files = [f for f in os.listdir(self.cards_folder) if f.endswith('.jpg')]
        logger.debug(f"Found {len(card_files)} card files")
        return card_files
    
    def draw_cards(self, count: int = 3) -> List[TarotCard]:
        """
        Draw a specified number of random tarot cards.
        
        Args:
            count: Number of cards to draw
            
        Returns:
            List of TarotCard objects
            
        Raises:
            InsufficientCardsError: When there are not enough cards available
        """
        card_files = self.get_available_cards()
        if len(card_files) < count:
            logger.error(f"Insufficient cards: need {count}, have {len(card_files)}")
            raise InsufficientCardsError(f"Not enough cards available. Need {count}, have {len(card_files)}")
        
        selected_cards = random.sample(card_files, count)
        logger.info(f"Drew {count} cards: {[card.replace('.jpg', '') for card in selected_cards]}")
        return [self._create_tarot_card(card_file) for card_file in selected_cards]
    
    def _create_tarot_card(self, card_file: str) -> TarotCard:
        """Create a TarotCard object from a file name."""
        card_key = card_file.replace('.jpg', '')
        card_name = card_key.replace('_', ' ').title()
        meaning = CARD_MEANINGS.get(card_key, "Unknown meaning")
        
        return TarotCard(
            image_path=f'/{self.cards_folder}/{card_file}',
            name=card_name,
            meaning=meaning,
            key=card_key
        ) 