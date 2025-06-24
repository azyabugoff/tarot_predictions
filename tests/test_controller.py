import pytest
from unittest.mock import patch, Mock
from controllers.tarot_controller import TarotController
from models import TarotCard
from exceptions import InsufficientCardsError, AIProphecyError, TarotServiceError


class TestTarotController:
    """Test cases for TarotController."""
    
    def test_controller_initialization(self):
        """Test TarotController initialization."""
        with patch('controllers.tarot_controller.CardService') as mock_card_service:
            with patch('controllers.tarot_controller.AIProphecyService') as mock_ai_service:
                controller = TarotController()
                
                mock_card_service.assert_called_once()
                mock_ai_service.assert_called_once()
                assert hasattr(controller, 'card_service')
                assert hasattr(controller, 'ai_service')
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_success(self, mock_card_service_class, mock_ai_service_class):
        """Test successful card drawing."""
        # Mock card service
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        
        # Mock AI service
        mock_ai_service = Mock()
        mock_ai_service_class.return_value = mock_ai_service
        
        # Create test cards
        test_cards = [
            TarotCard(
                image_path="/static/cards/the_magician.jpg",
                name="The Magician",
                meaning="Creator, leader, initiative, fulfillment of hopes, great potential.",
                key="the_magician"
            ),
            TarotCard(
                image_path="/static/cards/the_empress.jpg",
                name="The Empress",
                meaning="Mother, protector, birth of the new, joy of life.",
                key="the_empress"
            ),
            TarotCard(
                image_path="/static/cards/the_emperor.jpg",
                name="The Emperor",
                meaning="Father, power, responsibility, structure, order.",
                key="the_emperor"
            )
        ]
        
        mock_card_service.draw_cards.return_value = test_cards
        mock_ai_service.generate_prophecy.return_value = "Test prophecy content"
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        assert status_code == 200
        assert 'cards' in response_data
        assert 'prophecy' in response_data
        assert len(response_data['cards']) == 3
        assert response_data['prophecy'] == "Test prophecy content"
        
        # Check card data structure
        assert response_data['cards'][0]['image'] == "/static/cards/the_magician.jpg"
        assert response_data['cards'][0]['name'] == "The Magician"
        assert response_data['cards'][0]['meaning'] == "Creator, leader, initiative, fulfillment of hopes, great potential."
        
        # Verify service calls
        mock_card_service.draw_cards.assert_called_once_with(3)
        mock_ai_service.generate_prophecy.assert_called_once()
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_insufficient_cards_error(self, mock_card_service_class, mock_ai_service_class):
        """Test handling of InsufficientCardsError."""
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        mock_card_service.draw_cards.side_effect = InsufficientCardsError("Not enough cards")
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        assert status_code == 500
        assert 'error' in response_data
        assert response_data['error'] == "Not enough cards"
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_ai_prophecy_error(self, mock_card_service_class, mock_ai_service_class):
        """Test handling of AIProphecyError with fallback."""
        # Mock card service
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        
        # Mock AI service
        mock_ai_service = Mock()
        mock_ai_service_class.return_value = mock_ai_service
        
        # Create test cards
        test_cards = [
            TarotCard(
                image_path="/static/cards/the_magician.jpg",
                name="The Magician",
                meaning="Creator, leader, initiative, fulfillment of hopes, great potential.",
                key="the_magician"
            ),
            TarotCard(
                image_path="/static/cards/the_empress.jpg",
                name="The Empress",
                meaning="Mother, protector, birth of the new, joy of life.",
                key="the_empress"
            ),
            TarotCard(
                image_path="/static/cards/the_emperor.jpg",
                name="The Emperor",
                meaning="Father, power, responsibility, structure, order.",
                key="the_emperor"
            )
        ]
        
        mock_card_service.draw_cards.return_value = test_cards
        mock_ai_service.generate_prophecy.side_effect = AIProphecyError("AI failed")
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        # Should return 200 with fallback prophecy
        assert status_code == 200
        assert 'cards' in response_data
        assert 'prophecy' in response_data
        assert response_data['prophecy'] == "The oracle is silent... (AI error)"
        assert len(response_data['cards']) == 3
        
        # Should have called draw_cards twice (once for initial attempt, once for fallback)
        assert mock_card_service.draw_cards.call_count == 2
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_general_tarot_service_error(self, mock_card_service_class, mock_ai_service_class):
        """Test handling of general TarotServiceError."""
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        mock_card_service.draw_cards.side_effect = TarotServiceError("General service error")
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        assert status_code == 500
        assert 'error' in response_data
        assert response_data['error'] == "General service error"
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_unexpected_error(self, mock_card_service_class, mock_ai_service_class):
        """Test handling of unexpected errors."""
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        mock_card_service.draw_cards.side_effect = Exception("Unexpected error")
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        assert status_code == 500
        assert 'error' in response_data
        assert "Unexpected error" in response_data['error']
    
    def test_card_to_dict(self):
        """Test converting TarotCard to dictionary."""
        controller = TarotController()
        
        card = TarotCard(
            image_path="/static/cards/test.jpg",
            name="Test Card",
            meaning="Test meaning",
            key="test_card"
        )
        
        card_dict = controller._card_to_dict(card)
        
        assert card_dict['image'] == "/static/cards/test.jpg"
        assert card_dict['name'] == "Test Card"
        assert card_dict['meaning'] == "Test meaning"
    
    @patch('controllers.tarot_controller.AIProphecyService')
    @patch('controllers.tarot_controller.CardService')
    def test_draw_cards_empty_cards(self, mock_card_service_class, mock_ai_service_class):
        """Test drawing cards with empty result."""
        mock_card_service = Mock()
        mock_card_service_class.return_value = mock_card_service
        mock_card_service.draw_cards.return_value = []
        
        mock_ai_service = Mock()
        mock_ai_service_class.return_value = mock_ai_service
        mock_ai_service.generate_prophecy.return_value = "Empty prophecy"
        
        controller = TarotController()
        response_data, status_code = controller.draw_cards()
        
        assert status_code == 200
        assert 'cards' in response_data
        assert 'prophecy' in response_data
        assert len(response_data['cards']) == 0
        assert response_data['prophecy'] == "Empty prophecy" 