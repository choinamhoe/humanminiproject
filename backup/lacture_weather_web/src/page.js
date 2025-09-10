import axios from "axios";
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet"; // leaflet import 추가
import "leaflet/dist/leaflet.css";
const sample = [
  {
    STN_KO: "서울",
    STN_EN: "Seoul",
    latitude: 37.5665,
    longitude: 126.978,
    altitude: 86,
  },
  {
    STN_KO: "부산",
    STN_EN: "Busan",
    latitude: 35.1796,
    longitude: 129.0756,
    altitude: 69,
  },
  {
    STN_KO: "대구",
    STN_EN: "Daegu",
    latitude: 35.8714,
    longitude: 128.6014,
    altitude: 57,
  },
  {
    STN_KO: "광주",
    STN_EN: "Gwangju",
    latitude: 35.1595,
    longitude: 126.8526,
    altitude: 52,
  },
  {
    STN_KO: "제주",
    STN_EN: "Jeju",
    latitude: 33.4996,
    longitude: 126.5312,
    altitude: 20,
  },
];
const MapView = () => {
  const [locations, setLocations] = useState(sample);

  useEffect(() => {
    axios
      .get("http://localhost:3001/api/locations") // 실제 API endpoint로 변경
      .then((res) => setLocations(res.data))
      .catch((err) => console.error(err));
  }, []);

  // 기본 아이콘 문제 해결 (아이콘 수정)
  const defaultIcon = new L.Icon({
    iconUrl: require("leaflet/dist/images/marker-icon.png"),
    iconSize: [25, 41], // 마커 크기
    iconAnchor: [12, 41], // 마커 앵커 위치
    popupAnchor: [1, -34], // 팝업 앵커 위치
    shadowUrl: require("leaflet/dist/images/marker-shadow.png"), // 그림자 아이콘
    shadowSize: [41, 41], // 그림자 크기
  });

  return (
    <div style={{ height: "50%", width: "50%" }}>
      <MapContainer
        center={[37.5665, 126.978]} // 서울 중심 좌표
        zoom={12}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {locations.map((loc, idx) => (
          <Marker
            key={idx}
            position={[loc.latitude, loc.longitude]}
            icon={defaultIcon}
          >
            <Popup>
              {loc.STN_KO} ({loc.STN_EN})<br />
              `위도: {loc.latitude}, 경도: {loc.longitude}, 고도:
              {loc.altitude}m`
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapView;
