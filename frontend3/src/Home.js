// src/Home.js
import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/map"); // ✅ mapview 페이지로 이동
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
        backgroundColor: "#f5f5f5",
      }}
      onClick={handleClick} // ✅ 아무데나 클릭하면 이동
    >
      <h1>홈 화면 (클릭하면 지도 보기)</h1>
    </div>
  );
};

export default Home;
