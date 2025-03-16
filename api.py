from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import io
import os
from src.setup.config_manager import ConfigManager
from tts_engine import TTSFactory

app = FastAPI(title="Halloisland API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize TTS
config = ConfigManager()
tts_provider = TTSFactory.create_provider(config)

@app.post("/api/tts")
async def text_to_speech(text: str, voice: str = "alloy"):
    """Convert text to speech"""
    try:
        # Create temporary file path
        output_file = Path("temp.mp3")
        
        # Generate speech
        result = tts_provider.generate_speech(text, output_file, voice)
        
        if not result:
            raise HTTPException(status_code=500, detail="TTS generation failed")
        
        # Read the generated audio file
        audio_data = output_file.read_bytes()
        
        # Clean up
        output_file.unlink()
        
        # Return audio stream
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment;filename=audio.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/info")
async def get_info():
    """Get API information"""
    return {
        "name": "Halloisland TTS/STT API",
        "version": "1.0.0",
        "features": ["tts"],
        "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "80")))