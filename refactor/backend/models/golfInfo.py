from db.pool import engine
from sqlalchemy import text
import pandas as pd

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
FROM glofInfo
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
    FROM latestWeatherInfo
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
        df = pd.read_sql(text(query_golfList), conn)
    if len(df) > 0:
            return df
    else:
        return {"message": "데이터 없음"}

def post_model_lastWeatherInfo():
    print("models post_model_lastWeatherInfo start")
    with engine.connect() as conn:
        df = pd.read_sql(text(query_lastWeatherInfo), conn)
    if len(df) > 0:
            return df
    else:
        return {"message": "데이터 없음"}
