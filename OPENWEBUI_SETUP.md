# Integrating with Open WebUI

This guide explains how to connect the Halloisland TTS API to Open WebUI for testing TTS functionality.

## API Setup

The FastAPI service exposes the following endpoints:

- `POST /api/tts`: Convert text to speech
  - Parameters:
    - `text`: The text to convert (required)
    - `voice`: Voice to use (optional, default: "alloy")
  - Returns: Audio file (MP3)

- `POST /api/info`: Get API information
  - Returns: Information about available features and voices

## Local Development with Docker

1. Prerequisites:
   - Docker and Docker Compose installed
   - OpenAI API key

2. Setup:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   
   # Start the services
   docker-compose up -d
   ```

3. Available Services:
   - API: http://localhost:8000
   - Open WebUI: http://localhost:3000
   - Redis: localhost:6379
   - PostgreSQL: localhost:5432

4. Testing:
   - Access Open WebUI at http://localhost:3000
   - API documentation available at http://localhost:8000/docs
   - Test TTS directly using curl commands from below

## Railway Deployment

1. Ensure the following environment variables are set in Railway:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: Port for the FastAPI service (default: 8000)

2. The service will be automatically deployed using nixpacks configuration.

## Open WebUI Configuration

1. Access your Open WebUI deployment (e.g., open-webui-production-xxxx.up.railway.app)

2. Configure Custom API Endpoint:
   - Go to Settings > API Endpoints
   - Add new endpoint with your Railway API URL
   - Set endpoint type to "TTS Service"
   - Test connection using the built-in test function

3. Test TTS Integration:
   - Send a message in chat
   - Click the "Speech" button or use the `/tts` command
   - The text will be sent to your API and returned as audio

## Testing TTS/STT

1. Voice Generation Test:
   ```bash
   curl -X POST "https://your-api-url/api/tts" \
        -H "Content-Type: application/json" \
        -d '{"text": "Halló Ísland", "voice": "alloy"}'
   ```

2. API Information:
   ```bash
   curl -X POST "https://your-api-url/api/info"
   ```

## Troubleshooting

1. If audio generation fails:
   - Check API logs in Railway
   - Verify OpenAI API key is set
   - Ensure text input is valid

2. If connection fails:
   - Verify API endpoint URL in Open WebUI settings
   - Check CORS configuration if needed
   - Verify Railway service is running

3. Common Issues:
   - 404: API endpoint not found - Check URL configuration
   - 500: Server error - Check Railway logs
   - CORS errors - Verify allowed origins in API configuration