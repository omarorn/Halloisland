# Icelandic TTS and STT Model Comparison

This project contains scripts to compare various Text-to-Speech (TTS) and Speech-to-Text (STT) models for the Icelandic language.

## Setup

1. Create a virtual environment:
```bash
python -m venv icelandic-env
source icelandic-env/bin/activate  # Linux/Mac
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up API keys by copying the template:
```bash
cp .env.icelandic .env
```

4. Edit the `.env` file to add your API keys for each service:
   - Google Cloud
   - Microsoft Azure
   - OpenAI
   - Tiro.is (specialized Icelandic service)

## Download Sample Audio

Download sample Icelandic audio files for testing:

```bash
python download_sample_audio.py
```

This will download sample files to the `icelandic_samples` directory.

## Text-to-Speech (TTS) Comparison

Run the TTS comparison script to test different TTS systems:

```bash
python icelandic_tts_comparison.py
```

This will:
1. Generate Icelandic speech samples using different TTS providers
2. Save audio files to the `icelandic_tts_samples` directory
3. Report which providers succeeded or failed

## Speech-to-Text (STT) Comparison

Test STT models using a sample audio file:

```bash
python icelandic_stt_comparison.py icelandic_samples/icelandic_sample1.mp3
```

This will:
1. Transcribe the audio using different STT providers
2. Display the transcription from each provider
3. Save results to the `icelandic_stt_results` directory

## Available Models

### TTS Models
- Google Cloud TTS (is-IS)
- Microsoft Azure TTS (is-IS-GudrunNeural)
- OpenAI TTS (tts-1)
- Tiro.is (specialized Icelandic TTS)

### STT Models
- Google Cloud Speech-to-Text (is-IS)
- Microsoft Azure Speech (is-IS)
- OpenAI Whisper
- Local fine-tuned Whisper model for Icelandic

## Comparing Results

After running the tests:
1. Listen to the TTS audio samples in `icelandic_tts_samples` directory
2. Review the STT transcriptions in the `icelandic_stt_results` directory
3. Compare accuracy and quality for your specific needs

## Requirements

Create a requirements.txt file with:

```
# For environment and utils
python-dotenv
requests

# For Google Cloud
google-cloud-texttospeech
google-cloud-speech

# For Azure
azure-cognitiveservices-speech

# For OpenAI
openai

# For local Whisper model
torch
transformers
librosa
```