"""
Download a sample Icelandic audio file for testing STT models
"""
import requests
import os
from pathlib import Path

# Create directory for samples
SAMPLE_DIR = Path("icelandic_samples")
SAMPLE_DIR.mkdir(exist_ok=True)

# Sample URLs - Icelandic audio files
SAMPLES = [
    {
        "name": "icelandic_sample1.mp3",
        "url": "https://www.101languages.net/icelandic/wp-content/uploads/sites/83/2017/05/Icelandic-Lesson-1-Listen-to-the-Phrases.mp3"
    },
    {
        "name": "icelandic_sample2.mp3",
        "url": "https://gagnryni.is/wp-content/uploads/2020/04/Icelandic-for-Dummies-Lesson-1.mp3"
    }
]

def download_file(url, destination):
    """Download file from URL to destination"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def main():
    """Download sample files"""
    print("Downloading Icelandic audio samples...")
    
    success_count = 0
    for sample in SAMPLES:
        destination = SAMPLE_DIR / sample["name"]
        print(f"Downloading {sample['name']}...")
        
        if download_file(sample["url"], destination):
            print(f"✅ Successfully downloaded {destination}")
            success_count += 1
        else:
            print(f"❌ Failed to download {sample['name']}")
    
    print(f"\nDownloaded {success_count} of {len(SAMPLES)} samples to {SAMPLE_DIR.absolute()}")
    print("\nYou can use these samples to test STT models with the command:")
    print(f"python icelandic_stt_comparison.py {SAMPLE_DIR}/icelandic_sample1.mp3")

if __name__ == "__main__":
    main()