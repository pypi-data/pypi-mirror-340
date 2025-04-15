from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from cmscribe.core import CacheManager, CommitFormat


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the provider with configuration."""
        self.config = config
        self.cache_manager = CacheManager()
        self._context: Optional[Dict[str, Any]] = None
        self.model = config.get("model", self.get_default_model())
        self.max_tokens = int(config.get("max_tokens", 50))
        self.temperature = float(config.get("temperature", 0.7))
        self.commit_format = CommitFormat(config.get("commit_format", "conventional"))

    def _get_repo_name(self) -> str:
        """Get the current repository name."""
        from cmscribe.utils import get_repo_name

        try:
            return get_repo_name()
        except Exception:
            return "unknown"

    def _load_context(self) -> None:
        """Load context from cache if available."""
        if self._context is None:
            repo_name = self._get_repo_name()
            self._context = self.cache_manager.get_context(
                repo_name,
                self.__class__.__name__.lower().replace("provider", ""),
                self.model,
            )

    def _save_context(self, context: Dict[str, Any]) -> None:
        """Save context to cache."""
        self._context = context
        repo_name = self._get_repo_name()
        self.cache_manager.save_context(
            repo_name,
            self.__class__.__name__.lower().replace("provider", ""),
            self.model,
            context,
        )

    def clear_context(self) -> None:
        """Clear the cached context."""
        repo_name = self._get_repo_name()
        self.cache_manager.clear_context(
            repo_name,
            self.__class__.__name__.lower().replace("provider", ""),
            self.model,
        )
        self._context = None

    @abstractmethod
    def get_default_model(self) -> str:
        """Return the default model name for this provider."""
        pass

    @abstractmethod
    def generate_commit_message(self, diff_content: str) -> tuple:
        """Generate a commit message based on the git diff content."""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider's configuration."""
        pass

    def format_prompt(self, diff_content: str) -> str:
        """Format the prompt for commit message generation based on the selected format."""
        format_prompts = {
            CommitFormat.CONVENTIONAL: """Generate a Git commit message in the Conventional Commits format based on the following git diff.  

**Rules:**  
- Do **not** include explanations, reasoning, commit hashes, or anything extra.  
- Only return a **single line** in this format:  
  `<type>(optional scope): <message>`  
- Allowed types: feat, fix, chore, refactor, docs, test, ci, build.  

Git diff:
{diff}

**Example Output (nothing else!):**  
feat(app): add new method 'add'""",
            CommitFormat.SEMANTIC: """Generate a Git commit message in the Semantic Versioning format based on the following git diff.  

**Rules:**  
- Do **not** include explanations, reasoning, commit hashes, or anything extra.  
- Only return a **single line** in this format:  
  `<type>(scope): <message>`  
- Allowed types: major, minor, patch.  

Git diff:
{diff}

**Example Output (nothing else!):**  
minor(api): add new endpoint for user profiles""",
            CommitFormat.SIMPLE: """Generate a simple, clear Git commit message based on the following git diff.  

**Rules:**  
- Do **not** include explanations, reasoning, commit hashes, or anything extra.  
- Only return a **single line** with a clear description of the changes.  

Git diff:
{diff}

**Example Output (nothing else!):**  
Add user authentication system""",
            CommitFormat.ANGULAR: """Generate a Git commit message in the Angular format based on the following git diff.  

**Rules:**  
- Do **not** include explanations, reasoning, commit hashes, or anything extra.  
- Only return a **single line** in this format:  
  `<type>(scope): <message>`  
- Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore.  

Git diff:
{diff}

**Example Output (nothing else!):**  
feat(auth): implement JWT authentication""",
        }

        return format_prompts[self.commit_format].format(diff=diff_content)

    def get_supported_formats(self) -> List[CommitFormat]:
        """Return the list of commit message formats supported by this provider."""
        return list(CommitFormat)
