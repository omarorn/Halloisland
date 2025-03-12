import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY", "")

def chat_with_openai(message, history):
    if not api_key:
        return [], "Please set your OpenAI API key in the .env file"
    
    # Prepare conversation history for OpenAI API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Convert Gradio messages format to OpenAI format
    for msg in history:
        messages.append({"role": msg[0], "content": msg[1]})
    
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
        
        # Extract the assistant's reply
        assistant_message = response.json()["choices"][0]["message"]["content"]
        history.append(("user", message))
        history.append(("assistant", assistant_message))
        return history, ""
    except Exception as e:
        return history, f"Error: {str(e)}"

def webui_interface():
    # Create Gradio interface
    with gr.Blocks(title="AI Agent Interface") as demo:
        gr.Markdown("# AI Agent Interface")
        gr.Markdown("## Chat with the AI")
        
        chatbot = gr.Chatbot(height=600, type="messages")
        msg = gr.Textbox(label="Type your message")
        clear = gr.Button("Clear")
        
        msg.submit(chat_with_openai, [msg, chatbot], [chatbot, msg])
        clear.click(lambda: ([], ""), None, [chatbot, msg], queue=False)
        
    return demo

if __name__ == "__main__":
    demo = webui_interface()
    demo.launch(share=True, pwa=True)
