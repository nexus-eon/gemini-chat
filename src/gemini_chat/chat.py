"""Chat session management."""
from typing import List, Dict, cast
import re

import structlog
import google.generativeai as genai  # type: ignore
from google.generativeai.types import GenerateContentResponse  # type: ignore
from google.api_core import exceptions  # type: ignore

from .config import Settings

logger = structlog.get_logger()

# Type aliases
Message = Dict[str, str]
History = List[Message]


class RateLimitError(Exception):
    """Raised when the API rate limit is exceeded."""
    pass


class ChatSession:
    """Manages a chat session with the Gemini model."""

    def __init__(self, settings: Settings) -> None:
        """Initialize a chat session."""
        try:
            logger.debug("initializing_chat_session",
                        api_key_length=len(settings.gemini_api_key.get_secret_value()),
                        model_name=settings.model_name)

            self.settings: Settings = settings
            self.history: History = []

            # Configure the Gemini API
            genai.configure(api_key=settings.gemini_api_key.get_secret_value())

            # Configure the Gemini model
            model = genai.GenerativeModel(
                model_name=settings.model_name,
                generation_config=settings.generation_config.model_dump())

            logger.debug("gemini_configured")

            # Start a chat
            logger.debug("creating_chat",
                        generation_config=settings.generation_config.model_dump())
            self.chat = model.start_chat()
            logger.debug("chat_created")

        except Exception as e:
            logger.error("initialization_error", error=str(e))
            raise

    def send_message(self, message: str) -> str:
        """Send a message to the model and return its response."""
        try:
            logger.debug("sending_message", message=message)
            response = self.chat.send_message(message)

            if not response or not isinstance(response, GenerateContentResponse):
                raise ValueError("Invalid response from model")

            # Cast the response text to str to satisfy mypy
            response_text = cast(str, response.text)

            # Store the message and response in history
            self.history.append({"role": "user", "content": message})
            self.history.append({"role": "assistant", "content": response_text})

            logger.debug("message_sent",
                        message=message,
                        response_length=len(response_text))
            return response_text

        except exceptions.ResourceExhausted as e:
            logger.warning("rate_limit_exceeded", error=str(e))
            # Extract wait time from error message if available
            wait_time_match = re.search(r'try again in about (\d+) \w+', str(e))
            wait_time = wait_time_match.group(1) if wait_time_match else "60"
            raise RateLimitError(f"Rate limit exceeded. Please try again in {wait_time} minutes.")

        except Exception as e:
            logger.error("message_error", error=str(e))
            raise

    def get_history(self) -> History:
        """Get the chat history."""
        return self.history.copy()
