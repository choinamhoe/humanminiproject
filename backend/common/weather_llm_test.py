# pip install google-generativeai

import pandas as pd
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv() 


# 키 가져오기
GEMI_KEY = os.getenv("API_KEY_gemi", "")

# Gemini 모델 초기화
genai.configure(api_key=GEMI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ 1. 현재 시각 데이터 (DB나 API에서 불러오기, 여기선 예시 하드코딩)
current_weather = {
    "temperature": 27,
    "humidity": 70,
    "wind_speed": 2,
    "precipitation": 0,
    "visibility": 10
}

# ✅ 2. 6시간 예보 데이터 로드 (CSV)
df = pd.read_csv("weather_forecast_next_6h_20250911T1400_test.csv", encoding="cp949")

# ✅ 3. LLM 입력 프롬프트 생성
system_prompt = """
너는 골프 경기 보조 코치다.
현재 날씨와 앞으로 6시간의 예보 데이터를 보고,
골프장 이용자에게 필요한 추천 메시지를 2~3문장으로 제시한다.
출력은 "추천 메시지: ..." 형식으로 준다.
"""

# 현재 데이터 부분
user_input = f"""
현재 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}
현재 날씨: 기온 {current_weather['temperature']}℃,
습도 {current_weather['humidity']}%,
풍속 {current_weather['wind_speed']}m/s,
강수량 {current_weather['precipitation']}mm,
시정 {current_weather['visibility']}km
"""

# 예보 데이터 부분 (시간/기온/강수량만 예시로 넣음)
forecast_text = "\n예보 (시간별):\n"
for _, row in df.iterrows():
    forecast_text += (
        f"{row['datetime']} → "
        f"기온 {row['T1H']}℃, "
        f"습도 {row['REH']}%, "
        f"강수량 {row['RN1']}, "
        f"풍속 {row['WSD']}m/s, "
        f"풍향 {row['VEC']}°\n"
    )

# 전체 프롬프트
prompt = system_prompt + "\n\n" + user_input + forecast_text

# ✅ 4. LLM 호출
response = model.generate_content(prompt)

# ✅ 5. 결과 출력
print(response.text)
