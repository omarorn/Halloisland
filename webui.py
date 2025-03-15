import gradio as gr
import requests
import os
from dotenv import load_dotenv
import redis
import hashlib

# Initialize Redis connection
load_dotenv()
redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=False  # Keep audio data as bytes
)
CACHE_TTL = 86400  # 24 hours cache retention

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY", "")

def chat_with_openai(message, chat_history):
    """Chat with OpenAI API and return properly formatted messages"""
    if not api_key:
        return chat_history + [{"role": "assistant", "content": "Please set your OpenAI API key in the .env file"}]
    
    # Prepare conversation history for OpenAI API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add history to messages
    messages.extend(chat_history)
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Make API request
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": messages
            }
        )
        response.raise_for_status()
        
        # Get assistant's reply
        assistant_message = response.json()["choices"][0]["message"]
        
        # Return updated history
        return chat_history + [
            {"role": "user", "content": message},
            assistant_message
        ]
    except Exception as e:
        return chat_history + [{"role": "assistant", "content": f"Error: {str(e)}"}]

def clear_history():
    """Clear chat history"""
    return []

def webui_interface():
    # Create Gradio interface
    with gr.Blocks(title="AI Agent Interface") as demo:
        gr.Markdown("# AI Agent Interface")
        
        chatbot = gr.Chatbot(height=600, type="messages")
        msg = gr.Textbox(label="Type your message")
        clear = gr.Button("Clear")
        
        msg.submit(chat_with_openai, [msg, chatbot], [chatbot])
        clear.click(clear_history, None, chatbot, queue=False)
        
    return demo

if __name__ == "__main__":
    demo = webui_interface()
    demo.launch(pwa=True)