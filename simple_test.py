# Load model directly
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

print("Loading Icelandic whisper model...")
processor = AutoProcessor.from_pretrained("carlosdanielhernandezmena/whisper-large-icelandic-10k-steps-1000h")
model = AutoModelForSpeechSeq2Seq.from_pretrained("carlosdanielhernandezmena/whisper-large-icelandic-10k-steps-1000h")

print("Successfully loaded the Icelandic model!")
print(f"Model type: {type(model)}")
print("Test completed successfully!")