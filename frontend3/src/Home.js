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
        width: "100vw",
        position: "relative",
        cursor: "pointer",
        backgroundImage:
          "url('/runningchild-UmKbUNzzphE-unsplash%20%281%29.jpg')", // ✅ 배경 이미지
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
      onClick={handleClick}
    >
      {/* ✅ 왼쪽 상단 로고 */}
      <img
        src="/logogo.png" // ✅ 최신 로고 파일
        alt="Logo"
        style={{
          position: "absolute",
          top: 0,
          left: 20,
          width: 235,
          height: "auto",
          objectFit: "contain",
          userSelect: "none",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};

export default Home;
