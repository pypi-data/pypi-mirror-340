import requests

from .base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI API provider for commit message generation."""

    def get_default_model(self) -> str:
        return "gpt-3.5-turbo"

    def validate_config(self) -> bool:
        api_key = self.config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        return True

    def generate_commit_message(self, diff_content: str) -> str:
        """Generate a commit message using OpenAI's API."""
        self.validate_config()

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates concise commit messages.",
                },
                {"role": "user", "content": self.format_prompt(diff_content)},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        try:
            response = requests.post(url=url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # Extract the commit message from the response
            commit_message = result["choices"][0]["message"]["content"].strip()
            return commit_message

        except requests.RequestException as e:
            raise Exception(f"Error calling OpenAI API: {e!s}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing OpenAI API response: {e!s}")
