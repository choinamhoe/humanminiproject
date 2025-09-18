import pytz, datetime
import pandas as pd
from models.golfDetail import post_model_golfDetail
from utils.prediction import find_closest_location, fetch_weather_kma, parse_precip, compute_fog_index_playable_rule
from config.config import config

file_path = "./source/기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(2411).xlsx"
locationInfo = pd.read_excel(file_path)
locationInfo = locationInfo[["경도(초/100)","위도(초/100)","격자 X","격자 Y"]]
locationInfo.columns = ["lon","lat","x", "y"]
keys = config["SERVICE_KEYS"].split(",")
idx = 0
def post_services_golfDetail(id, lon, lat):
   res = dict()

   global idx
   print(f"services post_services_golfDetail start id : {id}")
   if len(keys)>1:
      idx = (idx + 1) % len(keys)
   key = keys[idx]

   calc_fun = find_closest_location(lon, lat)
   locationInfo.loc[:, 'distance'] = locationInfo.apply(calc_fun, axis=1)
   nx,ny = locationInfo.loc[locationInfo["distance"].idxmin(),["x",'y']]

   kst = pytz.timezone("Asia/Seoul")
   nowtime = datetime.datetime.now(kst)
   nowtime = nowtime.replace(minute=0, second=0)
   nowtime = nowtime - pd.Timedelta(hours=1)
   # 초단기 예보(6시간)
   sub_url = "getUltraSrtFcst"
   shot_pred_df = fetch_weather_kma(nx, ny, key, sub_url, nowtime)
   shot_pred_df = shot_pred_df.pivot(
       index="datetime", 
       columns="category", 
       values="fcstValue").reset_index()

   # 단기예보(24시간)
   sub_url = "getVilageFcst"
   long_pred_df = fetch_weather_kma(nx, ny, key, sub_url, nowtime)
   long_pred_df = long_pred_df.pivot(
       index="datetime", 
       columns="category", 
       values="fcstValue").reset_index()

   cutoff = datetime.datetime.now() + datetime.timedelta(hours=5)
   long_pred_df = long_pred_df[long_pred_df["datetime"] >= cutoff]

   # 24시간까지만 제한하려면 추가 필터링
   end = datetime.datetime.now() + datetime.timedelta(hours=24)
   long_pred_df = long_pred_df[long_pred_df["datetime"] <= end]
   try:
      shot_pred_df = pd.DataFrame({
         "time": shot_pred_df["datetime"],
         "temperature": shot_pred_df["T1H"].astype(float) if "T1H" in shot_pred_df.columns else 0.0,
         "humidity": shot_pred_df["REH"].astype(float) if "REH" in shot_pred_df.columns else 0.0,
         "wind_speed": shot_pred_df["WSD"].astype(float) if "WSD" in shot_pred_df.columns else 0.0,
         "visibility": 10000,
         "precip_prob": 0.00,  # 초단기예보에는 POP 없음
         "precipitation": shot_pred_df["RN1"].apply(parse_precip) if "RN1" in shot_pred_df.columns else 0.0,
         "precip_type": shot_pred_df["PTY"].astype(int) if "PTY" in shot_pred_df.columns else 0
      })
   except Exception as e:
      print("pivot error:", e)
   try:
      long_pred_df = pd.DataFrame({
         "time": long_pred_df["datetime"],
         "temperature": long_pred_df["TMP"].astype(float) if "TMP" in long_pred_df.columns else 0.0,
         "humidity": long_pred_df["REH"].astype(float) if "REH" in long_pred_df.columns else 0.0,
         "wind_speed": long_pred_df["WSD"].astype(float) if "WSD" in long_pred_df.columns else 0.0,
         "visibility": 10000,
         "precip_prob": long_pred_df["POP"].astype(float) if "POP" in long_pred_df.columns else 0.0,
         "precipitation": long_pred_df["PCP"].apply(parse_precip) if "PCP" in long_pred_df.columns else 0.0,
         "precip_type": 0         # 없음
      })
   except:
      print("pivot error")

   pred_df = pd.concat([shot_pred_df, long_pred_df], ignore_index=True)
   print(pred_df)
   pred_df = compute_fog_index_playable_rule(pred_df)
   pred_df["time"] = pred_df["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
   pred_df = pred_df.sort_values("time").reset_index(drop=True)
   pred_df["id"] = range(1, len(pred_df)+1)
   cols = ["id"] + [col for col in pred_df.columns if col != "id"]
   pred_df = pred_df[cols]

   res.update({"golf24HourWeather":pred_df.to_dict(orient="records")})

   golfDetail = post_model_golfDetail(id)
   res.update({"golfInfo":golfDetail.to_dict(orient="records")})

   return res