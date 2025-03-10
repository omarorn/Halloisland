from abc import ABC, abstractmethod
from pathlib import Path
import os
import time
import json
from typing import Optional, Dict
from src.setup.config_manager import ConfigManager

class TTSProvider(ABC):
    """Abstract base class for TTS providers"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
    
    @abstractmethod
    def generate_speech(self, text: str, output_file: Path, voice: str) -> Optional[Dict]:
        pass

class OpenAITTS(TTSProvider):
    """OpenAI TTS implementation"""
    
    def generate_speech(self, text: str, output_file: Path, voice: str) -> Optional[Dict]:
        try:
            import openai
            client = openai.OpenAI(api_key=self._get_api_key())
            
            start_time = time.time()
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            response.stream_to_file(str(output_file))
            return self._create_result(output_file, start_time)
            
        except Exception as e:
            print(f"OpenAI TTS error: {str(e)}")
            return None

    def _get_api_key(self) -> str:
        return self.config.get("openai_key") or os.environ.get("OPENAI_API_KEY", "")

    def _create_result(self, output_file: Path, start_time: float) -> Dict:
        return {
            "file": str(output_file),
            "duration": time.time() - start_time,
            "size_kb": output_file.stat().st_size / 1024,
            "provider": "openai"
        }

class TTSFactory:
    """Factory class for creating TTS providers"""
    
    @staticmethod
    def create_provider(config: ConfigManager) -> TTSProvider:
        provider = config.get("tts_provider", "openai").lower()
        
        if provider == "openai":
            return OpenAITTS(config)
        # Add other providers here
        else:
            raise ValueError(f"Unsupported TTS provider: {provider}")