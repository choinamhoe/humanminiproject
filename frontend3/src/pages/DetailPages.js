import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import WeatherNow from "../components/WeatherNow";
import WeatherChart from "../components/WeatherChart";
import RecommendMsg from "../components/RecommendMsg";
import "./DetailPages.css";

function DetailPages() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [golfInfo, setGolfInfo] = useState(null);
  const [weather, setWeather] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetch("http://192.168.0.38:8000/detail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id }),
    })
      .then((res) => res.json())
      .then((data) => {
        setGolfInfo(data.golfDetail.golfInfo[0]);
        setWeather(data.golfDetail.golfCurrentWeather);
      })
      .catch((err) => console.error("❌ 상세 API 오류:", err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="detail-container">로딩 중...</p>;

  return (
    <div
      className="detail-container"
      style={{
        backgroundImage: "url('/flagbackground.png')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      {/* 닫기 버튼 */}
      <button onClick={() => navigate("/map")} className="detail-close-btn">
        ✕
      </button>

      <h2 className="detail-title">
        {golfInfo ? golfInfo.storeName : `골프장 ${id}`} 상황
      </h2>

      {/* 기본 정보 */}
      {golfInfo && (
        <section className="detail-section">
          <h3>기본 정보</h3>
          <p className="detail-item">• 골프장: {golfInfo.storeName}</p>
          <p className="detail-item">• 주소: {golfInfo.addr}</p>
          <p className="detail-item">• 지역: {golfInfo.area}</p>
          <p className="detail-item">• 구분: {golfInfo.detailedType}</p>
          <p className="detail-item">• 위도: {golfInfo.Latitude}</p>
          <p className="detail-item">• 경도: {golfInfo.Longitude}</p>
        </section>
      )}

      {/* 현재 날씨 */}
      {weather.length > 0 && <WeatherNow weather={weather} />}

      {/* 예보 그래프 */}
      {weather.length > 0 && <WeatherChart weather={weather} />}

      {/* 추천 메시지 */}
      {weather.length > 0 && <RecommendMsg weather={weather} />}
    </div>
  );
}

export default DetailPages;
