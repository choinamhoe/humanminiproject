const Search = ({ searchTerm, handleSearch }) => {
  return (
    <div className="map-header" style={{ textAlign: "center" }}>
      <h2>📍 대한민국 골프장 지도</h2>
      <p>지역을 클릭하면 해당 지역의 골프장이 표시됩니다.</p>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "5px",
        }}
      >
        <div style={{ position: "relative", width: "350px" }}>
          <input
            type="text"
            placeholder="지역명 또는 골프장명 검색"
            value={searchTerm}
            onChange={handleSearch}
            style={{
              width: "85%",
              padding: "8px 35px 8px 12px",
              borderRadius: "20px",
              border: "1px solid #ccc",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
              fontSize: "14px",
            }}
          />
          <span
            style={{
              position: "absolute",
              right: "12px",
              top: "50%",
              transform: "translateY(-50%)",
              color: "#888",
              cursor: "pointer",
            }}
          >
            🔍
          </span>
        </div>
      </div>
    </div>
  );
};
export default Search;
