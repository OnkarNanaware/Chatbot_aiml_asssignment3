import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Missing GEMINI_API_KEY in environment or .env file.")
        return None
    return genai.Client(api_key=api_key)

client = get_gemini_client()

st.set_page_config(
    page_title="ONKAR>IO ASSISTANT",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Onkar.io Chatbot")
st.caption("Powered by Google Gemini AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox(
        "Select Model",
        options=["gemini-flash-latest", "gemini-1.5-flash"],
        index=0
    )
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_prompt := st.chat_input("Ask Gemini anything..."):
    if not client:
        st.error("Cannot proceed: GEMINI_API_KEY is not configured.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = client.models.generate_content(
                    model=model_choice,
                    contents=user_prompt
                )
                assistant_reply = response.text
                message_placeholder.markdown(assistant_reply)
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            except Exception as e:
                message_placeholder.error(f"Error generating response: {e}")