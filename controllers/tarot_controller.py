from typing import Dict, Any
from models import TarotCard
from services.card_service import CardService
from services.ai_service import AIProphecyService
from exceptions import TarotServiceError, InsufficientCardsError, AIProphecyError


class TarotController:
    """Controller responsible for handling tarot-related web requests."""
    
    def __init__(self):
        self.card_service = CardService()
        self.ai_service = AIProphecyService()
    
    def draw_cards(self) -> tuple[Dict[str, Any], int]:
        """
        Handle the draw cards request.
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Draw cards
            cards = self.card_service.draw_cards(3)
            
            # Get random image
            random_image = self.card_service.get_random_image()
            
            # Generate prophecy
            card_infos = [f"{card.name}: {card.meaning}" for card in cards]
            prophecy = self.ai_service.generate_prophecy(card_infos)
            
            # Create response
            response_data = {
                'cards': [self._card_to_dict(card) for card in cards],
                'random_image': random_image,
                'prophecy': prophecy
            }
            
            return response_data, 200
            
        except InsufficientCardsError as e:
            return {'error': str(e)}, 500
        except AIProphecyError as e:
            # Fallback to a default prophecy if AI fails
            prophecy = "The oracle is silent... (AI error)"
            cards = self.card_service.draw_cards(3)
            random_image = self.card_service.get_random_image()
            
            response_data = {
                'cards': [self._card_to_dict(card) for card in cards],
                'random_image': random_image,
                'prophecy': prophecy
            }
            return response_data, 200
        except TarotServiceError as e:
            return {'error': str(e)}, 500
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}, 500
    
    def _card_to_dict(self, card: TarotCard) -> Dict[str, str]:
        """Convert TarotCard to dictionary for JSON response."""
        return {
            'image': card.image_path,
            'name': card.name,
            'meaning': card.meaning
        } 