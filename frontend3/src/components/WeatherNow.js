// src/components/WeatherNow.jsx
function WeatherNow({ weather }) {
  const now = weather[0]; // 가장 최신 데이터

  return (
    <section className="detail-section">
      <h3>현재 날씨</h3>
      <p>🌡 기온: {now.T1H} ℃</p>
      <p>☔ 강수량: {now.RN1 === "강수없음" ? 0 : now.RN1} mm</p>
      <p>💨 풍속: {now.WSD} m/s</p>
      <p>
        🧭 풍향: {now.VEC} °
        <br />
        <span style={{ marginLeft: "20px", color: "#555" }}>
          ↳ 동서풍: {now.UUU} m/s
        </span>
        <br />
        <span style={{ marginLeft: "20px", color: "#555" }}>
          ↳ 남북풍: {now.VVV} m/s
        </span>
      </p>
    </section>
  );
}

export default WeatherNow;
