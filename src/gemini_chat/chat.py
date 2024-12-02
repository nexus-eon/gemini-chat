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
        self._setup_gemini()
        self.chat: Any = self._create_chat()
        
    def _setup_gemini(self) -> None:
        """Configure Gemini with API key and generation settings."""
        genai.configure(api_key=self.settings.gemini_api_key)
        
    def _create_chat(self) -> Any:
        """Create and return a new chat session."""
        model = genai.GenerativeModel(
            model_name=self.settings.model_name,
            generation_config=self.settings.generation_config.model_dump()
        )
        return model.start_chat(history=[])
    
    def send_message(self, message: str) -> str:
        """Send a message to the model and return its response."""
        try:
            logger.debug("sending_message", message=message)
            response = self.chat.send_message(message)
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
        
        # Try to render as markdown, fallback to plain text
        try:
            console.print(Markdown(message))
        except Exception:
            console.print(message)
