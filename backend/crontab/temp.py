import json,requests
from sqlalchemy import create_engine, text
import pandas as pd
import datetime


db_info = "mysql+pymysql://root:test@localhost:13306"
engine = create_engine(db_info,connect_args={}) 
con = engine.connect()

query ="SHOW databases;"
result = con.execute(text(query))
tables = result.fetchall()

now_time = datetime.datetime.now()
pd.to_datetime(now_time).strftime("%Y%m%d%H%M%S")