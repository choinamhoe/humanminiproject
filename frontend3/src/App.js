import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useMatch,
  useNavigate,
} from "react-router-dom";
import Home from "./Home"; // ✅ Home.js
import MapView from "./mapview"; // ✅ mapview.js
import DetailPages from "./pages/DetailPages"; // ✅ 상세 패널
import { motion, AnimatePresence } from "framer-motion";

function LayoutWithMap() {
  const matchDetail = useMatch("/detail/:id"); // URL이 /detail/:id 인지 확인
  const navigate = useNavigate();

  return (
    <div style={{ position: "relative", height: "100vh" }}>
      {/* 지도 항상 표시 */}
      <MapView />

      {/* 상세 페이지가 열릴 때 애니메이션 */}
      <AnimatePresence>
        {matchDetail && (
          <>
            {/* 검은 배경 오버레이 */}
            <motion.div
              key="overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.5 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                background: "black",
                zIndex: 9998,
              }}
              onClick={() => navigate(-1)} // 오버레이 클릭 시 뒤로가기
            />

            {/* 오른쪽 디테일 패널 */}
            <motion.div
              key="detail-panel"
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ duration: 0.4, ease: "easeInOut" }}
              style={{
                position: "absolute",
                top: 0,
                right: 0,
                width: "400px",
                height: "100%",
                background: "#fff",
                boxShadow: "-4px 0 12px rgba(0,0,0,0.2)",
                zIndex: 9999,
                overflowY: "auto",
              }}
            >
              <DetailPages />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        {/* 홈 */}
        <Route path="/" element={<Home />} />

        {/* 지도 */}
        <Route path="/map" element={<LayoutWithMap />} />

        {/* 디테일 패널은 /map 과 동일한 레이아웃 */}
        <Route path="/detail/:id" element={<LayoutWithMap />} />
      </Routes>
    </Router>
  );
}

export default App;
