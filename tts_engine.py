import os
from google.cloud import texttospeech
from google.oauth2 import service_account

class TTSEngine:
    def __init__(self):
        self.client = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Cloud using env credentials"""
        try:
            creds = service_account.Credentials.from_service_account_info(
                json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
            )
            return texttospeech.TextToSpeechClient(credentials=creds)
        except Exception as e:
            raise RuntimeError(f"Auth failed: {str(e)}")

    def synthesize(self, text: str, lang: str = 'is-IS') -> bytes:
        """Convert text to speech using Google's WaveNet model"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            name='is-IS-Wavenet-A'
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        return self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        ).audio_content
import os
from google.cloud import texttospeech
from google.auth import load_credentials_from_file

class TTSEngine:
    def __init__(self):
        self.client = self._init_client()
        
    def _init_client(self):
        """Initialize Google TTS client with credentials"""
        try:
            creds, _ = load_credentials_from_file(
                'config/google-credentials.json',
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            return texttospeech.TextToSpeechClient(credentials=creds)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize TTS client: {str(e)}")

    def generate_speech(self, text: str, language_code: str = 'is-IS',
                      voice_name: str = 'is-IS-Wavenet-A') -> bytes:
        """Generate speech audio from text"""
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return response.audio_content
import os
import json
from google.cloud import texttospeech
from google.oauth2 import service_account

class GoogleTTS:
    def __init__(self, config_path='config/google_tts.json'):
        self.config = self._load_config(config_path)
        self.client = self._authenticate()

    def _load_config(self, config_path):
        """Load TTS configuration from JSON file"""
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load TTS config: {str(e)}")

    def _authenticate(self):
        """Authenticate with Google Cloud using service account credentials"""
        try:
            creds = service_account.Credentials.from_service_account_info(
                self.config['service_account']
            )
            return texttospeech.TextToSpeechClient(credentials=creds)
        except Exception as e:
            raise RuntimeError(f"Authentication failed: {str(e)}")

    def synthesize(self, text, language='is-IS', voice_name='is-IS-Standard'):
        """Convert text to speech using Google TTS"""
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=voice_name
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
            
        except Exception as e:
            raise RuntimeError(f"TTS synthesis failed: {str(e)}")
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