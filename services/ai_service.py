import traceback
from typing import List
from huggingface_hub import InferenceClient
from config import Config
from exceptions import AIProphecyError
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AIProphecyService:
    """Service responsible for generating AI prophecies based on tarot cards."""
    
    def __init__(self):
        self.client = InferenceClient("HuggingFaceH4/zephyr-7b-alpha", token=Config.HF_TOKEN)
    
    def generate_prophecy(self, card_infos: List[str]) -> str:
        """
        Generate a political prophecy based on tarot card information.
        
        Args:
            card_infos: List of card descriptions with meanings
            
        Returns:
            Generated prophecy text
        """
        prompt = self._build_prompt(card_infos)
        
        try:
            logger.info("Generating AI prophecy...")
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            prophecy = response.choices[0].message["content"].strip()
            logger.info("AI prophecy generated successfully")
            return prophecy
        except Exception as e:
            logger.error(f"Error generating prophecy: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise AIProphecyError(f"Failed to generate prophecy: {str(e)}")
    
    def _build_prompt(self, card_infos: List[str]) -> str:
        """Build the prompt for AI prophecy generation."""
        return (
            "You are a mystical political oracle. Based on the following three tarot cards and their meanings, "
            "generate a short political prophecy (3-5 sentences) that describes possible future global or geopolitical events. "
            "Do not mention the cards directly in the text. "
            "Use simple english speech with easy-reading constructions. "
            "Here are the cards:\n\n" +
            "\n".join(card_infos) +
            "\n\nProphecy:"
        )