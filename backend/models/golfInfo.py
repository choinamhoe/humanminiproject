from db.pool import engine
from sqlalchemy import create_engine, text
import pandas as pd
from common.commonDf import dftoJson

query_golfList = """
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
"""
query_lastWeatherInfo = """
WITH ranked AS (
    SELECT id
         , STN
         , LON
         , LAT
         , TM
         , TA
         , PR
         , HM
         , WS
         , WD
         , RN
         , `geometry`
         , ROW_NUMBER() OVER (
             PARTITION BY DATE_FORMAT(STR_TO_DATE(TM, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H')
             ORDER BY ABS(TIMESTAMPDIFF(SECOND,
                       STR_TO_DATE(TM, '%Y-%m-%d %H:%i:%s'),
                       DATE_FORMAT(STR_TO_DATE(TM, '%Y-%m-%d %H:%i:%s'), '%Y-%m-%d %H:00:00')))
         ) AS rn1
    FROM miniproject.latestWeatherInfo
    WHERE STR_TO_DATE(TM, '%Y-%m-%d %H:%i:%s')
          >= DATE_SUB(CONVERT_TZ(NOW(), 'UTC', 'Asia/Seoul'), INTERVAL 24 HOUR)
)
SELECT *
FROM ranked
ORDER BY TM
"""

def post_model_golfList():
    print("models post_model_golfList start")
    with engine.connect() as conn:
        #print("models post_model_golfList 쿼리 호출 전")
        # 1. 데이터를 DataFrame으로 불러옵니다 (이 부분은 동일).
        df = pd.read_sql(query_golfList, conn)
        #print(f"models read_sql 호출 후 {df}")
        # name = 'golfInfo'
        # row = dftoJson(df,name)
    if len(df) > 0:
            return df
    else:
        return {"message": "데이터 없음"}

def post_model_lastWeatherInfo():
    print("models post_model_lastWeatherInfo start")
    with engine.connect() as conn:
        #print("models post_model_lastWeatherInfo 쿼리 호출 전")
        # 1. 데이터를 DataFrame으로 불러옵니다 (이 부분은 동일).
        df = pd.read_sql(text(query_lastWeatherInfo), conn)
        #print(f"models read_sql 호출 후 {df}")
        # name = 'golfInfo'
        # row = dftoJson(df,name)
    if len(df) > 0:
            return df
    else:
        return {"message": "데이터 없음"}
