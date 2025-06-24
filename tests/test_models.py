from models import TarotCard, CardReading


class TestTarotCard:
    """Test cases for TarotCard model."""
    
    def test_tarot_card_creation(self):
        """Test creating a TarotCard instance."""
        card = TarotCard(
            image_path="/static/cards/the_magician.jpg",
            name="The Magician",
            meaning="Creator, leader, initiative, fulfillment of hopes, great potential.",
            key="the_magician"
        )
        
        assert card.image_path == "/static/cards/the_magician.jpg"
        assert card.name == "The Magician"
        assert card.meaning == "Creator, leader, initiative, fulfillment of hopes, great potential."
        assert card.key == "the_magician"
    
    def test_tarot_card_attributes(self):
        """Test that TarotCard has all required attributes."""
        card = TarotCard(
            image_path="test.jpg",
            name="Test Card",
            meaning="Test meaning",
            key="test_card"
        )
        
        # Check that all attributes are present
        assert hasattr(card, 'image_path')
        assert hasattr(card, 'name')
        assert hasattr(card, 'meaning')
        assert hasattr(card, 'key')


class TestCardReading:
    """Test cases for CardReading model."""
    
    def test_card_reading_creation(self):
        """Test creating a CardReading instance."""
        cards = [
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
            )
        ]
        
        reading = CardReading(
            cards=cards,
            prophecy="Test prophecy content"
        )
        
        assert len(reading.cards) == 2
        assert reading.cards[0].name == "The Magician"
        assert reading.cards[1].name == "The Empress"
        assert reading.prophecy == "Test prophecy content"
    
    def test_card_reading_empty_cards(self):
        """Test creating a CardReading with empty cards list."""
        reading = CardReading(
            cards=[],
            prophecy="Empty reading"
        )
        
        assert len(reading.cards) == 0
        assert reading.prophecy == "Empty reading"
    
    def test_card_reading_attributes(self):
        """Test that CardReading has all required attributes."""
        reading = CardReading(
            cards=[],
            prophecy="Test"
        )
        
        # Check that all attributes are present
        assert hasattr(reading, 'cards')
        assert hasattr(reading, 'prophecy') 