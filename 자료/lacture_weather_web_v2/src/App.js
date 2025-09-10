import "./App.css";
import MapView from "./page";
function App() {
  return (
    <div
      style={{ height: "100%", boxSizing: "border-box", overflow: "hidden" }}
    >
      <h2 style={{ margin: 0, padding: "8px" }}>지도 시각화</h2>
      <MapView />
    </div>
  );
}

export default App;
