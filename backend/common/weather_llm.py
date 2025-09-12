from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMI_KEY = os.getenv("API_KEY_gemi", "")

genai.configure(api_key=GEMI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# ✅ CORS 설정 (프론트랑 연결 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 필요시 "http://localhost:3000"으로 제한 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    print("📌 받은 데이터:", data)   # 🔥 프론트에서 넘어온 전체 JSON
    weather = data["weather"]
    print("📌 weather[0]:", weather[0])  # 🔥 리스트 첫 번째 값

    prompt = f"""
    현재 날씨: 기온 {weather[0].get('T1H')}℃,
    습도 {weather[0].get('REH')}%,
    풍속 {weather[0].get('WSD')}m/s,
    풍향 {weather[0].get('VEC')}도
    앞으로 6시간 예보 데이터: {weather}
    → 골프장 이용자에게 필요한 추천 메시지를 2~3문장으로 제시해줘.
    """


    response = model.generate_content(prompt)
    return {"message": response.text}


