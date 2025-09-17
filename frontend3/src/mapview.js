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
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [hoveredItem, setHoveredItem] = useState(null); // 🔹 Hover 상태
  const mapRef = useRef();
  const [draggedItem, setDraggedItem] = useState(null);
  const navigate = useNavigate();
  // ✅ 추가: 선택된 골프장
  const [selectedGolf, setSelectedGolf] = useState(null);
  const searchBoxRef = useRef(null);

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
  //외부 클릭 감지 useEffect 추가
  useEffect(() => {
    function handleClickOutside(event) {
      if (
        searchBoxRef.current &&
        !searchBoxRef.current.contains(event.target)
      ) {
        // 박스 밖을 클릭하면 자동완성 닫기
        setSearchResults([]);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // ✅ 전국 데이터 불러오기
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.post("http://192.168.0.38:8000");
        console.log("res", res);
        if (res?.data?.golfList?.golfInfo) {
          const data = res.data.golfList.golfInfo;
          const parsed = data
            .map((item) => ({
              id: item.id,
              name: item.storeName,
              latitude: parseFloat(item.Latitude),
              longitude: parseFloat(item.Longitude),
              address: item.addr,
              area: item.area,
              imageUrl: item.imageUrl,
              PR: item.PR,
              RN: item.RN,
              TA: item.TA,
              WD: item.WD,
              WS: item.WS,
            }))
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

  // ✅ 깃발 아이콘
  const getFlagIcon = () =>
    new L.Icon({
      iconUrl: process.env.PUBLIC_URL + "/red.png",
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
    });

  // ✅ hover 전용 아이콘
  const getHoverIcon = () =>
    new L.Icon({
      iconUrl: process.env.PUBLIC_URL + "/red.png",
      iconSize: [35, 35],
      iconAnchor: [17, 35],
    });
  // ✅ 선택된 노란 깃발 아이콘
  const yellowFlagIcon = new L.Icon({
    iconUrl: process.env.PUBLIC_URL + "/yellow.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28],
  });

  const handleReset = () => {
    if (mapInstance) {
      mapInstance.setView([36.5, 127.5], 7); // 지도 초기 위치
      setSelectedRegion(null); // 지역 선택 해제
      setFilteredLocations([]); // 마커 제거
      setSelectedGolf(null); // state 초기화
      navigate("/map"); // ✅ 라우팅도 초기화
    }
  };

  const RainIcon = () =>
    new L.Icon({
      iconUrl: process.env.PUBLIC_URL + "/rain.png",
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
    });

  const WindIcon = () =>
    new L.Icon({
      iconUrl: process.env.PUBLIC_URL + "/wind.png",
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
    });

  const RainWindIcon = () =>
    new L.Icon({
      iconUrl: process.env.PUBLIC_URL + "/rain_wind.png",
      iconSize: [30, 30],
      iconAnchor: [15, 30],
      popupAnchor: [0, -28],
    });

  // ✅ 지역명 보정
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

  // ✅ 검색 처리 (검색 API 사용)
  const handleSearch = async (term) => {
    setSearchTerm(term);

    if (term.length > 0) {
      try {
        const res = await axios.post("http://192.168.0.38:8000/search", {
          search: term,
        });

        if (res?.data?.golfList?.golfInfo) {
          const data = res.data.golfList.golfInfo;
          const parsed = data.map((item) => ({
            id: item.id,
            name: item.storeName,
            latitude: parseFloat(item.Latitude),
            longitude: parseFloat(item.Longitude),
            address: item.addr,
            area: item.area,
            imageUrl: item.imageUrl,
          }));
          setSearchResults([{ type: "골프장", items: parsed }]);
        } else {
          setSearchResults([]);
        }
      } catch (err) {
        console.error("❌ 검색 API 오류:", err);
        setSearchResults([]);
      }
    } else {
      setSearchResults([]);
    }
  };

  // ✅ 검색 결과 클릭
  const handleResultClick = (item, type) => {
    if (type === "골프장") {
      setFilteredLocations([item]);
      if (mapRef.current) {
        mapRef.current.setView([item.latitude, item.longitude], 12);
      }
      navigate(`/detail/${item.id}`);
    } else {
      const parsed = areaIds.filter(
        (loc) =>
          loc.area.includes(searchTerm) || loc.address.includes(searchTerm)
      );
      setFilteredLocations(parsed);

      if (mapRef.current && parsed.length > 0) {
        const bounds = parsed.map((loc) => [loc.latitude, loc.longitude]);
        mapRef.current.fitBounds(bounds);
      }
    }

    setSearchResults([]);
    setSearchTerm("");
  };

  // ✅ 검색어 하이라이트
  const highlightMatch = (text, term) => {
    const parts = text.split(new RegExp(`(${term})`, "gi"));
    return parts.map((part, i) =>
      part.toLowerCase() === term.toLowerCase() ? (
        <strong key={i} style={{ color: "#007bff" }}>
          {part}
        </strong>
      ) : (
        part
      )
    );
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
      <div className="map-header" style={{ textAlign: "center" }}>
        <h2>📍 대한민국 골프장 지도</h2>
        <p>지역을 클릭하면 해당 지역의 골프장이 표시됩니다.</p>

        {/* ✅ 검색창 */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "5px",
          }}
        >
          <div
            style={{ position: "relative", width: "350px" }}
            ref={searchBoxRef}
          >
            <input
              type="text"
              placeholder="지역명 또는 골프장명 검색"
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch(searchTerm)} // 엔터키 검색
              style={{
                width: "85%",
                padding: "8px 35px 8px 12px",
                borderRadius: "20px",
                border: "1px solid #ccc",
                boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
                fontSize: "14px",
              }}
            />
            <span
              style={{
                position: "absolute",
                right: "12px",
                top: "50%",
                transform: "translateY(-50%)",
                color: "#888",
                cursor: "pointer",
              }}
              onClick={() => handleSearch(searchTerm)} // 돋보기 클릭 시 검색 실행
            >
              🔍
            </span>

            {/* 자동완성 리스트 */}
            {searchResults.some((group) => group.items.length > 0) && (
              <ul
                style={{
                  listStyle: "none",
                  margin: 0,
                  padding: "5px",
                  background: "white",
                  border: "1px solid #ccc",
                  borderTop: "none",
                  width: "100%",
                  maxHeight: "200px",
                  overflowY: "auto",
                  position: "absolute",
                  zIndex: 1000,
                }}
              >
                {searchResults.map(
                  (group) =>
                    group.items.length > 0 && (
                      <li key={group.type}>
                        <div style={{ fontWeight: "bold", margin: "4px 0" }}>
                          {group.type}
                        </div>
                        {group.items.map((item) => (
                          <div
                            key={item.id}
                            style={{
                              padding: "6px",
                              cursor: "pointer",
                              backgroundColor:
                                hoveredItem?.id === item.id
                                  ? "#e6f2ff"
                                  : "transparent",
                            }}
                            onMouseEnter={() => setHoveredItem(item)}
                            onMouseLeave={() => setHoveredItem(null)}
                            onClick={() => handleResultClick(item, group.type)}
                          >
                            {highlightMatch(item.name, searchTerm)} ({item.area}
                            )
                          </div>
                        ))}
                      </li>
                    )
                )}
              </ul>
            )}
          </div>
        </div>
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

        {filteredLocations.map((loc, idx) => (
          <Marker
            key={idx}
            position={[loc.latitude, loc.longitude]}
            icon={
              Number(loc.RN) >= 1 && Number(loc.WS) >= 10
                ? RainWindIcon()
                : Number(loc.RN) >= 1
                ? RainIcon()
                : Number(loc.WS) >= 10
                ? WindIcon()
                : selectedGolf?.id === loc.id
                ? yellowFlagIcon
                : getFlagIcon()
            }
            eventHandlers={{
              click: () => setSelectedGolf(loc), // ✅ 클릭 시 노란색으로 변경
            }}
          >
            <Popup>
              <div
                className="popup-card"
                style={{ padding: "12px", maxWidth: "220px" }}
              >
                <h3 style={{ marginBottom: "8px" }}>{loc.name}</h3>
                <p style={{ margin: 0, fontSize: "14px", color: "#555" }}>
                  {loc.address}
                </p>

                <div
                  style={{
                    marginTop: "10px",
                    fontSize: "14px",
                    lineHeight: "1.6",
                  }}
                >
                  <p>
                    <span style={{ display: "inline-block", width: "24px" }}>
                      ⏲️
                    </span>
                    기압: {loc.PR === 0 ? "데이터 없음" : `${loc.PR} hPa`}
                  </p>
                  <p>
                    <span style={{ display: "inline-block", width: "24px" }}>
                      ☔
                    </span>
                    강우량: {loc.RN} mm
                  </p>
                  <p>
                    <span style={{ display: "inline-block", width: "24px" }}>
                      🌡️
                    </span>
                    기온: {loc.TA} ℃
                  </p>
                  <p>
                    <span style={{ display: "inline-block", width: "24px" }}>
                      🧭
                    </span>
                    풍향: {Number(loc.WD).toFixed(1)}°
                  </p>
                  <p>
                    <span style={{ display: "inline-block", width: "24px" }}>
                      💨
                    </span>
                    풍속: {loc.WS} m/s
                  </p>
                </div>

                <p
                  style={{
                    marginTop: "12px",
                    color: "#007bff",
                    cursor: "pointer",
                    textDecoration: "underline",
                    fontWeight: "bold",
                    fontSize: "14px",
                  }}
                  onClick={() => {
                    setSelectedGolf(loc); // 패널 열릴 때도 선택 상태 유지
                    navigate(`/detail/${loc.id}`);
                  }}
                >
                  👉 실시간 골프장 정보 열기
                </p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* ✅ Hover된 검색 결과 강조 마커 */}
        {hoveredItem && (
          <Marker
            position={[hoveredItem.latitude, hoveredItem.longitude]}
            icon={getHoverIcon()}
          />
        )}

        {/* GeoJSON */}
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
              const rawArea = feature.properties?.CTP_KOR_NM;

              // 마우스 오버 이벤트
              layer.on("mouseover", () => {
                layer.setStyle({
                  weight: 3,
                  color: "#f7f3f3ff",
                  fillColor: "#f5f5f5ff",
                  fillOpacity: 0.6,
                });

                // ✅ 특정 지역만 좌표 강제 지정
                let tooltipPosition;
                if (rawArea === "경상북도") {
                  tooltipPosition = L.latLng(36.5, 128.7); // 경북 → 경도 줄여서 왼쪽 이동
                } else if (rawArea === "충청북도") {
                  tooltipPosition = L.latLng(36.8, 127.6); // 충북 → 경도 줄여서 왼쪽 이동
                } else {
                  tooltipPosition = layer.getBounds().getCenter(); // 나머지는 기본값
                }

                // ✅ 기존 툴팁 제거 후 다시 바인딩
                layer.unbindTooltip();
                layer
                  .bindTooltip(rawArea, {
                    permanent: true,
                    direction: "center",
                    className: "region-label",
                  })
                  .openTooltip(tooltipPosition);
              });

              // 마우스 아웃 이벤트
              layer.on("mouseout", () => {
                layer.setStyle({
                  color: "#204172ff",
                  weight: 2,
                  fillColor: "#204172ff",
                  fillOpacity: 0.2,
                });
                layer.closeTooltip();
              });

              // 클릭 이벤트
              layer.on("click", async () => {
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
              });
            }}
          />
        )}
      </MapContainer>

      {/* 초기화 버튼 */}
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
