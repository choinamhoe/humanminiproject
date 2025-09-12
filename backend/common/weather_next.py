
import pandas as pd
import requests, datetime
from geopy.distance import geodesic
# anaconda prompt 
# pip install openpyxl

# 엑셀파일 경로는 임의로 backend에 넣어뒀는데 path는 나중에 수정
df = pd.read_excel("E:/최남회/250909_미니프로젝트/자료/source/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx")
locationInfo = df[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]

def current_location(lon,lat):
    calc_fun = find_closest_location(lon, lat)
    locationInfo.loc[:, 'distance'] = locationInfo.apply(calc_fun, axis=1)
    nx,ny = locationInfo.loc[locationInfo["distance"].idxmin(),["x",'y']]
    # print(locationInfo)
    # API 호출
    key = "0a0633bc3348a83dc93f4b0516f2d5877db153b07792a880a3645c677029ce44"
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    nowtime = datetime.datetime.now()
    input_date = nowtime.strftime("%Y%m%d")
    now_time = nowtime.replace(minute=0, second=0)
    input_time = now_time - pd.Timedelta(hours=1)
    input_time = input_time.strftime("%H%M")
    # print("find_closest_location 4444444444444")
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
    # print("find_closest_location 5555555")
    response = requests.get(url, params=params)
    # print("find_closest_location 666666666")
    data = response.json()["response"]["body"]["items"]["item"]
    # print("find_closest_location 777777777777")
    pred_df = pd.DataFrame(data)
    # print(f"find_closest_location 88888888 {pred_df}")
    pred_df["datetime"] = pd.to_datetime(pred_df["fcstDate"]+pred_df["fcstTime"])
    # print(f"find_closest_location 999999999")
    


    pred_df = pred_df.pivot(index=["datetime"], columns="category", values="fcstValue").reset_index()
    
    # id 컬럼 추가 (1부터 시작)
    pred_df["id"] = range(1, len(pred_df)+1)

    # id를 제일 앞으로 이동
    cols = ["id"] + [col for col in pred_df.columns if col != "id"]
    pred_df = pred_df[cols]
    # print(f"find_closest_location 00000000000")
    # weather_future_file = f"weather_forecast_next_6h_{now_time.strftime('%Y%m%dT%H%M')}.csv"
    # print(f"find_closest_location aaaaaaaaaaaaaa")
    # pred_df.to_csv(weather_future_file, index=False, encoding="cp949")
    #print(f"find_closest_location end :  {pred_df}")
    return pred_df

def find_closest_location(lon, lat):
    # print(f"find_closest_location start lon : {lon},lat : {lat}")
    # 거리 계산 함수
    def calculate_distance(row):
        return geodesic((lat, lon), (row['lat'], row['lon'])).kilometers
    return calculate_distance
    # 골프장 위치
    # lon = 127
    # lat = 37
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
    pred_df["datetime"] = pd.to_datetime(pred_df["fcstDate"]+pred_df["fcstTime"])
    
    pred_df = pred_df.pivot(index=["datetime"], columns="category", values="fcstValue").reset_index()
    weather_future_file = f"weather_forecast_next_6h_{now_time.strftime('%Y%m%dT%H%M')}.csv"
    pred_df.to_csv(weather_future_file, index=False, encoding="cp949")
    
    return pred_df
    # 아래 변수는 엑셀로도 공유 total: 10
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