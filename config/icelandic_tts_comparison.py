"""
Icelandic TTS Comparison Tool

Tests different TTS providers for Icelandic and saves samples for comparison.
"""
import os
import requests
import time
from pathlib import Path
import argparse
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Create output directory
OUTPUT_DIR = Path("icelandic_tts_samples")
OUTPUT_DIR.mkdir(exist_ok=True)

# Test text (add your preferred Icelandic text here)
TEST_TEXT = "Góðan daginn, þetta er prófun á íslensku talgervli. Hvernig hljómar þetta?"

def google_tts(text, output_path):
    """Google Cloud TTS for Icelandic"""
    try:
        from google.cloud import texttospeech
        
        # Check if credentials file exists
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            print("❌ Google Cloud: Missing GOOGLE_APPLICATION_CREDENTIALS in .env")
            return False
            
        # Initialize client
        client = texttospeech.TextToSpeechClient()
        
        # Build the voice request
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Icelandic voice
        voice = texttospeech.VoiceSelectionParams(
            language_code="is-IS",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        # Select audio format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # Perform the TTS request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        # Save the audio file
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
        
        print(f"✅ Google TTS: Audio saved to {output_path}")
        return True
    
    except ImportError:
        print("❌ Google Cloud: texttospeech library not installed. Run 'pip install google-cloud-texttospeech'")
        return False
    except Exception as e:
        print(f"❌ Google Cloud TTS error: {str(e)}")
        return False

def azure_tts(text, output_path):
    """Microsoft Azure TTS for Icelandic"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # Check for required environment variables
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        speech_region = os.environ.get("AZURE_SPEECH_REGION")
        
        if not speech_key or not speech_region:
            print("❌ Azure: Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION in .env")
            return False
        
        # Configure speech service
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        
        # Set Icelandic voice
        speech_config.speech_synthesis_voice_name = "is-IS-GudrunNeural" 
        
        # Create audio output config
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
        
        # Create synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        # Synthesize text
        result = speech_synthesizer.speak_text_async(text).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✅ Azure TTS: Audio saved to {output_path}")
            return True
        else:
            print(f"❌ Azure TTS failed: {result.reason}")
            return False
            
    except ImportError:
        print("❌ Azure: speech library not installed. Run 'pip install azure-cognitiveservices-speech'")
        return False
    except Exception as e:
        print(f"❌ Azure TTS error: {str(e)}")
        return False

def openai_tts(text, output_path):
    """OpenAI TTS with best Icelandic support"""
    try:
        import openai
        
        # Check API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI: Missing OPENAI_API_KEY in .env")
            return False
            
        client = openai.OpenAI(api_key=api_key)
        
        # Create and save audio file
        response = client.audio.speech.create(
            model="tts-1", # Best for Icelandic
            voice="alloy",
            input=text
        )
        
        response.stream_to_file(output_path)
        print(f"✅ OpenAI TTS: Audio saved to {output_path}")
        return True
        
    except ImportError:
        print("❌ OpenAI: library not installed. Run 'pip install openai'")
        return False
    except Exception as e:
        print(f"❌ OpenAI TTS error: {str(e)}")
        return False

def tiro_tts(text, output_path):
    """Tiro.is - Specialized Icelandic TTS"""
    try:
        # Check API key
        api_key = os.environ.get("TIRO_API_KEY")
        if not api_key:
            print("❌ Tiro: Missing TIRO_API_KEY in .env")
            return False
        
        # Prepare API request
        url = "https://api.tiro.is/v1/tts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "text": text,
            "voice": "Alfur" # Icelandic voice
        }
        
        # Make request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Tiro TTS: Audio saved to {output_path}")
            return True
        else:
            print(f"❌ Tiro TTS error: Status {response.status_code}, {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Tiro TTS error: {str(e)}")
        return False
    
def main():
    """Run tests for all TTS providers"""
    results = {}
    
    # Google Cloud TTS
    google_output = OUTPUT_DIR / "google_icelandic.mp3"
    results["Google"] = google_tts(TEST_TEXT, google_output)
    
    # Azure TTS
    azure_output = OUTPUT_DIR / "azure_icelandic.mp3"
    results["Azure"] = azure_tts(TEST_TEXT, azure_output)
    
    # OpenAI TTS
    openai_output = OUTPUT_DIR / "openai_icelandic.mp3"
    results["OpenAI"] = openai_tts(TEST_TEXT, openai_output)
    
    # Tiro TTS
    tiro_output = OUTPUT_DIR / "tiro_icelandic.mp3"
    results["Tiro"] = tiro_tts(TEST_TEXT, tiro_output)
    
    # Print summary
    print("\n--- TTS Comparison Results ---")
    for provider, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"{provider}: {status}")
    
    # Successful providers
    successful = [p for p, s in results.items() if s]
    if successful:
        print(f"\nSuccessfully generated {len(successful)} out of {len(results)} samples.")
        print(f"Audio samples saved to {OUTPUT_DIR.absolute()}")
        print("\nTo compare the audio samples, listen to the files in the output directory.")
    else:
        print("\nNo samples were successfully generated. Check the error messages above.")
        print("Make sure you have the required API keys in your .env file.")

if __name__ == "__main__":
    main()