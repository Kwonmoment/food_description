import os
import base64
from openai import OpenAI
import streamlit as st
from PIL import Image

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Streamlit 앱 설정
st.title("음식 이미지 설명 생성기")

# 사용자로부터 이미지 업로드 받기
uploaded_file = st.file_uploader("음식 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 업로드된 이미지의 경로를 임시로 저장
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 이미지 인코딩
    base64_image = encode_image(image_path)

    # 업로드된 이미지 출력
    st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)

    # GPT 모델에 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are the assistant who explains the food. Identify the type of food in the image provided by the user and answer questions."},
            {"role": "user", "content": [
                {"type": "text", "text": "이 음식을 어떻게 먹는지 설명해 주세요."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }  
            ]}
        ],
        temperature=0.0,
    )

    # 결과 출력
    st.write("Assistant: " + response.choices[0].message.content)