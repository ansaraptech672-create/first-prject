
import streamlit as st
from groq import Groq
import os

from dotenv import load_dotenv
# -----------------------------
# Page configuration
# -----------------------------

load_dotenv()

st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Groq AI Chatbot")
st.caption("Your personal AI assistant, powered by Groq")

# -----------------------------
# Load Groq API key
# -----------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"].strip()
except (KeyError, FileNotFoundError):
    st.error(
        "GROQ_API_KEY is missing. Add it to "
        "Streamlit Cloud → App Settings → Secrets."
    )
    st.stop()

if not api_key:
    st.error("Your Groq API key is empty.")
    st.stop()

# -----------------------------
# Initialize Groq client
# -----------------------------
if "client" not in st.session_state:
    st.session_state.client = Groq(api_key=api_key)

# Choose a model supported by your Groq account
MODEL = "openai/gpt-oss-120b"

# -----------------------------
# Initialize conversation
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly AI assistant."
        }
    ]

# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Groq is thinking..."):
            try:
                completion = st.session_state.client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=1024
                )

                reply = (
                    completion.choices[0].message.content
                    or "No response received."
                )

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                # Remove the failed prompt from saved chat history
                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"] == "user"
                    and st.session_state.messages[-1]["content"] == prompt
                ):
                    st.session_state.messages.pop()

                st.error(f"Groq API error: {e}")

# -----------------------------
# Clear conversation
# -----------------------------
if st.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, friendly AI assistant."
        }
    ]
    st.rerun()
