from pathlib import Path
import logging
import yaml
from typing import Optional, Dict, Any
import os

class AIStructureConfig:
    """Manages AI documentation and structure configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the AI structure configuration.
        
        Args:
            config_path: Optional path to a custom config file.
        """
        self.base_dir = Path.cwd()
        self.config_dir = self.base_dir / "config"
        self.ai_docs_dir = self.base_dir / "ai-docs"
        self.logs_dir = self.base_dir / "logs"
        self.src_dir = self.base_dir / "src"
        
        # Create directory structure
        self._create_directory_structure()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Setup logging
        self._setup_logging()
    
    def _create_directory_structure(self) -> None:
        """Create the required directory structure."""
        directories = [
            # Main directories
            self.config_dir,
            self.ai_docs_dir,
            self.logs_dir,
            self.src_dir,
            
            # AI docs subdirectories
            self.ai_docs_dir / "voice" / "tts",
            self.ai_docs_dir / "voice" / "stt",
            self.ai_docs_dir / "calls" / "scenarios",
            self.ai_docs_dir / "calls" / "responses",
            self.ai_docs_dir / "comparisons",
            
            # Source code subdirectories
            self.src_dir / "setup",
            self.src_dir / "utils",
            
            # Configuration subdirectories
            self.config_dir / "templates",
            self.config_dir / "settings",
            
            # Logs subdirectories
            self.logs_dir / "voice-logs",
            self.logs_dir / "call-logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Optional path to config file. If not provided, uses default.
            
        Returns:
            Dict containing configuration values.
        """
        if config_path is None:
            config_path = self.config_dir / "settings" / "default_config.yaml"
            
        if not config_path.exists():
            # Create default configuration
            default_config = {
                "voice": {
                    "tts": {
                        "default_provider": "azure",
                        "voice_style": "professional",
                        "speaking_rate": 1.0
                    },
                    "stt": {
                        "default_provider": "azure",
                        "language": "is-IS"
                    }
                },
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            }
            
            # Ensure parent directory exists
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write default configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            
            return default_config
        
        # Load existing configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _setup_logging(self, log_level: Optional[str] = None) -> None:
        """
        Configure logging with specific handlers for different components.
        
        Args:
            log_level: Optional logging level to override config.
        """
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_level or log_config.get('level', 'INFO'))
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create formatters and handlers
        formatter = logging.Formatter(log_format)
        
        # Voice processing logger
        voice_logger = logging.getLogger('voice')
        voice_logger.setLevel(level)
        voice_handler = logging.FileHandler(self.logs_dir / 'voice-logs/processing.log')
        voice_handler.setFormatter(formatter)
        voice_logger.addHandler(voice_handler)
        
        # Call handling logger
        call_logger = logging.getLogger('calls')
        call_logger.setLevel(level)
        call_handler = logging.FileHandler(self.logs_dir / 'call-logs/handling.log')
        call_handler.setFormatter(formatter)
        call_logger.addHandler(call_handler)