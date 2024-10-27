import streamlit as st
import requests  # Use requests to call the Llama API
import os

# Set page configuration
st.set_page_config(page_title="EazyChatbot", page_icon="https://drive.google.com/uc?id=1Ga5aNAJlT3lPD9Sm0kJ-nUZ6nlW3onTX")

# Set your Llama API token here
llama_api_token = "LA-99a046935eed4a7e9423b60cefb546376009155c36214b488dc87b6ac6f0dc8b"  # Replace with your actual Llama API token

# App title and sidebar
st.sidebar.title('EazyChatbot')
st.sidebar.success('API key is set!', icon='✅')

# Model selection (adjust model names based on available models in Llama)
selected_model = st.sidebar.selectbox('Choose a Llama model', ['llama3.1-70b', 'llama3.2-11b'], key='selected_model')

temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=5.0, value=0.7, step=0.01)
max_length = st.sidebar.slider('Max Length', min_value=32, max_value=128, value=120, step=8)

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function to display messages
def display_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div style='text-align: right;'><span style='background-color: #DCF8C6; border-radius: 10px; padding: 10px; display: inline-block;'>{message['content']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left;'><span style='background-color: #F1F1F1; border-radius: 10px; padding: 10px; display: inline-block;'>{message['content']}</span></div>", unsafe_allow_html=True)

# Display chat messages
display_messages()

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating response using Llama API
def generate_llama_response(prompt_input):
    url = "https://api.llama-api.com/v1/chat"  # Replace with actual endpoint if different
    headers = {
        "Authorization": f"Bearer {llama_api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": selected_model,
        "messages": [{"role": "user", "content": prompt_input}],
        "temperature": temperature,
        "max_length": max_length
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("response")  # Adjust based on actual response structure
    else:
        st.error(f"An error occurred: {response.status_code} - {response.text}")
        return "Sorry, I couldn't process your request."

# User-provided prompt input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    display_messages()
    
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            response = generate_llama_response(prompt)
            # Append assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display assistant message
            display_messages()
