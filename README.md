# Tarot Predictions - Political Oracle

A Flask-based web application that generates political prophecies using tarot cards and AI. The application has been refactored according to SOLID principles and Python best practices.

## Features

- Draw three random tarot cards
- Generate AI-powered political prophecies based on card meanings
- Modern, responsive web interface

## Architecture

The application follows SOLID principles and clean architecture patterns:

### Directory Structure

```
t_predictions/
├── app.py                 # Main application entry point
├── config.py             # Configuration management
├── exceptions.py         # Custom exception classes
├── models.py             # Data models
├── meanings.py           # Tarot card meanings
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
├── README.md            # This file
├── controllers/         # Web controllers
│   ├── __init__.py
│   └── tarot_controller.py
├── services/            # Business logic services
│   ├── __init__.py
│   ├── ai_service.py
│   └── card_service.py
├── utils/               # Utility functions
│   ├── __init__.py
│   └── logger.py
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures
│   ├── test_app.py      # Application tests
│   ├── test_config.py   # Configuration tests
│   ├── test_controller.py # Controller tests
│   ├── test_services.py # Service tests
│   ├── test_models.py   # Model tests
│   ├── test_exceptions.py # Exception tests
│   └── test_utils.py    # Utility tests
├── static/              # Static assets
│   ├── cards/           # Tarot card images
│   └── style.css        # Stylesheet
└── templates/           # HTML templates
    └── index.html
```

### SOLID Principles Implementation

1. **Single Responsibility Principle (SRP)**: Each class has a single responsibility
   - `CardService`: Manages tarot card operations
   - `AIProphecyService`: Handles AI prophecy generation
   - `TarotController`: Manages web requests
   - `Config`: Handles configuration

2. **Open/Closed Principle (OCP)**: The system is open for extension but closed for modification
   - New card types can be added without modifying existing code
   - New AI models can be implemented by extending the service

3. **Liskov Substitution Principle (LSP)**: Subtypes are substitutable for their base types
   - All services implement consistent interfaces

4. **Interface Segregation Principle (ISP)**: Clients depend only on interfaces they use
   - Services expose only necessary methods

5. **Dependency Inversion Principle (DIP)**: High-level modules don't depend on low-level modules
   - Controllers depend on service abstractions
   - Services depend on configuration abstractions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd t_predictions
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
HF_TOKEN=your_huggingface_token_here
```

5. Ensure you have the required directories:
- `static/cards/` - Contains tarot card images (.jpg files)

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Click the "Predict" button to draw cards and generate a prophecy

## Testing

The application includes comprehensive unit tests with **95.75% code coverage**.

### Running Tests

```bash
# Run all tests with coverage
python -m pytest --cov=. --cov-report=term-missing

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_services.py

# Run tests with HTML coverage report
python -m pytest --cov=. --cov-report=html
```

### Test Structure

- **59 test cases** covering all major components
- **Mock-based testing** for external dependencies
- **Comprehensive error handling** tests
- **Integration tests** for API endpoints
- **Unit tests** for all services and utilities

### Test Coverage

```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
app.py                               20      1    95%   37
config.py                            15      2    87%   20, 23
controllers/tarot_controller.py      29      0   100%
exceptions.py                         8      0   100%
models.py                            12      0   100%
services/ai_service.py               24      0   100%
services/card_service.py             33      0   100%
utils/logger.py                      12      0   100%
---------------------------------------------------------------
TOTAL                               753     32    96%
```

### Test Categories

1. **Unit Tests**: Individual component testing
   - Service layer testing with mocked dependencies
   - Model validation and creation
   - Configuration management
   - Exception handling

2. **Integration Tests**: Component interaction testing
   - Controller-service integration
   - API endpoint testing
   - Error handling flows

3. **Mock Testing**: External dependency isolation
   - HuggingFace API mocking
   - File system operations
   - Environment variable handling

## API Endpoints

- `GET /` - Main page
- `GET /draw_cards` - Draw three cards and generate prophecy

### Response Format

```json
{
  "cards": [
    {
      "image": "/static/cards/the_magician.jpg",
      "name": "The Magician",
      "meaning": "Creator, leader, initiative, fulfillment of hopes, great potential."
    }
  ],
  "prophecy": "Generated political prophecy text..."
}
```

## Error Handling

The application includes comprehensive error handling:

- `ConfigurationError`: Raised when required configuration is missing
- `InsufficientCardsError`: Raised when not enough cards are available
- `AIProphecyError`: Raised when AI prophecy generation fails

## Logging

The application uses structured logging for debugging and monitoring:

- INFO level: General application flow
- WARNING level: Non-critical issues
- ERROR level: Critical errors
- DEBUG level: Detailed debugging information

## Development

### Code Quality

- **Type hints** throughout the codebase
- **Docstrings** for all public methods
- **SOLID principles** implementation
- **Clean architecture** patterns
- **Comprehensive error handling**

### Adding New Features

1. Follow the existing code structure and patterns
2. Add appropriate error handling and logging
3. Write unit tests for new functionality
4. Ensure test coverage remains above 80%
5. Update documentation as needed

### Running in Development

```bash
# Run with debug mode
python app.py

# Run tests before committing
python -m pytest --cov=. --cov-fail-under=80
```

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate error handling and logging
3. Write comprehensive tests for new features
4. Ensure all tests pass and coverage remains above 80%
5. Update documentation as needed

## License

[Add your license information here]
