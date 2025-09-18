import axios from "axios";
import URL from "../constants/url";
export const api = axios.create({
  baseURL: URL.SERVER_URL || "http://localhost:8000", // 백엔드 주소
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});
export const apiWithCookie = axios.create({
  baseURL: URL.SERVER_URL || "http://localhost:8000", // 백엔드 주소
  timeout: 15000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});
