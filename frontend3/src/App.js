// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import MapView from "./mapview";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} /> {/* ✅ 첫화면 */}
        <Route path="/map" element={<MapView />} /> {/* ✅ 지도화면 */}
      </Routes>
    </Router>
  );
}

export default App;
