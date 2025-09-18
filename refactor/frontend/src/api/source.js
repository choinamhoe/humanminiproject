import { api } from "./axios";
import axios from "axios";

export const getGolfInfoAll = async () => {
  try {
    const res = await api.post(`/`);
    return res.data;
  } catch (err) {
    console.error("api 요청 실패", err);
    throw err;
  }
};

export const getGeoData = async () => {
  try {
    const res = await axios.get(`${process.env.PUBLIC_URL}/geo/ctprvn.geojson`);
    return res;
  } catch (err) {
    console.error("GeoJSON 오류: ", err);
    throw err;
  }
};

export const getDetailData = async (id, lon, lat) => {
  try {
    const response = await api.post("/detail", { id, lon, lat });
    console.log(response);
    return response.data;
  } catch (error) {
    console.error("API 호출 실패:", error);
    throw error;
  }
};
