// src/App.js
import React from "react";
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

  return (
    <div style={{ position: "relative", height: "100vh" }}>
      {/* 항상 지도는 배경에 렌더링 */}
      <MapView />

      {/* /detail일 때만 오른쪽 패널 띄움 */}
      {location.pathname === "/detail" && (
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: "400px",
            height: "100%",
            background: "#fff",
            boxShadow: "-4px 0 12px rgba(0,0,0,0.2)",
            zIndex: 9999, // ✅ 지도 위로 오게 설정
            overflowY: "auto",
          }}
        >
          <DetailPages />
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
        {/* /map과 /detail은 같은 LayoutWithMap을 공유 */}
        <Route path="/map" element={<LayoutWithMap />} />
        <Route path="/detail" element={<LayoutWithMap />} />
      </Routes>
    </Router>
  );
}

export default App;
