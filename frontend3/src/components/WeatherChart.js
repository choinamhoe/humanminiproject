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
    time: w.datetime.slice(11, 16),
    rain: w.RN1 === "강수없음" ? 0 : Number(w.RN1), // ✅ 변환
    wind: Number(w.WSD),
  }));

  return (
    <section className="detail-section">
      <h3>날씨 예보 그래프</h3>
      <p>
        현재 골프장 기준의 날씨입니다.
        <br />
        (근데 차트가 중요해보이진 않습니다. 다같이 보고서 추후에 결정합시다.)
      </p>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 50, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="rain"
            stroke="#8884d8"
            name="강수량(mm)"
          />
          <Line
            type="monotone"
            dataKey="wind"
            stroke="#82ca9d"
            name="풍속(m/s)"
          />
        </LineChart>
      </ResponsiveContainer>
    </section>
  );
}

export default WeatherChart;
