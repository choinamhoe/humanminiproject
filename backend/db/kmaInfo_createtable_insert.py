# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 10:18:46 2025

@author: human
"""
import os
import pandas as pd
from sqlalchemy import text
import glob
from db.pool import engine

query = """
    DROP TABLE IF EXISTS kmaInfo;
"""

# 1. 테이블 존재 시 삭제
with engine.connect() as conn:
    result = conn.execute(text(query))


# 2. 연도별 CSV 파일 경로 가져오기
file_list = glob.glob("E:/최남회/250909_미니프로젝트/자료/기상청날씨자료/*.csv")  # 경로는 맞게 수정

# 3. CSV 읽어서 합치기
df_list = []
for file in file_list:
    df = pd.read_csv(file,encoding="cp949")
    df_list.append(df)

all_data = pd.concat(df_list, ignore_index=True)

# 4. DB에 넣기 (테이블명은 예: weather_info)
all_data.to_sql("kmaInfo", engine, if_exists="append", index=False)
    
query = """
    ALTER TABLE kmaInfo
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT FIRST;
"""
with engine.connect() as conn:
    result = conn.execute(text(query))
