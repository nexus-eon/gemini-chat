"""Test configuration and fixtures."""
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

from gemini_chat.config import Settings


@pytest.fixture
def mock_settings() -> Settings:
    """Create mock settings for testing."""
    return Settings(
        gemini_api_key=SecretStr("test-key"),
        model_name="test-model",
        log_level="DEBUG"
    )


@pytest.fixture
def mock_chat() -> Generator[MagicMock, None, None]:
    """Create a mock chat instance."""
    with patch('gemini_chat.chat.ChatSession') as mock:
        yield mock


@pytest.fixture
def mock_response() -> MagicMock:
    """Create a mock response object."""
    response = MagicMock()
    response.text = "Test response"
    return response
