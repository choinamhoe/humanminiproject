from db.pool import engine
from sqlalchemy import create_engine, text
import pandas as pd
from common.commonDf import dftoJson

query_golfList = """
SELECT id 
     , `지역` as area 
     , `업소명` as storeName
     , `소재지` as addr
     , Latitude
     , Longitude
FROM miniproject.glofInfo
"""
def post_model_golfList():
    print("models post_model_golfList start")
    with engine.connect() as conn:
        # 1. 데이터를 DataFrame으로 불러옵니다 (이 부분은 동일).
        df = pd.read_sql(query_golfList, conn)
        name = 'golfInfo'
        row = dftoJson(df,name)
    if row:
        return row
    else:
        return {"message": "데이터 없음"}

