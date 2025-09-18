import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { backgrounds, texts, logo } from "../constants/firstPage";

const Home = () => {
  const [current, setCurrent] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent((prev) => (prev + 1) % backgrounds.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="home-container" onClick={() => navigate("/map")}>
      {backgrounds.map((bg, index) => (
        <div
          key={index}
          className={`home-bg ${current === index ? "active" : ""}`}
          style={{ backgroundImage: `url(${bg})` }}
        />
      ))}

      <img src={logo} alt="로고" className="home-logo" />

      {texts.map((text, idx) => (
        <div
          key={idx}
          className={`home-text ${current === idx ? "active" : ""}`}
          style={text.position}
        >
          {text.highlight ? (
            <>
              <span>"{text.content} </span>
              <span className="highlight">{text.highlight}</span>
              <span>"</span>
            </>
          ) : (
            <span>"{text.content}"</span>
          )}
        </div>
      ))}
    </div>
  );
};

export default Home;
