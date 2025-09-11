from models.golfDetail import post_model_golfDetail,post_model_golfKmaInfo
from common.idw_interpolation import idw_df
import json, requests
import numpy as np
from common.commonDf import dftoDict
from common.weather_next import current_location
from common.weather_past import past_location
import pandas as pd
import requests, datetime
locationInfo = pd.read_excel("E:/최남회/250909_미니프로젝트/자료/source/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx")
locationInfo = locationInfo[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]

def post_services_golfDetail(id):
   print(f"services post_services_golfDetail start id : {id}")
   res = dict()
   #id로 골프상세정보 가져옴
   golfDetail = post_model_golfDetail(id)
   print(f"골프정보 : {golfDetail}")
   #kmaInfo = post_model_golfKmaInfo()
   #print(f" post_services_golfDetail 위도 : {kmaInfo.loc[:,"Latitude"]}")
   #print(kmaInfo.loc[:,"Longitude"])
   #print(kmaInfo.loc[:,"Latitude"])
   #print(f"첫번째데이터 :{kmaInfo}")
   #현재 골프장 정보에 대한 위도,경도
   lon = golfDetail.loc[:,"Longitude"].values
   lat = golfDetail.loc[:,"Latitude"].values
   #현재시간부터 6시간 후 날씨 예측 정보 
   print(f"current_location before lon: {lon}, lat: {lat}")
   current_weather = current_location(lon,lat)
   print(f"current_location after current_weather: {current_weather}")
   
   #현재시간부터 과거 날씨 데이터 예측 정보
   # print(f"past_location before lon: {lon}, lat: {lat}")
   # past_weather = past_location()
   # print(f"past_location before past_weather: {past_weather}")


   # idw태우는 로직
   #interpolated_values = idw_df(golfDetail,kmaInfo,"maxWindSpeed")

   #골프장 정보 상세
   name = 'golfInfo'
   golfDetailJson = dftoDict(golfDetail,name)
   res.update(golfDetailJson)

   #과거5년치 기상청 정보(DB)
   # name = 'pastKmaInfo'
   # kmaInfoJson = dftoDict(kmaInfo,name)
   # res.update(kmaInfoJson)
   #print(f" post_services_golfDetail end : {res}")

   #골프장 6시간 후 날씨정보
   name = 'golfCurrentWeather'
   current_weather["datetime"] = current_weather["datetime"].astype(str)
   golfCurrentWeather = dftoDict(current_weather,name)
   # print(f"골프장 6시간 후 날씨정보 딕셔너리로 변환 : {golfCurrentWeather}")
   res.update(golfCurrentWeather)

   #골프장 6시간 전 날씨정보
   # name = 'golfPastWeather'
   # golfPastWeather = dftoDict(past_weather,name)
   # # print(f"골프장 6시간 전 날씨정보 딕셔너리로 변환 : {golfPastWeather}")
   # res.update(golfPastWeather)
   
   print(f" post_services_golfDetail end")
  
   return res