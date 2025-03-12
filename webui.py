import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY", "")

def chat_with_openai(message, history):
    if not api_key:
        return [{"role": "assistant", "content": "Please set your OpenAI API key in the .env file"}]
    
    # Initialize conversation history if empty
    history = history or []
    
    # Prepare conversation history for OpenAI API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add history to messages
    messages.extend(history)
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Make API request to OpenAI
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages
            }
        )
        response.raise_for_status()
        
        # Get assistant's reply
        assistant_message = response.json()["choices"][0]["message"]
        # Add user message and assistant reply to history
        return history + [
            {"role": "user", "content": message},
            assistant_message
        ]
    except Exception as e:
        return history + [{"role": "assistant", "content": f"Error: {str(e)}"}]

def webui_interface():
    # Create Gradio interface
    with gr.Blocks(title="AI Agent Interface") as demo:
        gr.Markdown("# AI Agent Interface")
        gr.Markdown("## Chat with the AI")
        
        chatbot = gr.Chatbot(height=600, type="messages")
        msg = gr.Textbox(label="Type your message")
        clear = gr.Button("Clear")
        
        msg.submit(chat_with_openai, [msg, chatbot], [chatbot])
        clear.click(lambda: [], None, [chatbot], queue=False)
        
    return demo

if __name__ == "__main__":
    demo = webui_interface()
    demo.launch(pwa=True)
