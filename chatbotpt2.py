
import streamlit as st
from google import genai

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

API_KEY =  st.secrets["GEMINI_API_KEY"]
MODEL = "gemini-3.8-flash"

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="ansargenai"
)

st.title("ðŸ¤– Gemini AI Chatbot")
st.caption("Chat with your AI assistant")

# Initialize the client once per session
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

# Initialize chat history and Gemini chat
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model=MODEL
    )

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(
                    message=prompt
                )

                reply = response.text or "No response received."
                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error(f"Gemini error: {e}")

# Clear conversation
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat = st.session_state.client.chats.create(
        model=MODEL
    )
    st.rerun()