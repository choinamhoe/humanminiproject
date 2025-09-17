function WeatherNow({ weather }) {
  const now = weather[0]; // 가장 최신 데이터

  // ✅ 강수형태 코드 매핑
  const getPrecipitationText = (type) => {
    switch (Number(type)) {
      case 0:
        return { text: "없음", icon: "➖" };
      case 1:
        return { text: "비", icon: "🌧" };
      case 2:
        return { text: "비/눈", icon: "🌨❄️" };
      case 3:
        return { text: "눈", icon: "❄️" };
      case 4:
        return { text: "소나기", icon: "☔" };
      default:
        return { text: "알 수 없음", icon: "❓" };
    }
  };

  const precip = getPrecipitationText(now.precipitationType ?? 0);

  return (
    <section className="detail-section weather-now">
      <h3>현재 날씨</h3>
      <div className="weather-grid">
        {/* 기온: 소수 첫째자리 */}
        <div>🌡️ 기온: {now.T1H?.toFixed(1)} ℃</div>
        <div>💧 습도: {now.humidity?.toFixed(0)} %</div>

        {/* 강수량: 정수 */}
        <div>☔ 강수량: {Math.round(now.RN1)} mm</div>
        <div>
          ☔ 강수형태: {precip.text} {precip.icon}
        </div>

        {/* 풍속: 정수 */}
        <div>💨 풍속: {Math.round(now.WSD)} m/s</div>

        {/* 안개지수: 정수 */}
        <div>🌫 안개지수: {Math.round(now.fog)}</div>

        {/* 시정: 소수 첫째자리 (km 단위라 자연스러움) */}
        <div>👁 시정: {(now.visibility / 1000).toFixed(1)} km</div>
      </div>
    </section>
  );
}

export default WeatherNow;
