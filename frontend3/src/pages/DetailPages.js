// src/pages/DetailPages.js
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import WeatherNow from "../components/WeatherNow";
import WeatherChart from "../components/WeatherChart";
// import RecommendMsg from "../components/RecommendMsg";
import PlayAbility from "../components/PlayAbility";
import "./DetailPages.css";

function DetailPages() {
  const navigate = useNavigate();
  const { id } = useParams();

  const [golfInfo, setGolfInfo] = useState(null);
  const [weather, setWeather] = useState([]); // 항상 배열
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
        setGolfInfo(data?.golfDetail?.golfInfo?.[0] || null);

        // ✅ 날씨 데이터 매핑
        const mappedWeather = (data?.golfDetail?.golf24HourWeather || []).map(
          (w) => ({
            datetime: w.time,
            T1H: w.temperature, // 기온
            humidity: w.humidity,
            WSD: w.wind_speed, // 풍속
            RN1: w.precipitation, // 강수량
            rainProb: w.precip_prob, // 강수확률
            fog: w.fog_index,
            visibility: w.visibility,

            final_playable: w.final_playable,
            playableRule: w.playable_rule,
            playableProbML: w.playable_prob_ml,
            playableML: w.playable_ml,
            playableProbDL: w.playable_prob_dl,
            playableDL: w.playable_dl,

            summary: w.summary,
          })
        );

        setWeather(mappedWeather);
      })
      .catch((err) => {
        console.error("❌ 상세 API 오류:", err);
        setWeather([]);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="detail-container">로딩 중...</p>;

  return (
    <div className="detail-container">
      {/* 닫기 버튼 */}
      <button onClick={() => navigate("/map")} className="detail-close-btn">
        닫기 ✕
      </button>

      <h2 className="detail-title">
        {golfInfo ? golfInfo.storeName : `골프장 ${id}`} 상황
      </h2>

      {/* 기본 정보 */}
      {golfInfo && (
        <section className="detail-section">
          <h3>골프장 정보</h3>
          <p className="detail-item">• 골프장: {golfInfo.storeName}</p>
          <p className="detail-item">• 주소: {golfInfo.addr}</p>
          <p className="detail-item">• 구분: {golfInfo.detailedType}</p>

          {/* ✅ 총 홀 수 */}
          <p className="detail-item">
            • 총 홀 수: {18 + (golfInfo.addHole || 0)}홀
          </p>

          {/* ✅ 부지 면적 (있을 경우만) */}
          {golfInfo.totalAreaSquareMeters && (
            <p className="detail-item">
              • 부지 면적:{" "}
              {Math.round(golfInfo.totalAreaSquareMeters).toLocaleString()}㎡
            </p>
          )}
        </section>
      )}

      {/* 현재 날씨 */}
      {Array.isArray(weather) && weather.length > 0 && (
        <WeatherNow weather={weather} />
      )}

      {/* 플레이 가능 여부 */}
      {Array.isArray(weather) && weather.length > 0 && (
        <PlayAbility weather={weather} />
      )}

      {/* 예보 그래프 */}
      {Array.isArray(weather) && weather.length > 0 && (
        <section className="detail-weather-graph">
          <WeatherChart weather={weather} />
        </section>
      )}

      {/* 추천 메시지 */}
      {/* {Array.isArray(weather) && weather.length > 0 && (
        <RecommendMsg weather={weather} />
      )} */}
    </div>
  );
}

export default DetailPages;
