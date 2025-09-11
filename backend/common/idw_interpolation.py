import numpy as np
import geopandas as gpd
import pandas as pd 

def idw_df(origin_df,target_param_df,columnName):
    #기상청에 있는 위도,경도
    gdf = gpd.GeoDataFrame(target_param_df, geometry=gpd.points_from_xy(
        target_param_df.loc[:,"Longitude"], target_param_df.loc[:,"Latitude"]), crs="EPSG:4326")
    print(f" target_param_df 정보 : {gdf}")
    
    gdf_proj = gdf.to_crs(epsg=3857)
    gdf["x"] = gdf_proj.geometry.x
    gdf["y"] = gdf_proj.geometry.y
    gdf = gdf.dropna(ignore_index=True)
    print(f" target_param_df 정보 결측값 제거 : {gdf}")
    print(f" origin_df 위치(위도,경도) : {origin_df.iloc[:,:]}")
    
    print(f" origin_df 위치(위도,경도) 위도: {origin_df.loc[:,"Latitude"]}")
    print(f" origin_df 위치(위도,경도) 경도 : {origin_df.loc[:,"Longitude"]}")

    # 현재 골프장 위치(위도,경도)
    lat=[origin_df.loc[:,"Latitude"]] 
    lon=[origin_df.loc[:,"Longitude"]]
    print(f" origin_df 정보 lat : {lat}, lon : {lon}")

    #현재 골프장 위치를 df로 확인
    target_df = pd.DataFrame({"lon": lon, "lat": lat})
    target_gdf = gpd.GeoDataFrame(target_df, geometry=gpd.points_from_xy(target_df["lon"], target_df["lat"]), crs="EPSG:4326")
    target_proj = target_gdf.to_crs(epsg=3857)
    target_df["x"] = target_proj.geometry.x
    target_df["y"] = target_proj.geometry.y
    print(f" origin_df target_df x: {target_df["x"]}")
    print(f" origin_df target_df y: {target_df["y"]}")

    coords = gdf[["x", "y"]].values
    print(f" idw태우기 전  coords : {coords[:, 0]}")
    values = target_param_df.loc[:,columnName].values
    print(f" idw태우기 전  values : {values}")
    print(f" idw태우기 전  target_df[x] : {target_df["x"]}")
    print(f" idw태우기 전  target_df[y] : {target_df["y"]}")

    interpolated_values = []
    for x, y in zip(target_df["x"], target_df["y"]):
        print(f"idw 돌리기 전")

        val = idw_interpolation(x, y, coords, values)
        print(f"idw 돌리기 후 : {val}")
        interpolated_values.append(val)
    print(f"idw 돌리고 나온 값 : { interpolated_values}")
    return interpolated_values

def idw_interpolation(x, y, coords, values, power=2):
    print(f"idw_interpolation start x : {x}, y: {y}")
    distances = np.sqrt((coords[:, 0] - x)**2 + (coords[:, 1] - y)**2)
    print(f"idw_interpolation distances : {distances}")
    
    # if np.any(distances == 0):
    #     return values[distances == 0][0]
    weights = 1 / distances**power
    print(f"idw_interpolation weights : {weights}")
    result = np.sum(weights * values) / np.sum(weights)
    print(f"idw_interpolation end 결과 : {result}")
    return result