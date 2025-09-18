function WeatherNow({ weather }) {
  const now = weather[0];

  return (
    <section className="detail-section weather-now">
      <h3>현재 날씨</h3>
      <div className="weather-grid">
        <div>🌡 기온: {Number(now.T1H).toFixed(1)} ℃</div>
        <div>💧 습도: {Number(now.humidity).toFixed(1)} %</div>
        <div>☔ 강수량: {Number(now.RN1).toFixed(1)} mm</div>
        <div>💨 풍속: {Number(now.WSD).toFixed(1)} m/s</div>
        <div>🌫 안개지수: {Number(now.fog).toFixed(1)}</div>
        <div>👁 시정: {(now.visibility / 1000).toFixed(1)} km</div>
      </div>
    </section>
  );
}

export default WeatherNow;
