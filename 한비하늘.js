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
  const [mapInstance, setMapInstance] = useState(null); // ✅ 지도 인스턴스 상태
  const mapRef = useRef();

  // ✅ GeoJSON 불러오기
  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/ctprvn.geojson")
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => console.error("GeoJSON 오류:", err));
  }, []);

  // 기본 스타일
  const geoJsonStyle = {
    color: "#204172ff",
    weight: 2,
    fillColor: "#204172ff",
    fillOpacity: 0.2,
  };

  // 드래그 시 스타일
  const highlightStyle = {
    weight: 2,
    color: "#ffffff",
    fillColor: "#ffffff",
    fillOpacity: 0.4,
  };

  // 마커 아이콘 (public/red.png 사용)
  const flagIcon = new L.Icon({
    iconUrl: process.env.PUBLIC_URL + "/red.png",
    iconSize: [35, 35],
    iconAnchor: [17, 35],
    popupAnchor: [0, -30],
  });

  // ✅ 첫화면 버튼 클릭 시 초기화
  const handleReset = () => {
    console.log("첫화면 버튼 클릭됨!");
    if (mapInstance) {
      mapInstance.setView([36.5, 127.5], 7); // 대한민국 중심으로 이동
    } else {
      console.log("mapInstance 아직 null임");
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
          setMapInstance(ref); // ✅ 지도 인스턴스 등록
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* 클릭된 지역 내 마커 */}
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

        {/* GeoJSON 경계 */}
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
                      "http://192.168.0.41:8000/",
                      {}
                    );

                    const golfInfo = res.data.golfList?.golfInfo || [];
                    const parsed = golfInfo
                      .map((item) => ({
                        name: item.storeName,
                        latitude: parseFloat(item.Latitude),
                        longitude: parseFloat(item.Longitude),
                        address: item.addr,
                        area: item.area,
                      }))
                      .filter(
                        (loc) =>
                          !isNaN(loc.latitude) &&
                          !isNaN(loc.longitude) &&
                          (loc.area.includes(areaName) ||
                            areaName.includes(loc.area)) // 부분일치 허용
                      );

                    setFilteredLocations(parsed);
                    console.log("로드된 골프장:", parsed.length);

                    if (mapRef.current) {
                      mapRef.current.fitBounds(layer.getBounds());
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

      {/* 🔘 첫화면 버튼 (bottom: 490, left: 11 적용) */}
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
