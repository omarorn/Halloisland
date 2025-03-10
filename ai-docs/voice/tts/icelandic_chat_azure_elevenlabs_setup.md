# Azure and ElevenLabs Setup for Icelandic Chat System

This guide walks you through setting up Azure Speech Services and ElevenLabs for enhanced Icelandic voice capabilities in your real-time chat system.

## 1. Azure Speech Services Setup

Azure Speech Services provides high-quality neural Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities that we can leverage for Icelandic.

### Step 1: Create an Azure Account

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an account if you don't have one (you can use the free tier for testing)

### Step 2: Create a Speech Service Resource

1. In the Azure Portal, click "Create a resource"
2. Search for "Speech" and select "Speech"
3. Click "Create"
4. Fill in the required details:
   - Resource group: Create a new one or use existing
   - Region: Select a region with speech services (e.g., West Europe)
   - Name: Give your resource a name (e.g., "icelandic-speech")
   - Pricing tier: Select Free F0 (for testing) or S0 (for production)
5. Click "Review + create" and then "Create"

### Step 3: Get API Keys

1. Once your resource is created, go to the resource
2. In the left menu, under "Resource Management", click "Keys and Endpoint"
3. Copy "Key 1" and the "Location/Region" value
4. Add these to your .env file:
   ```
   AZURE_SPEECH_KEY=your_key_here
   AZURE_SPEECH_REGION=your_region_here
   ```

## 2. ElevenLabs Setup

ElevenLabs provides state-of-the-art voice AI capabilities, including their new Scribe STT service that can handle Icelandic.

### Step 1: Create an ElevenLabs Account

1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for an account (they offer a free tier with limited usage)

### Step 2: Get API Key

1. After signing in, click on your profile picture in the top-right
2. Select "Profile" from the dropdown
3. Navigate to the "API Key" section
4. Copy your API key
5. Add it to your .env file:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```

## 3. Testing Your Setup

Once you have set up both services, you can test them using the scripts provided in this repository:

### Test Azure Speech Services:

```bash
python test_azure_tts.py --list-voices
python test_azure_tts.py --text "Halló, þetta er próf á íslensku."
```

### Test ElevenLabs:

```bash
# List available voices
python test_elevenlabs.py --mode list-voices

# List available models
python test_elevenlabs.py --mode list-models

# Generate TTS
python test_elevenlabs.py --mode tts --text "Halló, þetta er próf á íslensku."

# Transcribe audio (STT)
python test_elevenlabs.py --mode stt --audio "path/to/audio/file.mp3" --language icelandic
```

## 4. Integrating with n8n

We've created an n8n workflow that leverages these services in our real-time chat system.

### Import the Workflow:

1. Open your n8n instance
2. Go to Workflows
3. Click "Import from File"
4. Select the `n8n-icelandic-voice-workflow.json` file
5. Save the workflow

### Configure Environment Variables:

In your n8n instance, set the following environment variables:

```
AZURE_SPEECH_KEY=your_key_here
AZURE_SPEECH_REGION=your_region_here
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Activate the Workflow:

1. Open the imported workflow
2. Click "Activate" in the top-right corner
3. The workflow will now be accessible at the webhook URL

## 5. Making API Requests

You can now make requests to your n8n webhook with these parameters:

### Text-to-Speech (TTS) Request:

```json
{
  "type": "tts",
  "text": "Halló, þetta er próf á íslensku.",
  "quality": "ultra"  // Options: "ultra", "high", "balanced", "basic"
}
```

### Speech-to-Text (STT) Request:

```json
{
  "type": "stt",
  "audio_file": "/path/to/audio/file.mp3",
  "quality": "ultra"  // Options: "ultra", "high", "balanced", "basic"
}
```

The quality parameter determines which service is used:
- "ultra": ElevenLabs (highest quality)
- "high": Azure Speech Services
- "balanced": OpenAI (good balance of quality and speed)
- "basic": Local optimized solutions

## 6. Service Selection Logic

The system automatically selects the best available service based on:

1. The requested quality level
2. Available API keys (if a service's API key is missing, it falls back to the next best option)
3. Special requirements (like offline operation)

## 7. Next Steps

- Create custom voices in ElevenLabs by recording native Icelandic speakers
- Fine-tune Azure neural voices for better Icelandic pronunciation
- Implement caching mechanisms to reduce API calls for common phrases
- Add a web interface that leverages WebSockets for real-time audio streaming