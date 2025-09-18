import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Map from "./pages/Map";

import "./css/index.css";
import "./css/App.css";
import "./css/DetailPages.css";
import { getGeoData, getGolfInfoAll } from "./api/source";
import AreaNormalizer from "./components/AreaNormalizer";

function App() {
  const [pointsData, setPointsData] = useState([]);
  const [geoData, setGeoData] = useState(null);

  useEffect(() => {
    const fetchGeoData = async () => {
      try {
        const res = await getGeoData();
        setGeoData(res.data);
      } catch (err) {
        console.error("GeoJSON 불러오기 실패:", err);
      }
    };
    const fetchGolfData = async () => {
      try {
        const res = await getGolfInfoAll();
        let data = res.golfList.golfInfo;
        data = data.filter(
          (item) => item.Latitude != null && item.Longitude != null
        );
        data = data.map((item) => ({
          ...item,
          area: AreaNormalizer(item.area),
        }));
        setPointsData(data);
      } catch (err) {
        console.error("GolfInfo 자료 불러오기 실패:", err);
      }
    };
    fetchGeoData();
    fetchGolfData();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Home />} />
        <Route
          path="/map"
          element={<Map pointsData={pointsData} geoData={geoData} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
