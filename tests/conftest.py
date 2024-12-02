"""Pytest configuration and fixtures."""
import pytest
from pydantic import SecretStr

from gemini_chat.config import GenerationConfig, Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return Settings(
        gemini_api_key=SecretStr("test_key"),
        model_name="test-model",
        generation_config=GenerationConfig(
            temperature=0.5,
            top_p=0.8,
            top_k=40,
            max_output_tokens=1000,
        ),
    )
