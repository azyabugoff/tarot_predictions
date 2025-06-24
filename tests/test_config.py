import pytest
import os
from unittest.mock import patch
from config import Config
from exceptions import ConfigurationError


class TestConfig:
    """Test cases for Config class."""
    
    def test_config_default_values(self):
        """Test that config has expected default values."""
        assert Config.CARDS_FOLDER == 'static/cards'
        assert Config.DEBUG is True
    
    def test_config_hf_token_attribute(self):
        """Test that HF_TOKEN attribute exists."""
        assert hasattr(Config, 'HF_TOKEN')
    
    def test_config_validate_method_exists(self):
        """Test that validate method exists."""
        assert hasattr(Config, 'validate')
        assert callable(Config.validate)
    
    @patch('os.path.exists')
    def test_validate_success_mocked(self, mock_exists):
        """Test successful configuration validation with mocked dependencies."""
        mock_exists.return_value = True
        
        # Mock the HF_TOKEN to be present
        with patch.object(Config, 'HF_TOKEN', 'test_token'):
            # Should not raise any exception
            Config.validate()
    
    @patch('os.path.exists')
    def test_validate_missing_token_mocked(self, mock_exists):
        """Test validation fails when HF_TOKEN is missing (mocked)."""
        mock_exists.return_value = True
        
        # Mock the HF_TOKEN to be None
        with patch.object(Config, 'HF_TOKEN', None):
            with pytest.raises(ConfigurationError, match="HF_TOKEN environment variable is required"):
                Config.validate()
    
    @patch('os.path.exists')
    def test_validate_missing_cards_folder_mocked(self, mock_exists):
        """Test validation fails when cards folder doesn't exist (mocked)."""
        mock_exists.side_effect = [False, True]  # Cards folder doesn't exist
        
        # Mock the HF_TOKEN to be present
        with patch.object(Config, 'HF_TOKEN', 'test_token'):
            with pytest.raises(ConfigurationError, match="Cards folder 'static/cards' does not exist"):
                Config.validate()
    
    def test_config_class_attributes(self):
        """Test that all required config attributes exist."""
        required_attrs = ['HF_TOKEN', 'CARDS_FOLDER', 'DEBUG']
        for attr in required_attrs:
            assert hasattr(Config, attr) 