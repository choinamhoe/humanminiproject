// src/components/WeatherNow.jsx
function WeatherNow({ weather }) {
  const now = weather[0]; // 가장 최신 데이터

  return (
    <section className="detail-section weather-now">
      <h3>현재 날씨</h3>
      <div className="weather-grid">
        <div>🌡 기온: {now.T1H} ℃</div>
        <div>💧 습도: {now.humidity} %</div>
        <div>☔ 강수량: {now.RN1} mm</div>
        <div>💨 풍속: {now.WSD} m/s</div>
        <div>🌫 안개지수: {now.fog}</div>
        <div>👁 시정: {(now.visibility / 1000).toFixed(1)} km</div>
      </div>
    </section>
  );
}

export default WeatherNow;
