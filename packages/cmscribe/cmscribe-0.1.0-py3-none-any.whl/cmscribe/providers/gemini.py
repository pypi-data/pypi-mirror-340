from typing import Any, Dict

import requests

from .base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini API provider for commit message generation."""

    def get_default_model(self) -> str:
        return "gemini-pro"

    def validate_config(self) -> bool:
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("Google API key is required")
        return True

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate a commit message using Google's Gemini API."""
        self.validate_config()

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.config["api_key"],
        }

        payload = {
            "contents": [{"parts": [{"text": self.format_prompt(diff_content)}]}],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens,
            },
        }

        try:
            response = requests.post(url=url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the commit message from the response
            commit_message = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return commit_message

        except requests.RequestException as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Gemini API response: {str(e)}")
