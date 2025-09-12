import { useEffect, useState } from "react";
import axios from "axios";

function RecommendMsg({ weather }) {
  const [chat, setChat] = useState("추천 메시지를 불러오는 중...");

  useEffect(() => {
    if (weather) {
      axios
        .post("http://localhost:8000/recommend", { weather })
        .then((res) => {
          setChat(res.data.message);
        })
        .catch((err) => {
          console.error(err);
          setChat("메시지를 불러오지 못했습니다.");
        });
    }
  }, [weather]);

  return (
    <section className="detail-section">
      <h3>추천 메시지</h3>
      <div className="detail-recommend">{chat}</div>
    </section>
  );
}

export default RecommendMsg;
