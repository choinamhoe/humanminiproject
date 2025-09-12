from db.pool import engine
from sqlalchemy import create_engine, text
import numpy as np
import pandas as pd
import json

query_golfDetail = """
SELECT id 
     , `지역` as area 
     , `업소명` as storeName
     , `소재지` as addr
     , `총면적제곱미터` as totalAreaSquareMeters
     , `홀수홀` as addHole
     , `세부종류` as detailedType
     , Latitude
     , Longitude
FROM miniproject.glofInfo
WHERE id = :id
"""
query_kmaInfo = """
SELECT kma.id
     , kma.`지점` as spot
     , kma.`지점명` as branchName
     , kma.`일시` as dateTime
     , kma.`평균기온(°C)` as temperature
     , kma.`일강수량(mm)` as dailyPrecipitation
     , kma.`최대 순간 풍속(m/s)` as maxInstantWindSpeed
     , kma.`최대 순간 풍속 풍향(16방위)` as maxInstantWindSpeedWindDirection
     , kma.`최대 풍속(m/s)` as maxWindSpeed
     , kma.`최대 풍속 풍향(16방위)` as maxWindSpeedWindDirection
     , kma.`평균 풍속(m/s)` as avgWindSpeed
     , kma.`평균 상대습도(%)` as AvgRelHumidity
     , kma.`합계 일사량(MJ/m2)` as totalDailyDose
     , wop.`시작일` as startDate
     , wop.`종료일` as endDate
     , wop.`위도` as Latitude
     , wop.`경도` as Longitude
  FROM miniproject.kmaInfo kma
  LEFT OUTER JOIN miniproject.weatherObsPointInfo wop
    ON kma.`지점` = wop.`지점`
   AND CURDATE() >= wop.`시작일`
   AND CURDATE() <= wop.`종료일`
   ;
"""

def post_model_golfDetail(id):
    print(f"models post_model_golfDetail start id : {id}")
    with engine.connect() as conn:
        #print("read_sql 읽기 전")
        # 1. 데이터를 DataFrame으로 불러옵니다 (이 부분은 동일).
        df = pd.read_sql(text(query_golfDetail), conn, params={"id": id} )
        print(f"post_model_golfDetail 위도 : {df.loc[:,"Latitude"]}")
         

    if len(df) > 0:
        return df
    else :
        return {"message": "데이터 없음"}

def post_model_golfKmaInfo():
    print(f"models post_model_golfKmaInfo start ")
    with engine.connect() as conn:
        #print("read_sql 읽기 전")
        # 1. 데이터를 DataFrame으로 불러옵니다 (이 부분은 동일).
        df = pd.read_sql(text(query_kmaInfo), conn)
        df = df.replace({np.nan: None})
        #df = df.iloc[:50000]
        #print(df.iloc[:1,:])
        #print(f"post_model_golfKmaInfo 위도 : {df.loc[:,"Latitude"]}")
    if len(df) > 0:
        return df
    else:
        return {"message": "데이터 없음"}