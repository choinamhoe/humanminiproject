from db.pool import engine
from sqlalchemy import create_engine, text
import pandas as pd
import json

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
        # 2. 💡 DataFrame을 딕셔너리의 '리스트' 형태로 변환합니다.
        # orient='records' 옵션이 각 행을 하나의 딕셔너리로 만들어 리스트에 담아줍니다.
        golf_list  = df.to_dict(orient='records')
        # 3. 원하는 대표 이름('golfInfo')을 키로 하는 최종 딕셔너리를 만듭니다.
        final_dict = {'golfInfo': golf_list}
        # 결과 확인 (pprint나 json.dumps를 사용하면 보기 편합니다)
        row = json.dumps(final_dict, indent=2, ensure_ascii=False)
        #print(row)
    if row:
        return row
    return {"message": "데이터 없음"}
    # with engine.connect() as conn:
    #     result = conn.execute(text(query_golfList))
    #     row = result.fetchall()
    #     print(f"models post_model_golfList end")
