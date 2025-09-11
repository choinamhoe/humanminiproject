import pandas as pd
import requests, datetime
from geopy.distance import geodesic

df = pd.read_excel("기상청41_단기예보 조회서비스_오픈API활용가이드_241128/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx")
locationInfo = df[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]
locationInfo

def find_closest_location(lon, lat):
    # 거리 계산 함수
    def calculate_distance(row):
        return geodesic((lat, lon), (row['lat'], row['lon'])).kilometers
    return calculate_distance
# 곮프장 위치
lon = 127
lat = 37

calc_fun = find_closest_location(lon, lat)
# 거리 계산
locationInfo.loc[:, 'distance'] = locationInfo.apply(calc_fun, axis=1)

# 가장 가까운 격자 산출
nx,ny = locationInfo.loc[locationInfo["distance"].idxmin(),["x",'y']]

# API 호출
key = "0a0633bc3348a83dc93f4b0516f2d5877db153b07792a880a3645c677029ce44"
url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
nowtime = datetime.datetime.now()
input_date = nowtime.strftime("%Y%m%d")
now_time = nowtime.replace(minute=0, second=0)
input_time = now_time - pd.Timedelta(hours=1)
input_time = input_time.strftime("%H%M")

params ={
    'serviceKey' : key, 
    'numOfRows' : '1000', # 한 페이지 결과
    'pageNo' : '1', 
    'dataType' : 'JSON', 
    'base_date' : input_date , # 발표일자
    'base_time' : input_time,  # 30분 단위
    'nx' : int(nx), 
    'ny' : int(ny) 
    }

response = requests.get(url, params=params)
data = response.json()["response"]["body"]["items"]["item"]
pred_df = pd.DataFrame(data)
pred_df
pred_df["datetime"] = pd.to_datetime(pred_df["fcstDate"]+pred_df["fcstTime"])
pred_df = pred_df.pivot(index=["datetime"], columns="category", values="fcstValue").reset_index()


"""
T1H	기온	℃
RN1	1시간 강수량	범주 (1 mm)
SKY	하늘상태	코드값
UUU	동서바람성분	m/s
VVV	남북바람성분	m/s
REH	습도	%
PTY	강수형태	코드값
LGT	낙뢰	kA(킬로암페어)
VEC	풍향	deg
WSD	풍속	m/s
"""