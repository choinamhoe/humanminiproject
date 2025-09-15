# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 09:18:16 2025

@author: human
"""
# gdf 컬럼 설명:
# STN      : 관측소 번호 (Station ID, 기상청 고유 식별자)
# LON      : 관측소 경도 (Longitude, WGS84 좌표계)
# LAT      : 관측소 위도 (Latitude, WGS84 좌표계)
# TM       : 관측 시각 (Timestamp, YYYY-MM-DD HH:MM:SS)
# TA       : 기온 (Temperature, ℃)
# PR       : 기압 (Pressure, hPa)
# HM       : 상대습도 (Humidity, %)
# WS       : 풍속 (Wind Speed, m/s)
# WD       : 풍향 (Wind Direction, degree, 0~360°)
# RN       : 강수량 (Precipitation, mm, 해당 시각까지의 누적 혹은 시강수 depending on KMA 제공값)
# geometry : Shapely Point 객체 (위치 좌표, EPSG:4326)
try:
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import datetime, requests, os, pytz
    from dotenv import load_dotenv
    from shapely.geometry import Point
    from sqlalchemy import create_engine, text
    import datetime
    #from db.pool import engine
    kst = pytz.timezone("Asia/Seoul")
    print(datetime.datetime.now(kst),f"cron_1hour start")
    user_id = "root"
    password = "15932!miniprojectdb"
    host = "host.docker.internal"
    port = 30000
    database_name = "miniproject"
    read_df = "/app/META_관측지점정보_20250912112452.csv"

    db_info = f"mysql+pymysql://{user_id}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(
        db_info,connect_args={}
        )

    # IDW 보간 함수
    def idw_interpolation(
            x, y, coords, values, power=2):
        distances = np.sqrt(
            (coords[:, 0] - x)**2 + (coords[:, 1] - y)**2)
        if np.any(distances == 0):
            return values[distances == 0][0]
        weights = 1 / distances**power
        return np.sum(weights * values) / np.sum(weights)

    #load_dotenv()
    key = os.getenv("KMA_API_KEY")
    key = "K66mUw9zTByuplMPczwchQ"

    BASE_URL = "https://apihub.kma.go.kr/api/typ01/url"
    SUB_URL = "kma_sfctm3.php"
    SUB_LOCATION_URL = "stn_inf.php"
    

    st_dt = datetime.datetime.now(kst) - pd.to_timedelta(1, unit="hour")
    st_dt = pd.Timestamp(st_dt).round("H")
    st_dt = pd.to_datetime(st_dt).strftime("%Y%m%d%H%M")
    ed_dt = pd.to_datetime(datetime.datetime.now(kst))
    ed_dt = pd.Timestamp(ed_dt).round("H").strftime("%Y%m%d%H%M")
    url = f"{BASE_URL}/{SUB_URL}?tm1={st_dt}&tm2={ed_dt}&help=1&authKey={key}"
    #print(datetime.datetime.now(kst),f"URL주소 : {url}")


    #location_df = pd.read_csv(
    #    "C:/Users/human/Downloads/META_관측지점정보_20250912112452.csv",
    #    encoding="cp949")
    location_df = pd.read_csv(
        read_df,
        encoding="cp949")
    #print(datetime.datetime.now(kst),f"읽어드린 판다스 관측지점정보 : {location_df}")

    res = requests.get(url)
    source = res.text.split("\n")

    _source = list()
    for line in source:
        _source.append(line.split())
    hour_df=pd.DataFrame(_source[54:-2],columns=[i[2] for i in _source[4:50]])
    #hour_df=hour_df[["STN","TM","TA","PR","HM","WS","WD"]].copy()
    # 필요한 컬럼들 추출 (강수량 RN 추가)
    hour_df = hour_df[["STN","TM","TA","PR","HM","WS","WD","RN"]].copy()
    hour_df["STN"] = hour_df["STN"].astype(int)
    hour_df["TM"] = pd.to_datetime(hour_df["TM"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    # 숫자형 컬럼 변환 + 소수점 2자리 반올림
    hour_df["TA"]  = hour_df["TA"].astype(float).round(2)   # 기온 (℃)
    hour_df["PR"]  = hour_df["PR"].astype(float).round(2)   # 기압 (hPa)
    hour_df["HM"]  = hour_df["HM"].astype(float).round(2)   # 습도 (%)
    hour_df["WS"]  = hour_df["WS"].astype(float).round(2)   # 풍속 (m/s)
    hour_df["WD"]  = hour_df["WD"].astype(float).round(2)   # 풍향 (deg)
    hour_df["RN"]  = hour_df["RN"].astype(float).round(2)   # 강수량 (mm)

    # ---------------------------
    # 결측값 처리
    # TA(기온 (℃)) = -99.9 → NaN (기온은 의미 없는 값이므로)
    # PR(# 기압 (hPa)) = -9 → 0.0 으로 치환
    # HM(습도 (%)) = -9 → NaN (습도는 의미 없는 값이므로)
    # WS(풍속 (m/s)) = -9 → NaN (풍속은 의미 없는 값이므로)
    # WD(풍향 (deg)) = -9 → NaN (풍향은 의미 없는 값이므로)
    # RN = -9 → 0.0 으로 치환
    # ---------------------------
    hour_df["TA"] = hour_df["TA"].replace(-99.9, np.nan)   # <- 꼭 숫자로 바꿔야 한다면 0.0으로도 가능
    hour_df["PR"] = hour_df["PR"].replace(-9.0, 0.0)
    hour_df["HM"] = hour_df["HM"].replace(-9.0, np.nan)
    hour_df["WS"] = hour_df["WS"].replace(-9.0, np.nan)
    hour_df["WD"] = hour_df["WD"].replace(-9.0, np.nan)
    hour_df["RN"] = hour_df["RN"].replace(-9.0, 0.0)
    
    location_df = location_df.loc[:,["지점", "경도","위도"]]
    location_df.columns = ["STN","LON","LAT"]
    location_df["STN"] = location_df["STN"].astype(int)
    location_df["LON"] = location_df["LON"].astype(float)
    location_df["LAT"] = location_df["LAT"].astype(float)
    merged_df = pd.merge(location_df, hour_df, on='STN')
    merged_df = merged_df.dropna()

    gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df['LON'], merged_df['LAT']), crs='EPSG:4326')
    print(datetime.datetime.now(kst),f"최종 현재부터 6시간 이후 판다스 호출 완료 : {gdf}")

    gdf.columns = gdf.columns.str.strip()          # 앞뒤 공백 제거
    gdf.columns = gdf.columns.str.replace(r'[()]', '', regex=True)  # 괄호 제거
    gdf.columns = gdf.columns.str.replace(' ', '_')  # 공백 → _

    query = """
        DROP TABLE IF EXISTS latestWeatherInfo;
    """

    # 1. 테이블 존재 시 삭제
    with engine.connect() as conn:
        result = conn.execute(text(query))
        
    # DB에 저장 (id는 자동 생성되게, DataFrame엔 없음)
    gdf.to_sql("latestWeatherInfo", con=engine, if_exists="replace", index=False)

    query = """
        ALTER TABLE latestWeatherInfo
        ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT FIRST;
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
except Exception as e:
    print("error",e)