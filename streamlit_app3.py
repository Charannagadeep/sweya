import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the API key from environment variables
GOOGLE_API_KEY = os.getenv('AIzaSyABUCj78nfkI8K5DW6vOApWhataFnH6WHs')

if GOOGLE_API_KEY is None:
    st.error("API key not found in environment variables.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Create a data/ folder if it doesn't already exist
if not os.path.exists('data/'):
    os.makedirs('data/')

# Load past chats
past_chats_path = 'data/past_chats_list'
if os.path.exists(past_chats_path):
    past_chats = joblib.load(past_chats_path)
else:
    past_chats = {}

# Sidebar for past chats
with st.sidebar:
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = st.selectbox(
            'Pick a past chat',
            options=[f'{time.time()}'] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            'Pick a past chat',
            options=[f'{time.time()}', st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.write('# Chat with Gemini')

# Load chat history
chat_id = st.session_state.chat_id
messages_file = f'data/{chat_id}-st_messages'
gemini_history_file = f'data/{chat_id}-gemini_messages'

if os.path.exists(messages_file) and os.path.exists(gemini_history_file):
    st.session_state.messages = joblib.load(messages_file)
    st.session_state.gemini_history = joblib.load(gemini_history_file)
else:
    st.session_state.messages = []
    st.session_state.gemini_history = []

# Initialize chat model
try:
    st.session_state.model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)
except Exception as e:
    st.error(f"Failed to initialize chat model: {e}")
    st.stop()

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('Your message here...'):
    if st.session_state.chat_id not in past_chats:
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, past_chats_path)

    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Send message to AI
    try:
        response = st.session_state.chat.send_message(prompt, stream=True)
        full_response = ''
        message_placeholder = st.empty()

        # Stream response
        for chunk in response:
            if chunk.text:
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05)
                    message_placeholder.write(full_response + '▌')

        message_placeholder.write(full_response)
        st.session_state.messages.append({'role': 'ai', 'content': full_response, 'avatar': '✨'})
        st.session_state.gemini_history = st.session_state.chat.history

        # Save to file
        joblib.dump(st.session_state.messages, messages_file)
        joblib.dump(st.session_state.gemini_history, gemini_history_file)

    except Exception as e:
        st.error(f"Failed to get a response from AI: {e}")
