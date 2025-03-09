"""
Icelandic Speech-to-Text (STT) Comparison Tool

Tests different STT providers for Icelandic using audio samples and compares the transcription results.
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
OUTPUT_DIR = Path("icelandic_stt_results")
OUTPUT_DIR.mkdir(exist_ok=True)

def google_stt(audio_file):
    """Google Cloud Speech-to-Text for Icelandic"""
    try:
        from google.cloud import speech
        
        # Check if credentials file exists
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            print("❌ Google Cloud: Missing GOOGLE_APPLICATION_CREDENTIALS in .env")
            return None
            
        # Create the client
        client = speech.SpeechClient()
        
        # Read the audio file
        with open(audio_file, "rb") as audio_file:
            content = audio_file.read()
        
        # Configure audio
        audio = speech.RecognitionAudio(content=content)
        
        # Configure recognition request
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="is-IS",
            model="default"
        )
        
        # Detect speech
        response = client.recognize(config=config, audio=audio)
        
        # Get transcription
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript
        
        if transcription:
            print(f"✅ Google STT: Successfully transcribed")
            return transcription
        else:
            print("❌ Google STT: No transcript produced")
            return None
    
    except ImportError:
        print("❌ Google Cloud: speech library not installed. Run 'pip install google-cloud-speech'")
        return None
    except Exception as e:
        print(f"❌ Google Cloud STT error: {str(e)}")
        return None

def azure_stt(audio_file):
    """Microsoft Azure STT for Icelandic"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # Check for required environment variables
        speech_key = os.environ.get("AZURE_SPEECH_KEY")
        speech_region = os.environ.get("AZURE_SPEECH_REGION")
        
        if not speech_key or not speech_region:
            print("❌ Azure: Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION in .env")
            return None
        
        # Configure speech service
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_recognition_language = "is-IS"
        
        # Create audio configuration
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        
        # Create recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        # Recognize speech
        result = speech_recognizer.recognize_once_async().get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"✅ Azure STT: Successfully transcribed")
            return result.text
        else:
            print(f"❌ Azure STT failed: {result.reason}")
            return None
            
    except ImportError:
        print("❌ Azure: speech library not installed. Run 'pip install azure-cognitiveservices-speech'")
        return None
    except Exception as e:
        print(f"❌ Azure STT error: {str(e)}")
        return None

def whisper_stt(audio_file):
    """OpenAI Whisper STT for Icelandic"""
    try:
        import openai
        
        # Check API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI: Missing OPENAI_API_KEY in .env")
            return None
            
        client = openai.OpenAI(api_key=api_key)
        
        # Create transcript
        with open(audio_file, "rb") as audio:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="is"
            )
        
        if response.text:
            print(f"✅ OpenAI Whisper: Successfully transcribed")
            return response.text
        else:
            print("❌ OpenAI Whisper: No transcript produced")
            return None
        
    except ImportError:
        print("❌ OpenAI: library not installed. Run 'pip install openai'")
        return None
    except Exception as e:
        print(f"❌ OpenAI Whisper error: {str(e)}")
        return None

def whisper_local_stt(audio_file):
    """Local Whisper model for Icelandic"""
    try:
        from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
        import torch
        import librosa
        import numpy as np
        
        # Load model
        print("Loading whisper model...")
        processor = AutoProcessor.from_pretrained("carlosdanielhernandezmena/whisper-large-icelandic-10k-steps-1000h")
        model = AutoModelForSpeechSeq2Seq.from_pretrained("carlosdanielhernandezmena/whisper-large-icelandic-10k-steps-1000h")
        
        # Load audio
        waveform, sample_rate = librosa.load(audio_file, sr=16000)
        
        # Process audio
        input_features = processor(waveform, sampling_rate=16000, return_tensors="pt").input_features
        
        # Generate token ids
        predicted_ids = model.generate(input_features)
        
        # Decode token ids to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        if transcription:
            print(f"✅ Local Whisper: Successfully transcribed")
            return transcription
        else:
            print("❌ Local Whisper: No transcript produced")
            return None
        
    except ImportError:
        print("❌ Local Whisper: Required libraries not installed. Run 'pip install torch transformers librosa'")
        return None
    except Exception as e:
        print(f"❌ Local Whisper error: {str(e)}")
        return None

def process_audio(audio_file):
    """Process an audio file through all STT providers"""
    results = {}
    
    # Google Cloud STT
    print(f"\nTesting Google Cloud STT with {audio_file}...")
    results["Google"] = google_stt(audio_file)
    
    # Azure STT
    print(f"\nTesting Azure STT with {audio_file}...")
    results["Azure"] = azure_stt(audio_file)
    
    # OpenAI Whisper
    print(f"\nTesting OpenAI Whisper with {audio_file}...")
    results["OpenAI Whisper"] = whisper_stt(audio_file)
    
    # Local Whisper
    print(f"\nTesting Local Whisper with {audio_file}...")
    results["Local Whisper"] = whisper_local_stt(audio_file)
    
    return results

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Icelandic STT Comparison Tool")
    parser.add_argument("audio_file", help="Path to Icelandic audio file (preferably WAV format)")
    args = parser.parse_args()
    
    audio_file = args.audio_file
    if not os.path.exists(audio_file):
        print(f"Error: Audio file {audio_file} not found")
        return
    
    # Process audio
    print(f"Processing {audio_file}...")
    results = process_audio(audio_file)
    
    # Save results
    output_file = OUTPUT_DIR / f"results_{Path(audio_file).stem}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Display results
    print("\n--- STT Comparison Results ---")
    for provider, transcript in results.items():
        if transcript:
            print(f"\n{provider}:")
            print(f"  {transcript}")
    
    # Successful providers
    successful = [p for p, t in results.items() if t]
    print(f"\nSuccessfully transcribed with {len(successful)} out of {len(results)} providers.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Check if arguments provided
    import sys
    if len(sys.argv) < 2:
        print("Usage: python icelandic_stt_comparison.py <audio_file>")
        print("Example: python icelandic_stt_comparison.py sample.wav")
        sys.exit(1)
    
    main()