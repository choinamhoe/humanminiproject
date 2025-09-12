import React, { useState, useEffect } from "react";

const backgrounds = [
  `${process.env.PUBLIC_URL}/firstpage.avif`,
  `${process.env.PUBLIC_URL}/background.avif`,
];

const texts = [
  "골프장의 하늘을 미리 보는, ",
  "날씨를 알고, 완벽한 라운드를 즐기다.",
];

const highlightText = "swing sky";

const Home = () => {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    // Pretendard 웹폰트 로드
    const pretendardLink = document.createElement("link");
    pretendardLink.href =
      "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css";
    pretendardLink.rel = "stylesheet";
    document.head.appendChild(pretendardLink);

    // Montserrat 웹폰트 로드
    const montserratLink = document.createElement("link");
    montserratLink.href =
      "https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap"; // 400으로 변경
    montserratLink.rel = "stylesheet";
    document.head.appendChild(montserratLink);

    const interval = setInterval(() => {
      setCurrent((prev) => (prev + 1) % backgrounds.length);
    }, 4000);

    return () => {
      clearInterval(interval);
      document.head.removeChild(pretendardLink);
      document.head.removeChild(montserratLink);
    };
  }, []);

  const commonTextStyle = {
    color: "#ddd",
    fontSize: "18px",
    fontWeight: 500,
    fontFamily: "Pretendard, sans-serif",
    textShadow: "1px 1px 3px rgba(0,0,0,0.4)",
    zIndex: 10,
    transition: "opacity 1s ease-in-out",
  };

  const highlightStyle = {
    fontSize: "25px",
    fontWeight: 600, // 두껍지 않게 400으로 설정
    fontFamily: "'Montserrat', sans-serif",
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        position: "relative",
        cursor: "pointer",
      }}
    >
      {backgrounds.map((bg, index) => (
        <div
          key={index}
          style={{
            backgroundImage: `url(${bg})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            position: "absolute",
            top: 0,
            left: 0,
            height: "100%",
            width: "100%",
            opacity: current === index ? 1 : 0,
            transition: "opacity 1s ease-in-out",
            zIndex: index === current ? 1 : 0,
          }}
        />
      ))}

      {/* 로고 */}
      <img
        src={`${process.env.PUBLIC_URL}/logogo.png`}
        alt="로고"
        style={{
          position: "absolute",
          top: 0,
          left: 15,
          height: "180px",
          objectFit: "contain",
          userSelect: "none",
          pointerEvents: "none",
          zIndex: 10,
        }}
      />

      {/* 첫 번째 소개글 (우측 위) */}
      <div
        style={{
          position: "absolute",
          top: "23%",
          right: "10%",
          ...commonTextStyle,
          opacity: current === 0 ? 1 : 0,
        }}
      >
        {`"`}
        <span>{texts[0]}</span>
        <span style={highlightStyle}>{highlightText}</span>
        {`"`}
      </div>

      {/* 두 번째 소개글 (좌측 아래) */}
      <div
        style={{
          position: "absolute",
          top: "67%",
          left: "10%",
          width: "90%",
          maxWidth: "1000px",
          whiteSpace: "normal",
          wordBreak: "keep-all",
          ...commonTextStyle,
          fontSize: "22px",
          opacity: current === 1 ? 1 : 0,
        }}
      >
        {`"${texts[1]}"`}
      </div>
    </div>
  );
};

export default Home;
