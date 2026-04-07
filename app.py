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

if "box_color" not in st.session_state:
    st.session_state.box_color = "#FFFFFF"

def change_color(hex_code: str) -> dict:
    """
    이 함수는 사이드바에 있는 컬러 박스의 색상을 변경합니다.
    
    Args:
        hex_code (str): 색상의 HEX 코드 (예: "#87CEEB")
    """
    st.session_state.box_color = hex_code

    return {
        "status": "success",
        "message": f"{hex_code}으로 색상이 변경되었습니다."
    }

if "chat_session" not in st.session_state:
    system_prompt = """
    
    """
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[change_color],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False
            )
        )
    )



for content in st.session_state.chat_session.get_history():
    role = "ai"if content.role == "model" else "user"
    with st.chat_message(role):
        for part in content.parts:
            if part.text:
                st.write(part.text)


if prompt:= st.chat_input("챗봇에게 물어보기"):
    with st.chat_message("user"):
        st.write(prompt)
        

    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)

        st.write(response.text)
       


with st.sidebar:
    st.header("팔레트")
    st.markdown(f"""
        <div
            style="background-color: {st.session_state.box_color};
            height: 150px;
            border-radius: 15px; 
            border: 2px solid #ddd;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            transition: background-color 0.5s ease;
        ">
        </div>
    """, unsafe_allow_html=True)


if st.sidebar.button("색상 변경"):
    change_color("#245ebd")