# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 10:18:46 2025

@author: human
"""

import pandas as pd
from sqlalchemy import create_engine

user_id = "root"
password = "15932!miniprojectdb"
host = "localhost"
port = 30000
database_name = "miniproject"
db_info = f"mysql+pymysql://{user_id}:{password}@{host}:{port}/{database_name}"
engine = create_engine(
    db_info, connect_args={}) 

# CSV 읽기
df = pd.read_csv(r"E:/최남회/250909_미니프로젝트/자료/문화체육관광부_전국 골프장 현황_20221231.csv")
df.columns = df.columns.str.strip()          # 앞뒤 공백 제거
df.columns = df.columns.str.replace(r'[()]', '', regex=True)  # 괄호 제거
df.columns = df.columns.str.replace(' ', '_')  # 공백 → _

# DB에 저장 (id는 자동 생성되게, DataFrame엔 없음)
df.to_sql("glofInfo", con=engine, if_exists="replace", index=False)

query = """
    ALTER TABLE glofInfo
    ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT FIRST;
"""

with engine.connect() as conn:
    result = conn.execute(query)
