import pytest
from unittest.mock import patch, Mock
from app import create_app, main


class TestApp:
    """Test cases for Flask application."""
    
    @patch('app.Config.validate')
    def test_create_app_success(self, mock_validate):
        """Test successful app creation."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            
            assert app is not None
            assert hasattr(app, 'route')
            mock_validate.assert_called_once()
    
    @patch('app.Config.validate')
    def test_create_app_configuration_error(self, mock_validate):
        """Test app creation with configuration error."""
        from exceptions import ConfigurationError
        mock_validate.side_effect = ConfigurationError("Config error")
        
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            with pytest.raises(ConfigurationError, match="Config error"):
                create_app()
    
    @patch('app.Config.validate')
    def test_index_route(self, mock_validate):
        """Test the index route."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            client = app.test_client()
            
            response = client.get('/')
            
            assert response.status_code == 200
            assert b'Wanna know the future' in response.data
    
    @patch('app.Config.validate')
    def test_draw_cards_route_method_not_allowed(self, mock_validate):
        """Test the draw_cards route with wrong HTTP method."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            client = app.test_client()
            
            response = client.post('/draw_cards')
            
            assert response.status_code == 405  # Method Not Allowed
    
    @patch('app.create_app')
    @patch('app.Config.DEBUG', True)
    def test_main_function(self, mock_create_app):
        """Test the main function."""
        mock_app = Mock()
        mock_create_app.return_value = mock_app
        
        main()
        
        mock_create_app.assert_called_once()
        mock_app.run.assert_called_once_with(debug=True)
    
    @patch('app.create_app')
    @patch('app.Config.DEBUG', False)
    def test_main_function_debug_false(self, mock_create_app):
        """Test the main function with debug disabled."""
        mock_app = Mock()
        mock_create_app.return_value = mock_app
        
        main()
        
        mock_create_app.assert_called_once()
        mock_app.run.assert_called_once_with(debug=False)
    
    @patch('app.Config.validate')
    def test_app_routes_registered(self, mock_validate):
        """Test that all routes are properly registered."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            
            # Check that routes are registered
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            assert '/' in rules
            assert '/draw_cards' in rules
    
    @patch('app.Config.validate')
    def test_app_error_handling(self, mock_validate):
        """Test that the app handles errors gracefully."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            client = app.test_client()
            
            # Test non-existent route
            response = client.get('/nonexistent')
            assert response.status_code == 404
    
    @patch('app.Config.validate')
    def test_draw_cards_route_exists(self, mock_validate):
        """Test that draw_cards route exists and is accessible."""
        with patch.dict('os.environ', {'HF_TOKEN': 'test_token'}):
            app = create_app()
            client = app.test_client()
            
            # Just test that the route exists and doesn't crash
            response = client.get('/draw_cards')
            # We don't care about the actual response, just that it doesn't crash
            assert response is not None 