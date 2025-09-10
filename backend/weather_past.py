import json, requests
import numpy as np
import pandas as pd
import geopandas as gpd
import os
from dotenv import load_dotenv
load_dotenv() 
import datetime

key = os.getenv("API_KEY", "")

BASE_URL = "https://apihub.kma.go.kr/api/typ01/url"
SUB_URL ="kma_sfctm3.php"
#st_dt = "2015-12-11 01:00"
#ed_dt = "2015-12-11 02:00"
now_time = datetime.datetime.now().replace(
    minute=0, second=0, microsecond=0)
ed_dt = now_time 
st_dt = now_time - pd.to_timedelta(6, unit='h')
st_dt=pd.to_datetime(st_dt).strftime("%Y%m%d%H%M")
ed_dt=pd.to_datetime(ed_dt).strftime("%Y%m%d%H%M")


url = f"{BASE_URL}/{SUB_URL}?tm1={st_dt}&tm2={ed_dt}&help=1&authKey={key}"
response = requests.get(url)

source = response.text.split("\n")
source = [line.split() for line in source]
hour_df=pd.DataFrame(source[54:-2],columns=[i[2] for i in source[4:50]])

print(st_dt)
print(ed_dt)

