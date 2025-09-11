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
  const [regionWeather, setRegionWeather] = useState({}); // 지역별 비 여부 상태 (ex: { 서울특별시: true, 부산광역시: false })
  const mapRef = useRef();

  // GeoJSON 불러오기
  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/ctprvn.geojson")
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.error("GeoJSON 오류:", err));
  }, []);

  // 예시로 지역별 비 여부 데이터 하드코딩 (실제는 API 호출 등으로 대체)
  useEffect(() => {
    const exampleWeatherData = {
      서울특별시: true,
      부산광역시: false,
      대구광역시: false,
      인천광역시: true,
      광주광역시: true,
      대전광역시: false,
      울산광역시: false,
      세종특별자치시: false,
      경기도: true,
      강원특별자치도: false,
      충청북도: false,
      충청남도: false,
      전라북도: true,
      전라남도: false,
      경상북도: true,
      경상남도: false,
      제주특별자치도: true,
    };
    setRegionWeather(exampleWeatherData);
  }, []);

  // 지역명 보정
  const regionMapping = {
    충북: "충청북도",
    충남: "충청남도",
    전북: "전라북도",
    전남: "전라남도",
    경북: "경상북도",
    경남: "경상남도",
    강원: "강원특별자치도",
  };

  // 기본 스타일 - 비 오는지 여부에 따라 색상 달라짐
  const getRegionStyle = (feature) => {
    const regionName = feature.properties?.CTP_KOR_NM;
    const isRaining = regionWeather[regionName];

    if (selectedRegion === regionName) {
      return {
        weight: 2,
        color: "#ffffff",
        fillColor: "#ffffff",
        fillOpacity: 0.4,
      };
    }

    if (isRaining === true) {
      // 비 오는 지역 - 파란색
      return {
        color: "#204172ff", // 테두리 색상
        weight: 2,
        fillColor: "#a6d9f7",
        fillOpacity: 0.6,
      };
    } else if (isRaining === false) {
      // 비 안 오는 지역 - 회색
      return {
        color: "#999999",
        weight: 2,
        fillColor: "#e0e0e0",
        fillOpacity: 0.4,
      };
    } else {
      // 정보 없는 지역 기본 스타일
      return {
        color: "#204172ff",
        weight: 2,
        fillColor: "#cccccc",
        fillOpacity: 0.3,
      };
    }
  };

  // 마커 아이콘
  const flagIcon = new L.Icon({
    iconUrl: process.env.PUBLIC_URL + "/red.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28],
  });

  // 초기화 버튼
  const handleReset = () => {
    if (mapInstance) {
      mapInstance.setView([36.5, 127.5], 7);
      setSelectedRegion(null);
      setFilteredLocations([]);
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

        {/* 골프장 마커 */}
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

        {/* GeoJSON */}
        {geoData && (
          <GeoJSON
            data={geoData}
            style={getRegionStyle}
            onEachFeature={(feature, layer) => {
              layer.on({
                mouseover: (e) => {
                  if (selectedRegion !== feature.properties?.CTP_KOR_NM) {
                    e.target.setStyle({
                      weight: 2,
                      color: "#ffffff",
                      fillColor: "#ffffff",
                      fillOpacity: 0.4,
                    });
                  }
                },
                mouseout: (e) => {
                  if (selectedRegion !== feature.properties?.CTP_KOR_NM) {
                    e.target.setStyle(getRegionStyle(feature));
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

      {/* 초기화 버튼 */}
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
