import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY", "")

# Set page config
st.set_page_config(
    page_title="AI Agent Interface",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant with multiple capabilities."}
    ]

# Set up sidebar
st.sidebar.title("AI Agent Interface")
st.sidebar.subheader("Configuration")

# API key input in sidebar (pre-filled from environment)
api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    value=api_key,
    type="password"
)

# Model selection
model = st.sidebar.selectbox(
    "Select Model",
    ["gpt-4o", "gpt-3.5-turbo"]
)

# Temperature slider
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)

# Tool selection
tools_enabled = st.sidebar.checkbox("Enable Function Calling", value=True)

# Main area
st.title("AI Agent Web Interface")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] \!= "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get API key
    api_key_to_use = api_key_input or api_key
    
    if not api_key_to_use:
        st.error("Please enter an OpenAI API key")
    else:
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {api_key_to_use}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": st.session_state.messages,
            "temperature": temperature
        }
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Make API request
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                # Extract response
                full_response = response.json()["choices"][0]["message"]["content"]
                message_placeholder.write(full_response)
            except Exception as e:
                full_response = f"Error: {str(e)}"
                message_placeholder.error(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant with multiple capabilities."}
    ]
    st.rerun()

# Info section
with st.sidebar.expander("About"):
    st.write("""
    This is a simple web interface for interacting with AI agents.
    It currently supports OpenAI's models for chat interactions.
    """)
