"""Test configuration module."""
from gemini_chat.config import GenerationConfig, get_settings


def test_generation_config_defaults():
    """Test GenerationConfig default values."""
    config = GenerationConfig()
    assert config.temperature == 1.0
    assert config.top_p == 0.95
    assert config.top_k == 64
    assert config.max_output_tokens == 8192
    assert config.response_mime_type == "text/plain"


def test_settings_cache():
    """Test settings caching."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2  # Should return the same cached instance
