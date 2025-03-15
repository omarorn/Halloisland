#!/bin/bash

# Test script for Halloisland TTS API setup

echo "Testing Halloisland TTS API setup..."

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Test API info endpoint
echo -e "\nTesting API info endpoint..."
curl -X POST "http://localhost:8000/api/info"

# Test TTS endpoint
echo -e "\n\nTesting TTS endpoint..."
curl -X POST "http://localhost:8000/api/tts" \
     -H "Content-Type: application/json" \
     -d '{"text":"Halló Ísland", "voice":"alloy"}' \
     --output test.mp3

if [ -f "test.mp3" ]; then
    echo "✅ TTS test successful - audio file generated"
else
    echo "❌ TTS test failed - no audio file generated"
fi

# Test Open WebUI connection
echo -e "\nTesting Open WebUI connection..."
curl -s "http://localhost:3000" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Open WebUI is accessible"
else
    echo "❌ Open WebUI is not accessible"
fi

echo -e "\nSetup test complete!"