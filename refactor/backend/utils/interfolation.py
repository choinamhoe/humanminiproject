import numpy as np
import pandas as pd 
import geopandas as gpd
def idw(
        x, y, coords, values, power=2):
    distances = np.sqrt(
        (coords[:, 0] - x)**2 + (coords[:, 1] - y)**2)
    if np.any(distances == 0):
        return values[distances == 0][0]
    weights = 1 / distances**power
    return np.sum(weights * values) / np.sum(weights)


def idw_df(origin_df, target_param_df, columnNames):
    try: 
        # 기상 정보가 있는 데이터
        gdf = gpd.GeoDataFrame(origin_df, geometry=gpd.points_from_xy(
            origin_df.loc[:,"LON"], origin_df.loc[:,"LAT"]), crs="EPSG:4326")
        gdf_proj = gdf.to_crs(epsg=3857)
        gdf["x"] = gdf_proj.geometry.x
        gdf["y"] = gdf_proj.geometry.y
        gdf = gdf.dropna(ignore_index=True)


        # 기상정보가 없는 데이터
        lat=target_param_df.loc[:,"Latitude"] 
        lon=target_param_df.loc[:,"Longitude"]
        target_df = pd.DataFrame({"lon": lon, "lat": lat})
        target_gdf = gpd.GeoDataFrame(target_df, geometry=gpd.points_from_xy(target_df["lon"], target_df["lat"]), crs="EPSG:4326")
        target_proj = target_gdf.to_crs(epsg=3857)
        target_df["x"] = target_proj.geometry.x
        target_df["y"] = target_proj.geometry.y
        
        coords = gdf[["x", "y"]].values
        for columnName in columnNames:
            values = gdf.loc[:,columnName].values
            
            interpolated_values = []
            for x, y in zip(target_df["x"], target_df["y"]):
                val = idw(x, y, coords, values)
                interpolated_values.append(val)
            target_param_df.loc[:, columnName] = interpolated_values
    except Exception as e:
        print("error",e)
    return target_param_df
