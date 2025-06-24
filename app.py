from flask import Flask, render_template, jsonify
from config import Config
from controllers.tarot_controller import TarotController


def create_app() -> Flask:
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    
    # Validate configuration
    Config.validate()
    
    # Initialize controller
    tarot_controller = TarotController()
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html')
    
    @app.route('/draw_cards', methods=['GET'])
    def draw_cards():
        """Handle card drawing request."""
        response_data, status_code = tarot_controller.draw_cards()
        return jsonify(response_data), status_code
    
    return app


def main():
    """Main application entry point."""
    app = create_app()
    app.run(debug=Config.DEBUG)


if __name__ == '__main__':
    main()
