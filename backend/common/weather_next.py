
import os
import pandas as pd
import requests, datetime
from geopy.distance import geodesic
import pytz

# 현재 실행 중인 파일(weather_next.py)의 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 상대경로로 접근할 파일 (.. 은 상위폴더)
excel_path = os.path.join(BASE_DIR, "..", "..", "자료", "source", "기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx")

# 엑셀 불러오기
df = pd.read_excel(excel_path)

print(df.head())

# 엑셀파일 경로는 임의로 backend에 넣어뒀는데 path는 나중에 수정
locationInfo = df[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]

# ---------------------------
# pred_df 컬럼 설명
# ---------------------------
# id             : 각 row 고유 번호 (1부터 시작)
# datetime       : 예보 시간 (서울시간 기준, datetime)
# temperature    : 기온 (℃)
# humidity       : 상대습도 (%)
# precip_type    : 강수 형태 (0=없음, 1=비, 2=비/눈, 3=눈)
# precip_prob    : 강수 확률 (%)
# snow_6h        : 6시간 적설량 (cm)
# rain_6h        : 6시간 강수량 (mm)
# wind_u         : 동서성분 풍속 (m/s)
# wind_v         : 남북성분 풍속 (m/s)
# wave_height    : 파고 (m)
# wind_dir       : 풍향 (°)
# wind_speed     : 풍속 (m/s)
# ※ category에 없는 항목은 컬럼에서 제외됨

# ※ 참고
# - category 컬럼들은 KMA 초단기예보 API에서 제공하는 항목 이름 그대로 유지
# - pivot 처리 후 category 별로 컬럼이 생성됨
# - datetime을 기준으로 pivot하여 각 category 값이 컬럼으로 배치됨
# - id 컬럼은 단순 순번
def current_location(lon, lat):
    calc_fun = find_closest_location(lon, lat,lat_col='lat',  lon_col='lon')
    locationInfo.loc[:, 'distance'] = locationInfo.apply(calc_fun, axis=1)
    nx, ny = locationInfo.loc[locationInfo["distance"].idxmin(), ["x", 'y']]
    print(locationInfo)

    # API 호출
    key = "0a0633bc3348a83dc93f4b0516f2d5877db153b07792a880a3645c677029ce44"
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    # 한국 시간대 설정
    seoul_tz = pytz.timezone("Asia/Seoul")
    nowtime = datetime.datetime.now(seoul_tz)
    input_date = nowtime.strftime("%Y%m%d")
    now_time = nowtime.replace(minute=0, second=0)
    input_time = (now_time - pd.Timedelta(hours=1)).strftime("%H%M")

    params = {
        'serviceKey': key,
        'numOfRows': '1000',
        'pageNo': '1',
        'dataType': 'JSON',
        'base_date': input_date,
        'base_time': input_time,
        'nx': int(nx),
        'ny': int(ny)
    }

    response = requests.get(url, params=params)
    data = response.json()["response"]["body"]["items"]["item"]
    pred_df = pd.DataFrame(data)

    # datetime 컬럼 생성
    pred_df["datetime"] = pd.to_datetime(pred_df["fcstDate"] + pred_df["fcstTime"])

    # pivot 처리: category별 값을 열로 변환
    pred_df = pred_df.pivot(index=["datetime"], columns="category", values="fcstValue").reset_index()

    # ---------------------------
    # KMA category 코드 → 의미 있는 컬럼명 매핑
    # ---------------------------
    column_mapping = {
        "T1H": "temperature",  # 기온 (℃)
        "REH": "humidity",     # 상대습도 (%)
        "PTY": "precip_type",  # 강수형태 (0=없음, 1=비, 2=비/눈, 3=눈)
        "POP": "precip_prob",  # 강수확률 (%)
        "S06": "snow_6h",      # 6시간 적설량 (cm)
        "R06": "rain_6h",      # 6시간 강수량 (mm)
        "UUU": "wind_u",       # 동서성분 풍속 (m/s)
        "VVV": "wind_v",       # 남북성분 풍속 (m/s)
        "WAV": "wave_height",  # 파고 (m)
        "VEC": "wind_dir",     # 풍향 (°)
        "WSD": "wind_speed"    # 풍속 (m/s)
        # 필요 시 다른 category 추가 가능
    }
    pred_df.rename(columns=column_mapping, inplace=True)

    # id 컬럼 추가 (1부터 시작)
    pred_df["id"] = range(1, len(pred_df) + 1)

    # id를 제일 앞으로 이동
    cols = ["id"] + [col for col in pred_df.columns if col != "id"]
    pred_df = pred_df[cols]

    # ---------------------------
    # pred_df 컬럼 설명
    # ---------------------------
    # id             : 각 row 고유 번호 (1부터 시작)
    # datetime       : 예보 시간 (서울시간 기준, datetime)
    # temperature    : 기온 (℃)
    # humidity       : 상대습도 (%)
    # precip_type    : 강수 형태 (0=없음, 1=비, 2=비/눈, 3=눈)
    # precip_prob    : 강수 확률 (%)
    # snow_6h        : 6시간 적설량 (cm)
    # rain_6h        : 6시간 강수량 (mm)
    # wind_u         : 동서성분 풍속 (m/s)
    # wind_v         : 남북성분 풍속 (m/s)
    # wave_height    : 파고 (m)
    # wind_dir       : 풍향 (°)
    # wind_speed     : 풍속 (m/s)
    # ※ category에 없는 항목은 컬럼에서 제외됨

    #print(f"find_closest_location end :  {pred_df}")
    return pred_df


def find_closest_location(lon, lat, lat_col, lon_col):
    # print(f"find_closest_location start lon : {lon},lat : {lat}")
    # 거리 계산 함수
    def calculate_distance(row):
        #return geodesic((lat, lon), (row['lat'], row['lon'])).kilometers
        #return geodesic((lat, lon), (row['Latitude'], row['Longitude'])).kilometers
        return geodesic((lat, lon), (row[lat_col], row[lon_col])).kilometers
    return calculate_distance

def find_closest_location2(lat, lon, location_df, lat_col, lon_col, x_col, y_col):
    from geopy.distance import geodesic

    # 거리 계산 함수
    location_df = location_df.copy()
    location_df['distance'] = location_df.apply(
        lambda row: geodesic((lat, lon), (row[lat_col], row[lon_col])).kilometers,
        axis=1
    )
    closest = location_df.loc[location_df['distance'].idxmin()]
    nx = closest[x_col]
    ny = closest[y_col]
    return closest, nx, ny

