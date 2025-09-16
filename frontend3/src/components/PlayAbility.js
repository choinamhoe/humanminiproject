function PlayAbility({ weather }) {
  const now = weather[0];
  const playableText =
    now.final_playable === 1 ? "✔️ 플레이 가능" : "❌ 플레이 불가";

  let cleanSummary = "";
  if (now.summary) {
    // 날짜 뽑기
    const dateMatch = now.summary.match(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/);
    const dateText = dateMatch ? dateMatch[0] : "";

    // ML 값
    const mlMatch = now.summary.match(/ML:[0-9.]+/);
    const mlValue = mlMatch ? mlMatch[0] : "";

    // DL 값 (NaN이면 출력 안 함)
    let dlValue = "";
    if (now.playableDL !== null && !isNaN(now.playableDL)) {
      dlValue = `, DL:${now.playableDL.toFixed(2)}`;
    }

    // 👉 이후 설명 부분
    const tipMatch = now.summary.match(/👉.+/s);
    const tipText = tipMatch ? tipMatch[0] : "";

    cleanSummary = `${dateText}<br/>모델 판정: ${mlValue}${dlValue}<br/>${tipText}`;
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
