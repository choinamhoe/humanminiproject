// src/components/WeatherChart.jsx
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function WeatherChart({ weather }) {
  const chartData = weather.map((w) => ({
    time: w.datetime.slice(11, 16), // HH:mm
    rain: w.RN1 === "강수없음" ? 0 : Number(w.RN1), // 강수량
    wind: Number(w.WSD), // 풍속
    temp: Number(w.T1H), // 기온
    fog: Number(w.fog), // 안개지수
  }));

  return (
    <section className="detail-section">
      <h3>날씨 예보 그래프</h3>
      <p>⏱ 24시간 동안의 강수량, 풍속, 안개지수, 기온 변화를 확인하세요</p>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          {/* 강수량 */}
          <Line
            type="monotone"
            dataKey="rain"
            stroke="#8884d8"
            name="강수량(mm)"
          />
          {/* 풍속 */}
          <Line
            type="monotone"
            dataKey="wind"
            stroke="#82ca9d"
            name="풍속(m/s)"
          />
          {/* 기온 */}
          <Line
            type="monotone"
            dataKey="temp"
            stroke="#ff7300"
            name="기온(℃)"
          />
          {/* 안개지수 */}
          <Line
            type="monotone"
            dataKey="fog"
            stroke="#555555"
            name="안개지수"
            strokeDasharray="5 5" // 점선으로 구분
          />
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}

export default WeatherChart;
