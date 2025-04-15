import unittest
from unittest.mock import MagicMock, patch

from cmscribe.core.types import CommitFormat
from cmscribe.providers.anthropic import AnthropicProvider
from cmscribe.providers.azure_openai import AzureOpenAIProvider
from cmscribe.providers.base import AIProvider
from cmscribe.providers.gemini import GeminiProvider
from cmscribe.providers.huggingface import HuggingFaceProvider
from cmscribe.providers.ollama import OllamaProvider
from cmscribe.providers.openai import OpenAIProvider


class TestAIProvider(unittest.TestCase):
    """Test the base AIProvider class."""

    def setUp(self):
        self.config = {
            "model": "test-model",
            "max_tokens": 50,
            "temperature": 0.7,
            "commit_format": "conventional",
        }
        self.provider = AIProvider(self.config)

    def test_get_supported_formats(self):
        """Test that all commit formats are supported."""
        formats = self.provider.get_supported_formats()
        self.assertEqual(len(formats), len(CommitFormat))
        self.assertIn(CommitFormat.CONVENTIONAL, formats)
        self.assertIn(CommitFormat.SEMANTIC, formats)
        self.assertIn(CommitFormat.SIMPLE, formats)
        self.assertIn(CommitFormat.ANGULAR, formats)

    def test_format_prompt(self):
        """Test prompt formatting for different commit formats."""
        diff_content = "test diff"

        # Test conventional format
        self.provider.commit_format = CommitFormat.CONVENTIONAL
        prompt = self.provider.format_prompt(diff_content)
        self.assertIn("Conventional Commits format", prompt)
        self.assertIn(diff_content, prompt)

        # Test semantic format
        self.provider.commit_format = CommitFormat.SEMANTIC
        prompt = self.provider.format_prompt(diff_content)
        self.assertIn("Semantic Versioning format", prompt)
        self.assertIn(diff_content, prompt)

        # Test simple format
        self.provider.commit_format = CommitFormat.SIMPLE
        prompt = self.provider.format_prompt(diff_content)
        self.assertIn("simple, clear Git commit message", prompt)
        self.assertIn(diff_content, prompt)

        # Test angular format
        self.provider.commit_format = CommitFormat.ANGULAR
        prompt = self.provider.format_prompt(diff_content)
        self.assertIn("Angular format", prompt)
        self.assertIn(diff_content, prompt)


class TestOpenAIProvider(unittest.TestCase):
    """Test the OpenAI provider."""

    def setUp(self):
        self.config = {
            "api_key": "test-key",
            "model": "gpt-3.5-turbo",
            "max_tokens": 50,
            "temperature": 0.7,
        }
        self.provider = OpenAIProvider(self.config)

    def test_validate_config(self):
        """Test configuration validation."""
        # Test valid config
        self.assertTrue(self.provider.validate_config())

        # Test missing API key
        self.provider.config = {"model": "test"}
        with self.assertRaises(ValueError):
            self.provider.validate_config()

    @patch("requests.post")
    def test_generate_commit_message(self, mock_post):
        """Test commit message generation."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "feat(test): add test method"}}]
        }
        mock_post.return_value = mock_response

        # Test successful generation
        message = self.provider.generate_commit_message("test diff")
        self.assertEqual(message, "feat(test): add test method")

        # Test API error
        mock_post.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            self.provider.generate_commit_message("test diff")


class TestOllamaProvider(unittest.TestCase):
    """Test the Ollama provider."""

    def setUp(self):
        self.config = {
            "endpoint": "http://localhost:11434",
            "model": "llama2",
            "max_tokens": 50,
            "temperature": 0.7,
        }
        self.provider = OllamaProvider(self.config)

    def test_validate_config(self):
        """Test configuration validation."""
        # Test valid config
        self.assertTrue(self.provider.validate_config())

        # Test missing endpoint
        self.provider.config = {"model": "test"}
        with self.assertRaises(ValueError):
            self.provider.validate_config()

    @patch("requests.post")
    def test_generate_commit_message(self, mock_post):
        """Test commit message generation."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "feat(test): add test method"}
        mock_post.return_value = mock_response

        # Test successful generation
        message = self.provider.generate_commit_message("test diff")
        self.assertEqual(message, "feat(test): add test method")

        # Test API error
        mock_post.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            self.provider.generate_commit_message("test diff")


class TestAzureOpenAIProvider(unittest.TestCase):
    """Test the Azure OpenAI provider."""

    def setUp(self):
        self.config = {
            "api_key": "test-key",
            "endpoint": "https://test.openai.azure.com",
            "model": "gpt-35-turbo",
            "max_tokens": 50,
            "temperature": 0.7,
        }
        self.provider = AzureOpenAIProvider(self.config)

    def test_validate_config(self):
        """Test configuration validation."""
        # Test valid config
        self.assertTrue(self.provider.validate_config())

        # Test missing API key
        self.provider.config = {"endpoint": "https://test.openai.azure.com"}
        with self.assertRaises(ValueError):
            self.provider.validate_config()

        # Test missing endpoint
        self.provider.config = {"api_key": "test-key"}
        with self.assertRaises(ValueError):
            self.provider.validate_config()

    @patch("requests.post")
    def test_generate_commit_message(self, mock_post):
        """Test commit message generation."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "feat(test): add test method"}}]
        }
        mock_post.return_value = mock_response

        # Test successful generation
        message = self.provider.generate_commit_message("test diff")
        self.assertEqual(message, "feat(test): add test method")

        # Verify the API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn(
            "https://test.openai.azure.com/openai/deployments/gpt35turbo/chat/completions",
            call_args[0][0],
        )
        self.assertEqual(call_args[1]["headers"]["api-key"], "test-key")

        # Test API error
        mock_post.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            self.provider.generate_commit_message("test diff")

    def test_get_default_model(self):
        """Test default model name."""
        self.assertEqual(self.provider.get_default_model(), "gpt-35-turbo")

    def test_endpoint_formatting(self):
        """Test endpoint URL formatting."""
        # Test without trailing slash
        provider = AzureOpenAIProvider(
            {
                "api_key": "test-key",
                "endpoint": "https://test.openai.azure.com",
            }
        )
        self.assertEqual(provider.endpoint, "https://test.openai.azure.com/")

        # Test with trailing slash
        provider = AzureOpenAIProvider(
            {
                "api_key": "test-key",
                "endpoint": "https://test.openai.azure.com/",
            }
        )
        self.assertEqual(provider.endpoint, "https://test.openai.azure.com/")


if __name__ == "__main__":
    unittest.main()
