// src/components/RecommendMsg.jsx
function RecommendMsg({ weather }) {
  const now = weather[0];

  return (
    <section className="detail-section">
      <h3>추천 메시지(!!! 구현 예정 !!!)</h3>
      <div className="detail-recommend">
        {/* 지금은 간단한 예시 → 나중에 AI/규칙 기반으로 교체 */}
        오늘은 바람이 {now.VEC}° 방향에서 약 {now.WSD}m/s 속도로 불고 있어
        주의가 필요합니다.
      </div>
    </section>
  );
}

export default RecommendMsg;
