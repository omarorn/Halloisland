# Icelandic Voice Services Comparison

This project provides tools to compare different Text-to-Speech (TTS) and Speech-to-Text (STT) services for the Icelandic language. It includes implementation and testing scripts for:

- OpenAI Whisper and TTS (baseline we've already tested)
- Azure Speech Services
- ElevenLabs TTS and Scribe STT
- Optimized local TTS solution

## Setup

1. **Clone the repository** (if you haven't already)

2. **Install required dependencies**:
   ```bash
   # The comparison scripts will install dependencies automatically
   # but you can also install them beforehand:
   pip install python-dotenv openai requests azure-cognitiveservices-speech pyttsx3
   ```

3. **Configure API keys**:
   ```bash
   # Copy the template file
   cp .env.icelandic .env
   
   # Edit the .env file with your API keys
   nano .env
   ```

## Running TTS Comparison

The `compare_icelandic_tts_services.py` script compares different TTS services with the same Icelandic text samples.

```bash
# Test all services with all sample texts
python compare_icelandic_tts_services.py

# Test specific services only
python compare_icelandic_tts_services.py --services azure elevenlabs

# Test with a specific sample
python compare_icelandic_tts_services.py --sample podcast
```

Sample texts included:
- `short`: A short phrase in Icelandic
- `medium`: A medium-length paragraph
- `podcast`: An excerpt from a podcast script

## Running STT Comparison

The `compare_icelandic_stt_services.py` script compares different STT services with the same Icelandic audio sample.

```bash
# Test all services with the default audio sample
python compare_icelandic_stt_services.py

# Test specific services only
python compare_icelandic_stt_services.py --services azure elevenlabs

# Test with a specific audio file
python compare_icelandic_stt_services.py --audio /path/to/your/audio.wav
```

## Individual Service Testing

You can also test each service individually with their dedicated scripts:

```bash
# Test Azure TTS
python test_azure_tts.py --list-voices
python test_azure_tts.py --text "Góðan daginn. Þetta er prófun á talgervli fyrir íslensku."

# Test ElevenLabs 
python test_elevenlabs.py --mode list-voices
python test_elevenlabs.py --mode tts --text "Góðan daginn. Þetta er prófun á talgervli fyrir íslensku."
python test_elevenlabs.py --mode stt --audio "/path/to/audio.mp3"

# Test optimized local TTS
python improved_icelandic_tts.py --rate 80 --voice 1
```

## Understanding Results

The comparison scripts save results in the following directories:
- TTS results: `tts_comparison_results/`
- STT results: `stt_comparison_results/`

Each test run generates:
- Audio files for TTS tests
- Transcript files for STT tests
- `results.json` file with metrics (processing time, file size, etc.)

## Choosing the Best Service

Based on our testing, here's a guide to selecting the best service for your needs:

### Text-to-Speech (TTS):

| Service | Quality | Speed | File Size | Best For |
|---------|---------|-------|-----------|----------|
| ElevenLabs | Highest | Slowest | Largest | Production-quality audio with natural Icelandic |
| Azure Neural | Good | Medium | Medium | Good balance of quality and performance |
| OpenAI | Good | Fast | Medium | Clear voice but with some accent |
| Local (pyttsx3) | Basic | Fast | Small | Offline use, limited resources |

### Speech-to-Text (STT):

| Service | Accuracy | Speed | Best For |
|---------|----------|-------|----------|
| OpenAI Whisper | Highest | Fast | Best overall Icelandic transcription |
| ElevenLabs Scribe | Very Good | Medium | Alternative with good Icelandic support |
| Azure Speech | Good | Fast | Real-time applications |

## Integration in Real-time Chat Applications

To integrate these services into your real-time Icelandic chat application, see the n8n workflow in `n8n-icelandic-voice-workflow.json`. This workflow provides:

- Smart service selection based on quality requirements
- Automatic fallback when services are unavailable
- Processing for both TTS and STT results

For more details, see `icelandic_chat_azure_elevenlabs_setup.md` and `icelandic_realtime_chat_plan.md`.