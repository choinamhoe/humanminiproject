import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from "react-leaflet";
import { useNavigate } from "react-router-dom";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./mapview.css";

const MapView = () => {
  const [geoData, setGeoData] = useState(null);
  const [filteredLocations, setFilteredLocations] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);
  const [areaIds, setAreaIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const mapRef = useRef();

  const navigate = useNavigate();

  // ✅ GeoJSON 불러오기
  useEffect(() => {
    fetch(process.env.PUBLIC_URL + "/ctprvn.geojson")
      .then((res) => res.json())
      .then((data) => setGeoData(data))
      .catch((err) => {
        console.error("GeoJSON 오류:", err);
        setError("지역 경계 데이터를 불러오지 못했습니다.");
      });
  }, []);

  // 🔴 마커 아이콘
  const flagIcon = new L.Icon({
    iconUrl: process.env.PUBLIC_URL + "/red.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28],
  });

  // ✅ 초기화 버튼
  const handleReset = () => {
    if (mapInstance) {
      mapInstance.setView([36.5, 127.5], 7);
      setSelectedRegion(null);
      setFilteredLocations([]);
    }
  };

  // ✅ 지역명 보정 함수
  const normalizeArea = (name) => {
    if (!name) return "";
    return name
      .replace("세종특별자치시", "세종")
      .replace("특별자치도", "")
      .replace("광역시", "")
      .replace("특별시", "")
      .replace("자치시", "")
      .replace("충청북", "충북")
      .replace("충청남", "충남")
      .replace("전라북", "전북")
      .replace("전라남", "전남")
      .replace("경상북", "경북")
      .replace("경상남", "경남")
      .replace("도", "")
      .replace("시", "")
      .trim();
  };

  // ✅ 전체 데이터 불러오기
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.post("http://192.168.0.38:8000");
        if (res?.data?.golfList?.golfInfo) {
          const data = res.data.golfList.golfInfo;
          const parsed = data
            .map((item) => {
              const lat = parseFloat(item.Latitude);
              const lng = parseFloat(item.Longitude);

              return {
                id: item.id,
                name: item.storeName,
                latitude: lat,
                longitude: lng,
                address: item.addr,
                area: item.area,
                imageUrl: item.imageUrl,
              };
            })
            .filter((loc) => !isNaN(loc.latitude) && !isNaN(loc.longitude));

          setAreaIds(parsed);
        } else {
          setError("골프장 데이터를 불러오지 못했습니다.");
        }
      } catch (e) {
        console.error("❌ 데이터 불러오기 오류:", e);
        setError("서버에서 데이터를 불러올 수 없습니다.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // ✅ 로딩/에러 처리
  if (loading) {
    return (
      <div className="loading-overlay">
        <img
          src={process.env.PUBLIC_URL + "/golfball.png"}
          alt="loading"
          className="golfball-spinner"
        />
      </div>
    );
  }

  if (error) {
    return <div style={{ padding: "20px", color: "red" }}>{error}</div>;
  }

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

        {/* 🔴 현재 선택된 지역 마커 */}
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

                <img
                  src={loc.imageUrl || process.env.PUBLIC_URL + "/샘플.jpg"}
                  alt={loc.name}
                  style={{
                    width: "100%",
                    marginTop: "8px",
                    cursor: "pointer",
                  }}
                  onClick={() => navigate(`/detail/${loc.id}`)}
                />
              </div>
            </Popup>
          </Marker>
        ))}

        {/* ✅ 데이터 준비된 후에만 GeoJSON 표시 */}
        {geoData && areaIds.length > 0 && (
          <GeoJSON
            data={geoData}
            style={(feature) =>
              selectedRegion === feature.properties?.CTP_KOR_NM
                ? {
                    weight: 2,
                    color: "#ffffff",
                    fillColor: "#ffffff",
                    fillOpacity: 0.4,
                  }
                : {
                    color: "#204172ff",
                    weight: 2,
                    fillColor: "#204172ff",
                    fillOpacity: 0.2,
                  }
            }
            onEachFeature={(feature, layer) => {
              layer.on({
                click: async () => {
                  const rawArea = feature.properties?.CTP_KOR_NM;
                  setSelectedRegion(rawArea);

                  try {
                    const parsed = areaIds.filter(
                      (item) =>
                        item.area &&
                        normalizeArea(item.area) === normalizeArea(rawArea)
                    );

                    setFilteredLocations(parsed);

                    if (mapRef.current && parsed.length > 0) {
                      const bounds = parsed.map((loc) => [
                        loc.latitude,
                        loc.longitude,
                      ]);
                      mapRef.current.fitBounds(bounds);
                    }

                    layer.bindPopup(`<b>${rawArea}</b>`).openPopup();
                  } catch (err) {
                    console.error("❌ 지역별 필터링 오류:", err);
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
          bottom: 780,
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
