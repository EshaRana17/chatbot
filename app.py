import streamlit as st
import replicate
import os

# Set the page configuration with an image as an icon
st.set_page_config(page_title="EazyChatbot", page_icon="https://drive.google.com/uc?id=1Ga5aNAJlT3lPD9Sm0kJ-nUZ6nlW3onTX")

# Set your API token directly for testing
replicate_api = "r8_CkVuErpSK2qbeOcrxQxCzUmtgMg1gIa04QyhK"
os.environ['REPLICATE_API_TOKEN'] = replicate_api  # Set the environment variable

# App title and sidebar
st.sidebar.title('EazyChatbot')
st.sidebar.success('API key is set!', icon='✅')

# Model selection and parameters
selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
if selected_model == 'Llama2-7B':
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
elif selected_model == 'Llama2-13B':
    llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=5.0, value=0.7, step=0.01)
top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
max_length = st.sidebar.slider('Max Length', min_value=32, max_value=128, value=120, step=8)

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Chat message display function with styling
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

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant."
    
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += f":User {dict_message['content']}\n\n"
        else:
            string_dialogue += f"Assistant: {dict_message['content']}\n\n"
    
    try:
        output = replicate.run(
            llm,
            input={
                "prompt": f"{string_dialogue} {prompt_input} Assistant:",
                "temperature": temperature,
                "top_p": top_p,
                "max_length": max_length,
                "repetition_penalty": 1
            }
        )
        return output
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, I couldn't process your request."

# User-provided prompt input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    display_messages()
    
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            full_response = ''.join(response)  # Join the response list into a single string
            
            # Append assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Display assistant message
            display_messages()
