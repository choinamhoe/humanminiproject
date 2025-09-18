from models.golfInfo import post_model_golfList,post_model_lastWeatherInfo
from utils.interfolation import idw_df

def post_services_golfList():
   print("services post_services_golfList start")
   res = dict()

   lastWeatherInfo = post_model_lastWeatherInfo()
   print(lastWeatherInfo)
   golfInfo = post_model_golfList()
   
   golfInfo = idw_df(
      lastWeatherInfo, golfInfo, ["TA", "PR", "HM", "WS", "WD", "RN"])
   res.update({"golfInfo":golfInfo.to_dict(orient='records')})
   
   print(f"services post_services_golfList end")
   return res