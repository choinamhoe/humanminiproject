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
  const [weatherMap, setWeatherMap] = useState({});
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

  // ✅ 지역 클릭 시 해당 골프장의 날씨 불러오기
  const fetchWeatherForLocations = async (locations) => {
    const weatherData = {};
    for (const loc of locations) {
      try {
        const res = await axios.post("http://192.168.0.38:8000/detail", {
          id: loc.id,
        });
        const weatherList = res.data?.golfDetail?.golfCurrentWeather || [];
        if (weatherList.length > 0) {
          // 현재 시간과 가장 가까운 데이터 선택
          const now = new Date();
          let closest = weatherList[0];
          let minDiff = Math.abs(new Date(weatherList[0].time) - now);

          for (const w of weatherList) {
            const diff = Math.abs(new Date(w.time) - now);
            if (diff < minDiff) {
              closest = w;
              minDiff = diff;
            }
          }
          weatherData[loc.id] = closest;
        }
      } catch (err) {
        console.error(`❌ 날씨 불러오기 오류 (골프장 ${loc.id}):`, err);
      }
    }
    setWeatherMap(weatherData);
  };

  // ✅ 날씨 점수 계산 (가중치 방식)
  const calculateScore = (weather) => {
    if (!weather) return 0;

    let score = 0;
    // 기온 (20~27도 가장 적합)
    const temp = parseFloat(weather.temperature);
    if (temp >= 20 && temp <= 27) score += 30;
    else if (temp >= 15 && temp <= 30) score += 20;
    else score += 5;

    // 습도 (40~70% 적합)
    const hum = parseFloat(weather.humidity);
    if (hum >= 40 && hum <= 70) score += 25;
    else if (hum >= 30 && hum <= 80) score += 15;
    else score += 5;

    // 풍속 (0~5m/s 적합)
    const wind = parseFloat(weather.wind_speed);
    if (wind <= 5) score += 20;
    else if (wind <= 8) score += 10;
    else score += 3;

    // 강수 확률
    const rain = parseFloat(weather.precip_prob);
    if (rain < 20) score += 25;
    else if (rain < 50) score += 10;
    else score += 0;

    return score; // 총합: 0 ~ 100
  };

  // ✅ 깃발 색상 선택
  const getFlagIcon = (score) => {
    let iconUrl = process.env.PUBLIC_URL + "/red.png";
    if (score >= 70) iconUrl = process.env.PUBLIC_URL + "/green.png";
    else if (score >= 40) iconUrl = process.env.PUBLIC_URL + "/yellow.png";

    return new L.Icon({
      iconUrl,
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
    });
  };

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

        {/* ✅ 선택된 지역의 골프장 마커 */}
        {filteredLocations.map((loc, idx) => {
          const weather = weatherMap[loc.id];
          const score = calculateScore(weather);
          return (
            <Marker
              key={idx}
              position={[loc.latitude, loc.longitude]}
              icon={getFlagIcon(score)}
            >
              <Popup>
                <div className="popup-card">
                  <h3>{loc.name}</h3>
                  <p>{loc.address}</p>
                  {weather && (
                    <>
                      <p>기온: {weather.temperature}°C</p>
                      <p>습도: {weather.humidity}%</p>
                      <p>풍속: {weather.wind_speed}m/s</p>
                      <p>강수확률: {weather.precip_prob}%</p>
                      <p>→ 점수: {score}</p>
                    </>
                  )}
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
          );
        })}

        {/* ✅ GeoJSON */}
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
                    await fetchWeatherForLocations(parsed);

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
