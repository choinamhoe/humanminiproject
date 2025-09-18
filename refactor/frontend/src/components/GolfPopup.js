import { Popup } from "react-leaflet";

const GolfPopup = ({ item, onClickDetail }) => {
  const infoItems = [
    {
      label: "⏲️",
      text:
        Number(item.PR).toFixed(1) < 800
          ? "데이터 없음"
          : `${Number(item.PR).toFixed(1)} hPa`,
    },
    { label: "☔", text: `${Number(item.RN).toFixed(1)} mm` },
    { label: "🌡️", text: `${Number(item.TA).toFixed(1)} ℃` },
    { label: "🧭", text: `${Number(item.WD).toFixed(1)}°` },
    { label: "💨", text: `${Number(item.WS).toFixed(1)} m/s` },
  ];

  return (
    <Popup>
      <div className="popup-card">
        <h3 style={{ marginBottom: "8px" }}>{item.storeName}</h3>
        <p style={{ margin: 0, fontSize: "14px", color: "#555" }}>
          {item.address}
        </p>

        <div style={{ marginTop: "10px", fontSize: "14px", lineHeight: 1.6 }}>
          {infoItems.map((info, idx) => (
            <p key={idx}>
              <span className="popup-label">{info.label}</span>
              {info.text}
            </p>
          ))}
        </div>

        <p
          style={{
            marginTop: "12px",
            color: "#007bff",
            cursor: "pointer",
            textDecoration: "underline",
            fontWeight: "bold",
            fontSize: "14px",
          }}
          onClick={onClickDetail}
        >
          👉 실시간 골프장 정보 열기
        </p>
      </div>
    </Popup>
  );
};

export default GolfPopup;
