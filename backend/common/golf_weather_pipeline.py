import pandas as pd
import numpy as np
import datetime
import pytz
import requests
import joblib

from geopy.distance import geodesic
from common.weather_next import find_closest_location2
from common.model_train import compute_fog_index_playable_rule
from common.commonDf import parse_precip

# ML/DL 함수 import (합성 데이터 관련 제거)
from common.model_train import (
    generate_synthetic_training_data,
    train_ml_model,
    train_deep_model,
    compute_fog_index_row
)

# SERVICE_KEY = "3b8dcb53f1ccdd05fb434481223a53ff8fe1a47df3860abbb1a315ddf2637338"
SERVICE_KEYS = [
    "3b8dcb53f1ccdd05fb434481223a53ff8fe1a47df3860abbb1a315ddf2637338",
    "b4334a15c2d153a244e846cf40edf1532f9bf56f262a9cc4ea5e2522ea38f9ea",
    "420b63b417a99ff90d24fb6538f51d9a3785c2e2756a544c05d27c9ebf0c0673",
    "89d11f51ba180d310e2afc89e6e9b9ce2b190d2bbac6eb6dedf116ebd641b6d2",
    ]
# DROP_KEYS = ["3b8dcb53f1ccdd05fb434481223a53ff8fe1a47df3860abbb1a315ddf2637338"]
# SERVICE_KEYS = list(set(SERVICE_KEYS) - set(DROP_KEYS))
idx = 0
# --- 샘플 골프장 좌표 (x,y는 기상청 좌표) ---
GOLF_LOCATIONS = pd.DataFrame({
    "Latitude": [37.5665, 35.1796],
    "Longitude": [126.9780, 129.0756],
    "x": [60, 98],
    "y": [127, 76]
})

# --- 위치 관련 ---
# def find_closest_location(lat, lon):
#     closest = GOLF_LOCATIONS.iloc[(GOLF_LOCATIONS[["Latitude","Longitude"]] - [lat, lon]).pow(2).sum(axis=1).idxmin()]
#     nx, ny = closest["x"], closest["y"]
#     return closest, nx, ny

# --- 위치 관련 (기존 find_closest_location 대체) ---
def find_closest_location(lat, lon):
    # GOLF_LOCATIONS 데이터프레임 사용
    closest, nx, ny = find_closest_location2(
        lat, lon,
        location_df=GOLF_LOCATIONS,
        lat_col="Latitude",
        lon_col="Longitude",
        x_col="x",
        y_col="y"
    )
    # nx, ny를 정수로 변환 (기상청 API 요구)
    nx = int(nx)
    ny = int(ny)
    return closest, nx, ny

# --- 반환값 컬럼 설명 ---
"""
df (DataFrame) 컬럼:
    id                : int   -> 순번 (1부터 시작)
    time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
    temperature       : float -> 기온(℃)
    humidity          : float -> 상대습도(%)
    wind_speed        : float -> 풍속(m/s)
    visibility        : float -> 가시거리(m), 기본 10000m
    precip_prob       : float -> 강수 확률(%)
    fog_index         : float -> 안개 지수(0~100, 높을수록 안개 심함)
    playable_rule     : int   -> Rule 기반 골프 가능 여부 (0=불가,1=가능)
    playable_prob_ml  : float -> ML(RandomForest) 예측 확률(0~1)
    playable_ml       : int   -> ML(RandomForest) 예측 결과 (0=불가,1=가능)
    playable_prob_dl  : float -> DL(NeuralNetwork) 예측 확률(0~1)
    playable_dl       : int   -> DL(NeuralNetwork) 예측 결과 (0=불가,1=가능)
    final_playable    : int   -> 최종 골프 가능 여부 (0=불가,1=가능), playable_rule OR playable_ml

summary (list of str):
    각 시간별 날씨 정보 및 골프 가능 여부를 사람이 읽기 좋은 문자열 형태
    예시:
    "2025-09-13 14:00:00 — 기온 25.0°C, 습도 65%, 풍속 4.0m/s, 안개지수 12.0 → 골프장: 가능 (ML:0.92)"
"""
# --- KMA API 호출 ---
def fetch_weather_kma(lat, lon):
    global idx 
    # print(len(SERVICE_KEYS))
    # print(idx)
    idx += 1
    idx = idx%len(SERVICE_KEYS)
    SERVICE_KEY = SERVICE_KEYS[idx]
    closest, nx, ny = find_closest_location(lat, lon)
    seoul_tz = pytz.timezone("Asia/Seoul")
    now = datetime.datetime.now(seoul_tz)
    base_date = now.strftime("%Y%m%d")
    base_time = (now.replace(minute=0, second=0) - pd.Timedelta(hours=1)).strftime("%H%M")

    # --- 테스트 모드 (SERVICE_KEY가 없는 경우 랜덤 데이터 생성) ---
    if SERVICE_KEY is None:
        hours = pd.date_range(start=now, periods=6, freq="H", tz=seoul_tz)
        rng = np.random.default_rng(123)
        df = pd.DataFrame({
            "time": hours,
            "temperature": 10 + 5*rng.normal(size=len(hours)),
            "humidity": np.clip(60 + 20*rng.normal(size=len(hours)), 0, 100),
            "wind_speed": np.clip(3 + 2*rng.normal(size=len(hours)), 0, 20),
            "visibility": 10000,
            "precip_prob": 0.00,   # 초단기예보에는 없음
            "precipitation": np.clip(0 + 10*rng.normal(size=len(hours)), 0, 100),
            "precip_type": 0         # 없음
        })
        return df

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    params = {"serviceKey": SERVICE_KEY, "numOfRows":1000, "pageNo":1,
              "dataType":"JSON","base_date":base_date,"base_time":base_time,
              "nx":int(nx),"ny":int(ny)}
    resp = requests.get(url, params=params, timeout=15)

    resp.raise_for_status()
    data = resp.json()
    #print(f"resp.json data :{data}")  # <- 먼저 API 응답 구조 확인
    items = data["response"]["body"]["items"]["item"]
    df_raw = pd.DataFrame(items)
    df_raw["datetime"] = pd.to_datetime(df_raw["fcstDate"] + df_raw["fcstTime"], format="%Y%m%d%H%M").dt.tz_localize(seoul_tz)
    pivot = df_raw.pivot(index="datetime", columns="category", values="fcstValue").reset_index()
    # --- 초단기예보에 맞게 DF 생성 ---
    try:
        df = pd.DataFrame({
            "time": pivot["datetime"],
            "temperature": pivot["T1H"].astype(float) if "T1H" in pivot.columns else 0.0,
            "humidity": pivot["REH"].astype(float) if "REH" in pivot.columns else 0.0,
            "wind_speed": pivot["WSD"].astype(float) if "WSD" in pivot.columns else 0.0,
            "visibility": 10000,
            "precip_prob": 0.00,  # 초단기예보에는 POP 없음
            "precipitation": pivot["RN1"].apply(parse_precip) if "RN1" in pivot.columns else 0.0,
            "precip_type": pivot["PTY"].astype(int) if "PTY" in pivot.columns else 0
        })
    except Exception as e:
        print("pivot error:", e)
    return df

# --- 외부 호출용 함수 ---
def fetch_weather_kma_short(lat, lon, use_deep=True):
    #print(f"fetch_weather_kma_short start lat : {lat}, lon : {lon}")
    df = fetch_weather_kma(lat, lon)
    #print(f"fetch_weather_kma after df: {df}")
    df = compute_fog_index_playable_rule(df)
    #print(f"fetch_weather_kma_short end df: {df}")
    return df

# --- 단기예보 (6~24시간) ---
def fetch_weather_kma_long(lat, lon):
    global idx 
    # print(len(SERVICE_KEYS))
    # print(idx)
    idx += 1
    idx = idx%len(SERVICE_KEYS)
    SERVICE_KEY = SERVICE_KEYS[idx]
    
    #print(f"fetch_weather_kma_long start lat : {lat}, lon : {lon}")
    closest, nx, ny = find_closest_location(lat, lon)
    seoul_tz = pytz.timezone("Asia/Seoul")
    now = datetime.datetime.now(seoul_tz)
    # --- base_time 자동 계산 ---
    def get_base_time(now):
        base_times = ["0200","0500","0800","1100","1400","1700","2000","2300"]
        for bt in reversed(base_times):
            if now.strftime("%H%M") >= bt:
                return bt
        return "2300"    
    base_date = now.strftime("%Y%m%d")
    base_time = get_base_time(now)  # 단기예보 기준시간 (예시, 실제는 KMA 기준 확인 필요)
   
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": int(nx),
        "ny": int(ny)
    }
    # print(f"fetch_weather_kma_long 요청 url : {url}, params : {params}")

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
        
    #print(f"fetch_weather_kma_long 응답 data : {data}")
    if data['response']['header']['resultCode'] != '00':
        raise ValueError(f"단기예보 API 오류: {data['response']['header']['resultMsg']}")

    items = data['response']['body']['items']['item']
    df_raw = pd.DataFrame(items)
    df_raw["datetime"] = pd.to_datetime(df_raw["fcstDate"] + df_raw["fcstTime"], format="%Y%m%d%H%M").dt.tz_localize(seoul_tz)
    pivot = df_raw.pivot(index="datetime", columns="category", values="fcstValue").reset_index()
    try:
        df = pd.DataFrame({
            "time": pivot["datetime"],
            "temperature": pivot["TMP"].astype(float) if "TMP" in pivot.columns else 0.0,
            "humidity": pivot["REH"].astype(float) if "REH" in pivot.columns else 0.0,
            "wind_speed": pivot["WSD"].astype(float) if "WSD" in pivot.columns else 0.0,
            "visibility": 10000,
            "precip_prob": pivot["POP"].astype(float) if "POP" in pivot.columns else 0.0,
            "precipitation": pivot["PCP"].apply(parse_precip) if "PCP" in pivot.columns else 0.0,
            "precip_type": 0         # 없음
        })
    except:
        print("pivot error")

    # 6시간 이상 데이터만 선택
    #df = df[df["time"] > datetime.datetime.now(seoul_tz)]
    # 6시간 이후 데이터만 선택
    cutoff = datetime.datetime.now(seoul_tz) + datetime.timedelta(hours=5)
    df = df[df["time"] >= cutoff]

    # 24시간까지만 제한하려면 추가 필터링
    end = datetime.datetime.now(seoul_tz) + datetime.timedelta(hours=24)
    df = df[df["time"] <= end]
    
    df = compute_fog_index_playable_rule(df)
    #print(f"fetch_weather_kma_long end df: {df}")

    return df

# --- 0~24시간 통합 ---
def predict_weather_for_location(lat, lon):
    df_train = generate_synthetic_training_data(2000)
    train_ml_model(df_train)
    train_deep_model(df_train)
    df_short = fetch_weather_kma_short(lat, lon)
    df_long = fetch_weather_kma_long(lat, lon)
    #print(f"predict_weather_for_location after df_short : {df_short}, df_long : {df_long}")
    df_all = pd.concat([df_short, df_long], ignore_index=True)
    #print(f"predict_weather_for_location after df_short와 df_long 합침 df_all : {df_all}")
    df_all = df_all.sort_values("time").reset_index(drop=True)
    #print(f"predict_weather_for_location after df_short와 df_long 합침 df_all : {df_all}")
    # --- id 컬럼 추가 (1부터 시작) ---
    df_all["id"] = range(1, len(df_all)+1)

    # --- id를 제일 앞으로 이동 ---
    cols = ["id"] + [col for col in df_all.columns if col != "id"]
    df_all = df_all[cols]

    return df_all