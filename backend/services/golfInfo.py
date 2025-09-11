from models.golfInfo import post_model_golfList
from common.weather_next import current_location
from common.commonDf import dftoDict

def post_services_golfList():
   print("services post_services_golfList start")
   res = dict()
   golfInfo = post_model_golfList()
   # print(f"post_model_golfList after 위도 : {golfInfo.loc[:,"Longitude"].values}")
   # print(f"post_model_golfList after 경도 : {golfInfo.loc[:,"Latitude"].values}")
   #print(f"post_model_golfList after 건수 : {len(golfInfo)}")
   
   # current_weather 값을 담을 리스트 생성
   # weather_list = []

   # for i in range(len(golfInfo)):
   #    lon = golfInfo.loc[i, "Longitude"]
   #    lat = golfInfo.loc[i, "Latitude"]
      
   #    # 현재 위치 기반 예측
   #    current_weather = current_location(lon, lat)
      
   #    # 리스트에 추가
   #    weather_list.append(current_weather)
   # print(f"루프문 끝 weather_list : {weather_list}")
   
   # # golfInfo에 새로운 컬럼으로 추가
   # golfInfo["current_weather"] = weather_list
   # print(f"루프문 끝 current_weather golfInfo : {golfInfo}")
   #골프장 정보 상세
   name = 'golfInfo'
   golfInfoDict = dftoDict(golfInfo,name)
   res.update(golfInfoDict)

   print(f"services post_services_golfList end")
   return res