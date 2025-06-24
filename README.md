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

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```
HF_TOKEN=your_huggingface_token_here
```

4. Ensure you have the required directories:
- `static/cards/` - Contains tarot card images (.jpg files)

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Click the "Predict" button to draw cards and generate a prophecy

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

## Testing

To run tests (if implemented):
```bash
python -m pytest tests/
```

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate error handling and logging
3. Update documentation as needed
4. Ensure all tests pass

## License

[Add your license information here]
