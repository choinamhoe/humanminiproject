import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useMatch,
  useNavigate,
} from "react-router-dom";
import Home from "./Home";
import MapView from "./mapview";
import DetailPages from "./pages/DetailPages";
import { motion, AnimatePresence } from "framer-motion";

function LayoutWithMap() {
  const matchDetail = useMatch("/detail/:id");
  const navigate = useNavigate();

  return (
    <div style={{ position: "relative", height: "100vh" }}>
      {/* 항상 지도 */}
      <MapView />

      <AnimatePresence>
        {matchDetail && (
          <>
            {/* ✅ 검은 오버레이 */}
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
              onClick={() => navigate(-1)} // 오버레이 클릭 → 닫기
            />

            {/* ✅ 오른쪽 슬라이드 패널 */}
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
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<LayoutWithMap />} />
        {/* ✅ /detail/:id 라우트 */}
        <Route path="/detail/:id" element={<LayoutWithMap />} />
      </Routes>
    </Router>
  );
}

export default App;
