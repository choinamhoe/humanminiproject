function PlayAbility({ weather }) {
  const now = weather[0];
  const playableText = now.playable === 1 ? "✔️ 플레이 가능" : "❌ 플레이 불가";

  let cleanSummary = "";
  if (now.summary) {
    // ✅ 날짜 + 모델 판정 + 요약만 남기기
    // 원문 예: "2025-09-15 16:00:00 — 기온 29.0°C, 습도 ... → 골프장: 가능 (ML:1.00) 👉 요약..."
    // 1) 날짜 뽑기
    const dateMatch = now.summary.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/);
    const dateText = dateMatch ? dateMatch[0] : "";

    // 2) ML 값 뽑기
    const mlMatch = now.summary.match(/ML:[0-9.]+/);
    const mlValue = mlMatch ? mlMatch[0] : "";

    // 3) 👉 이후 설명 부분만 남기기
    const tipMatch = now.summary.match(/👉.+/s);
    const tipText = tipMatch ? tipMatch[0] : "";

    cleanSummary = `${dateText} — 모델 판정: ${mlValue}<br/>${tipText}`;
  }

  return (
    <section className="detail-section">
      <h3>플레이 가능 여부</h3>
      <p className="detail-playable">{playableText}</p>
      {cleanSummary && (
        <div
          className="detail-recommend"
          dangerouslySetInnerHTML={{ __html: cleanSummary }}
        />
      )}
    </section>
  );
}

export default PlayAbility;
