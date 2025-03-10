# Icelandic Real-Time Chat Implementation Guide

This guide provides practical steps to implement the Icelandic real-time chat system using n8n and the speech technologies we've developed.

## Prerequisites

- n8n instance set up and running
- OpenAI API key for Whisper
- Basic understanding of JavaScript and node.js
- Web server for hosting the chat interface

## Quick Start

### 1. Set Up n8n

```bash
# Install n8n (if not already installed)
npm install n8n -g

# Start n8n
n8n start
```

### 2. Import the Workflow

1. Open n8n in your browser (default: http://localhost:5678)
2. Go to "Workflows" and click "Import from File"
3. Upload the `n8n-icelandic-chat-workflow.json` file
4. Save the workflow

### 3. Configure Environment Variables

In n8n, set up the following environment variables:

```
OPENAI_API_KEY=your_openai_api_key
ICELANDIC_TTS_VOICE=1
ICELANDIC_TTS_RATE=80
```

### 4. Create a Simple Web Interface

Create an `index.html` file:

```html
<!DOCTYPE html>
<html lang="is">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Icelandic Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat-container { height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #message-input { width: 70%; padding: 8px; }
        button { padding: 8px 15px; background: #0066ff; color: white; border: none; cursor: pointer; }
        .user-message { text-align: right; margin: 5px; padding: 8px; background: #e6f2ff; border-radius: 10px; }
        .bot-message { text-align: left; margin: 5px; padding: 8px; background: #f0f0f0; border-radius: 10px; }
        #voice-btn { background: #ff6600; }
    </style>
</head>
<body>
    <h1>Icelandic Chat</h1>
    <div id="chat-container"></div>
    <div id="input-container">
        <input type="text" id="message-input" placeholder="Skrifaðu skilaboð...">
        <button id="send-btn">Senda</button>
        <button id="voice-btn">🎤 Tala</button>
    </div>

    <script>
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        const voiceBtn = document.getElementById('voice-btn');
        const N8N_ENDPOINT = 'http://localhost:5678/webhook/icelandic-chat';
        
        // OpenAI API key - in production, handle this securely
        const OPENAI_KEY = 'your_openai_api_key';
        
        let isRecording = false;
        let mediaRecorder;
        let audioChunks = [];
        
        // Send text message
        sendBtn.addEventListener('click', async () => {
            const message = messageInput.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            messageInput.value = '';
            
            const response = await sendToN8N({ 
                messageType: 'text',
                text: message,
                outputFormat: 'audio' // Request audio response
            });
            
            if (response) {
                addMessage(response.text, 'bot');
                // Play audio if available
                if (response.audio) {
                    playAudio(response.audio);
                }
            }
        });
        
        // Voice message handling
        voiceBtn.addEventListener('mousedown', startRecording);
        voiceBtn.addEventListener('mouseup', stopRecording);
        
        async function startRecording() {
            if (isRecording) return;
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.addEventListener('dataavailable', event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.start();
                isRecording = true;
                voiceBtn.textContent = '🔴 Taka upp...';
            } catch (err) {
                console.error('Error accessing microphone:', err);
                alert('Could not access microphone');
            }
        }
        
        async function stopRecording() {
            if (!isRecording) return;
            
            mediaRecorder.stop();
            isRecording = false;
            voiceBtn.textContent = '🎤 Tala';
            
            // Wait for data to be available
            await new Promise(resolve => {
                mediaRecorder.addEventListener('stop', resolve);
            });
            
            // Convert audio to base64
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const reader = new FileReader();
            
            reader.readAsDataURL(audioBlob);
            reader.onloadend = async () => {
                const base64Audio = reader.result.split(',')[1]; // Remove data URL prefix
                
                addMessage('🎤 [Voice message]', 'user');
                
                const response = await sendToN8N({
                    messageType: 'audio',
                    audio: base64Audio,
                    openaiKey: OPENAI_KEY,
                    outputFormat: 'audio'
                });
                
                if (response) {
                    addMessage(response.text, 'bot');
                    if (response.audio) {
                        playAudio(response.audio);
                    }
                }
            };
        }
        
        async function sendToN8N(data) {
            try {
                const response = await fetch(N8N_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                return await response.json();
            } catch (err) {
                console.error('Error sending to n8n:', err);
                addMessage('Error: Could not connect to the chat service', 'bot');
                return null;
            }
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
            messageDiv.textContent = text;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function playAudio(base64Audio) {
            const audio = new Audio(`data:audio/mp3;base64,${base64Audio}`);
            audio.play();
        }
    </script>
</body>
</html>
```

## Integrating Our Icelandic Speech Technologies

### Setting Up Speech-to-Text Integration

1. Create a Python API wrapper for our Whisper implementation:

```python
# whisper_api.py
from flask import Flask, request, jsonify
import base64
import tempfile
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    audio_base64 = data.get('audio')
    
    if not audio_base64:
        return jsonify({'error': 'No audio provided'}), 400
    
    # Decode base64 audio
    audio_data = base64.b64decode(audio_base64)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file.write(audio_data)
        temp_path = temp_file.name
    
    try:
        # Use our Whisper implementation
        from test_openai_whisper import test_openai_whisper
        
        output_file = Path("temp_output.json")
        api_key = os.environ.get("OPENAI_API_KEY")
        
        # Call our existing function
        result = test_openai_whisper(temp_path, output_file, api_key)
        
        # Return the transcription
        return jsonify({
            'text': result.get('transcription', ''),
            'processing_time': result.get('processing_time_seconds', 0),
            'language': 'is'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temp file
        os.unlink(temp_path)
        if output_file.exists():
            os.unlink(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

2. Create a Text-to-Speech API wrapper:

```python
# tts_api.py
from flask import Flask, request, jsonify
import base64
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    output_file = Path("temp_output.mp3")
    
    try:
        # Use our improved TTS implementation
        from improved_icelandic_tts import generate_improved_tts
        
        rate = int(os.environ.get("ICELANDIC_TTS_RATE", 80))
        voice_id = int(os.environ.get("ICELANDIC_TTS_VOICE", 1))
        
        # Call our existing function
        result = generate_improved_tts(text, output_file, rate=rate, voice_id=voice_id)
        
        # Read the audio file and convert to base64
        with open(output_file, 'rb') as f:
            audio_bytes = f.read()
        
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Return the audio
        return jsonify({
            'audio': audio_base64,
            'format': 'mp3',
            'duration': result.get('processing_time', 0),
            'text': text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temp file
        if output_file.exists():
            os.unlink(output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

3. Update n8n Function nodes to call these APIs:

```javascript
// In the "Process Speech to Text" node
const response = await $http.post({
  url: 'http://localhost:5000/api/transcribe',
  body: {
    audio: $input.item.json.audio
  }
});

return {
  json: {
    messageType: 'text',
    text: response.data.text,
    metadata: {
      processingTime: response.data.processing_time,
      language: response.data.language,
      source: 'whisper'
    }
  }
};

// In the "Generate Text to Speech" node
const response = await $http.post({
  url: 'http://localhost:5001/api/synthesize',
  body: {
    text: $input.item.json.response || $input.item.json.message
  }
});

return {
  json: {
    messageType: 'audio',
    text: $input.item.json.response || $input.item.json.message,
    audio: response.data.audio,
    format: response.data.format,
    metadata: {
      duration: response.data.duration,
      voice: 'icelandic_optimized'
    }
  }
};
```

## Starting the Complete System

1. Start the STT API:
```bash
export OPENAI_API_KEY=your_openai_api_key
python whisper_api.py
```

2. Start the TTS API:
```bash
export ICELANDIC_TTS_RATE=80
export ICELANDIC_TTS_VOICE=1
python tts_api.py
```

3. Start n8n:
```bash
n8n start
```

4. Serve the web interface (using a simple HTTP server):
```bash
python -m http.server 8000
```

5. Access the chat interface at http://localhost:8000

## Additional Features and Customizations

### Adding Session Management

1. Add a Redis session store for conversation history:

```javascript
// In the "Chat Webhook" node processing
const sessionId = $input.item.json.sessionId || uuidv4();
const redisClient = await connectToRedis();

// Retrieve conversation history
const history = await redisClient.get(`icelandic:chat:${sessionId}`);
const messages = history ? JSON.parse(history) : [];

// Add new message
messages.push({
  role: 'user',
  content: $input.item.json.text
});

// Save updated history
await redisClient.set(`icelandic:chat:${sessionId}`, JSON.stringify(messages));
```

### Adding Offline Mode

1. Implement a fallback mechanism when API is unavailable:

```javascript
// In the "Process Speech to Text" node
try {
  // Try OpenAI Whisper API first
  const response = await $http.post({
    url: 'https://api.openai.com/v1/audio/transcriptions',
    // ... API configuration
  });
  
  return { json: { /* ... */ } };
} catch (error) {
  // Fallback to local implementation
  const response = await $http.post({
    url: 'http://localhost:5000/api/local-transcribe',
    // ... Local API configuration
  });
  
  return { json: { /* ... */ } };
}
```

## Troubleshooting

### Common Issues

1. **Audio not being recognized:**
   - Check if the audio format is supported (MP3 or WAV)
   - Ensure the audio isn't too large (split if needed)
   - Verify that the OpenAI API key is valid

2. **Poor Icelandic pronunciation:**
   - Try different voice settings (voice_id and rate)
   - Test with the Bark TTS if available
   - Consider post-processing the audio

3. **n8n workflow not responding:**
   - Check that all APIs are running
   - Review n8n logs for errors
   - Ensure webhook URLs are correctly configured

## Next Steps

1. **Scale the system:**
   - Deploy APIs using Docker containers
   - Set up load balancing for high usage
   - Implement caching for frequent queries

2. **Improve quality:**
   - Fine-tune models with Icelandic language data
   - Integrate with specialized Icelandic TTS providers
   - Collect feedback from native speakers

3. **Add features:**
   - Multi-user support
   - Voice authentication
   - Message translation
   - Conversation archiving