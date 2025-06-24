import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from flask import Flask
from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test cards directory
        cards_dir = os.path.join(temp_dir, 'static', 'cards')
        os.makedirs(cards_dir, exist_ok=True)
        
        # Create some test card files
        test_cards = ['the_magician.jpg', 'the_empress.jpg', 'the_emperor.jpg']
        for card in test_cards:
            with open(os.path.join(cards_dir, card), 'w') as f:
                f.write('test image content')
        
        # Mock environment variables
        with patch.dict(os.environ, {'HF_TOKEN': 'test_token'}):
            # Mock the config to use test directories
            with patch('config.Config.CARDS_FOLDER', cards_dir):
                with patch('config.Config.validate'):
                    app = create_app()
                    app.config['TESTING'] = True
                    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def mock_hf_client():
    """Mock HuggingFace client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = {"content": "Test prophecy content"}
    mock_client.chat_completion.return_value = mock_response
    return mock_client


@pytest.fixture
def sample_cards():
    """Sample tarot cards for testing."""
    return [
        {
            'image': '/static/cards/the_magician.jpg',
            'name': 'The Magician',
            'meaning': 'Creator, leader, initiative, fulfillment of hopes, great potential.',
            'key': 'the_magician'
        },
        {
            'image': '/static/cards/the_empress.jpg',
            'name': 'The Empress',
            'meaning': 'Mother, protector, birth of the new, joy of life.',
            'key': 'the_empress'
        },
        {
            'image': '/static/cards/the_emperor.jpg',
            'name': 'The Emperor',
            'meaning': 'Father, power, responsibility, structure, order.',
            'key': 'the_emperor'
        }
    ] 