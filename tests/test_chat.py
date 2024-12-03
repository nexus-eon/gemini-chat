"""Test chat functionality."""
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from google.generativeai.types import GenerateContentResponse  # type: ignore
from pydantic import SecretStr

from gemini_chat.chat import ChatSession
from gemini_chat.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Create test settings."""
    return Settings(
        gemini_api_key=SecretStr("test-key"),
        model_name="test-model"
    )


@pytest.fixture
async def mock_model() -> AsyncGenerator[MagicMock, None]:
    """Create a mock Gemini model."""
    with patch('google.generativeai.GenerativeModel') as mock:
        mock_chat = MagicMock()
        mock_chat.send_message = AsyncMock(return_value=MagicMock(
            text="Test response"
        ))
        mock.return_value.start_chat.return_value = mock_chat
        yield mock


@pytest.mark.asyncio
async def test_chat_session_init(settings: Settings, mock_model: MagicMock) -> None:
    """Test ChatSession initialization."""
    session = ChatSession(settings)
    assert session.settings == settings
    assert session.history == []
    mock_model.assert_called_once_with(
        model_name=settings.model_name,
        generation_config=settings.generation_config.model_dump(),
        api_key=settings.gemini_api_key.get_secret_value()
    )


@pytest.mark.asyncio
async def test_chat_session_send_message(settings: Settings, mock_model: MagicMock) -> None:
    """Test sending a message."""
    session = ChatSession(settings)
    response = await session.send_message("Hello")
    assert response == "Test response"
    assert len(session.history) == 2
    assert session.history[0] == {"role": "user", "content": "Hello"}
    assert session.history[1] == {"role": "assistant", "content": "Test response"}


@pytest.mark.asyncio
async def test_chat_session_send_message_error(settings: Settings) -> None:
    """Test error handling when sending a message."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_chat = MagicMock()
        mock_chat.send_message = AsyncMock(side_effect=Exception("Test error"))
        mock_model.return_value.start_chat.return_value = mock_chat

        session = ChatSession(settings)
        with pytest.raises(Exception, match="Test error"):
            await session.send_message("Hello")


@pytest.mark.asyncio
async def test_chat_session_invalid_response(settings: Settings) -> None:
    """Test handling of invalid response from model."""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_chat = MagicMock()
        mock_chat.send_message = AsyncMock(return_value=None)
        mock_model.return_value.start_chat.return_value = mock_chat

        session = ChatSession(settings)
        with pytest.raises(ValueError, match="Invalid response from model"):
            await session.send_message("Hello")


def test_chat_session_get_history(settings: Settings) -> None:
    """Test getting chat history."""
    session = ChatSession(settings)
    history = session.get_history()
    assert history == []
    assert history is not session.history  # Should return a copy
