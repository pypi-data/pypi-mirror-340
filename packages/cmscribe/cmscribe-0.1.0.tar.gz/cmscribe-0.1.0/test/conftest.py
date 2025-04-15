"""Test configuration and fixtures."""

import pytest

from cmscribe.core.config import DEFAULT_CONFIG_PATH, create_config


@pytest.fixture
def test_config(tmp_path):
    """Create a temporary config file for testing."""
    config_path = tmp_path / "test_config.ini"
    create_config(config_path)
    return config_path


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com")
