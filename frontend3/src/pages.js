import React from "react";
import MapView from "./mapview.js"; // mapview.js 불러오기

const Page = () => {
  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <h1>골프장 지도</h1>
      <MapView /> {/* mapview.js의 MapView 불러오기 */}
    </div>
  );
};

export default Page;
