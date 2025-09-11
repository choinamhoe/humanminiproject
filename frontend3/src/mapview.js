// src/mapview.js
import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapview.css";

const MapView = () => {
  const [geoData, setGeoData] = useState(null);
  const [filteredLocations, setFilteredLocations] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);
  const mapRef = useRef();

  // ✅ GeoJSON 불러오기
  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/ctprvn.geojson")
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.error("GeoJSON 오류:", err));
  }, []);

  // ✅ 지역명 보정
  const regionMapping = {
    충북: "충청북도",
    충남: "충청남도",
    전북: "전라북도",
    전남: "전라남도",
    경북: "경상북도",
    경남: "경상남도",
  };

  // GeoJSON 기본 스타일
  const geoJsonStyle = {
    color: "#204172ff",
    weight: 2,
    fillColor: "#204172ff",
    fillOpacity: 0.2,
  };

  // 하이라이트 스타일
  const highlightStyle = {
    weight: 2,
    color: "#ffffff",
    fillColor: "#ffffff",
    fillOpacity: 0.4,
  };

  // 🔴 마커 아이콘
  const flagIcon = new L.Icon({
    iconUrl: process.env.PUBLIC_URL + "/red.png", // 반드시 public/red.png 확인!
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28],
  });

  // ✅ 초기화 버튼
  const handleReset = () => {
    if (mapInstance) {
      mapInstance.setView([36.5, 127.5], 7);
    }
  };

  return (
    <div className="map-wrapper" style={{ position: "relative" }}>
      <div className="map-header">
        <h2>📍 대한민국 골프장 지도</h2>
        <p>지역을 클릭하면 해당 지역의 골프장이 표시됩니다.</p>
      </div>

      <MapContainer
        center={[37.5665, 126.978]}
        zoom={7}
        className="map-container"
        ref={(ref) => {
          mapRef.current = ref;
          setMapInstance(ref);
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* 🔴 지역 클릭 후 마커 표시 */}
        {filteredLocations.map((loc, idx) => (
          <Marker
            key={idx}
            position={[loc.latitude, loc.longitude]}
            icon={flagIcon}
          >
            <Popup>
              <div className="popup-card">
                <h3>{loc.name}</h3>
                <p>{loc.address}</p>
                <small>
                  위도: {loc.latitude}, 경도: {loc.longitude}
                </small>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* GeoJSON 지역 경계 */}
        {geoData && (
          <GeoJSON
            data={geoData}
            style={(feature) =>
              selectedRegion === feature.properties?.CTP_KOR_NM
                ? highlightStyle
                : geoJsonStyle
            }
            onEachFeature={(feature, layer) => {
              layer.on({
                mouseover: (e) => {
                  if (selectedRegion !== feature.properties?.CTP_KOR_NM) {
                    e.target.setStyle(highlightStyle);
                  }
                },
                mouseout: (e) => {
                  if (selectedRegion !== feature.properties?.CTP_KOR_NM) {
                    e.target.setStyle(geoJsonStyle);
                  }
                },
                click: async () => {
                  const areaName =
                    feature.properties?.CTP_KOR_NM ||
                    feature.properties?.name ||
                    "선택 지역";

                  setSelectedRegion(areaName);
                  console.log("클릭된 지역:", areaName);

                  try {
                    // ✅ 서버에서 데이터 가져오기
                    const res = await axios.post(
                      "http://192.168.0.38:8000/detail",
                      {}
                    );
                    console.log("API 응답:", res.data);

                    const golfInfo = res.data.golfList?.golfInfo || [];

                    const parsed = golfInfo
                      .map((item) => {
                        const lat = parseFloat(item.Latitude);
                        const lng = parseFloat(item.Longitude);

                        console.log(
                          "좌표:",
                          item.storeName,
                          lat,
                          lng,
                          item.area
                        );

                        return {
                          name: item.storeName,
                          latitude: lat,
                          longitude: lng,
                          address: item.addr,
                          area: regionMapping[item.area] || item.area,
                        };
                      })
                      .filter(
                        (loc) =>
                          !isNaN(loc.latitude) &&
                          !isNaN(loc.longitude) &&
                          (loc.area.includes(areaName) ||
                            areaName.includes(loc.area))
                      );

                    console.log("필터링된 골프장:", parsed);
                    setFilteredLocations(parsed);

                    if (mapRef.current && parsed.length > 0) {
                      const bounds = parsed.map((loc) => [
                        loc.latitude,
                        loc.longitude,
                      ]);
                      mapRef.current.fitBounds(bounds);
                    }

                    layer.bindPopup(`<b>${areaName}</b>`).openPopup();
                  } catch (err) {
                    console.error("지역별 API 요청 오류:", err);
                  }
                },
              });
            }}
          />
        )}
      </MapContainer>

      {/* 🔘 초기화 버튼 */}
      <div
        style={{
          position: "absolute",
          bottom: 490,
          left: 11,
          zIndex: 10000,
          pointerEvents: "auto",
        }}
      >
        <button
          onClick={handleReset}
          style={{
            backgroundColor: "white",
            color: "black",
            border: "1px solid black",
            padding: "4px 8px",
            fontSize: "18px",
            borderRadius: "2px",
            cursor: "pointer",
            width: "32px",
            height: "32px",
            lineHeight: "24px",
            textAlign: "center",
          }}
        >
          ↻
        </button>
      </div>
    </div>
  );
};

export default MapView;
