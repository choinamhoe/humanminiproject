// src/Home.js
import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 새로고침 시 항상 첫 화면으로 이동
  useEffect(() => {
    if (location.pathname !== "/") {
      navigate("/", { replace: true });
    }
  }, [location.pathname, navigate]);

  const handleClick = () => {
    navigate("/map");
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
        backgroundImage: `url(${process.env.PUBLIC_URL}/firstpage.avif)`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        position: "relative",
      }}
      onClick={handleClick}
    >
      {/* ✅ 왼쪽 위 로고 (public 기준) */}
      <img
        src={`${process.env.PUBLIC_URL}/로고사진.png`}
        alt="로고"
        style={{
          position: "absolute",
          top: "20px",
          left: "20px",
          height: "50px",
        }}
      />

      <h1 style={{ color: "white", textShadow: "2px 2px 4px rgba(0,0,0,0.7)" }}>
        홈 화면 (클릭하면 지도 보기)
      </h1>
    </div>
  );
};

export default Home;
