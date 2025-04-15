"""Azure OpenAI provider for commit message generation."""

import os
from typing import Any, Dict

import requests

from .base import AIProvider


class AzureOpenAIProvider(AIProvider):
    """Azure OpenAI provider for commit message generation."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = config.get("endpoint") or os.getenv("AZURE_OPENAI_ENDPOINT")
        if not self.endpoint.endswith("/"):
            self.endpoint += "/"

    def get_default_model(self) -> str:
        """Return the default model name for this provider."""
        return "gpt-35-turbo"

    def validate_config(self) -> bool:
        """Validate the provider's configuration."""
        if not self.api_key:
            raise ValueError("Azure OpenAI API key is required")
        if not self.endpoint:
            raise ValueError("Azure OpenAI endpoint is required")
        return True

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate a commit message based on the git diff content."""
        self.validate_config()

        # Format the prompt based on the selected commit format
        prompt = self.format_prompt(diff_content)

        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        # Azure OpenAI requires the deployment name in the URL
        deployment_name = self.model.replace(".", "")  # Remove dots from model name
        url = f"{self.endpoint}openai/deployments/{deployment_name}/chat/completions?api-version=2024-02-15-preview"

        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates Git commit messages based on code diffs.",
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate commit message: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response from Azure OpenAI API: {str(e)}")
