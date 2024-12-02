"""Chat functionality implementation."""
from typing import Any, Optional

import google.generativeai as genai  # type: ignore
import structlog
from rich.console import Console
from rich.markdown import Markdown

from .config import Settings, get_settings

logger = structlog.get_logger()
console = Console()


class ChatSession:
    """Manages a chat session with the Gemini model."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        """Initialize chat session."""
        self.settings = settings or get_settings()
        logger.debug("initializing_chat_session", 
                    model_name=self.settings.model_name,
                    api_key_length=len(self.settings.gemini_api_key) if self.settings.gemini_api_key else 0)
        self._setup_gemini()
        self.chat: Any = self._create_chat()
        
    def _setup_gemini(self) -> None:
        """Configure Gemini with API key and generation settings."""
        try:
            genai.configure(api_key=self.settings.gemini_api_key)
            logger.debug("gemini_configured")
        except Exception as e:
            logger.error("gemini_configuration_error", error=str(e))
            raise
        
    def _create_chat(self) -> Any:
        """Create and return a new chat session."""
        try:
            generation_config = self.settings.generation_config.model_dump()
            logger.debug("creating_chat", generation_config=generation_config)
            
            model = genai.GenerativeModel(
                model_name=self.settings.model_name,
                generation_config=generation_config
            )
            chat = model.start_chat(history=[])
            logger.debug("chat_created")
            return chat
        except Exception as e:
            logger.error("chat_creation_error", error=str(e))
            raise
    
    def send_message(self, message: str) -> str:
        """Send a message to the model and return its response."""
        try:
            logger.debug("sending_message", message=message)
            response = self.chat.send_message(message)
            if not response or not response.text:
                logger.error("empty_response")
                raise ValueError("Received empty response from Gemini")
            
            logger.debug("received_response", response=response.text)
            return str(response.text)
        except Exception as e:
            logger.error("message_error", error=str(e))
            raise

    def display_message(self, message: str, is_user: bool = False) -> None:
        """Display a message in the console with proper formatting."""
        prefix = "You:" if is_user else "Gemini:"
        style = "bold cyan" if is_user else "bold green"
        console.print(f"\n{prefix}", style=style)
        
        # Handle markdown formatting for bot responses
        if not is_user:
            console.print(Markdown(message))
        else:
            console.print(message)
