import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY", "")

def chat_with_openai(message, history):
    history = history or []
    if not api_key:
        return "Please set your OpenAI API key in the .env file"
    
    # Prepare conversation history for OpenAI API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        if h[1]:
            messages.append({"role": "assistant", "content": h[1]})
    
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
                "model": "gpt-4o",
                "messages": messages
            }
        )
        response.raise_for_status()
        
        # Extract the assistant's reply
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

def webui_interface():
    # Create Gradio interface
    with gr.Blocks(title="AI Agent Interface") as demo:
        gr.Markdown("# AI Agent Interface")
        gr.Markdown("## Chat with the AI")
        
        chatbot = gr.Chatbot(height=600)
        msg = gr.Textbox(label="Type your message")
        clear = gr.Button("Clear")
        
        msg.submit(chat_with_openai, [msg, chatbot], [chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)
        
    return demo

if __name__ == "__main__":
    demo = webui_interface()
    demo.launch(share=True)
