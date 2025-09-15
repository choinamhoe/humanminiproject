import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/map");
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        backgroundImage: `url(${process.env.PUBLIC_URL}/firstpage.avif)`, // ✅ public 폴더에 있는 배경
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        position: "relative",
        cursor: "pointer",
      }}
      onClick={handleClick}
    >
      {/* ✅ 왼쪽 상단 로고 */}
      <img
        src={`${process.env.PUBLIC_URL}/로고사진.png`} // ✅ public 폴더의 로고 파일
        alt="로고"
        style={{
          position: "absolute",
          top: 20,
          left: 20,
          height: "50px",
          objectFit: "contain",
          userSelect: "none",
          pointerEvents: "none",
        }}
      />

      {/* ✅ 중앙 제목 */}
      <h1
        style={{
          color: "white",
          textShadow: "2px 2px 4px rgba(0,0,0,0.7)",
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
        }}
      >
        홈 화면 (클릭하면 지도 보기)
      </h1>
    </div>
  );
};

export default Home;
