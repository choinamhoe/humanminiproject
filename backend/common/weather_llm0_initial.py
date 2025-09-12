from fastapi import FastAPI, Request
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()
GEMI_KEY = os.getenv("API_KEY_gemi", "")

# Gemini 초기화
genai.configure(api_key=GEMI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI 앱 생성
app = FastAPI()

@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    weather = data["weather"]  # 프론트에서 보낸 날씨 데이터

    # 프롬프트 생성
    prompt = f"""
    너는 골프 경기 보조 코치다.
    현재 날씨와 앞으로 6시간의 예보 데이터를 보고,
    골프장 이용자에게 필요한 추천 메시지를 2~3문장으로 제시한다.
    출력은 "추천 메시지: ..." 형식으로 준다.

    현재 날씨: 기온 {weather[0]['T1H']}℃,
    습도 {weather[0]['REH']}%,
    풍속 {weather[0]['WSD']}m/s,
    풍향 {weather[0]['VEC']}도
    """

    response = model.generate_content(prompt)

    return {"message": response.text}
