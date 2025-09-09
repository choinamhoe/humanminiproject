import { useState, useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// --- TodayPopup 컴포넌트 ---
function TodayPopup({ recommendedRegions }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    const today = new Date().toISOString().slice(0, 10);
    const closedDate = localStorage.getItem("popupClosedDate");
    if (closedDate !== today) setShow(true);
  }, []);

  if (!show) return null;

  return (
    <div
      style={{
        position: "fixed",
        top: "20%",
        left: "50%",
        transform: "translateX(-50%)",
        width: "280px",
        backgroundColor: "white",
        padding: "10px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
        borderRadius: "18px",
        textAlign: "center",
        zIndex: 2000,
      }}
    >
      <h3 style={{ margin: "1px 0" }}>오늘의 추천 골프장</h3>

      <ul
        style={{
          paddingLeft: "20px",
          textAlign: "left",
          maxHeight: "120px",
          overflowY: "auto",
          margin: 0, // ul 기본 margin 제거
          padding: 0, // ul 기본 padding 제거
        }}
      >
        {recommendedRegions.map((r) => (
          <li key={r.name} style={{ fontSize: "13px", lineHeight: "1.8em" }}>
            {r.name}
          </li>
        ))}
      </ul>
      <div style={{ marginTop: "10px" }}>
        <button
          onClick={() => setShow(false)}
          style={{ marginRight: "19px", padding: "5px 10px" }}
        >
          닫기
        </button>
        <button
          onClick={() => {
            const today = new Date().toISOString().slice(0, 10);
            localStorage.setItem("popupClosedDate", today);
            setShow(false);
          }}
          style={{ padding: "5px 10px" }}
        >
          오늘 하루 열지 않기
        </button>
      </div>
    </div>
  );
}

// --- 메인 App ---
export default function App() {
  const regions = [
    {
      name: "서울특별시",
      lat: 37.5665,
      lng: 126.978,
      weather: { temp: 28, rain: 0, wind: 3 },
    },
    {
      name: "경기도",
      lat: 37.4138,
      lng: 127.5183,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
    {
      name: "부산광역시",
      lat: 35.1796,
      lng: 129.0756,
      weather: { temp: 29, rain: 0, wind: 4 },
    },
    {
      name: "강원특별자치도",
      lat: 37.8228,
      lng: 128.1555,
      weather: { temp: 26, rain: 0, wind: 3 },
    },
    {
      name: "경상남도",
      lat: 35.4606,
      lng: 128.2132,
      weather: { temp: 28, rain: 0.2, wind: 3 },
    },
    {
      name: "경상북도",
      lat: 36.4919,
      lng: 128.8889,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
    {
      name: "광주광역시",
      lat: 35.1595,
      lng: 126.8526,
      weather: { temp: 29, rain: 0, wind: 3 },
    },
    {
      name: "대구광역시",
      lat: 35.8714,
      lng: 128.6014,
      weather: { temp: 28, rain: 0, wind: 4 },
    },
    {
      name: "대전광역시",
      lat: 36.3504,
      lng: 127.3845,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
    {
      name: "세종특별자치시",
      lat: 36.48,
      lng: 127.289,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
    {
      name: "울산광역시",
      lat: 35.5384,
      lng: 129.3114,
      weather: { temp: 28, rain: 0, wind: 3 },
    },
    {
      name: "인천광역시",
      lat: 37.4563,
      lng: 126.7052,
      weather: { temp: 27, rain: 0, wind: 3 },
    },
    {
      name: "전라남도",
      lat: 34.8161,
      lng: 126.4912,
      weather: { temp: 29, rain: 0, wind: 2 },
    },
    {
      name: "전북특별자치도",
      lat: 35.7175,
      lng: 127.153,
      weather: { temp: 28, rain: 0.1, wind: 2 },
    },
    {
      name: "제주특별자치도",
      lat: 33.4996,
      lng: 126.5312,
      weather: { temp: 30, rain: 0, wind: 3 },
    },
    {
      name: "충청남도",
      lat: 36.5184,
      lng: 126.8002,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
    {
      name: "충청북도",
      lat: 36.6285,
      lng: 127.9299,
      weather: { temp: 27, rain: 0, wind: 2 },
    },
  ];

  const recommendedRegions = regions.filter((r) => r.weather.rain === 0);

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      {/* 오늘 하루 열지 않기 팝업 */}
      <TodayPopup recommendedRegions={recommendedRegions} />

      {/* 지도 */}
      <MapContainer
        center={[36.5, 127.8]}
        zoom={7}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"
          attribution="&copy; OpenStreetMap &copy; CARTO"
        />
        {regions.map((region) => (
          <CircleMarker
            key={region.name}
            center={[region.lat, region.lng]}
            radius={20} // hover 영역 충분히 확보
            color="transparent"
            fillOpacity={0.01} // 거의 투명하지만 hover 감지 가능
          >
            <Tooltip direction="top" offset={[0, -10]}>
              <div style={{ textAlign: "center" }}>
                <strong>{region.name}</strong>
                <br />
                🌡 {region.weather.temp}°C &nbsp; ☔ {region.weather.rain}mm
                &nbsp; 💨 {region.weather.wind}m/s
              </div>
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
