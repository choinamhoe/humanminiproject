from models.golfDetail import post_model_golfDetail,post_model_golfKmaInfo
from common.idw_interpolation import idw_df
import json, requests
import numpy as np
from common.commonDf import dftoJson

def post_services_golfDetail(id):
   print(f"services post_services_golfDetail start id : {id}")
   res = list()
   #id로 골프상세정보 가져옴
   golfDetail = post_model_golfDetail(id)
   print(f"골프정보 : {golfDetail}")
   kmaInfo = post_model_golfKmaInfo()
   print(f" post_services_golfDetail 위도 : {kmaInfo.loc[:,"Latitude"]}")
   #print(kmaInfo.loc[:,"Longitude"])
   #print(kmaInfo.loc[:,"Latitude"])
   #print(f"첫번째데이터 :{kmaInfo}")

   # idw태우는 로직
   #interpolated_values = idw_df(golfDetail,kmaInfo,"maxWindSpeed")

   #골프장 정보 상세
   name = 'golfInfo'
   golfDetailJson = dftoJson(golfDetail,name)
   res.append(golfDetailJson)

   #과거 기상청 정보(DB)
   name = 'pastKmaInfo'
   kmaInfoJson = dftoJson(kmaInfo,name)
   res.append(kmaInfoJson)
   #print(f" post_services_golfDetail end : {res}")
   print(f" post_services_golfDetail end")
  
   return res