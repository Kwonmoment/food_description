import os
import base64
from openai import OpenAI
import streamlit as st
from PIL import Image

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

@st.cache_data
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Streamlit 앱 설정
st.title("Food descriptor")
# with st.sidebar:
#     st.sidebar.title("Menu")
#     st.sidebar.radio("옵션", ["Home", "History"])
languages = ["한국어", "English" , "日本語", "中国人","Français","español"]
selected_language = st.selectbox("언어를 선택하세요.(Choose your language)😄:", languages)
language_str = {"English":"english", "한국어":"korean", "日本語":"japanese", "中国人":"chinese", "Français":"french", "español":"spanish"}


# 사용자로부터 이미지 업로드 받기
uploaded_file = st.file_uploader("🍳음식 사진을 업로드 해주세요.(Upload your food image)👈", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # 업로드된 이미지의 경로를 임시로 저장
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 이미지 인코딩
    base64_image = encode_image(image_path)

    # 업로드된 이미지 출력
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # GPT 모델에 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are the assistant who explains the food. Identify the type of food in the image provided by the user and answer questions. If you can't identify the type of food in the image you provided, reply 'I don\'t know what that food is.'"},
            {"role": "user", "content": [
                {"type": "text", "text": f"Please explain in {language_str[selected_language]} how to eat this food."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }  
            ]}
        ],
        temperature=0.0,
    )

    # 결과 출력
    st.write("Assistant: " + response.choices[0].message.content)