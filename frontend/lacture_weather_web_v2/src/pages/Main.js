import MapView from "../page";
import { Navigate } from "react-router-dom";
function Main() {
  return (
    <>
      <a href="/detail">aaa</a>
      <h>Main 테스트 화면</h>
      <div
        style={{ height: "100%", boxSizing: "border-box", overflow: "hidden" }}
      >
        <h2 style={{ margin: 0, padding: "8px" }}>지도 시각화</h2>
        <MapView />
      </div>
    </>
  );
}

export default Main;
