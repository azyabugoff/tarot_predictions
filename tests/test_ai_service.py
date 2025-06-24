import pytest
from unittest.mock import patch, Mock
from services.ai_service import AIProphecyService
from exceptions import AIProphecyError


class TestAIProphecyService:
    """Test cases for AIProphecyService."""
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_ai_service_initialization(self):
        """Test AIProphecyService initialization."""
        with patch('services.ai_service.InferenceClient') as mock_client:
            service = AIProphecyService()
            mock_client.assert_called_once_with("HuggingFaceH4/zephyr-7b-alpha", token='test_token')
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_generate_prophecy_success(self):
        """Test successful prophecy generation."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {"content": "Test prophecy content"}
        mock_client.chat_completion.return_value = mock_response
        
        with patch('services.ai_service.InferenceClient', return_value=mock_client):
            service = AIProphecyService()
            
            card_infos = [
                "The Magician: Creator, leader, initiative, fulfillment of hopes, great potential.",
                "The Empress: Mother, protector, birth of the new, joy of life.",
                "The Emperor: Father, power, responsibility, structure, order."
            ]
            
            result = service.generate_prophecy(card_infos)
            
            assert result == "Test prophecy content"
            mock_client.chat_completion.assert_called_once()
            
            # Check that the prompt was built correctly
            call_args = mock_client.chat_completion.call_args
            messages = call_args[1]['messages']
            assert len(messages) == 1
            assert messages[0]['role'] == 'user'
            assert 'mystical political oracle' in messages[0]['content']
            assert 'The Magician: Creator, leader' in messages[0]['content']
            assert 'The Empress: Mother, protector' in messages[0]['content']
            assert 'The Emperor: Father, power' in messages[0]['content']
            assert call_args[1]['temperature'] == 0.7
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_generate_prophecy_api_error(self):
        """Test prophecy generation when API fails."""
        mock_client = Mock()
        mock_client.chat_completion.side_effect = Exception("API Error")
        
        with patch('services.ai_service.InferenceClient', return_value=mock_client):
            service = AIProphecyService()
            
            card_infos = ["The Magician: Test meaning"]
            
            with pytest.raises(AIProphecyError, match="Failed to generate prophecy: API Error"):
                service.generate_prophecy(card_infos)
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_build_prompt(self):
        """Test prompt building functionality."""
        mock_client = Mock()
        
        with patch('services.ai_service.InferenceClient', return_value=mock_client):
            service = AIProphecyService()
            
            card_infos = [
                "The Magician: Creator, leader, initiative, fulfillment of hopes, great potential.",
                "The Empress: Mother, protector, birth of the new, joy of life."
            ]
            
            prompt = service._build_prompt(card_infos)
            
            assert "mystical political oracle" in prompt
            assert "political prophecy" in prompt
            assert "3-5 sentences" in prompt
            assert "Do not mention the cards directly" in prompt
            assert "simple english speech" in prompt
            assert "The Magician: Creator, leader, initiative, fulfillment of hopes, great potential." in prompt
            assert "The Empress: Mother, protector, birth of the new, joy of life." in prompt
            assert prompt.endswith("\n\nProphecy:")
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_generate_prophecy_empty_cards(self):
        """Test prophecy generation with empty card list."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {"content": "Empty prophecy"}
        mock_client.chat_completion.return_value = mock_response
        
        with patch('services.ai_service.InferenceClient', return_value=mock_client):
            service = AIProphecyService()
            
            result = service.generate_prophecy([])
            
            assert result == "Empty prophecy"
            mock_client.chat_completion.assert_called_once()
            
            # Check that the prompt was built correctly even with empty cards
            call_args = mock_client.chat_completion.call_args
            messages = call_args[1]['messages']
            assert "mystical political oracle" in messages[0]['content']
            assert "Here are the cards:\n\n" in messages[0]['content']
    
    @patch('config.Config.HF_TOKEN', 'test_token')
    def test_generate_prophecy_single_card(self):
        """Test prophecy generation with single card."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = {"content": "Single card prophecy"}
        mock_client.chat_completion.return_value = mock_response
        
        with patch('services.ai_service.InferenceClient', return_value=mock_client):
            service = AIProphecyService()
            
            card_infos = ["The Magician: Creator, leader, initiative, fulfillment of hopes, great potential."]
            
            result = service.generate_prophecy(card_infos)
            
            assert result == "Single card prophecy"
            mock_client.chat_completion.assert_called_once()
            
            # Check that the prompt contains the single card
            call_args = mock_client.chat_completion.call_args
            messages = call_args[1]['messages']
            assert "The Magician: Creator, leader, initiative, fulfillment of hopes, great potential." in messages[0]['content'] 