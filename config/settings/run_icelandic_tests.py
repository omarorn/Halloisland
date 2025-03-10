"""
Complete Icelandic TTS and STT Testing Suite

This script:
1. Downloads Icelandic audio files from Google Drive
2. Runs TTS comparison tests
3. Runs STT comparison tests on the downloaded files
"""
import os
import subprocess
import sys
from pathlib import Path
import argparse

def check_env_file():
    """Check if .env file exists and has API keys"""
    if not os.path.exists(".env"):
        print("Creating .env file from template...")
        if os.path.exists(".env.icelandic"):
            subprocess.run(["cp", ".env.icelandic", ".env"])
            print("Created .env file. Please edit it to add your API keys.")
            print("Then run this script again.")
            return False
        else:
            print("Error: .env.icelandic template file not found.")
            return False
    
    # Basic check if API keys are set
    with open(".env", "r") as f:
        env_content = f.read()
        
    if "your_api_key" in env_content or "your_azure_speech_key" in env_content:
        print("Warning: .env file contains placeholder API keys.")
        print("Please edit .env file to add your actual API keys.")
        
        user_input = input("Continue anyway? (y/n): ")
        if user_input.lower() != "y":
            return False
    
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements_icelandic.txt"
        ], check=True)
        print("Successfully installed requirements.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def download_from_gdrive():
    """Download files from Google Drive"""
    print("\n--- Downloading files from Google Drive ---")
    
    # Check if files already downloaded
    if os.path.exists("helloiceland_files") and len(os.listdir("helloiceland_files")) > 0:
        print("helloiceland_files directory already contains files.")
        user_input = input("Download again? (y/n): ")
        if user_input.lower() != "y":
            return True
    
    # Try rclone method first (easier)
    try:
        print("Attempting download using rclone...")
        subprocess.run([
            sys.executable, "download_with_rclone.py"
        ], check=True)
        
        # Check if download was successful
        if os.path.exists("helloiceland_files") and len(os.listdir("helloiceland_files")) > 0:
            print("Successfully downloaded files using rclone.")
            return True
        else:
            print("rclone download failed or found no files.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("rclone method failed.")
    
    # Fall back to Google Drive API method
    try:
        print("\nAttempting download using Google Drive API...")
        subprocess.run([
            sys.executable, "download_from_gdrive.py"
        ], check=True)
        
        # Check if download was successful
        if os.path.exists("helloiceland_files") and len(os.listdir("helloiceland_files")) > 0:
            print("Successfully downloaded files using Google Drive API.")
            return True
        else:
            print("Google Drive API download failed or found no files.")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Both download methods failed.")
        return False

def run_tts_comparison():
    """Run TTS comparison tests"""
    print("\n--- Running Text-to-Speech Comparison ---")
    
    try:
        subprocess.run([
            sys.executable, "icelandic_tts_comparison.py"
        ], check=True)
        print("TTS comparison completed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running TTS comparison: {e}")
        return False

def run_stt_comparison():
    """Run STT comparison tests"""
    print("\n--- Running Speech-to-Text Comparison ---")
    
    # Get audio files
    audio_files = []
    
    # Check downloaded files first
    if os.path.exists("helloiceland_files"):
        for file in os.listdir("helloiceland_files"):
            if file.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')):
                audio_files.append(os.path.join("helloiceland_files", file))
    
    # If no files from Google Drive, check sample files
    if not audio_files and os.path.exists("icelandic_samples"):
        for file in os.listdir("icelandic_samples"):
            if file.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')):
                audio_files.append(os.path.join("icelandic_samples", file))
    
    # If still no files, download samples
    if not audio_files:
        print("No audio files found. Downloading samples...")
        try:
            subprocess.run([
                sys.executable, "download_sample_audio.py"
            ], check=True)
            
            if os.path.exists("icelandic_samples"):
                for file in os.listdir("icelandic_samples"):
                    if file.lower().endswith(('.wav', '.mp3', '.ogg', '.flac')):
                        audio_files.append(os.path.join("icelandic_samples", file))
        except subprocess.CalledProcessError:
            print("Error downloading sample audio.")
    
    # Run STT comparison on each audio file
    if audio_files:
        print(f"Found {len(audio_files)} audio files for testing.")
        success = True
        
        for audio_file in audio_files:
            print(f"\nTesting with {audio_file}...")
            try:
                subprocess.run([
                    sys.executable, "icelandic_stt_comparison.py", audio_file
                ], check=True)
            except subprocess.CalledProcessError:
                print(f"Error processing {audio_file}")
                success = False
        
        return success
    else:
        print("No audio files found for testing.")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Icelandic TTS and STT Testing Suite")
    parser.add_argument("--tts-only", action="store_true", help="Run only TTS tests")
    parser.add_argument("--stt-only", action="store_true", help="Run only STT tests")
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading files from Google Drive")
    parser.add_argument("--skip-install", action="store_true", help="Skip installing requirements")
    args = parser.parse_args()
    
    print("=== Icelandic TTS and STT Testing Suite ===")
    
    # Check environment
    if not check_env_file():
        return
    
    # Install requirements
    if not args.skip_install:
        if not install_requirements():
            return
    
    # Download files from Google Drive
    if not args.skip_download and not args.tts_only:
        download_from_gdrive()
    
    # Run tests
    if not args.stt_only:
        run_tts_comparison()
    
    if not args.tts_only:
        run_stt_comparison()
    
    print("\n=== Testing Complete ===")
    print("Results:")
    if not args.stt_only and os.path.exists("icelandic_tts_samples"):
        print(f"- TTS samples: {Path('icelandic_tts_samples').absolute()}")
    if not args.tts_only and os.path.exists("icelandic_stt_results"):
        print(f"- STT results: {Path('icelandic_stt_results').absolute()}")

if __name__ == "__main__":
    main()