import os
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.defaults = {
            "podcast_script": "podcast_script.md",
            "output_dir": "podcast_output",
            "tts_provider": "openai",
            "voices": {
                "kynnir": "echo",
                "gestur": "onyx"
            },
            "audio_settings": {
                "sample_rate": 44100,
                "bit_depth": 256
            }
        }
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from environment and config file"""
        # Load environment variables first
        env_config = {
            "openai_key": os.environ.get("OPENAI_API_KEY"),
            "elevenlabs_key": os.environ.get("ELEVENLABS_API_KEY"),
            "azure_key": os.environ.get("AZURE_SPEECH_KEY")
        }
        
        # Merge with file config if exists
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                file_config = json.load(f)
                return {**file_config, **env_config}
                
        return {**self.defaults, **env_config}

    def create_default_config(self) -> Dict[str, Any]:
        """Create default config file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.defaults, f, indent=2)
        return self.defaults

    def get(self, key: str, default=None) -> Any:
        """Get config value with env var override"""
        env_val = os.getenv(f"PODCAST_{key.upper()}")
        if env_val:
            try:
                return json.loads(env_val)
            except json.JSONDecodeError:
                return env_val
        return self.config.get(key, default)

    @property
    def podcast_script(self) -> Path:
        return Path(self.get("podcast_script"))

    @property
    def output_dir(self) -> Path:
        return Path(self.get("output_dir"))