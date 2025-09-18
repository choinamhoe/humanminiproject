from db.pool import engine
from sqlalchemy import text
import numpy as np
import pandas as pd

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
FROM glofInfo
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
  FROM kmaInfo kma
  LEFT OUTER JOIN weatherObsPointInfo wop
    ON kma.`지점` = wop.`지점`
   AND CURDATE() >= wop.`시작일`
   AND CURDATE() <= wop.`종료일`
   ;
"""

def post_model_golfDetail(id):
    with engine.connect() as conn:
        df = pd.read_sql(text(query_golfDetail), conn, params={"id": id} )
    if len(df) > 0:
        return df
    else :
        return {"message": "데이터 없음"}

def post_model_golfKmaInfo():
    with engine.connect() as conn:
        df = pd.read_sql(text(query_kmaInfo), conn)
        df = df.replace({np.nan: None})
    if len(df) > 0:
        return df
    else:
        return {"message": "데이터 없음"}