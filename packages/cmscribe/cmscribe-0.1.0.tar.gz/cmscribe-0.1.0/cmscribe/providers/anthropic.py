import requests

from .base import AIProvider


class AnthropicProvider(AIProvider):
    """Anthropic (Claude) API provider for commit message generation."""

    def get_default_model(self) -> str:
        return "claude-3-sonnet-20240229"

    def validate_config(self) -> bool:
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("Anthropic API key is required")
        return True

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate a commit message using Anthropic's API."""
        self.validate_config()

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.config["api_key"],
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": self.format_prompt(diff_content)}],
        }

        try:
            response = requests.post(url=url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the commit message from the response
            commit_message = result["content"][0]["text"].strip()
            return commit_message

        except requests.RequestException as e:
            raise Exception(f"Error calling Anthropic API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Anthropic API response: {str(e)}")
