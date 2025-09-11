# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 10:18:46 2025

@author: human
"""
import os
import pandas as pd
from sqlalchemy import text
from db.pool import engine

query = """
    DROP TABLE IF EXISTS weatherObsPointInfo;
"""

# 1. 테이블 존재 시 삭제
with engine.connect() as conn:
    result = conn.execute(text(query))


# CSV 읽기
df = pd.read_csv(r"E:/최남회/250909_미니프로젝트/자료/META_관측지점정보.csv" ,encoding="cp949")
df.columns = df.columns.str.strip()          # 앞뒤 공백 제거
df.columns = df.columns.str.replace(r'[()]', '', regex=True)  # 괄호 제거
df.columns = df.columns.str.replace(' ', '_')  # 공백 → _
# '종료일' 컬럼의 null(NaN)을 99991231로 대체
df['종료일'] = df['종료일'].fillna("9999-12-31")

# DB에 저장 (id는 자동 생성되게, DataFrame엔 없음)
df.to_sql("weatherObsPointInfo", con=engine, if_exists="replace", index=False)

query = """
    ALTER TABLE weatherObsPointInfo
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT FIRST;
"""

with engine.connect() as conn:
    result = conn.execute(text(query))
