import requests
import numpy as np 
import pandas as pd
from config.config import config
from geopy.distance import geodesic

idx = 0
SERVICE_KEYS = config["SERVICE_KEYS"].split(",")
GOLF_LOCATIONS = pd.DataFrame({
    "Latitude": [37.5665, 35.1796],
    "Longitude": [126.9780, 129.0756],
    "x": [60, 98],
    "y": [127, 76]
})

def find_closest_location(lon, lat):
    # 거리 계산 함수
    def calculate_distance(row):
        return geodesic((lat, lon), (row['lat'], row['lon'])).kilometers
    return calculate_distance

def fetch_weather_kma(nx, ny, key, sub_url, datetime):
    input_date = datetime.strftime("%Y%m%d")

    
    BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
    url = f"{BASE_URL}/{sub_url}"
    if sub_url=="getVilageFcst":
        input_time = get_base_time(datetime)
    else:
        input_time = datetime.strftime("%H%M")

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
    
    data = response.json()
    data = data["response"]["body"]["items"]["item"]
    data = pd.DataFrame(data)
    data["datetime"] = pd.to_datetime(
        data["fcstDate"] + data["fcstTime"], format="%Y%m%d%H%M"
        )
    return data

def get_base_time(now):
    base_times = ["0200","0500","0800","1100","1400","1700","2000","2300"]
    for bt in reversed(base_times):
        if now.strftime("%H%M") >= bt:
            return bt
    return "2300"  

def parse_precip(pcp_str):
    #print(f"강수량 start : {pcp_str}")
    """
    기상청 초단기예보 PCP(강수량) 문자열을 float(mm)로 변환
    """
    if pcp_str is None or (isinstance(pcp_str, float) and np.isnan(pcp_str)):
        print("parse_precip 강수량이 nan")
        return 0.0
    try:
        if isinstance(pcp_str, str):
            s = pcp_str.strip()

            # --- 케이스 1: 강수 없음
            if s in ["강수없음", "0", "0.0"]:
                return 0.0

            # --- 케이스 2: 1mm 미만 (띄어쓰기 포함)
            if "1mm미만" in s or "1mm 미만" in s:
                return 0.5  # 0~1mm → 평균 0.5로 가정

            # --- 케이스 3: 범위 (~)
            if "~" in s:
                parts = s.replace("mm", "").replace(" ", "").split("~")
                try:
                    start, end = map(float, parts)
                    return (start + end) / 2
                except:
                    return 0.0

            # --- 케이스 4: 이상 (최소값 기준)
            if "이상" in s:
                try:
                    val = float(s.replace("mm 이상", "").replace("mm이상", "").strip())
                    return val + 5.0  # 최소값 + 보정치
                except:
                    return 10.0  # fallback

            # --- 케이스 5: 단순 숫자(mm 단위 포함)
            if "mm" in s:
                return float(s.replace("mm", "").strip())

            # --- 케이스 6: 숫자만
            return float(s)

        # 숫자형 (float/int)
        elif isinstance(pcp_str, (int, float)):
            if np.isnan(pcp_str):
                return 0.0
            return float(pcp_str)

    except Exception as e:
        print("precip parse error:", pcp_str, type(pcp_str), e)
        return 0.0

# --- 안개지수 계산 ---
def dew_point_celsius(Tc, RH):
    a = 17.27
    b = 237.7
    gamma = (a * Tc) / (b + Tc) + np.log(np.maximum(RH, 1) / 100.0)
    Td = (b * gamma) / (a - gamma)
    return Td

def compute_fog_index_row(T, RH, W, V):
    Td = dew_point_celsius(T, RH)
    delta = abs(T - Td)
    vis_score = np.clip((2000 - V) / 2000.0, 0, 1)
    rh_score = np.clip((RH - 70) / 30.0, 0, 1)
    wind_score = np.clip((2 - W) / 2.0, 0, 1)
    delta_score = np.clip((2 - delta) / 2.0, 0, 1)
    fog_raw = 100 * (0.4*vis_score + 0.3*rh_score + 0.2*delta_score + 0.1*wind_score)
    return float(np.clip(fog_raw, 0, 100))

def compute_fog_index_playable_rule(df):
    """
    골프장 단기 예보 DataFrame을 받아서:
    1) 안개 지수 계산
    2) Rule 기반 playable 계산
    3) ML/DL 예측
    4) 최종 playable 결정
    5) summary 생성
    """

    # --- 안개지수 계산 ---
    df["fog_index"] = df.apply(
        lambda r: compute_fog_index_row(r.temperature, r.humidity, r.wind_speed, r.visibility),
        axis=1
    )

    # --- 가시거리 추정 ---
    # 안개지수(fog_index)와 강수량(precipitation) 기반으로 visibility 계산
    # 안개 많고 강수량 많을수록 visibility 감소
    if "precipitation" not in df.columns:
        df["precipitation"] = 0.0
    df["visibility"] = 10000 - (df["fog_index"] * 50) - (df["precipitation"] * 100)
    df["visibility"] = df["visibility"].clip(lower=500)  # 최소 500m

    # --- rule 기반 골프 가능 여부 ---
    # 💡 강수량도 포함 (예: precipitation < 10mm)
    df["playable_rule"] = df.apply(
        lambda r: 1 if (r.precip_prob < 30 and r.precipitation < 10 and r.wind_speed < 10 and r.fog_index < 40) else 0,
        axis=1
    )

    # --- ML/DL 예측용 feature 리스트 ---
    features = ["temperature", "humidity", "wind_speed", "visibility", "precip_prob", "precipitation", "fog_index"]

    # 💡 예측용 df에 precipitation 컬럼이 없으면 0으로 생성
    if "precipitation" not in df.columns:
        df["precipitation"] = 0.0

    # --- 최종 골프 가능 여부 결정 ---
    # rule OR ML OR DL 예측 결과를 사용
    df["final_playable"] = df.apply(
        lambda r: int(bool(r.playable_rule)),
        axis=1
    )

    # --- summary 생성 ---
    summary = []
    for _, r in df.iterrows():
        tstr = r.time.strftime("%Y-%m-%d %H:%M:%S")

        # 멘트 조합
        comments = [
            get_temp_comment(r.temperature),
            get_humidity_comment(r.humidity),
            get_wind_comment(r.wind_speed),
            get_precip_prob_comment(r.precip_prob),
            get_precip_amount_comment(r.precipitation),
            get_visibility_comment(r.visibility)
        ]
        comments = [c for c in comments if c]  # 빈 문자열 제거
        comment_str = " ".join(comments)

        # 최종 요약 문구 (HTML 줄바꿈 적용)
        txt = (
            f"{tstr} — 기온 {r.temperature:.1f}°C, "
            f"습도 {r.humidity:.0f}%, "
            f"풍속 {r.wind_speed:.1f}m/s, "
            f"강수량 {r.precipitation:.1f}mm, "
            f"가시거리 {r.visibility:.0f}m, "
            f"안개지수 {r.fog_index:.1f} "
            f"→ 골프장: {'가능' if r.final_playable==1 else '불가'} "
            "\n"
            f"👉 {comment_str}"
        )
        txt = txt.replace("\n", "<br>")
        summary.append(txt)

    df["summary"] = summary
    df = df.reset_index(drop=True)

    # --- 최종 반환 DataFrame df ---
    # df 컬럼 설명:
    # time              : datetime -> 예측 시간 (한국 시간, tz=Asia/Seoul)
    # temperature       : float    -> 기온(℃)
    # humidity          : float    -> 상대습도(%)
    # wind_speed        : float    -> 풍속(m/s)
    # visibility        : float    -> 가시거리(m), 기본 10000m
    # precip_prob       : float    -> 강수 확률(%), 초단기예보에는 0.0
    # precipitation     : float    -> 1시간 강수량(mm), RN1 기준
    # precip_type       : int      -> 강수 형태, PTY 기준 (0=없음, 1=비, 2=비/눈, 3=눈, 4=소나기)
    # fog_index         : float    -> 안개 지수(0~100, 높을수록 안개 심함)
    # playable_rule     : int      -> Rule 기반 골프 가능 여부 (0=불가, 1=가능)
    # playable_prob_ml  : float    -> ML(RandomForest) 예측 확률(0~1)
    # playable_ml       : int      -> ML(RandomForest) 예측 결과 (0=불가, 1=가능)
    # playable_prob_dl  : float    -> DL(NeuralNetwork) 예측 확률(0~1)
    # playable_dl       : int      -> DL(NeuralNetwork) 예측 결과 (0=불가, 1=가능)
    # final_playable    : int      -> 최종 골프 가능 여부 (0=불가, 1=가능), playable_rule OR playable_ml
    # summary           : str      -> 사람이 읽기 좋은 요약 문자열 (HTML 줄바꿈 <br> 적용)
    # 예시:
    # "2025-09-16 14:00:00 — 기온 26.0°C, 습도 85%, 풍속 2.0m/s, 강수량 7.0mm, 안개지수 12.0 → 골프장: 불가 (ML:0.12, DL:0.05)<br>👉 기온 적당, 바람 약함, 강수 주의"
    return df

def get_temp_comment(t):
    if 18 <= t <= 27:
        return "쾌적한 날씨로 라운딩하기 좋습니다."
    elif 10 <= t <= 17:
        return "약간 선선합니다. 얇은 외투가 필요할 수 있습니다."
    elif 28 <= t <= 32:
        return "다소 더운 날씨, 수분 보충에 신경 쓰세요."
    elif t < 10:
        return "추운 날씨, 방한 준비가 필요합니다."
    elif t > 32:
        return "무더위 주의! 라운딩 시 열사병 예방에 주의하세요."
    return ""

def get_humidity_comment(h):
    if 40 <= h <= 70:
        return "쾌적한 습도로 플레이하기 좋습니다."
    elif 71 <= h <= 85:
        return "습도가 높아 후텁지근할 수 있습니다."
    elif h > 85:
        return "습도가 매우 높아 불쾌지수가 큽니다. 수분 보충 필요합니다."
    return ""

def get_wind_comment(w):
    if 0 <= w <= 2:
        return "바람이 거의 없어 안정적인 플레이가 가능합니다."
    elif 3 <= w <= 5:
        return "약간의 바람이 있어 클럽 선택에 참고하세요."
    elif 6 <= w <= 9:
        return "강한 바람으로 공 방향에 영향이 있습니다. 주의하세요."
    elif w >= 10:
        return "매우 강한 바람, 안전에 유의하세요."
    return ""

def get_precip_prob_comment(p):
    if p < 20:
        return "비 예보는 거의 없어 안심하고 플레이하세요."
    elif 20 <= p <= 50:
        return "소나기 가능성이 있습니다. 대비가 필요합니다."
    elif p > 50:
        return "비가 올 가능성이 큽니다. 우산을 준비하세요."
    return ""

def get_precip_amount_comment(mm):
    if mm == 0:
        return "비가 내리지 않아 쾌적합니다."
    elif 0 < mm <= 2:
        return "약한 비가 올 수 있어 레인커버를 준비하세요."
    elif 2 < mm <= 5:
        return "비가 이어질 수 있으니 플레이에 유의하세요."
    elif mm > 5:
        return "라운딩이 어려울 수 있습니다. 취소 고려 필요합니다."
    return ""

def get_visibility_comment(v):
    if v > 5000:
        return "시야가 좋아 플레이에 문제 없습니다."
    elif 2000 <= v <= 5000:
        return "안개로 인해 시야가 다소 흐립니다."
    elif v < 2000:
        return "안개가 짙어 시야 확보가 어렵습니다. 주의하세요."
    return ""
