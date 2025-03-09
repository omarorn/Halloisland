"""
Generate an Icelandic podcast demo using the provided script
"""
import os
import json
import time
import re
from pathlib import Path
import argparse

# Constants
PODCAST_SCRIPT = Path("/home/azureuser/helloiceland/texttovoice/podcasttest.md")
OUTPUT_DIR = Path("podcast_demo")
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_speaking_parts(markdown_text):
    """Extract speaking parts from markdown script"""
    # Define patterns for speakers
    patterns = {
        "KYNNIR": r'🎙\s+\*\*Kynnir:\*\*\s*(.*?)(?=\n\n|\n[👨🎙]|\n\*\(|$)',
        "GESTUR": r'👨‍💻\s+\*\*Gestur:\*\*\s*(.*?)(?=\n\n|\n[👨🎙]|\n\*\(|$)',
    }
    
    segments = []
    
    # Process the markdown text
    lines = markdown_text.split('\n')
    current_segment = None
    segment_name = ""
    
    for line in lines:
        # Check for segment headers
        if line.startswith("## **[Segment") or line.startswith("## **[Intro") or line.startswith("## **[Outro"):
            match = re.search(r'## \*\*\[(.*?):', line)
            if match:
                segment_name = match.group(1)
                current_segment = {"segment": segment_name, "parts": []}
                segments.append(current_segment)
        
        # Extract speaking parts
        for speaker, pattern in patterns.items():
            matches = re.findall(pattern, line)
            if matches and current_segment:
                for text in matches:
                    current_segment["parts"].append({
                        "speaker": speaker,
                        "text": text.strip()
                    })
    
    return segments

def test_openai_tts(text, output_file, api_key, voice="alloy"):
    """Generate TTS using OpenAI API"""
    try:
        import openai
        
        # Set API key
        os.environ["OPENAI_API_KEY"] = api_key
        client = openai.OpenAI()
        
        print(f"Generating TTS for text ({len(text)} chars)...")
        start_time = time.time()
        
        # Generate speech
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Save to file
        response.stream_to_file(str(output_file))
        
        elapsed_time = time.time() - start_time
        
        if output_file.exists():
            file_size = output_file.stat().st_size / 1024  # KB
            print(f"✅ Generated {file_size:.2f} KB audio in {elapsed_time:.2f} seconds")
            return {
                "file": str(output_file),
                "duration": elapsed_time,
                "size_kb": file_size
            }
        else:
            print("❌ Failed to generate audio file")
            return None
            
    except Exception as e:
        print(f"❌ TTS error: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate Icelandic podcast demo")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--segment", type=int, help="Generate specific segment only (1-3, 0 for intro, 4 for outro)")
    parser.add_argument("--kynnir-voice", default="echo", help="Voice for the presenter (kynnir)")
    parser.add_argument("--gestur-voice", default="onyx", help="Voice for the guest (gestur)")
    
    args = parser.parse_args()
    
    # Get OpenAI API key
    api_key = args.openai_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: No OpenAI API key provided")
        print("Please provide a key with --openai-key or set the OPENAI_API_KEY environment variable")
        return
    
    # Read podcast script
    if not PODCAST_SCRIPT.exists():
        print(f"Error: Podcast script not found at {PODCAST_SCRIPT}")
        return
    
    with open(PODCAST_SCRIPT, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    # Extract speaking parts
    segments = extract_speaking_parts(script_text)
    
    if not segments:
        print("Error: No segments found in the script")
        return
    
    print(f"Found {len(segments)} segments in the script:")
    for i, segment in enumerate(segments):
        print(f"{i}. {segment['segment']} - {len(segment['parts'])} parts")
    
    # Generate selected segment or all
    target_segments = [args.segment] if args.segment is not None else range(len(segments))
    
    for seg_idx in target_segments:
        if 0 <= seg_idx < len(segments):
            segment = segments[seg_idx]
            print(f"\nGenerating audio for segment: {segment['segment']}")
            
            segment_dir = OUTPUT_DIR / f"segment_{seg_idx}"
            segment_dir.mkdir(exist_ok=True)
            
            # Generate each part
            part_files = []
            for i, part in enumerate(segment['parts']):
                speaker = part['speaker']
                text = part['text']
                
                # Select voice based on speaker
                voice = args.kynnir_voice if speaker == "KYNNIR" else args.gestur_voice
                
                output_file = segment_dir / f"{i:02d}_{speaker.lower()}.mp3"
                result = test_openai_tts(text, output_file, api_key, voice)
                
                if result:
                    part_files.append(result)
            
            # Save segment metadata
            metadata = {
                "segment": segment["segment"],
                "parts": part_files
            }
            
            with open(segment_dir / "metadata.json", 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"Generated {len(part_files)} audio files for segment {seg_idx}")
        else:
            print(f"Error: Segment {seg_idx} not found")
    
    print("\nPodcast generation complete!")
    print(f"Output files are in: {OUTPUT_DIR.absolute()}")

if __name__ == "__main__":
    main()