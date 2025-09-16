from models.golfSearch import post_model_golfSearchList,post_model_lastWeatherInfo
from common.weather_next import current_location
from common.commonDf import dftoDict
from common.idw_interpolation import idw_df
import pandas as pd
import geopandas as gpd

def post_services_golfSearchList(search):
   print("services post_services_golfSearchList start")
   res = dict()
   golfInfo = post_model_golfSearchList(search)
   # print(f"post_model_golfSearchList after 위도 : {golfInfo.loc[:,"Longitude"].values}")
   # print(f"post_model_golfSearchList after 경도 : {golfInfo.loc[:,"Latitude"].values}")
   #print(f"post_model_golfSearchList after 건수 : {len(golfInfo)}")

   lastWeatherInfo = post_model_lastWeatherInfo()
   #print(f"post_model_lastWeatherInfo after 건수 : {len(lastWeatherInfo)}")
   #print(f"post_model_lastWeatherInfo after : {lastWeatherInfo}")
   
   TA_idw=idw_df(golfInfo,lastWeatherInfo,"TA")
   #print(f"TA_idw after 건수 : {len(TA_idw)}")
   PR_idw=idw_df(golfInfo,lastWeatherInfo,"PR")
   #print(f"PR_idw after 건수 : {len(PR_idw)}")
   HM_idw=idw_df(golfInfo,lastWeatherInfo,"HM")
   #print(f"HM_idw after 건수 : {len(HM_idw)}")
   WS_idw=idw_df(golfInfo,lastWeatherInfo,"WS")
   #print(f"WS_idw after 건수 : {len(WS_idw)}")
   WD_idw=idw_df(golfInfo,lastWeatherInfo,"WD")
   #print(f"WD_idw after 건수 : {len(WD_idw)}")
   RN_idw=idw_df(golfInfo,lastWeatherInfo,"RN")
   # print(f"TA_idw : {TA_idw}")
   # print(f"PR_idw : {PR_idw}")
   # print(f"HM_idw : {HM_idw}")
   # print(f"WS_idw : {WS_idw}")
   # print(f"WD_idw : {WD_idw}")
   # print(f"RN_idw : {RN_idw}")

   for i in range(len(golfInfo)):
      golfInfo.loc[i,"TA"] = TA_idw[i]
      golfInfo.loc[i,"PR"] = PR_idw[i]
      golfInfo.loc[i,"HM"] = HM_idw[i]
      golfInfo.loc[i,"WS"] = WS_idw[i]
      golfInfo.loc[i,"WD"] = WD_idw[i]
      golfInfo.loc[i,"RN"] = RN_idw[i]
   #print(f"golfInfo : {golfInfo}")
   #골프장 정보 상세
   name = 'golfInfo'
   golfInfoDict = dftoDict(golfInfo,name)
   res.update(golfInfoDict)

   print(f"services post_services_golfSearchList end")
   return res