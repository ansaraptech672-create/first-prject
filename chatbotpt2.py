
import streamlit as st
from google import genai

st.title("Gemini Connection Test")

try:
    key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=key)

    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello"
    )

    st.success("Connection successful!")
    st.write(result.text)

except Exception as error:
    st.error(f"Gemini request failed: {error}")
