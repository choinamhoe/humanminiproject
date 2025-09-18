import datetime, requests, os, pytz
import numpy as np
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, text
from dotenv import dotenv_values
config = dotenv_values()
print(config)
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
HOST = "host.docker.internal"
db_info = f"mysql+pymysql://{config['DB_ID']}:{config['DB_PW']}@{HOST}:{config['PORT']}/{config['DB_NAME']}"
kst = pytz.timezone("Asia/Seoul")
read_df = "/app/source/META_관측지점정보_20250912112452.csv"
BASE_URL = "https://apihub.kma.go.kr/api/typ01/url"
kma_keys = config["KMA_KEYS"].split(",")
idx = 0
try:
    if len(kma_keys)>1:
        idx = (idx + 1) % len(kma_keys)
    
    SUB_URL = "kma_sfctm3.php"
    SUB_LOCATION_URL = "stn_inf.php"
    st_dt = datetime.datetime.now(kst) - pd.to_timedelta(1, unit="hour")
    st_dt = pd.Timestamp(st_dt).round("H")
    st_dt = pd.to_datetime(st_dt).strftime("%Y%m%d%H%M")
    ed_dt = pd.to_datetime(datetime.datetime.now(kst))
    ed_dt = pd.Timestamp(ed_dt).round("H").strftime("%Y%m%d%H%M")
    key = kma_keys[idx]
    url = f"{BASE_URL}/{SUB_URL}?tm1={st_dt}&tm2={ed_dt}&help=1&authKey={key}"
    
    res = requests.get(url)
    source = res.text.split("\n")
    _source = list()
    for line in source:
        _source.append(line.split())
    hour_df=pd.DataFrame(_source[54:-2],columns=[i[2] for i in _source[4:50]])
    # 필요한 컬럼들 추출 (강수량 RN 추가)
    hour_df = hour_df[["STN","TM","TA","PR","HM","WS","WD","RN"]].copy()
    hour_df["STN"] = hour_df["STN"].astype(int)
    hour_df["TM"] = pd.to_datetime(hour_df["TM"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    # 숫자형 컬럼 변환 + 소수점 2자리 반올림
    cols = ["TA", "PR", "HM", "WS", "WD", "RN"]
    hour_df[cols] = hour_df[cols].astype(float).round(2)
    
    # ---------------------------
    # 결측값 처리
    # TA(기온 (℃)) = -99.9 → NaN (기온은 의미 없는 값이므로)
    # PR(# 기압 (hPa)) = -9 → 0.0 으로 치환
    # HM(습도 (%)) = -9 → NaN (습도는 의미 없는 값이므로)
    # WS(풍속 (m/s)) = -9 → NaN (풍속은 의미 없는 값이므로)
    # WD(풍향 (deg)) = -9 → NaN (풍향은 의미 없는 값이므로)
    # RN = -9 → 0.0 으로 치환
    # ---------------------------
    replace_map = {
        "TA": {-99.9: np.nan},  # 기온
        "PR": {-9.0: 0.0},      # 기압
        "HM": {-9.0: np.nan},   # 습도
        "WS": {-9.0: np.nan},   # 풍속
        "WD": {-9.0: np.nan},   # 풍향
        "RN": {-9.0: 0.0},      # 강수량
    }
    hour_df = hour_df.replace(replace_map)

    print(hour_df)
    location_df = pd.read_csv(read_df, encoding="cp949")
    location_df = location_df.loc[:,["지점", "경도","위도"]]
    location_df.columns = ["STN","LON","LAT"]
    location_df = location_df.astype({
        "STN": int, "LON": float, "LAT": float})
    merged_df = pd.merge(location_df, hour_df, on='STN')
    merged_df = merged_df.dropna()

    gdf = gpd.GeoDataFrame(
        merged_df, geometry=gpd.points_from_xy(
            merged_df['LON'], merged_df['LAT']), crs='EPSG:4326')
    print(
        datetime.datetime.now(kst),
        f"최종 현재부터 6시간 이후 판다스 호출 완료 : {gdf}")

    gdf.columns = gdf.columns.str.strip()          # 앞뒤 공백 제거
    gdf.columns = gdf.columns.str.replace(r'[()]', '', regex=True)  # 괄호 제거
    gdf.columns = gdf.columns.str.replace(' ', '_')  # 공백 → _

    engine = create_engine(db_info,connect_args={})
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
