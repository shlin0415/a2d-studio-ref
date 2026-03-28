"""
Configuration loader for dialogue server
Reads from .env and provides defaults
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration for dialogue generation server"""

    def __init__(self, env_path: Optional[Path] = None):
        """Load configuration from .env file"""
        if env_path is None:
            # Look for .env in parent of dialogue-server
            env_path = Path(__file__).parent.parent.parent / ".env"

        self.env_path = env_path
        self._load_env()

    def _load_env(self):
        """Load environment variables from .env file"""
        if self.env_path.exists():
            with open(self.env_path, "r", encoding="utf-8") as f:
                for line in f:
                    # Remove comments
                    if "#" in line:
                        line = line[: line.index("#")]

                    line = line.strip()
                    if not line:
                        continue

                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip('"').strip("'")

                        # Handle variable substitution ${VAR}
                        import re

                        value = re.sub(
                            r"\$\{([^}]+)\}",
                            lambda m: os.environ.get(m.group(1), ""),
                            value,
                        )

                        os.environ[key] = value

    @property
    def api_key(self) -> str:
        """Get API key from environment"""
        return os.environ.get("DIALOGUE_API_KEY", os.environ.get("DS_LLM_API_KEY", ""))

    @property
    def model(self) -> str:
        """Get model from environment"""
        return os.environ.get(
            "DIALOGUE_MODEL", os.environ.get("DS_LLM_MODEL_ID", "gpt-3.5-turbo")
        )

    @property
    def base_url(self) -> str:
        """Get API base URL"""
        return os.environ.get(
            "DIALOGUE_BASE_URL",
            os.environ.get("DS_LLM_BASE_URL", "https://api.openai.com/v1"),
        )

    @property
    def max_sentences(self) -> int:
        """Get max sentences per character"""
        return int(os.environ.get("DIALOGUE_MAX_SENTENCES", "5"))

    @property
    def languages(self) -> str:
        """Get target languages"""
        return os.environ.get("DIALOGUE_LANGUAGES", "zh,ja")

    @property
    def translate_mode(self) -> str:
        """Get translation mode: 'inline' (LLM outputs both) or 'posthoc' (separate translate step)"""
        return os.environ.get("TRANSLATE_MODE", "inline")

    @property
    def gpt_sovits_url(self) -> str:
        """Get GPT-SoVITS API URL"""
        return os.environ.get("GPT_SOVITS_URL", "http://127.0.0.1:31801")

    def get(self, key: str, default: str = "") -> str:
        """Get any environment variable"""
        return os.environ.get(key, default)
