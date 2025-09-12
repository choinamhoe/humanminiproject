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


weather_past_test = f"weather_obs_past_6h_{now_time.strftime('%Y%m%dT%H%M')}.csv"
hour_df.to_csv(weather_past_test, index=False, encoding="cp949")


# 아래 변수는 엑셀로도 공유 toal: 46
"""
TM	관측시각 (KST)
WD	풍향 (36방위)
GST_WD	돌풍향 (36방위)
GST_TM	돌풍속이 관측된 시각 (시분)
PS	해면기압 (hPa)
PR	기압변화량 (hPa)
TD	이슬점온도 (C)
PV	수증기압 (hPa)
RN_DAY	위 관측시간까지의 일강수량 (mm)
SD_HR3	3시간 신적설 (cm)
SD_TOT	적설 (cm)
WP	GTS 과거일기 (Code 4561)
CA_TOT	전운량 (1/10)
CH_MIN	최저운고 (100m)
CT_TOP	GTS 상층운형 (Code 0509)
CT_LOW	GTS 하층운형 (Code 0513)
SS	일조 (hr)
ST_GD	지면상태 코드 (코드는 기상자원과 문의) 종료: 2016.7.1. 00시
TE_005	5cm 지중온도 (C)
TE_02	20cm 지중온도 (C)
ST_SEA	해면상태 코드 (코드는 기상자원과 문의)
BF	Beaufart 최대풍력(GTS코드)
IX	유인관측/무인관측
STN	국내 지점번호
WS	풍속 (m/s)
GST_WS	돌풍속 (m/s)
PA	현지기압 (hPa)
PT	기압변화경향 (Code 0200)
TA	기온 (C)
HM	상대습도 (%)
RN	강수량 (mm)
RN_INT	강수강도 (mm/h)
SD_DAY	일 신적설 (cm)
WC	GTS 현재일기 (Code 4677)
WW	국내식 일기코드 (문자열 22개)
CA_MID	중하층운량 (1/10)
CT	운형 (문자열 8개)
CT_MID	GTS 중층운형 (Code 0515)
VS	시정 (10m)
SI	일사 (MJ/m2)
TS	지면온도 (C)
TE_01	10cm 지중온도 (C)
TE_03	30cm 지중온도 (C)
WH	파고 (m)
IR	강수자료
RN_JUN	일강수량 (mm)

"""












