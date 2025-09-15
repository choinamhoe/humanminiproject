// src/App.js
import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import Home from "./Home";
import MapView from "./mapview";
import DetailPages from "./pages/DetailPages";

function LayoutWithMap() {
  const location = useLocation();
  const [panelWidth, setPanelWidth] = useState(400); // ✅ 초기 패널 너비

  // 드래그 시작
  const startResize = (e) => {
    const startX = e.clientX;
    const startWidth = panelWidth;

    const onMouseMove = (moveEvent) => {
      const newWidth = startWidth - (moveEvent.clientX - startX);
      if (newWidth > 300 && newWidth < 800) {
        setPanelWidth(newWidth);
      }
    };

    const onMouseUp = () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    };

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  };

  return (
    <div style={{ position: "relative", height: "100vh" }}>
      {/* 항상 지도는 배경에 렌더링 */}
      <MapView />

      {/* /detail/:id 일 때 오른쪽 패널 띄움 */}
      {location.pathname.startsWith("/detail") && (
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: `${panelWidth}px`,
            height: "100%",
            background: "#fff",
            boxShadow: "-4px 0 12px rgba(0,0,0,0.2)",
            zIndex: 9999,
            overflowY: "auto",
          }}
        >
          <DetailPages />

          {/* 리사이즈 핸들 */}
          <div
            onMouseDown={startResize}
            style={{
              position: "absolute",
              left: 0,
              top: 0,
              width: "5px",
              height: "100%",
              cursor: "ew-resize",
              background: "transparent",
            }}
          />
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<LayoutWithMap />} />
        <Route path="/detail/:id" element={<LayoutWithMap />} />
      </Routes>
    </Router>
  );
}

export default App;
