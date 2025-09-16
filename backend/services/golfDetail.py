from models.golfDetail import post_model_golfDetail,post_model_golfKmaInfo
from common.idw_interpolation import idw_df
import json, requests
import numpy as np
from common.commonDf import dftoDict,postprocess_weather
from common.weather_next import current_location
from common.weather_past import past_location
import pandas as pd
import requests, datetime
import os
from common.golf_weather_pipeline import generate_synthetic_training_data,train_ml_model,train_deep_model,predict_weather_for_location

# 현재 파일(golfDetail.py) 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ../../자료/source/...xlsx 로 이동
file_path = os.path.join(BASE_DIR, "..", "..", "자료", "source", "기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx")

locationInfo = pd.read_excel(file_path)
locationInfo = locationInfo[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]

def post_services_golfDetail(id):
   print(f"services post_services_golfDetail start id : {id}")
   res = dict()
   #id로 골프상세정보 가져옴
   golfDetail = post_model_golfDetail(id)
   #print(f"골프정보 : {golfDetail}")
   #kmaInfo = post_model_golfKmaInfo()
   #print(f" post_services_golfDetail 위도 : {kmaInfo.loc[:,"Latitude"]}")
   #print(kmaInfo.loc[:,"Longitude"])
   #print(kmaInfo.loc[:,"Latitude"])
   #print(f"첫번째데이터 :{kmaInfo}")
   #현재 골프장 정보에 대한 위도,경도
   lon = golfDetail.loc[:,"Longitude"].values
   lat = golfDetail.loc[:,"Latitude"].values

   #현재시간부터 6시간 후 날씨 예측 정보
   # pred_df DataFrame 컬럼 설명
   # ---------------------------
   # id         : 각 row 고유 번호 (1부터 시작)
   # datetime   : 예보 시간 (datetime 타입, 서울시간 기준, fcstDate + fcstTime 합성)
   # POP        : 강수확률 (%) — 'Probability of Precipitation'
   # PTY        : 강수형태 (0=없음, 1=비, 2=비/눈, 3=눈 등 KMA 코드)
   # R06        : 6시간 강수량 (mm)
   # REH        : 상대습도 (%)
   # S06        : 6시간 적설량 (cm)
   # SKY        : 하늘 상태 (1=맑음, 3=구름많음, 4=흐림 등 KMA 코드)
   # T1H        : 기온 (℃)
   # UUU        : 동서성분 풍속 (m/s)
   # VVV        : 남북성분 풍속 (m/s)
   # WAV        : 파고 (m)
   # VEC        : 풍향 (도)
   # WSD        : 풍속 (m/s)
   # 그 외 category 컬럼 : KMA 초단기예보 API의 category 코드에 따라 추가될 수 있음

   # ※ 참고
   # - category 컬럼들은 KMA 초단기예보 API에서 제공하는 항목 이름 그대로 유지
   # - pivot 처리 후 category 별로 컬럼이 생성됨
   # - datetime을 기준으로 pivot하여 각 category 값이 컬럼으로 배치됨
   # - id 컬럼은 단순 순번
   #print(f"current_location before lon: {lon}, lat: {lat}")
   # current_weather = current_location(lon,lat)
   #print(f"current_location after current_weather: {current_weather}")

    # --- 최종 반환 DataFrame df ---
    # df 컬럼 설명:
    # time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
    # temperature       : float    -> 기온(℃)
    # humidity          : float    -> 상대습도(%)
    # wind_speed        : float    -> 풍속(m/s)
    # visibility        : float    -> 가시거리(m), 기본 10000m
    # precip_prob       : float    -> 강수 확률(%), 초단기예보에는 0.0
    # precipitation     : float    -> 1시간 강수량(mm), RN1 기준
    # precip_type       : int      -> 강수 형태, PTY 기준 (0=없음, 1=비, 2=비/눈, 3=눈, 4=소나기)
    # fog_index         : float    -> 안개 지수(0~100, 높을수록 안개 심함)
    # playable_rule     : int      -> Rule 기반 골프 가능 여부 (0=불가, 1=가능)
    # playable_prob_ml  : float    -> ML(RandomForest) 예측 확률(0~1)
    # playable_ml       : int      -> ML(RandomForest) 예측 결과 (0=불가, 1=가능)
    # playable_prob_dl  : float    -> DL(NeuralNetwork) 예측 확률(0~1)
    # playable_dl       : int      -> DL(NeuralNetwork) 예측 결과 (0=불가, 1=가능)
    # final_playable    : int      -> 최종 골프 가능 여부 (0=불가, 1=가능), playable_rule OR playable_ml
    # summary           : str      -> 사람이 읽기 좋은 요약 문자열 (HTML 줄바꿈 <br> 적용)
    # 예시:
    # "2025-09-16 14:00:00 — 기온 26.0°C, 습도 85%, 풍속 2.0m/s, 강수량 7.0mm, 안개지수 12.0 → 골프장: 불가 (ML:0.12, DL:0.05)<br>👉 기온 적당, 바람 약함, 강수 주의"

   # 위도/경도만 넣으면 예측
   lon = golfDetail.loc[:,"Longitude"].values[0]
   lat = golfDetail.loc[:,"Latitude"].values[0]
   forecast_df = predict_weather_for_location(lat, lon)

   # DataFrame도 앞 6개로 잘라서 summary[:6]과 맞추기
   # df_head6 = forecast_df.head(6).copy()
   # df_head6["summary"] = summary[:6]
   # forecast_df = pd.concat([df_head6, forecast_df.iloc[6:]], axis=0)
   #print(forecast_df[["time","summary"]].head(10))

   # print("\n=== Summary 리스트 출력 ===")
   # for line in summary[:6]:
   #    print(line)

   #골프장 정보 상세
   name = 'golfInfo'
   golfDetailJson = dftoDict(golfDetail,name)
   res.update(golfDetailJson)


   #골프장 6시간 후 날씨정보
   # name = 'golfCurrentWeather'
   # timeColumn = "datetime"
   # current_weather[timeColumn] = current_weather[timeColumn].astype(str)
   # golfCurrentWeather = dftoDict(current_weather,name)
   # # print(f"골프장 6시간 후 날씨정보 딕셔너리로 변환 : {golfCurrentWeather}")
   # res.update(golfCurrentWeather)

   #골프장 24시간 후 날씨정보
   name = 'golf24HourWeather'
   timeColumn = "time"
   forecast_df[timeColumn] = forecast_df[timeColumn].astype(str)
   forecast_df  = forecast_df.to_dict(orient='records')
   forecast_df = postprocess_weather(forecast_df,timeColumn)
   #golf24HourWeather = dftoDict(forecast_df,name)
   golf24HourWeather = {name : forecast_df}
   #print(f"골프장 24시간 후 날씨정보 딕셔너리로 변환 : {golf24HourWeather}")
   res.update(golf24HourWeather)
  
   #print(f" post_services_golfDetail end")
  
   return res