<<<<<<< HEAD
import React from "react";
import { useNavigate } from "react-router-dom";
=======
// src/Home.js
import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
>>>>>>> main

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
        width: "100vw",
        position: "relative",
        cursor: "pointer",
<<<<<<< HEAD
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
=======
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
>>>>>>> main
    </div>
  );
};

export default Home;
