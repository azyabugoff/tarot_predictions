import pytest
import os
import tempfile
from unittest.mock import patch, Mock
from services.card_service import CardService
from models import TarotCard
from exceptions import InsufficientCardsError


class TestCardService:
    """Test cases for CardService."""
    
    def test_card_service_initialization(self):
        """Test CardService initialization."""
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            assert service.cards_folder == '/test/cards'
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_available_cards_success(self, mock_listdir, mock_exists):
        """Test getting available cards successfully."""
        mock_exists.return_value = True
        mock_listdir.return_value = ['the_magician.jpg', 'the_empress.jpg', 'not_a_card.txt']
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            cards = service.get_available_cards()
            
            assert cards == ['the_magician.jpg', 'the_empress.jpg']
            mock_exists.assert_called_once_with('/test/cards')
            mock_listdir.assert_called_once_with('/test/cards')
    
    @patch('os.path.exists')
    def test_get_available_cards_folder_not_exists(self, mock_exists):
        """Test getting available cards when folder doesn't exist."""
        mock_exists.return_value = False
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            cards = service.get_available_cards()
            
            assert cards == []
            mock_exists.assert_called_once_with('/test/cards')
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_draw_cards_success(self, mock_listdir, mock_exists):
        """Test drawing cards successfully."""
        mock_exists.return_value = True
        mock_listdir.return_value = ['the_magician.jpg', 'the_empress.jpg', 'the_emperor.jpg']
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            with patch('random.sample') as mock_sample:
                mock_sample.return_value = ['the_magician.jpg', 'the_empress.jpg', 'the_emperor.jpg']
                
                service = CardService()
                cards = service.draw_cards(3)
                
                assert len(cards) == 3
                assert all(isinstance(card, TarotCard) for card in cards)
                assert cards[0].name == "The Magician"
                assert cards[1].name == "The Empress"
                assert cards[2].name == "The Emperor"
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_draw_cards_insufficient_cards(self, mock_listdir, mock_exists):
        """Test drawing cards when there are insufficient cards."""
        mock_exists.return_value = True
        mock_listdir.return_value = ['the_magician.jpg']  # Only 1 card available
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            
            with pytest.raises(InsufficientCardsError, match="Not enough cards available. Need 3, have 1"):
                service.draw_cards(3)
    
    @patch('os.path.exists')
    def test_draw_cards_no_folder(self, mock_exists):
        """Test drawing cards when cards folder doesn't exist."""
        mock_exists.return_value = False
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            
            with pytest.raises(InsufficientCardsError, match="Not enough cards available. Need 3, have 0"):
                service.draw_cards(3)
    
    def test_create_tarot_card(self):
        """Test creating a TarotCard from file name."""
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            
            card = service._create_tarot_card('the_magician.jpg')
            
            assert isinstance(card, TarotCard)
            assert card.image_path == '//test/cards/the_magician.jpg'
            assert card.name == "The Magician"
            assert card.meaning == "Creator, leader, initiative, fulfillment of hopes, great potential."
            assert card.key == "the_magician"
    
    def test_create_tarot_card_unknown_meaning(self):
        """Test creating a TarotCard with unknown meaning."""
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            
            card = service._create_tarot_card('unknown_card.jpg')
            
            assert isinstance(card, TarotCard)
            assert card.image_path == '//test/cards/unknown_card.jpg'
            assert card.name == "Unknown Card"
            assert card.meaning == "Unknown meaning"
            assert card.key == "unknown_card"
    
    def test_create_tarot_card_with_underscores(self):
        """Test creating a TarotCard with underscores in name."""
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            service = CardService()
            
            card = service._create_tarot_card('wheel_of_fortune.jpg')
            
            assert isinstance(card, TarotCard)
            assert card.name == "Wheel Of Fortune"
            assert card.key == "wheel_of_fortune"
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_draw_cards_default_count(self, mock_listdir, mock_exists):
        """Test drawing cards with default count (3)."""
        mock_exists.return_value = True
        mock_listdir.return_value = ['card1.jpg', 'card2.jpg', 'card3.jpg', 'card4.jpg', 'card5.jpg']
        
        with patch('config.Config.CARDS_FOLDER', '/test/cards'):
            with patch('random.sample') as mock_sample:
                mock_sample.return_value = ['card1.jpg', 'card2.jpg', 'card3.jpg']
                
                service = CardService()
                cards = service.draw_cards()  # Default count
                
                assert len(cards) == 3
                mock_sample.assert_called_once_with(['card1.jpg', 'card2.jpg', 'card3.jpg', 'card4.jpg', 'card5.jpg'], 3) 