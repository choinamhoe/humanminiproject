import WeatherNow from "./WeatherNow";
import WeatherChart from "./WeatherChart";
import PlayAbility from "./PlayAbility";
const Sidebar = ({ detailData, setDetailData }) => {
  let golfInfo = detailData.golfInfo;
  if (golfInfo) {
    golfInfo = golfInfo[0];
  }
  const weather = (detailData?.golf24HourWeather || []).map((w) => ({
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
  }));
  console.log(weather);
  return (
    <>
      <div className="detail-container">
        <button
          onClick={() => setDetailData(null)}
          className="detail-close-btn"
        >
          닫기 ✕
        </button>

        <h2 className="detail-title">
          {golfInfo ? golfInfo.storeName : `골프장 ${golfInfo.id}`} 상황
        </h2>

        {golfInfo && (
          <section className="detail-section">
            <h3>골프장 정보</h3>
            <p className="detail-item">• 골프장: {golfInfo.storeName}</p>
            <p className="detail-item">• 주소: {golfInfo.addr}</p>
            <p className="detail-item">• 구분: {golfInfo.detailedType}</p>

            <p className="detail-item">
              • 총 홀 수: {18 + (golfInfo.addHole || 0)}홀
            </p>

            {golfInfo.totalAreaSquareMeters && (
              <p className="detail-item">
                • 부지 면적:{" "}
                {Math.round(golfInfo.totalAreaSquareMeters).toLocaleString()}㎡
              </p>
            )}
          </section>
        )}

        {Array.isArray(weather) && weather.length > 0 && (
          <WeatherNow weather={weather} />
        )}

        {Array.isArray(weather) && weather.length > 0 && (
          <PlayAbility weather={weather} />
        )}

        {Array.isArray(weather) && weather.length > 0 && (
          <section className="detail-weather-graph">
            <WeatherChart weather={weather} />
          </section>
        )}
      </div>
    </>
  );
};

export default Sidebar;
