// src/pages/DetailPages.jsx
import { useNavigate } from "react-router-dom";

function DetailPages() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <button
        onClick={() => navigate("/map")}
        style={{
          float: "right",
          background: "transparent",
          border: "none",
          fontSize: "14px",
          cursor: "pointer",
        }}
      >
        닫기 ✕
      </button>

      <h2 style={{ marginTop: 0 }}>골프장 이름(DB) 상황</h2>

      {/* 🔽 DB/날씨 데이터 자리 */}
      <section style={{ marginTop: "20px" }}>
        <h3>기본 정보</h3>
        <p>• 골프장 이름: (DB)</p>
        <p>• 주소: (DB)</p>
        <p>• 연락처: (DB)</p>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>현재 날씨</h3>
        <p>🌡 기온: (API)</p>
        <p>💧 습도: (API)</p>
        <p>☔ 강수량: (API)</p>
        <p>💨 풍속: (API)</p>
        <p>🧭 풍향: (API → WD 값)</p>
        <p>🌫 시정: (API)</p>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>예보 그래프</h3>
        <p>앞으로 6시간 강수량/풍속/풍향/시정 그래프</p>
      </section>

      <section style={{ marginTop: "20px" }}>
        <h3>추천 메시지</h3>
        <div
          style={{
            background: "#f9f9f9",
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "12px",
            fontStyle: "italic",
          }}
        >
          오늘은 바람이 북서풍(약 8m/s)으로 강하게 불고 있어 주의가 필요합니다.
        </div>
      </section>
    </div>
  );
}

export default DetailPages;
