import streamlit as st
from google import genai
from google.genai import types


import os
from dotenv import load_dotenv

st.title(":orange[:material/smart_toy:] 챗봇")
st.caption("제미나이에요.")
MODEL_NAME = "gemini-2.5-flash"

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🔑API 키가 설정되지 않았습니다.")
        st.stop()

    return genai.Client(api_key=api_key)
    
client = get_client()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME
    )



for content in st.session_state.chat_session.get_history():
    role = "ai"if content.role == "model" else "user"
    with st.chat_message(content.role):
        for part in content.parts:
            if part.text:
                st.write(part.text)


if prompt:= st.chat_input("챗봇에게 물어보기"):
    with st.chat_message("user"):
        st.write(prompt)
        

    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)

        st.write(response.text)
       