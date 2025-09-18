import { useEffect, useState, useRef } from "react";

import LeafletMap from "../components/LeafletMap";
import Search from "../components/Search";
import Sidebar from "../components/Sidebar";
import { getDetailData } from "../api/source";
import ResizableSidebar from "../components/ResizableSidebar";
const Map = ({ pointsData, geoData }) => {
  const [selectedData, setSelectedData] = useState([]);
  const [selectedPoint, setSelectedPoint] = useState(null);

  const [searchTerm, setSearchTerm] = useState("");
  const [detailData, setDetailData] = useState(null);
  const [sidebarWidth, setSidebarWidth] = useState(0);

  const handleSearch = async (e) => {
    setSearchTerm(e.target.value);
  };

  useEffect(() => {
    if (!searchTerm) return;

    const filteredData = pointsData.filter((item) =>
      item.storeName?.includes(searchTerm)
    );
    setSelectedData(filteredData);
  }, [searchTerm, pointsData]);

  const onClickDetail = async () => {
    console.log(selectedPoint);
    const id = selectedPoint.id;
    const lon = selectedPoint.Longitude;
    const lat = selectedPoint.Latitude;
    try {
      const res = await getDetailData(id, lon, lat);
      if (Object.keys(res?.golfDetail).length === 0) {
        // alert("자료가 없습니다.");
        // return;
        setDetailData(selectedPoint);
        return;
      }
      setDetailData(res?.golfDetail);
      setSidebarWidth(400);
    } catch (err) {
      alert("상세보기 API 요청에 실패하였습니다.");
    }
  };
  console.log(detailData);
  return (
    <>
      <Search searchTerm={searchTerm} handleSearch={handleSearch} />
      <LeafletMap
        pointsData={pointsData}
        selectedData={selectedData}
        setSelectedData={setSelectedData}
        setSearchTerm={setSearchTerm}
        selectedPoint={selectedPoint}
        setSelectedPoint={setSelectedPoint}
        onClickDetail={onClickDetail}
        geoData={geoData}
      />
      {detailData && Object.keys(detailData).length > 0 && (
        <ResizableSidebar>
          <Sidebar detailData={detailData} setDetailData={setDetailData} />
        </ResizableSidebar>
      )}
    </>
  );
};

export default Map;
