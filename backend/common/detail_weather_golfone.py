import requests
import pandas as pd
from datetime import datetime

def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    hourly_data = data['hourly'][:24]  # 현재 시간부터 24시간 데이터
    # DataFrame 변환
    df = pd.DataFrame(hourly_data)
    df['time'] = pd.to_datetime(df['dt'], unit='s')
    df['temperature'] = df['temp']
    df['humidity'] = df['humidity']
    df['wind_speed'] = df['wind_speed']
    df['visibility'] = df.get('visibility', 10000)  # 없으면 기본 10km
    return df[['time','temperature','humidity','wind_speed','visibility']]

# 예시
lat = 37.5665  # 서울
lon = 126.9780
api_key = 'YOUR_OPENWEATHERMAP_API_KEY'

weather_df = get_weather_data(lat, lon, api_key)
print(weather_df.head())

# 간단한 안개지수 계산식:
#Fog Index= Humidity×DewPoint / 100
#Dew Point를 근사로 계산합니다.​
def calculate_fog_index(temp, humidity):
    # Dew point 근사 공식
    dew_point = temp - ((100 - humidity) / 5)
    fog_index = dew_point * humidity / 100
    return fog_index

weather_df['fog_index'] = weather_df.apply(lambda row: calculate_fog_index(row['temperature'], row['humidity']), axis=1)
print(weather_df[['time','fog_index']])

#1: 골프 가능
#0: 골프 불가
def label_golf_playable(row):
    # 간단 규칙 예시: 안개지수 < 2, 시야 >= 1000m, 바람 <= 10m/s
    if row['fog_index'] < 2 and row['visibility'] >= 1000 and row['wind_speed'] <= 10:
        return 1
    else:
        return 0

weather_df['golf_playable'] = weather_df.apply(label_golf_playable, axis=1)
print(weather_df[['time','golf_playable']])
